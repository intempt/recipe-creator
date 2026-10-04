#!/usr/bin/env python3
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import support

import build_artifacts
import recipe_contract as rc


class Catalog(unittest.TestCase):
    def test_the_catalog_publishes_the_curator(self):
        front, _ = rc.read(support.EXAMPLE)
        self.assertEqual(build_artifacts.catalog_entry(front, front)["curator"], "harish")

    def test_the_catalog_leaves_curator_out_when_none_is_set(self):
        front, _ = rc.read(support.EXAMPLE)
        front.pop("curator", None)
        self.assertNotIn("curator", build_artifacts.catalog_entry(front, front))

    def test_a_recipe_without_classification_still_publishes_the_full_shape(self):
        front, _ = rc.read(support.EXAMPLE)
        front.pop("classification", None)
        c = build_artifacts.catalog_entry(front, front)["classification"]
        self.assertEqual((c["product"], c["mode"], c["tags"]), ([], [], []))
        self.assertIn(c["complexity"], {"quick", "standard", "advanced"})

    def test_a_partial_classification_keeps_its_values_and_fills_the_rest(self):
        front, _ = rc.read(support.EXAMPLE)
        front["classification"] = {"mode": ["ecommerce"]}
        c = build_artifacts.catalog_entry(front, front)["classification"]
        self.assertEqual(c["mode"], ["ecommerce"])
        self.assertEqual(c["product"], [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
