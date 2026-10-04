#!/usr/bin/env python3
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import SCRIPTS


def recipe_md(slug):
    return f"---\nid: {slug}\ntitle: {slug}\nsteps:\n  - id: s1\n    title: One\n    description: Build the private instruction for {slug}.\n---\n\n# {slug}\n"


class SyncMarketplace(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.recipes = self.root / "recipes"
        for owner, slug in (("intempt", "alpha"), ("acme", "beta")):
            d = self.recipes / owner / slug
            d.mkdir(parents=True)
            (d / "recipe.md").write_text(recipe_md(slug))
        self.catalog = self.root / "recipes.json"
        self.write_catalog([
            {"slug": "alpha", "title": "Alpha", "procedure": [{"step": 1, "title": "One", "description": "Public summary."}]},
            {"slug": "beta", "title": "Beta", "procedure": [{"step": 1, "title": "One", "description": "Public summary."}]},
        ])
        self.out = self.root / "payload.json"

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def write_catalog(self, recipes):
        self.catalog.write_text(json.dumps({"version": "abc123", "count": len(recipes), "recipes": recipes}))

    def run_sync(self, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "sync_marketplace.py"), "--catalog", str(self.catalog),
             "--recipes", str(self.recipes), "--out", str(self.out), *extra],
            capture_output=True, text=True,
        )

    def test_payload_carries_version_public_objects_and_every_source(self):
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(self.out.read_text())
        self.assertEqual(payload["version"], "abc123")
        self.assertEqual([r["slug"] for r in payload["recipes"]], ["alpha", "beta"])
        self.assertEqual(payload["sources"]["beta"], recipe_md("beta"))
        self.assertEqual(set(payload["sources"]), {"alpha", "beta"})

    def test_refuses_a_catalog_recipe_with_no_source_file(self):
        shutil.rmtree(self.recipes / "acme")
        result = self.run_sync()
        self.assertEqual(result.returncode, 1)
        self.assertIn("beta", result.stderr)

    def test_public_step_summary_under_the_description_key_is_allowed(self):
        self.assertEqual(self.run_sync().returncode, 0)

    def test_refuses_a_public_step_that_repeats_its_engine_instruction(self):
        self.write_catalog([{"slug": "alpha", "procedure": [{"step": 1, "description": "Build the private instruction for alpha."}]}])
        shutil.rmtree(self.recipes / "acme")
        result = self.run_sync()
        self.assertEqual(result.returncode, 1)
        self.assertIn("engine instruction", result.stderr)

    def test_refuses_duplicate_slugs(self):
        self.write_catalog([{"slug": "alpha", "procedure": []}, {"slug": "alpha", "procedure": []}])
        result = self.run_sync()
        self.assertEqual(result.returncode, 1)
        self.assertIn("alpha", result.stderr)

    def test_sending_requires_a_token(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "sync_marketplace.py"), "--catalog", str(self.catalog),
             "--recipes", str(self.recipes), "--url", "http://127.0.0.1:9/v1/marketplace/recipes"],
            capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"},
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("MARKETPLACE_SYNC_SECRET", result.stderr)


if __name__ == "__main__":
    unittest.main()
