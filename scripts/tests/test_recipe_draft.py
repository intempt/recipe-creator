#!/usr/bin/env python3
"""recipe_draft.py: what job 1, job 3 and the gate share — the temporary key job 1
sends LM, the owner (D1) and the unique key (D2)."""
import pathlib
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import recipe_draft as rd

BODY = "# Nudge\n\n## Step 1: X\n\nDo x.\n"


class WithKey(unittest.TestCase):
    def test_no_front_matter_gets_one_with_the_key(self):
        out = rd.with_key(BODY, "draft-nudge")
        self.assertEqual(rd.split(out), ({"frontmatter_id": "draft-nudge"}, BODY))

    def test_front_matter_without_a_key_gets_it_as_its_first_line(self):
        text = "\n\n---\nauthor:\n  name: B\n---\n" + BODY
        out = rd.with_key(text, "draft-nudge")
        self.assertEqual(out, '\n\n---\nfrontmatter_id: "draft-nudge"\nauthor:\n  name: B\n---\n' + BODY)
        self.assertEqual(rd.split(out)[0]["author"], {"name": "B"})

    def test_a_bom_and_crlf_are_kept(self):
        text = "﻿---\r\nauthor:\r\n  name: B\r\n---\r\n" + BODY
        out = rd.with_key(text, "k")
        self.assertTrue(out.startswith('﻿---\r\nfrontmatter_id: "k"\r\nauthor:'))

    def test_a_draft_naming_its_key_is_sent_unchanged(self):
        text = "---\nfrontmatter_id: nudge\n---\n" + BODY
        self.assertIs(rd.with_key(text, "draft-x"), text)

    def test_bad_yaml_is_a_draft_error(self):
        with self.assertRaises(rd.DraftError):
            rd.with_key("---\nauthor: [\n---\n" + BODY, "k")
        with self.assertRaises(rd.DraftError):
            rd.split("---\n- a list\n---\n")


class Names(unittest.TestCase):
    def test_temp_key_is_per_draft_path(self):
        self.assertEqual(rd.temp_key("draft/Form Nudge.md"), "draft-form-nudge")
        self.assertEqual(rd.temp_key("draft/team/a.md"), "draft-team-a")
        self.assertNotEqual(rd.temp_key("draft/a/b.md"), rd.temp_key("draft/a-c.md"))

    def test_is_draft(self):
        self.assertTrue(rd.is_draft("draft/x.md"))
        self.assertTrue(rd.is_draft("draft/team/x.md"))
        self.assertFalse(rd.is_draft("draft/README.md"))
        self.assertFalse(rd.is_draft("draft/x.txt"))
        self.assertFalse(rd.is_draft("recipes/intempt/x/recipe.md"))

    def test_d1_owner(self):
        self.assertEqual(rd.owner_of({}), "intempt")
        self.assertEqual(rd.owner_of({"author": {"name": "B"}}), "intempt")
        self.assertEqual(rd.owner_of({"author": {"org_name": " "}}), "intempt")
        self.assertEqual(rd.owner_of({"author": {"org_name": "acme-co"}}), "acme-co")
        for bad in ("Acme", "acme co", "../x", "-x", "a--b"):
            with self.subTest(bad=bad), self.assertRaises(rd.DraftError):
                rd.owner_of({"author": {"org_name": bad}})

    def test_d2_new_key(self):
        self.assertEqual(rd.new_key("a", set()), "a")
        self.assertEqual(rd.new_key("a", {"a"}), "a-2")
        self.assertEqual(rd.new_key("a", {"a", "a-2", "a-3"}), "a-4")
        self.assertEqual(rd.slugify("/Form-Abandonment Nudge!"), "form-abandonment-nudge")


class Taken(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def put(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def test_folders_ids_keys_and_contract_slashes_are_all_taken(self):
        self.put("recipes/intempt/folder-a/recipe.md", "---\nid: id-a\nslash_command: /slash-a\n---\n")
        self.put("recipes/acme/folder-b/recipe.md", "---\nfrontmatter_id: key-b\n---\n")
        self.put("recipes/acme/folder-c/recipe.json", '{"frontmatter_id": "key-c"}')
        self.put("recipes/acme/folder-d/recipe.md", "---\nauthor: [\n---\n")
        self.assertEqual(set(rd.taken(str(self.root))),
                         {"folder-a", "id-a", "slash-a", "folder-b", "key-b", "folder-c", "key-c", "folder-d"})

    def test_find_recipe_across_owners(self):
        self.put("recipes/acme/k/recipe.md", "x")
        self.assertEqual(rd.find_recipe("k", str(self.root)), "recipes/acme/k")
        self.assertIsNone(rd.find_recipe("nope", str(self.root)))
        self.put("recipes/intempt/k/recipe.md", "x")
        with self.assertRaises(rd.DraftError):
            rd.find_recipe("k", str(self.root))


if __name__ == "__main__":
    unittest.main()
