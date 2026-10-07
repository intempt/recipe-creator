#!/usr/bin/env python3
"""git_validate_writeback.py: recipe.json beside each validated recipe.md, and a
`description:` line inserted into the md ONLY when its frontmatter has none —
a line insert, so everything else stays byte-identical (RG1 §51.3a, §55, §57)."""
import json
import pathlib
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import ROOT

import git_validate_writeback as wb

WITHOUT = (
    "---\n"
    "id: accounts-at-risk-count\n"
    "title: Accounts at risk\n"
    "slash_command: /accounts-at-risk-count\n"
    "# a comment the author kept\n"
    "summary: >-\n"
    "  Counts accounts in predefined engagement-decline segments and tracks the weekly total. Uses fixed segments\n"
    "  as an approximate at-risk signal.\n"
    "version: 2.0.0\n"
    "---\n"
    "\n"
    "## Steps\n"
    "description: this line is body, not frontmatter\n"
)
WITH = WITHOUT.replace("title: Accounts at risk\n",
                       "title: Accounts at risk\ndescription: >-\n  Written by the author.\n", 1)


class Insert(unittest.TestCase):
    def test_absent_inserts_one_line_right_after_title(self):
        out = wb.insert_description(WITHOUT, "Weekly count: accounts at risk.")
        self.assertEqual(out, WITHOUT.replace(
            "title: Accounts at risk\n",
            'title: Accounts at risk\ndescription: "Weekly count: accounts at risk."\n', 1))

    def test_inserted_value_parses_back_as_the_description(self):
        import yaml
        out = wb.insert_description(WITHOUT, 'Has "quotes", a # and: colons')
        meta = yaml.safe_load(out.split("---\n")[1])
        self.assertEqual(meta["description"], 'Has "quotes", a # and: colons')
        self.assertEqual(meta["summary"].split()[0], "Counts")

    def test_present_is_byte_identical(self):
        self.assertIs(wb.insert_description(WITH, "Generated."), WITH)

    def test_present_but_empty_is_still_left_alone(self):
        text = WITHOUT.replace("version: 2.0.0\n", "description:\nversion: 2.0.0\n")
        self.assertEqual(wb.insert_description(text, "Generated."), text)

    def test_body_and_folded_block_untouched(self):
        out = wb.insert_description(WITHOUT, "Generated.")
        head, body = out.split("---\n\n", 1)
        self.assertEqual(body, WITHOUT.split("---\n\n", 1)[1])
        self.assertIn("summary: >-\n  Counts accounts", head)
        self.assertIn("# a comment the author kept\n", head)
        self.assertEqual(out.replace('description: "Generated."\n', "", 1), WITHOUT)

    def test_title_with_continuation_inserts_after_the_whole_entry(self):
        text = WITHOUT.replace("title: Accounts at risk\n", "title: >-\n  Accounts\n  at risk\n")
        out = wb.insert_description(text, "D.")
        self.assertIn("title: >-\n  Accounts\n  at risk\ndescription: \"D.\"\nslash_command:", out)

    def test_crlf_file_gets_a_crlf_line(self):
        text = WITHOUT.replace("\n", "\r\n")
        out = wb.insert_description(text, "D.")
        self.assertIn('title: Accounts at risk\r\ndescription: "D."\r\nslash_command', out)

    def test_every_corpus_recipe_already_has_one_so_is_unchanged(self):
        paths = sorted((ROOT / "recipes").glob("*/*/recipe.md"))
        self.assertGreater(len(paths), 200)
        for p in paths:
            text = p.read_bytes().decode("utf-8")
            self.assertIs(wb.insert_description(text, "Generated."), text, p)

    def test_corpus_md_with_its_description_removed_round_trips(self):
        p = ROOT / "recipes" / "intempt" / "accounts-at-risk-count" / "recipe.md"
        text = p.read_text(encoding="utf-8")
        start = text.index("\ndescription: >-\n") + 1
        end = text.index("\nversion:", start) + 1
        stripped = text[:start] + text[end:]
        out = wb.insert_description(stripped, "New.")
        self.assertEqual(out.replace('description: "New."\n', "", 1), stripped)
        self.assertLess(out.index('description: "New."'), out.index("slash_command:"))

    def test_no_frontmatter_or_empty_description_is_unchanged(self):
        self.assertEqual(wb.insert_description("# no frontmatter\n", "D."), "# no frontmatter\n")
        self.assertIs(wb.insert_description(WITHOUT, "  "), WITHOUT)


class WriteBack(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def md(self, slug, text):
        p = self.root / "recipes" / "intempt" / slug / "recipe.md"
        p.parent.mkdir(parents=True)
        p.write_text(text, encoding="utf-8")
        return str(p)

    def test_writes_json_verbatim_and_inserts_missing_description(self):
        md = self.md("accounts-at-risk-count", WITHOUT)
        answer = {"f_id": "accounts-at-risk-count", "description": "Gen.", "steps": [{"id": "s1"}]}
        written, problems = wb.write_back([answer], [md])
        self.assertEqual(problems, [])
        out = pathlib.Path(md).with_name("recipe.json")
        self.assertEqual(json.loads(out.read_text()), answer)
        self.assertEqual(written, [str(out), md])
        self.assertIn('description: "Gen."', pathlib.Path(md).read_text())

    def test_present_description_md_not_rewritten(self):
        md = self.md("accounts-at-risk-count", WITH)
        written, _ = wb.write_back([{"f_id": "accounts-at-risk-count", "description": "Gen."}], [md])
        self.assertEqual(written, [str(pathlib.Path(md).with_name("recipe.json"))])
        self.assertEqual(pathlib.Path(md).read_text(), WITH)

    def test_f_id_key_wins_over_id(self):
        md = self.md("x", WITHOUT.replace("id: accounts-at-risk-count\n", "id: x\nf_id: real-f-id\n"))
        _, problems = wb.write_back([{"f_id": "real-f-id", "description": "D."}], [md])
        self.assertEqual(problems, [])

    def test_unmatched_and_duplicate_answers_are_problems(self):
        a = self.md("a", WITHOUT)
        b = self.md("b", WITHOUT)
        _, problems = wb.write_back([{"f_id": "accounts-at-risk-count"}, {"f_id": "nope"}], [a, b])
        self.assertEqual(len(problems), 2)
        self.assertIn("matches 2", problems[0])
        self.assertIn("matches 0", problems[1])
        self.assertFalse((self.root / "recipes" / "intempt" / "a" / "recipe.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
