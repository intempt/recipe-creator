#!/usr/bin/env python3
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import ROOT

EXAMPLES = sorted((ROOT / "examples").glob("*/*/recipe.md"))


class Examples(unittest.TestCase):
    def test_an_example_copied_from_the_catalog_matches_its_source_byte_for_byte(self):
        copied = 0
        for path in EXAMPLES:
            source = ROOT / "recipes" / path.parent.parent.name / path.parent.name / "recipe.md"
            if source.exists():
                copied += 1
                self.assertEqual(path.read_bytes(), source.read_bytes(), f"{path} drifted from {source}")
        self.assertGreater(copied, 0)

    def test_the_examples_readme_names_every_example(self):
        readme = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        for path in EXAMPLES:
            self.assertIn(f"./{path.parent.parent.name}/{path.parent.name}/recipe.md", readme)


if __name__ == "__main__":
    unittest.main(verbosity=1)
