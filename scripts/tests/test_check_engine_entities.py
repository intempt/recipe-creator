#!/usr/bin/env python3
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
from recipe_contract import BUILDABLE_ENTITIES as BUILDABLE

BUILDABLE_ENTITIES = set(BUILDABLE)


def engine_file(entities):
    rows = "\n".join(f'    ("{e}", "words"),' for e in entities)
    path = pathlib.Path(tempfile.mkdtemp()) / "md_import.py"
    path.write_text(f"X = 1\nALLOWED_ENTITIES: tuple[tuple[str, str], ...] = (\n{rows}\n)\nY = 2\n")
    return path


def run(path):
    return subprocess.run([sys.executable, str(SCRIPTS / "check_engine_entities.py"), str(path)], capture_output=True, text=True)


class EngineEntities(unittest.TestCase):
    def test_matching_lists_pass(self):
        result = run(engine_file(sorted(BUILDABLE_ENTITIES)))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_an_entity_the_engine_added_fails_and_is_named(self):
        result = run(engine_file(sorted(BUILDABLE_ENTITIES) + ["journey"]))
        self.assertEqual(result.returncode, 1)
        self.assertIn("journey", result.stderr)

    def test_an_entity_the_engine_dropped_fails_and_is_named(self):
        result = run(engine_file(sorted(BUILDABLE_ENTITIES - {"sms"})))
        self.assertEqual(result.returncode, 1)
        self.assertIn("sms", result.stderr)

    def test_a_file_without_the_allowlist_fails(self):
        path = pathlib.Path(tempfile.mkdtemp()) / "md_import.py"
        path.write_text("X = 1\n")
        self.assertEqual(run(path).returncode, 2)


if __name__ == "__main__":
    unittest.main()
