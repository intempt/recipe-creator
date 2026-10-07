#!/usr/bin/env python3
"""check_recipe_consistency.py: a git-format recipe.md and its recipe.json agree, and
the folder is recipes/<author.org_name>/<frontmatter_id>/."""
import contextlib
import io
import json
import os
import pathlib
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import check_recipe_consistency as crc

AUTHOR = {"name": "Beso", "last_name": "Gugushvili", "org_name": "intempt"}
MD = ("---\nfrontmatter_id: nudge\nslash_command: /nudge\ndescription: Nudges.\n"
      "author:\n  name: Beso\n  last_name: Gugushvili\n  org_name: intempt\n---\n# Nudge\n")
JSON = {"frontmatter_id": "nudge", "slash_command": "/nudge", "description": "Nudges.",
        "author": AUTHOR, "steps": []}


class Consistency(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def folder(self, owner="intempt", key="nudge", md=MD, record=JSON):
        d = self.root / "recipes" / owner / key
        d.mkdir(parents=True)
        if md is not None:
            (d / "recipe.md").write_text(md)
        if record is not None:
            (d / "recipe.json").write_text(json.dumps(record))
        return str(d)

    def test_agreeing_files_pass(self):
        self.assertEqual(crc.check(self.folder()), [])

    def test_each_field_that_differs_is_named(self):
        for field, value in (("frontmatter_id", "other"), ("slash_command", "/x"),
                             ("description", "Else."), ("author", {**AUTHOR, "name": "Sid"})):
            with self.subTest(field=field):
                shutil.rmtree(self.root / "recipes", ignore_errors=True)
                problems = crc.check(self.folder(record={**JSON, field: value}))
                self.assertTrue(any(f"{field} differs" in p for p in problems), problems)

    def test_half_a_recipe_fails(self):
        self.assertIn("no recipe.json", crc.check(self.folder(record=None))[0])
        shutil.rmtree(self.root / "recipes")
        self.assertIn("no git-format recipe.md", crc.check(self.folder(md=None))[0])

    def test_the_folder_must_be_owner_then_key(self):
        self.assertTrue(any("should be" in p for p in crc.check(self.folder(owner="acme"))))

    def test_a_contract_recipe_is_not_its_business(self):
        self.assertEqual(crc.check(self.folder(md="---\nid: nudge\ntitle: T\n---\nb\n", record=None)), [])

    def test_main_scans_the_tree(self):
        self.folder(record={**JSON, "description": "Else."})
        cwd = os.getcwd()
        os.chdir(self.root)
        try:
            with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(crc.main([]), 1)
        finally:
            os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
