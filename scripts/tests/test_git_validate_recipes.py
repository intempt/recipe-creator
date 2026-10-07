#!/usr/bin/env python3
"""git_validate_recipes.py — job 1 of the draft/ flow: it sends each changed draft
(never draft/README.md, never recipes/) to LM, a new draft with a temporary key, and
records each passing answer with the draft it came from."""
import contextlib
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import git_validate_recipes as job1
import recipe_draft

DRAFT = "---\nauthor:\n  name: Beso\n  last_name: Gugushvili\n---\n# Nudge\n\n## Step 1: X\n\nDo x.\n"


class FakeLM(BaseHTTPRequestHandler):
    sent: list = []

    def do_POST(self):
        md = json.loads(self.rfile.read(int(self.headers["Content-Length"])))["markdown"]
        FakeLM.sent.append((md, self.headers.get(job1.HEADER)))
        meta, _ = recipe_draft.split(md)
        out = json.dumps({"frontmatter_id": meta["frontmatter_id"], "steps": [{"id": "s1"}]}).encode()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


class Job1(unittest.TestCase):
    def setUp(self):
        self.repo = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        self.cwd = os.getcwd()
        os.chdir(self.repo)
        self.addCleanup(os.chdir, self.cwd)
        self.git("init", "-q", "-b", "staging")
        self.put({"draft/README.md": "how\n", "draft/old.md": DRAFT, "recipes/intempt/a/recipe.md": "a\n"})
        self.git("commit", "-qm", "base")
        self.git("branch", "base")
        self.put({"draft/new.md": DRAFT, "draft/team/edit.md": DRAFT.replace("---\nauthor", "---\nfrontmatter_id: a\nauthor"),
                  "draft/README.md": "more\n", "recipes/intempt/a/recipe.md": "b\n", "draft/notes.txt": "x\n"})
        self.git("rm", "-q", "draft/old.md")
        self.git("commit", "-qm", "change")

    def git(self, *args):
        env = {**os.environ, "GIT_AUTHOR_NAME": "B", "GIT_AUTHOR_EMAIL": "b@x",
               "GIT_COMMITTER_NAME": "B", "GIT_COMMITTER_EMAIL": "b@x"}
        subprocess.run(["git", *args], check=True, capture_output=True, env=env)

    def put(self, files):
        for path, text in files.items():
            p = self.repo / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        self.git("add", "-A")

    def test_only_added_or_changed_drafts_are_selected(self):
        self.assertEqual(job1.changed_drafts("base"), ["draft/new.md", "draft/team/edit.md"])

    def test_main_sends_a_temporary_key_and_records_the_draft(self):
        server = HTTPServer(("127.0.0.1", 0), FakeLM)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        FakeLM.sent = []
        out = self.repo / "checked"
        url = f"http://127.0.0.1:{server.server_port}/v1/recipes/git_validate"
        os.environ["RECIPE_GIT_VALIDATE_SECRET"] = "s"
        self.addCleanup(os.environ.pop, "RECIPE_GIT_VALIDATE_SECRET", None)
        sys.argv = ["job1", "--base", "base", "--url", url, "--out", str(out)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(job1.main(), 0)
        keys = sorted(recipe_draft.split(md)[0]["frontmatter_id"] for md, _ in FakeLM.sent)
        self.assertEqual(keys, ["a", "draft-new"])
        self.assertEqual({secret for _, secret in FakeLM.sent}, {"s"})
        self.assertEqual((out / "draft-new.path").read_text().strip(), "draft/new.md")
        self.assertEqual((out / "a.path").read_text().strip(), "draft/team/edit.md")

    def test_a_draft_with_broken_yaml_fails_without_a_call(self):
        bad = self.repo / "draft" / "bad.md"
        bad.write_text("---\nauthor: [\n---\n# X\n")
        os.environ["RECIPE_GIT_VALIDATE_SECRET"] = "s"
        self.addCleanup(os.environ.pop, "RECIPE_GIT_VALIDATE_SECRET", None)
        sys.argv = ["job1", "--url", "http://127.0.0.1:9/never", str(bad)]
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(job1.main(), 1)
        self.assertIn("not valid YAML", out.getvalue())


if __name__ == "__main__":
    unittest.main()
