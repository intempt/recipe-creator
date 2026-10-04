#!/usr/bin/env python3
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import SCRIPTS, example_text

FROM_CREATOR = example_text().replace("owner: intempt", "owner: maya-chen").replace("curator: harish\n", "")


def scrambled(text):
    head, sep, rest = text.partition("\nsteps:\n")
    lines = head.split("\n")
    return "\n".join([lines[0], *reversed(lines[1:3]), *lines[3:]]) + sep + rest


class Accept(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.repo = self.root / "repo"
        (self.repo / "recipes").mkdir(parents=True)
        self.submitted = self.root / "submitted.md"

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def accept(self, text, *extra):
        self.submitted.write_text(text)
        return subprocess.run([sys.executable, str(SCRIPTS / "accept_submission.py"), str(self.submitted),
                               "--repo", str(self.repo), *extra], capture_output=True, text=True)

    def target(self):
        return self.repo / "recipes" / "maya-chen" / "trial-expiring-nudge" / "recipe.md"

    def test_lands_under_the_creator_folder_and_is_normalised(self):
        result = self.accept(scrambled(FROM_CREATOR))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.target().exists())
        check = subprocess.run([sys.executable, str(SCRIPTS / "normalise_recipe.py"), "--check", str(self.target())],
                               capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_refuses_to_overwrite_an_accepted_recipe_without_replace(self):
        self.assertEqual(self.accept(FROM_CREATOR).returncode, 0)
        again = self.accept(FROM_CREATOR)
        self.assertEqual(again.returncode, 1)
        self.assertIn("--replace", again.stderr)
        self.assertEqual(self.accept(FROM_CREATOR, "--replace").returncode, 0)

    def test_refuses_an_outside_submission_claiming_the_intempt_folder(self):
        result = self.accept(example_text().replace("curator: harish\n", ""), "--external")
        self.assertEqual(result.returncode, 1)
        self.assertIn("intempt", result.stderr)

    def test_refuses_a_recipe_that_fails_the_contract(self):
        result = self.accept(FROM_CREATOR.replace("touches:", "touched:"))
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.target().exists())


if __name__ == "__main__":
    unittest.main()
