#!/usr/bin/env python3
"""recipe_archive.py: the delete action moves a recipe into archived/ on its own branch, and a
push to main that adds archived/*/*/recipe.json deletes exactly those recipes from SM."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import support  # noqa: F401  (puts scripts/ on sys.path)

import recipe_archive as ra
import recipe_deploy as rd


class Repo(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "t@t")
        self.git("config", "user.name", "t")

    def git(self, *a):
        return subprocess.run(["git", *a], cwd=self.root, check=True, capture_output=True,
                              text=True).stdout.strip()

    def put(self, slug, fid, top="recipes"):
        p = self.root / top / "intempt" / slug / "recipe.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"frontmatter_id": fid}), encoding="utf-8")
        (p.parent / "recipe.md").write_text("# r\n", encoding="utf-8")

    def commit(self, msg="c"):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", msg)
        return self.git("rev-parse", "HEAD")


class Move(Repo):
    def test_moves_the_folder_on_its_own_branch(self):
        self.put("a", "a-id")
        self.put("b", "b-id")
        base = self.commit()
        branch, src, dst = ra.move(str(self.root), "b-id", base)
        self.assertEqual((branch, src, dst), ("archive/b-id", "recipes/intempt/b", "archived/intempt/b"))
        self.assertEqual(self.git("branch", "--show-current"), "archive/b-id")
        self.assertFalse((self.root / "recipes/intempt/b").exists())
        self.assertTrue((self.root / "archived/intempt/b/recipe.json").exists())
        self.assertTrue((self.root / "archived/intempt/b/recipe.md").exists())
        self.assertTrue((self.root / "recipes/intempt/a/recipe.json").exists())
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(self.git("rev-parse", "HEAD^"), base)

    def test_unknown_or_already_archived_is_refused(self):
        self.put("a", "a-id", top="archived")
        base = self.commit()
        with self.assertRaisesRegex(rd.Refused, "no recipes"):
            ra.move(str(self.root), "a-id", base)

    def test_existing_archive_folder_is_refused(self):
        self.put("a", "a-id")
        self.put("a", "old", top="archived")
        base = self.commit()
        with self.assertRaisesRegex(rd.Refused, "already exists"):
            ra.move(str(self.root), "a-id", base)


class ArchivedBetween(Repo):
    def test_only_recipes_the_range_archived(self):
        self.put("a", "a-id")
        self.put("b", "b-id")
        self.put("old", "old-id", top="archived")
        before = self.commit()
        ra.move(str(self.root), "a-id", before)
        after = self.git("rev-parse", "HEAD")
        hits = ra.archived_between(str(self.root), before, after)
        self.assertEqual(hits, [("archived/intempt/a/recipe.json", {"frontmatter_id": "a-id"})])

    def test_an_edit_inside_archived_is_not_an_archive(self):
        self.put("old", "old-id", top="archived")
        before = self.commit()
        (self.root / "archived/intempt/old/recipe.md").write_text("# edited\n", encoding="utf-8")
        after = self.commit()
        self.assertEqual(ra.archived_between(str(self.root), before, after), [])


class DeleteMerged(Repo):
    def run_cmd(self, before, after, statuses):
        calls = []

        def fake_call(method, url, secret, body):
            calls.append((method, url, body))
            return statuses.pop(0), ""

        args = mock.Mock(root=str(self.root), before=before, after=after, url="http://sm/v1/recipes")
        with mock.patch.dict("os.environ", {"RECIPE_GIT_VALIDATE_SECRET": "s"}), \
                mock.patch.object(rd, "call", fake_call):
            rc = ra.cmd_delete_merged(args)
        return rc, calls

    def archive(self, *fids):
        for fid in fids:
            self.put(fid, fid)
        before = self.commit()
        (self.root / "archived/intempt").mkdir(parents=True, exist_ok=True)
        for fid in fids:
            self.git("mv", f"recipes/intempt/{fid}", f"archived/intempt/{fid}")
        return before, self.commit("archive")

    def test_deployed_recipes_are_deleted_from_sm(self):
        before, after = self.archive("x", "y")
        self.git("tag", "deployed/x", before)
        self.git("tag", "deployed/y", before)
        rc, calls = self.run_cmd(before, after, [200, 204])
        self.assertEqual(rc, 0)
        self.assertEqual(calls, [("DELETE", "http://sm/v1/recipes", {"frontmatter_id": "x"}),
                                 ("DELETE", "http://sm/v1/recipes", {"frontmatter_id": "y"})])

    def test_never_deployed_is_not_sent(self):
        before, after = self.archive("x")
        rc, calls = self.run_cmd(before, after, [])
        self.assertEqual((rc, calls), (0, []))

    def test_sm_refusal_fails_the_run(self):
        before, after = self.archive("x")
        self.git("tag", "deployed/x", before)
        rc, _ = self.run_cmd(before, after, [404])
        self.assertEqual(rc, 1)

    def test_new_branch_push_reads_the_last_commit(self):
        before, after = self.archive("x")
        self.git("tag", "deployed/x", before)
        rc, calls = self.run_cmd("0" * 40, after, [200])
        self.assertEqual((rc, len(calls)), (0, 1))


if __name__ == "__main__":
    unittest.main()
