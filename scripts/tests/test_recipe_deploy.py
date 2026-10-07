#!/usr/bin/env python3
"""recipe_deploy.py: tag parsing, frontmatter_id → recipe.json lookup, the on-main gate,
and the request each action sends to SM (RG1 §50/§51.3b)."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import support  # noqa: F401  (puts scripts/ on sys.path)

import recipe_deploy as rd


class ParseTag(unittest.TestCase):
    def test_create(self):
        self.assertEqual(rd.parse_tag("create/10499/email-nonopener"),
                         {"action": "create", "person_id": 10499, "frontmatter_id": "email-nonopener"})

    def test_update_and_delete(self):
        self.assertEqual(rd.parse_tag("update/abc"), {"action": "update", "frontmatter_id": "abc"})
        self.assertEqual(rd.parse_tag("refs/tags/delete/abc"), {"action": "delete", "frontmatter_id": "abc"})

    def test_malformed_is_refused(self):
        for bad in ("create/abc", "create/x1/abc", "create/1/", "create/1/a/b", "update/",
                    "update/a/b", "delete", "publish/abc", "", "Update/abc"):
            with self.subTest(bad=bad), self.assertRaises(rd.Refused):
                rd.parse_tag(bad)


class FindRecipeJson(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def put(self, slug, record, raw=None):
        p = self.root / "recipes" / "intempt" / slug / "recipe.json"
        p.parent.mkdir(parents=True)
        p.write_text(raw if raw is not None else json.dumps(record), encoding="utf-8")
        return p

    def test_found(self):
        self.put("a", {"frontmatter_id": "a-id", "steps": []})
        p = self.put("b", {"frontmatter_id": "b-id", "steps": [1]})
        self.put("broken", None, raw="{not json")
        path, record = rd.find_recipe_json(str(self.root), "b-id")
        self.assertEqual((path, record), (str(p), {"frontmatter_id": "b-id", "steps": [1]}))

    def test_not_found(self):
        self.put("a", {"frontmatter_id": "a-id"})
        with self.assertRaisesRegex(rd.Refused, "no recipes"):
            rd.find_recipe_json(str(self.root), "b-id")

    def test_duplicate(self):
        self.put("a", {"frontmatter_id": "same"})
        self.put("b", {"frontmatter_id": "same"})
        with self.assertRaisesRegex(rd.Refused, "in 2 recipe.json"):
            rd.find_recipe_json(str(self.root), "same")


class Request(unittest.TestCase):
    URL = "https://sm.example/v1/recipes"

    def test_each_action(self):
        r = {"frontmatter_id": "a b"}
        self.assertEqual(rd.request({"action": "create", "person_id": 7, "frontmatter_id": "a b"}, self.URL, r),
                         ("POST", self.URL, {"person_id": 7, "recipe": r}))
        self.assertEqual(rd.request({"action": "update", "frontmatter_id": "a b"}, self.URL, r),
                         ("PUT", self.URL, {"recipe": r}))
        self.assertEqual(rd.request({"action": "delete", "frontmatter_id": "a b"}, self.URL, None),
                         ("DELETE", self.URL, {"frontmatter_id": "a b"}))


class OnMain(unittest.TestCase):
    def test_only_a_commit_on_main_passes(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        git = lambda *a: subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                                         *a], check=True, capture_output=True)
        git("init", "-q", "-b", "main")
        git("commit", "-q", "--allow-empty", "-m", "one")
        git("tag", "update/on")
        git("checkout", "-q", "-b", "side")
        git("commit", "-q", "--allow-empty", "-m", "two")
        git("tag", "-a", "-m", "annotated", "update/off")
        self.assertTrue(rd.on_main("refs/tags/update/on", "main", d))
        self.assertFalse(rd.on_main("refs/tags/update/off", "main", d))
        self.assertFalse(rd.on_main("refs/tags/update/missing", "main", d))


class MainRef(unittest.TestCase):
    """`--ref` (the manual run): the on-main gate reads that commit, not refs/tags/<name>."""

    def run_main(self, d, *argv):
        import contextlib, io, os
        out = io.StringIO()
        old = sys.argv, os.environ.get("RECIPE_GIT_VALIDATE_SECRET")
        sys.argv = ["recipe_deploy.py", *argv, "--main", "main", "--url", "https://sm.invalid", "--root", d]
        os.environ["RECIPE_GIT_VALIDATE_SECRET"] = "x"
        try:
            with contextlib.redirect_stdout(out):
                rc = rd.main()
        finally:
            sys.argv = old[0]
            if old[1] is None:
                os.environ.pop("RECIPE_GIT_VALIDATE_SECRET", None)
            else:
                os.environ["RECIPE_GIT_VALIDATE_SECRET"] = old[1]
        return rc, out.getvalue()

    def test_ref_head_is_gated_without_a_tag(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        git = lambda *a: subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                                         *a], check=True, capture_output=True)
        git("init", "-q", "-b", "main")
        git("commit", "-q", "--allow-empty", "-m", "one")
        # No tag exists: on main, HEAD passes the gate and the run stops at the missing recipe.json.
        rc, out = self.run_main(d, "update/x", "--ref", "HEAD")
        self.assertEqual(rc, 1)
        self.assertIn("no recipes", out)
        self.assertNotIn("is not on", out)
        # Without --ref the same name is looked up as a tag, which does not exist.
        rc, out = self.run_main(d, "update/x")
        self.assertIn("is not on main", out)
        # Off main, HEAD is refused.
        git("checkout", "-q", "-b", "side")
        git("commit", "-q", "--allow-empty", "-m", "two")
        rc, out = self.run_main(d, "update/x", "--ref", "HEAD")
        self.assertEqual(rc, 1)
        self.assertIn("is not on main", out)


class SkipUnchanged(MainRef):
    """`--skip-unchanged` (manual run): create/update need a change since deployed/<id>;
    delete needs deployed/<id> to exist. A skip exits 0 without calling SM."""

    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, ignore_errors=True)
        self.git("init", "-q", "-b", "main")
        self.rj = pathlib.Path(self.d, "recipes", "o", "a", "recipe.json")
        self.rj.parent.mkdir(parents=True)
        self.commit({"frontmatter_id": "a-id", "steps": [1]}, "one")

    def git(self, *a):
        return subprocess.run(["git", "-C", self.d, "-c", "user.name=t", "-c", "user.email=t@t", *a],
                              check=True, capture_output=True)

    def commit(self, record, msg):
        self.rj.write_text(json.dumps(record), encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", msg)

    def test_update_and_create_skip_when_unchanged(self):
        self.git("tag", "deployed/a-id")
        self.git("commit", "-q", "--allow-empty", "-m", "unrelated commit on main")
        for name in ("update/a-id", "create/7/a-id"):
            with self.subTest(name=name):
                rc, out = self.run_main(self.d, name, "--ref", "HEAD", "--skip-unchanged")
                self.assertEqual(rc, 0)
                self.assertIn("UNCHANGED  a-id", out)

    def test_changed_or_never_deployed_is_not_skipped(self):
        path = str(self.rj)
        self.assertFalse(rd.unchanged_since_deploy(self.d, "a-id", path, "HEAD"))  # no marker yet
        self.git("tag", "deployed/a-id")
        self.assertTrue(rd.unchanged_since_deploy(self.d, "a-id", path, "HEAD"))
        self.commit({"frontmatter_id": "a-id", "steps": [1, 2]}, "edit the recipe")
        self.assertFalse(rd.unchanged_since_deploy(self.d, "a-id", path, "HEAD"))

    def test_delete_skips_only_without_a_marker(self):
        rc, out = self.run_main(self.d, "delete/a-id", "--ref", "HEAD", "--skip-unchanged")
        self.assertEqual(rc, 0)
        self.assertIn("NOT DEPLOYED  a-id", out)
        self.git("tag", "deployed/a-id")
        self.assertTrue(rd.has_marker(self.d, "a-id"))

    def test_without_the_flag_nothing_is_skipped(self):
        self.git("tag", "deployed/a-id")
        rc, out = self.run_main(self.d, "update/x-missing", "--ref", "HEAD")
        self.assertNotIn("UNCHANGED", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
