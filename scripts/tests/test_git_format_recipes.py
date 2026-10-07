#!/usr/bin/env python3
"""A git-validated recipe (frontmatter_id + author + free prose) lives under recipes/
beside contract recipes: the contract gates skip it, the identity gate checks it."""
import contextlib
import io
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import check_recipe_identity
from recipe_contract import git_front, recipe_files, recipe_paths

# Beso's example (/home/beso/Downloads/email-nonopener-reengagement-recipe.md), with the
# key renamed to frontmatter_id; the two leading blank lines are kept on purpose.
GIT_RECIPE = '\n\n---\nfrontmatter_id: email-nonopener-reengagement\nauthor:\n  name: Beso\n  last_name: Gugushvili\n  org_name: intempt\n---\n# Email Non-Opener Re-Engagement\n\n## Step 1: Create Email Non-Openers Segment\n\nCreate a segment called "Email Non-Openers" for users. Base it on the "Messaged email" event — a real system event already in this project. Add one group with two conditions: triggered "Messaged email" within the last 7 days, AND did NOT trigger "Opened email" in that same 7-day window.\n\n## Step 2: Generate Re-Send Banner Image\n\nGenerate a simple, friendly banner image for a follow-up email, 600×200px, clean and purely illustrative with no text overlay, warm color palette.\n\n## Step 3: Generate Re-Send Email\n\nWrite a short, friendly follow-up email for the "Email Non-Openers" segment created in Step 1, using the banner image generated in Step 2. Use a different, more curiosity-driven subject line than the original send, keep the body under 60 words, and close with one clear button to the same offer.\n\n'

CONTRACT_RECIPE = """---
id: vip-users
title: VIP users
slash_command: /vip-users
---
body
"""


class GitFormat(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.cwd = os.getcwd()
        os.chdir(self.root)

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def write(self, folder, text):
        path = self.root / "recipes" / "intempt" / folder / "recipe.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def identity(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = check_recipe_identity.main()
        return code, err.getvalue()

    def test_git_front_reads_past_blank_lines_and_a_bom(self):
        path = self.write("email-nonopener-reengagement", GIT_RECIPE)
        self.assertEqual(git_front(path)["frontmatter_id"], "email-nonopener-reengagement")
        path.write_text("\ufeff" + GIT_RECIPE, encoding="utf-8")
        self.assertIsNotNone(git_front(path))

    def test_a_contract_recipe_is_not_the_git_format(self):
        self.assertIsNone(git_front(self.write("vip-users", CONTRACT_RECIPE)))

    def test_the_contract_loaders_skip_the_git_format(self):
        git = self.write("email-nonopener-reengagement", GIT_RECIPE)
        contract = self.write("vip-users", CONTRACT_RECIPE)
        self.assertEqual(recipe_paths(self.root / "recipes"), [contract])
        self.assertEqual(recipe_files([self.root / "recipes"]), [contract])
        self.assertEqual(recipe_files([git]), [])

    def test_identity_passes_a_well_formed_git_recipe(self):
        self.write("email-nonopener-reengagement", GIT_RECIPE)
        self.assertEqual(self.identity()[0], 0)

    def test_identity_wants_folder_equal_to_frontmatter_id(self):
        self.write("some-other-folder", GIT_RECIPE)
        code, err = self.identity()
        self.assertEqual(code, 1)
        self.assertIn("does not match its folder", err)

    def test_identity_wants_author_name_and_last_name(self):
        self.write("email-nonopener-reengagement", GIT_RECIPE.replace("  last_name: Gugushvili\n", ""))
        code, err = self.identity()
        self.assertEqual(code, 1)
        self.assertIn("author is missing last_name", err)

    def test_identity_wants_the_owner_folder_to_be_org_name(self):
        self.write("email-nonopener-reengagement", GIT_RECIPE.replace("org_name: intempt", "org_name: acme"))
        code, err = self.identity()
        self.assertEqual(code, 1)
        self.assertIn("does not match its owner folder 'intempt'", err)

    def test_identity_refuses_a_deploy_key_another_recipe_owns(self):
        self.write("email-nonopener-reengagement", GIT_RECIPE)
        self.write("email-nonopener-reengagement-copy", CONTRACT_RECIPE.replace("vip-users", "email-nonopener-reengagement-copy")
                   .replace("title:", "frontmatter_id: email-nonopener-reengagement\ntitle:"))
        code, err = self.identity()
        self.assertEqual(code, 1)
        self.assertIn("duplicate deploy key", err)


if __name__ == "__main__":
    unittest.main()
