#!/usr/bin/env python3
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import ROOT

import recipe_contract as rc

FAMILY = ROOT / "references" / "entities"
ROW = re.compile(r"^\|[^|]+\|([^|]+)\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|$", re.M)


def index_rows():
    rows = {}
    for match in ROW.finditer((FAMILY / "README.md").read_text(encoding="utf-8")):
        for entity in re.findall(r"`([a-z_]+)`", match.group(1)):
            rows[entity] = match.group(3)
    return rows


class EntityDocs(unittest.TestCase):
    def test_every_buildable_entity_has_a_row_in_the_index(self):
        rows = index_rows()
        for entity in rc.BUILDABLE_ENTITIES:
            self.assertIn(entity, rows, f"{entity} has no family page in references/entities/README.md")

    def test_every_page_the_index_links_exists_and_names_its_entities(self):
        for entity, page in index_rows().items():
            text = (FAMILY / page).read_text(encoding="utf-8")
            self.assertIn(f"| `{entity}` |", text, f"{page} has no table row for {entity}")

    def test_no_family_page_lists_an_entity_the_contract_does_not_know(self):
        known = set(rc.BUILDABLE_ENTITIES) | set(rc.COMING_SOON_ENTITIES)
        for page in FAMILY.glob("*.md"):
            for entity in re.findall(r"^\| `([a-z_]+)` \|", page.read_text(encoding="utf-8"), re.M):
                if entity != "builds":
                    self.assertIn(entity, known, f"{page.name} lists {entity}")


if __name__ == "__main__":
    unittest.main(verbosity=1)
