#!/usr/bin/env python3
"""recipe_deploy.py: tag parsing, f_id → recipe.json lookup, the on-main gate,
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
                         {"action": "create", "person_id": 10499, "f_id": "email-nonopener"})

    def test_update_and_delete(self):
        self.assertEqual(rd.parse_tag("update/abc"), {"action": "update", "f_id": "abc"})
        self.assertEqual(rd.parse_tag("refs/tags/delete/abc"), {"action": "delete", "f_id": "abc"})

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
        self.put("a", {"f_id": "a-id", "steps": []})
        p = self.put("b", {"f_id": "b-id", "steps": [1]})
        self.put("broken", None, raw="{not json")
        path, record = rd.find_recipe_json(str(self.root), "b-id")
        self.assertEqual((path, record), (str(p), {"f_id": "b-id", "steps": [1]}))

    def test_not_found(self):
        self.put("a", {"f_id": "a-id"})
        with self.assertRaisesRegex(rd.Refused, "no recipes"):
            rd.find_recipe_json(str(self.root), "b-id")

    def test_duplicate(self):
        self.put("a", {"f_id": "same"})
        self.put("b", {"f_id": "same"})
        with self.assertRaisesRegex(rd.Refused, "in 2 recipe.json"):
            rd.find_recipe_json(str(self.root), "same")


class Request(unittest.TestCase):
    URL = "https://sm.example/v1/recipes"

    def test_each_action(self):
        r = {"f_id": "a b"}
        self.assertEqual(rd.request({"action": "create", "person_id": 7, "f_id": "a b"}, self.URL, r),
                         ("POST", self.URL, {"person_id": 7, "recipe": r}))
        self.assertEqual(rd.request({"action": "update", "f_id": "a b"}, self.URL, r),
                         ("PUT", self.URL, {"recipe": r}))
        self.assertEqual(rd.request({"action": "delete", "f_id": "a b"}, self.URL, None),
                         ("DELETE", self.URL, {"f_id": "a b"}))


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


if __name__ == "__main__":
    unittest.main(verbosity=1)
