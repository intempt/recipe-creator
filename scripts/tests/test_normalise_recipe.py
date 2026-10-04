#!/usr/bin/env python3
import pathlib
import subprocess
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import SCRIPTS, cleanup, example_text, write_recipe

import normalise_recipe as nr
import recipe_contract as rc


def front_of(text):
    head = text.split("\n---\n", 1)[0][4:]
    import yaml
    return yaml.safe_load(head)


class Normalise(unittest.TestCase):
    def test_the_worked_example_is_already_normalised(self):
        self.assertEqual(nr.normalise(example_text()), example_text())

    def test_crlf_line_endings_become_lf(self):
        out = nr.normalise(example_text().replace("\n", "\r\n"))
        self.assertNotIn("\r", out)
        self.assertEqual(out, example_text())

    def test_trailing_whitespace_is_removed(self):
        messy = example_text().replace("owner: intempt\n", "owner: intempt   \n", 1)
        self.assertEqual(nr.normalise(messy), example_text())

    def test_top_level_keys_follow_the_template_order(self):
        text = example_text()
        moved = text.replace("title: Nudge trials before they expire\n", "", 1).replace(
            "version: 1.0.0\n", "version: 1.0.0\ntitle: Nudge trials before they expire\n", 1)
        self.assertNotEqual(moved, text)
        self.assertEqual(nr.normalise(moved), text)

    def test_step_keys_follow_the_template_order(self):
        text = example_text()
        moved = text.replace("    builds: email_html\n", "", 1).replace(
            "  - id: s2\n", "  - id: s2\n    builds: email_html\n", 1)
        self.assertNotEqual(moved, text)
        self.assertEqual(nr.normalise(moved), text)

    def test_a_stale_body_is_regenerated_from_the_frontmatter(self):
        stale = example_text().replace("# Nudge trials before they expire", "# Old title", 1)
        self.assertEqual(nr.normalise(stale), example_text())

    def test_normalising_twice_changes_nothing(self):
        messy = example_text().replace("\n", "\r\n").replace("group: Segments", "group: Segments  ")
        once = nr.normalise(messy)
        self.assertEqual(nr.normalise(once), once)

    def test_the_frontmatter_values_never_change(self):
        text = example_text()
        moved = text.replace("    builds: segment\n", "", 1).replace(
            "  - id: s1\n", "  - id: s1\n    builds: segment\n", 1)
        self.assertEqual(front_of(nr.normalise(moved)), front_of(text))
        self.assertEqual(rc.render_body(front_of(text)), nr.normalise(moved).split("\n---\n", 1)[1])

    def test_check_exits_1_on_a_file_that_is_not_normalised_and_writes_nothing(self):
        messy = example_text().replace("owner: intempt\n", "owner: intempt \n", 1)
        path = write_recipe(messy)
        try:
            run = subprocess.run([sys.executable, str(SCRIPTS / "normalise_recipe.py"), "--check", str(path)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
            self.assertEqual(path.read_text(encoding="utf-8"), messy)
        finally:
            cleanup(path)

    def test_without_check_it_rewrites_the_file_in_place(self):
        path = write_recipe(example_text().replace("\n", "\r\n"))
        try:
            run = subprocess.run([sys.executable, str(SCRIPTS / "normalise_recipe.py"), str(path)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertEqual(path.read_bytes(), example_text().encode("utf-8"))
        finally:
            cleanup(path)


if __name__ == "__main__":
    unittest.main(verbosity=1)
