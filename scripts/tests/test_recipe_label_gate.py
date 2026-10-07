#!/usr/bin/env python3
"""The draft/ flow's PR gate: only the write-back bot touches recipes/, and a draft in
the tree keeps the check red (label missing → add it; label on → being validated)."""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import recipe_draft
import recipe_label_gate as gate
from recipe_label_gate import LABEL, verdict


class Verdict(unittest.TestCase):
    def test_a_person_touching_recipes_fails_and_is_named(self):
        code, message = verdict(["abc123 beso@intempt.com"], [], [LABEL])
        self.assertEqual(code, 1)
        self.assertIn("abc123 beso@intempt.com", message)

    def test_a_draft_without_the_label_fails_and_asks_for_it(self):
        code, message = verdict([], ["draft/x.md"], ["bug"])
        self.assertEqual(code, 1)
        self.assertIn(LABEL, message)
        self.assertIn("draft/x.md", message)

    def test_a_draft_with_the_label_still_fails_until_the_write_back(self):
        code, message = verdict([], ["draft/x.md"], [LABEL])
        self.assertEqual(code, 1)
        self.assertIn("being validated", message)

    def test_nothing_waiting_passes(self):
        self.assertEqual(verdict([], [], [])[0], 0)


class InARepo(unittest.TestCase):
    def setUp(self):
        self.repo = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        self.cwd = os.getcwd()
        os.chdir(self.repo)
        self.addCleanup(os.chdir, self.cwd)
        self.git("init", "-q", "-b", "staging")
        self.commit("base", {"recipes/intempt/a/recipe.md": "a\n"},
                    "Base", "base@example.com")
        self.git("branch", "base")

    def git(self, *args, env=None):
        return subprocess.run(["git", *args], check=True, capture_output=True, text=True,
                              env={**os.environ, **(env or {})}).stdout

    def commit(self, msg, files, name, email, remove=()):
        for path, text in files.items():
            p = self.repo / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        for path in remove:
            self.git("rm", "-q", path)
        self.git("add", "-A")
        who = {"GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": email,
               "GIT_COMMITTER_NAME": name, "GIT_COMMITTER_EMAIL": email}
        self.git("commit", "-q", "-m", msg, env=who)

    def run_gate(self, labels='[]'):
        return gate.main(["--base", "base", "--labels", labels])

    def test_the_draft_flow_end_to_end(self):
        self.commit("draft", {"draft/x.md": "# X\n"}, "Beso", "beso@intempt.com")
        self.assertEqual(self.run_gate(), 1)                         # no label
        self.assertEqual(self.run_gate(f'["{LABEL}"]'), 1)           # validating
        self.commit("write-back", {"recipes/intempt/x/recipe.md": "x\n"},
                    recipe_draft.BOT_NAME, recipe_draft.BOT_EMAIL, remove=["draft/x.md"])
        self.assertEqual(self.run_gate(f'["{LABEL}"]'), 0)
        self.assertEqual(self.run_gate(), 0)                         # label gone later: still fine

    def test_a_person_s_commit_to_recipes_fails_even_with_the_label(self):
        self.commit("hand edit", {"recipes/intempt/a/recipe.md": "changed\n"}, "Beso", "beso@intempt.com")
        self.assertEqual(self.run_gate(f'["{LABEL}"]'), 1)
        self.assertEqual(gate.person_commits("base")[0].split()[1], "beso@intempt.com")

    def test_a_bot_author_with_a_person_committer_is_a_person(self):
        (self.repo / "recipes/intempt/a/recipe.md").write_text("changed\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "x",
                 env={"GIT_AUTHOR_NAME": recipe_draft.BOT_NAME, "GIT_AUTHOR_EMAIL": recipe_draft.BOT_EMAIL,
                      "GIT_COMMITTER_NAME": "Beso", "GIT_COMMITTER_EMAIL": "beso@intempt.com"})
        self.assertEqual(len(gate.person_commits("base")), 1)

    def test_a_person_merging_staging_after_a_write_back_is_not_a_hand_edit(self):
        self.git("checkout", "-q", "-b", "pr")
        self.commit("write-back", {"recipes/intempt/x/recipe.md": "x\n"},
                    recipe_draft.BOT_NAME, recipe_draft.BOT_EMAIL)
        self.git("checkout", "-q", "staging")
        self.commit("on staging", {"recipes/intempt/a/recipe.md": "moved on\n"},
                    recipe_draft.BOT_NAME, recipe_draft.BOT_EMAIL)
        self.git("checkout", "-q", "pr")
        who = {"GIT_AUTHOR_NAME": "Beso", "GIT_AUTHOR_EMAIL": "beso@intempt.com",
               "GIT_COMMITTER_NAME": "Beso", "GIT_COMMITTER_EMAIL": "beso@intempt.com"}
        self.git("merge", "-q", "--no-ff", "-m", "merge staging", "staging", env=who)
        self.assertEqual(gate.person_commits("staging"), [])
        self.assertEqual(gate.main(["--base", "staging", "--labels", "[]"]), 0)

    def test_other_paths_need_nothing(self):
        self.commit("code", {"scripts/x.py": "x\n", "USAGE.md": "how\n"}, "Beso", "beso@intempt.com")
        self.assertEqual(self.run_gate(), 0)

    def test_anything_but_a_draft_in_draft_fails(self):
        self.commit("stray", {"draft/notes.txt": "x\n"}, "Beso", "beso@intempt.com")
        self.assertEqual(self.run_gate(f'["{LABEL}"]'), 1)
        code, message = verdict([], ["draft/notes.txt"], [LABEL])
        self.assertIn("not a recipe draft", message)


if __name__ == "__main__":
    unittest.main()
