#!/usr/bin/env python3
"""git_validate_writeback.py — job 3 of the draft/ flow (R-RG4-6): each validated
draft becomes recipes/<owner>/<frontmatter_id>/recipe.md + recipe.json and is deleted.
Owner D1, key D2, edit D3; each draft stands on its own (a problem leaves only that draft)."""
import contextlib
import io
import json
import pathlib
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import ROOT  # noqa: F401  (puts scripts/ on sys.path)

import check_recipe_consistency
import git_validate_writeback as wb
import recipe_draft

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures" / "drafts"
CONTRACT = "---\nid: {id}\ntitle: T\nslash_command: {slash}\n---\nbody\n"


def answer(**over):
    a = {"frontmatter_id": "draft-form-abandonment-nudge", "title": "Form Abandonment Nudge",
         "slash_command": "/form-abandonment-nudge", "description": "Nudges form abandoners.",
         "markdown": "# Form Abandonment Nudge\n", "classification": {"industry": ["ecommerce"]},
         "complexity": "medium", "author": {"name": "Beso", "last_name": "Gugushvili"},
         "steps": [{"id": "s1"}, {"id": "s2"}, {"id": "s3"}]}
    a.update(over)
    return a


class Base(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        (self.root / "draft").mkdir()
        (self.root / "recipes").mkdir()

    def draft(self, name, text=None, fixture=None):
        p = self.root / "draft" / name
        p.write_text(text if text is not None else (FIXTURES / fixture).read_text(encoding="utf-8"),
                     encoding="utf-8")
        return f"draft/{name}"

    def recipe(self, owner, key, md, record=None):
        d = self.root / "recipes" / owner / key
        d.mkdir(parents=True)
        (d / "recipe.md").write_text(md, encoding="utf-8")
        if record is not None:
            (d / "recipe.json").write_text(json.dumps(record), encoding="utf-8")
        return d

    def run_plan(self, pairs):
        plans, problems = wb.plan(pairs, str(self.root))
        if not problems:
            wb.apply(plans, str(self.root))
        return plans, problems

    def written(self, owner, key):
        d = self.root / "recipes" / owner / key
        md = (d / "recipe.md").read_text(encoding="utf-8")
        return d, recipe_draft.split(md), json.loads((d / "recipe.json").read_text(encoding="utf-8"))


class NewRecipe(Base):
    def test_a_new_draft_becomes_md_and_json_and_is_deleted(self):
        draft = self.draft("form-abandonment-nudge.md", fixture="form-abandonment-nudge.md")
        _, problems = self.run_plan([(answer(), draft)])
        self.assertEqual(problems, [])
        d, (front, body), record = self.written("intempt", "form-abandonment-nudge")
        self.assertFalse((self.root / draft).exists())
        self.assertEqual(list(front), ["frontmatter_id", "slash_command", "description", "author"])
        self.assertEqual(front["frontmatter_id"], "form-abandonment-nudge")
        self.assertEqual(front["slash_command"], "/form-abandonment-nudge")
        self.assertEqual(front["author"], {"name": "Beso", "last_name": "Gugushvili", "org_name": "intempt"})
        _, draft_body = recipe_draft.split((FIXTURES / "form-abandonment-nudge.md").read_text(encoding="utf-8"))
        self.assertEqual(body.lstrip("\n"), draft_body.lstrip("\n"))
        self.assertEqual(record["frontmatter_id"], "form-abandonment-nudge")
        self.assertEqual(record["author"]["org_name"], "intempt")
        self.assertEqual(record["steps"], answer()["steps"])
        self.assertEqual(check_recipe_consistency.check(str(d)), [])

    def test_the_second_fixture_with_leading_blank_lines(self):
        draft = self.draft("whatever.md", fixture="email-nonopener-reengagement.md")
        a = answer(frontmatter_id="draft-whatever", title="Email Non-Opener Re-Engagement",
                   slash_command="/email-nonopener-reengagement")
        _, problems = self.run_plan([(a, draft)])
        self.assertEqual(problems, [])
        d, (front, body), _ = self.written("intempt", "email-nonopener-reengagement")
        self.assertTrue(body.lstrip("\n").startswith("# Email Non-Opener Re-Engagement\n"))
        self.assertEqual(check_recipe_consistency.check(str(d)), [])

    def test_d1_missing_org_name_is_intempt(self):
        text = (FIXTURES / "form-abandonment-nudge.md").read_text(encoding="utf-8").replace("  org_name: intempt\n", "")
        _, problems = self.run_plan([(answer(), self.draft("f.md", text))])
        self.assertEqual(problems, [])
        self.assertEqual(self.written("intempt", "form-abandonment-nudge")[2]["author"]["org_name"], "intempt")

    def test_another_org_name_is_the_owner_folder(self):
        text = (FIXTURES / "form-abandonment-nudge.md").read_text(encoding="utf-8").replace("org_name: intempt", "org_name: acme")
        _, problems = self.run_plan([(answer(), self.draft("f.md", text))])
        self.assertEqual(problems, [])
        self.assertTrue((self.root / "recipes" / "acme" / "form-abandonment-nudge" / "recipe.json").exists())

    def test_d2_a_clash_with_any_owner_gets_dash_2_and_the_slash_follows(self):
        self.recipe("acme", "form-abandonment-nudge", CONTRACT.format(id="form-abandonment-nudge", slash="/x"))
        _, problems = self.run_plan([(answer(), self.draft("f.md", fixture="form-abandonment-nudge.md"))])
        self.assertEqual(problems, [])
        _, (front, _), record = self.written("intempt", "form-abandonment-nudge-2")
        self.assertEqual(front["slash_command"], "/form-abandonment-nudge-2")
        self.assertEqual(record["slash_command"], "/form-abandonment-nudge-2")

    def test_d2_a_contract_recipe_s_slash_command_is_a_clash_too(self):
        self.recipe("intempt", "other", CONTRACT.format(id="other", slash="/form-abandonment-nudge"))
        self.run_plan([(answer(), self.draft("f.md", fixture="form-abandonment-nudge.md"))])
        self.assertTrue((self.root / "recipes" / "intempt" / "form-abandonment-nudge-2").is_dir())

    def test_d2_counts_past_2_and_two_drafts_in_one_run_do_not_collide(self):
        self.recipe("intempt", "form-abandonment-nudge", CONTRACT.format(id="form-abandonment-nudge", slash="/a"))
        self.recipe("intempt", "form-abandonment-nudge-2", CONTRACT.format(id="form-abandonment-nudge-2", slash="/b"))
        a = self.draft("a.md", fixture="form-abandonment-nudge.md")
        b = self.draft("b.md", fixture="form-abandonment-nudge.md")
        _, problems = self.run_plan([(answer(), a), (answer(), b)])
        self.assertEqual(problems, [])
        for key in ("form-abandonment-nudge-3", "form-abandonment-nudge-4"):
            self.assertTrue((self.root / "recipes" / "intempt" / key / "recipe.json").exists(), key)

    def test_no_slash_command_falls_back_to_the_title(self):
        self.run_plan([(answer(slash_command=None), self.draft("f.md", fixture="form-abandonment-nudge.md"))])
        self.assertTrue((self.root / "recipes" / "intempt" / "form-abandonment-nudge").is_dir())

    def test_an_author_description_is_what_both_files_carry(self):
        text = (FIXTURES / "form-abandonment-nudge.md").read_text(encoding="utf-8").replace(
            "---\nauthor:", '---\ndescription: "Written by Beso."\nauthor:', 1)
        # LM keeps a front-matter description (git_validate.description_of), so its answer carries it.
        self.run_plan([(answer(description="Written by Beso."), self.draft("f.md", text))])
        _, (front, _), record = self.written("intempt", "form-abandonment-nudge")
        self.assertEqual(front["description"], "Written by Beso.")
        self.assertEqual(record["description"], "Written by Beso.")


class Edit(Base):
    def existing(self, owner="intempt"):
        md = ("---\nfrontmatter_id: form-abandonment-nudge\nslash_command: /nudge\ndescription: Old.\n"
              f"author:\n  name: Beso\n  last_name: Gugushvili\n  org_name: {owner}\n---\n# Old\n")
        return self.recipe(owner, "form-abandonment-nudge", md,
                           {"frontmatter_id": "form-abandonment-nudge", "slash_command": "/nudge"})

    def edit_draft(self, owner="intempt"):
        text = (FIXTURES / "form-abandonment-nudge.md").read_text(encoding="utf-8").replace(
            "---\nauthor:", "---\nfrontmatter_id: form-abandonment-nudge\nauthor:", 1)
        return self.draft("edit.md", text.replace("org_name: intempt", f"org_name: {owner}"))

    def test_d3_keeps_key_folder_and_slash_command(self):
        self.existing()
        draft = self.edit_draft()
        _, problems = self.run_plan([(answer(frontmatter_id="form-abandonment-nudge",
                                             slash_command="/something-else"), draft)])
        self.assertEqual(problems, [])
        d, (front, body), record = self.written("intempt", "form-abandonment-nudge")
        self.assertEqual(front["slash_command"], "/nudge")
        self.assertEqual(record["slash_command"], "/nudge")
        self.assertIn("## Step 1: Create Form Abandoners Segment", body)
        self.assertFalse((self.root / draft).exists())
        self.assertEqual(sorted(p.name for p in (self.root / "recipes" / "intempt").iterdir()),
                         ["form-abandonment-nudge"])
        self.assertEqual(check_recipe_consistency.check(str(d)), [])

    def test_an_edit_of_an_unknown_key_is_refused(self):
        _, problems = self.run_plan([(answer(frontmatter_id="form-abandonment-nudge"), self.edit_draft())])
        self.assertIn("names no recipe to edit", problems[0])

    def test_an_edit_under_another_owner_is_refused(self):
        self.existing(owner="acme")
        _, problems = self.run_plan([(answer(frontmatter_id="form-abandonment-nudge"), self.edit_draft())])
        self.assertIn("belongs to 'acme'", problems[0])

    def test_an_edit_of_a_contract_recipe_is_refused(self):
        self.recipe("intempt", "form-abandonment-nudge", CONTRACT.format(id="form-abandonment-nudge", slash="/x"))
        _, problems = self.run_plan([(answer(frontmatter_id="form-abandonment-nudge"), self.edit_draft())])
        self.assertIn("contract recipe", problems[0])


class Refusals(Base):
    def _job1_dir(self, pairs):
        out = self.root / "checked"
        out.mkdir()
        for name, path, ans in pairs:
            (out / f"{name}.json").write_text(json.dumps(ans))
            (out / f"{name}.path").write_text(path + "\n")
        return out

    def test_one_problem_leaves_that_draft_and_writes_the_others(self):
        good = self.draft("good.md", fixture="form-abandonment-nudge.md")
        bad_text = (FIXTURES / "form-abandonment-nudge.md").read_text(encoding="utf-8").replace("org_name: intempt", "org_name: Acme Inc")
        bad = self.draft("bad.md", bad_text)
        out = self._job1_dir([("a", good, answer()), ("b", bad, answer())])
        with contextlib.redirect_stdout(io.StringIO()) as log:
            self.assertEqual(wb.main([str(out), "--root", str(self.root)]), 0)
        self.assertFalse((self.root / good).exists())
        self.assertTrue((self.root / bad).exists())
        self.assertEqual(check_recipe_consistency.check(
            str(self.root / "recipes" / "intempt" / "form-abandonment-nudge")), [])
        self.assertIn("PASSED  draft/good.md", log.getvalue())
        self.assertIn("FAILED  draft/bad.md", log.getvalue())
        self.assertIn("::warning", log.getvalue())

    def test_every_draft_failing_fails_and_writes_nothing(self):
        d = self.draft("f.md", fixture="form-abandonment-nudge.md")
        out = self._job1_dir([("a", d, answer(description=""))])
        with contextlib.redirect_stdout(io.StringIO()) as log:
            self.assertEqual(wb.main([str(out), "--root", str(self.root)]), 1)
        self.assertEqual(list((self.root / "recipes").iterdir()), [])
        self.assertTrue((self.root / d).exists())
        self.assertIn("0 passed, 1 failed", log.getvalue())
        self.assertNotIn("::warning", log.getvalue())

    def test_an_inconsistent_result_is_put_back_alone(self):
        good = self.draft("good.md", fixture="form-abandonment-nudge.md")
        other = self.draft("other.md", fixture="form-abandonment-nudge.md")
        plans, problems = wb.plan([(answer(), good), (answer(), other)], str(self.root))
        self.assertEqual(problems, [])
        real = check_recipe_consistency.check
        bad_folder = plans[1]["folder"]
        check_recipe_consistency.check = (
            lambda folder: ["mismatch"] if folder.endswith(bad_folder) else real(folder))
        self.addCleanup(setattr, check_recipe_consistency, "check", real)
        with contextlib.redirect_stdout(io.StringIO()):
            written, failed = wb.apply_each(plans, str(self.root))
        self.assertEqual(written, [good])
        self.assertEqual([d for d, _ in failed], [other])
        self.assertTrue((self.root / other).exists())
        self.assertFalse((self.root / bad_folder).exists())
        self.assertFalse((self.root / good).exists())

    def test_no_description_or_author_is_a_problem(self):
        d = self.draft("f.md", fixture="form-abandonment-nudge.md")
        self.assertIn("no description", wb.plan([(answer(description=""), d)], str(self.root))[1][0])
        self.assertIn("no author", wb.plan([(answer(author={"name": "B"}), d)], str(self.root))[1][0])

    def test_load_wants_a_recorded_draft_path(self):
        out = self.root / "checked"
        out.mkdir()
        (out / "a.json").write_text(json.dumps({"frontmatter_id": "a"}))
        (out / "a.path").write_text("draft/a.md\n")
        (out / "b.json").write_text(json.dumps({"frontmatter_id": "b"}))
        (out / "c.json").write_text(json.dumps({"frontmatter_id": "c"}))
        (out / "c.path").write_text("recipes/intempt/c/recipe.md\n")
        pairs, problems = wb.load(str(out))
        self.assertEqual(pairs, [({"frontmatter_id": "a"}, "draft/a.md")])
        self.assertEqual(len(problems), 2)

    def test_main_end_to_end_from_job_1_s_directory(self):
        draft = self.draft("form-abandonment-nudge.md", fixture="form-abandonment-nudge.md")
        out = self.root / "checked"
        out.mkdir()
        (out / "draft-form-abandonment-nudge.json").write_text(json.dumps(answer()))
        (out / "draft-form-abandonment-nudge.path").write_text(draft + "\n")
        self.assertEqual(wb.main([str(out), "--root", str(self.root)]), 0)
        self.assertFalse((self.root / draft).exists())
        self.assertEqual(check_recipe_consistency.check(
            str(self.root / "recipes" / "intempt" / "form-abandonment-nudge")), [])

    def test_failed_steps_are_written_with_their_errors(self):
        """R34-3: a record whose steps failed is written (and later deployed) like any other;
        each failed step's `errors` reaches recipe.json, which recipe_deploy.py sends as-is."""
        errors = [{"kind": "vague", "message": "too vague"}]
        steps = [{"id": "s1", "errors": errors}, {"id": "s2"}, {"id": "s3"}]
        failed = [{"id": "s1", "title": "One", "errors": errors}]
        draft = self.draft("form-abandonment-nudge.md", fixture="form-abandonment-nudge.md")
        out = self.root / "checked"
        out.mkdir()
        (out / "draft-form-abandonment-nudge.json").write_text(
            json.dumps(answer(steps=steps, failed_steps=failed)))
        (out / "draft-form-abandonment-nudge.path").write_text(draft + "\n")
        with contextlib.redirect_stdout(io.StringIO()) as log:
            self.assertEqual(wb.main([str(out), "--root", str(self.root)]), 0)
        self.assertIn("1 passed, 0 failed", log.getvalue())
        _, _, record = self.written("intempt", "form-abandonment-nudge")
        self.assertEqual(record["steps"], steps)
        self.assertEqual(record["failed_steps"], failed)


if __name__ == "__main__":
    unittest.main(verbosity=1)
