#!/usr/bin/env python3
"""git_validate_recipes.py — job 1 of the draft/ flow: it sends each changed draft
(never a non-.md file, never recipes/) to LM, a new draft with a temporary key, and
records each answer with the draft it came from.

LM's contract (R34-5): `POST <url>/start {markdown}` → 202 {job_id}; `GET <url>/<job_id>`
→ running | done (+result) | refused (+detail, the old 422s) | failed (+detail, the old
503); 404 = unknown or expired job. A record whose steps failed is a `done` with
`failed_steps` (R34-2/R34-3): it is kept and reported, never refused."""
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
STEP_ERRORS = [{"kind": "vague", "message": "too vague"}]


class FakeLM(BaseHTTPRequestHandler):
    """The start-then-poll routes. `plan[key]` is the outcome of each successive job started
    for that frontmatter_id (default `done`):
      done     → done, every step passes          steps  → done, step s1 carries `errors`
      run1     → running once, then done          running → running forever
      refused  → refused (author_invalid)         failed → failed (check_failed)
      lost     → the poll answers 404"""
    sent: list = []        # (markdown, secret) per start
    calls: list = []       # (method, path)
    plan: dict = {}
    jobs: dict = {}

    def _send(self, code, body):
        out = json.dumps(body).encode()
        self.send_response(code)
        self.end_headers()
        self.wfile.write(out)

    def do_POST(self):
        FakeLM.calls.append(("POST", self.path))
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if self.headers.get(job1.HEADER) != "s":
            return self._send(404, {"detail": "Not found."})
        if not self.path.endswith("/git_validate/start"):
            return self._send(410, {"detail": "the sync route is not used"})
        md = body["markdown"]
        FakeLM.sent.append((md, self.headers.get(job1.HEADER)))
        key = recipe_draft.split(md)[0]["frontmatter_id"]
        queue = FakeLM.plan.get(key) or []
        outcome = queue.pop(0) if queue else "done"
        job_id = f"gv_{len(FakeLM.jobs):012x}"
        FakeLM.jobs[job_id] = {"key": key, "outcome": outcome, "polls": 0}
        self._send(202, {"job_id": job_id})

    def do_GET(self):
        FakeLM.calls.append(("GET", self.path))
        if self.headers.get(job1.HEADER) != "s":
            return self._send(404, {"detail": "Not found."})
        job = FakeLM.jobs.get(self.path.rsplit("/", 1)[-1])
        if job is None or job["outcome"] == "lost":
            return self._send(404, {"detail": "Job not found."})
        job["polls"] += 1
        outcome = job["outcome"]
        if outcome == "running" or (outcome == "run1" and job["polls"] == 1):
            return self._send(200, {"state": "running"})
        if outcome == "refused":
            return self._send(200, {"state": "refused", "detail": {
                "code": "author_invalid", "message": "The author needs a name.", "missing": ["last_name"]}})
        if outcome == "failed":
            return self._send(200, {"state": "failed", "detail": {
                "code": "check_failed", "message": "The check could not be made."}})
        steps = [{"id": "s1", "title": "X"}, {"id": "s2", "title": "Y"}]
        failed = []
        if outcome == "steps":
            steps[0]["errors"] = STEP_ERRORS
            failed = [{"id": "s1", "title": "X", "errors": STEP_ERRORS}]
        self._send(200, {"state": "done", "result": {
            "frontmatter_id": job["key"], "steps": steps, "failed_steps": failed}})

    def log_message(self, *a):
        pass


class Server(unittest.TestCase):
    def serve(self):
        server = HTTPServer(("127.0.0.1", 0), FakeLM)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        FakeLM.sent, FakeLM.calls, FakeLM.plan, FakeLM.jobs = [], [], {}, {}
        return f"http://127.0.0.1:{server.server_port}/v1/recipes/git_validate"


class Client(Server):
    """job1.validate: start → poll → the same (status, body) the sync route used to give."""
    MD = "---\nfrontmatter_id: k\n---\n# K\n"

    def check(self, *outcomes, timeout_s=10.0, retries=1):
        url = self.serve()
        FakeLM.plan = {"k": list(outcomes)}
        return job1.validate(url, "s", self.MD, timeout_s=timeout_s, interval_s=0.01,
                             retries=retries)

    def starts(self):
        return [p for m, p in FakeLM.calls if m == "POST"]

    def test_running_then_done_is_the_record(self):
        status, body = self.check("run1")
        self.assertEqual(status, 200)
        self.assertEqual(body["frontmatter_id"], "k")
        self.assertEqual(body["failed_steps"], [])
        self.assertEqual(len(self.starts()), 1)
        self.assertGreaterEqual(sum(1 for m, _ in FakeLM.calls if m == "GET"), 2)

    def test_it_starts_then_polls_the_job_never_the_sync_route(self):
        self.check("done")
        self.assertEqual(FakeLM.calls[0], ("POST", "/v1/recipes/git_validate/start"))
        self.assertEqual(FakeLM.calls[1], ("GET", "/v1/recipes/git_validate/gv_000000000000"))

    def test_failed_steps_are_a_record_not_a_refusal(self):
        status, body = self.check("steps")
        self.assertEqual(status, 200)
        self.assertEqual(body["steps"][0]["errors"], STEP_ERRORS)
        self.assertEqual(body["failed_steps"][0]["id"], "s1")

    def test_refused_is_the_old_422(self):
        status, body = self.check("refused")
        self.assertEqual(status, 422)
        self.assertEqual(body["detail"]["code"], "author_invalid")
        self.assertEqual(len(self.starts()), 1)   # a refusal is not retried

    def test_failed_is_retried_as_a_new_job(self):
        status, body = self.check("failed", "done")
        self.assertEqual(status, 200)
        self.assertEqual(len(self.starts()), 2)

    def test_failed_past_the_retries_is_the_old_503(self):
        status, body = self.check("failed", "failed", "done", retries=1)
        self.assertEqual(status, 503)
        self.assertEqual(body["detail"]["code"], "check_failed")
        self.assertEqual(len(self.starts()), 2)

    def test_a_lost_job_is_restarted_once(self):
        status, _ = self.check("lost", "done")
        self.assertEqual(status, 200)
        self.assertEqual(len(self.starts()), 2)

    def test_a_job_lost_twice_fails(self):
        status, body = self.check("lost", "lost", "done")
        self.assertNotEqual(status, 200)
        self.assertIn("job", body["detail"]["message"].lower())
        self.assertEqual(len(self.starts()), 2)

    def test_a_job_that_never_ends_times_out(self):
        status, body = self.check("running", timeout_s=0.3)
        self.assertEqual(body["detail"]["code"], "timeout")
        self.assertNotEqual(status, 200)

    def test_a_transport_error_is_retried_then_fails(self):
        status, body = job1.validate("http://127.0.0.1:9/v1/recipes/git_validate", "s", self.MD,
                                     timeout_s=5, interval_s=0.01, retries=1)
        self.assertEqual(status, 503)
        self.assertEqual(body["detail"]["code"], "unreachable")

    def test_a_wrong_secret_is_the_404_it_always_was(self):
        url = self.serve()
        status, _ = job1.validate(url, "wrong", self.MD, timeout_s=5, interval_s=0.01, retries=1)
        self.assertEqual(status, 404)


class Job1(Server):
    def setUp(self):
        self.repo = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        self.cwd = os.getcwd()
        os.chdir(self.repo)
        self.addCleanup(os.chdir, self.cwd)
        self.git("init", "-q", "-b", "staging")
        self.put({"draft/old.md": DRAFT, "recipes/intempt/a/recipe.md": "a\n"})
        self.git("commit", "-qm", "base")
        self.git("branch", "base")
        self.put({"draft/new.md": DRAFT, "draft/team/edit.md": DRAFT.replace("---\nauthor", "---\nfrontmatter_id: a\nauthor"),
                  "recipes/intempt/a/recipe.md": "b\n", "draft/notes.txt": "x\n"})
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

    def _run(self, plan=None):
        url = self.serve()
        FakeLM.plan = {k: list(v) for k, v in (plan or {}).items()}
        out = self.repo / "checked"
        summary = self.repo / "summary.md"
        os.environ["RECIPE_GIT_VALIDATE_SECRET"] = "s"
        os.environ["GITHUB_STEP_SUMMARY"] = str(summary)
        self.addCleanup(os.environ.pop, "RECIPE_GIT_VALIDATE_SECRET", None)
        self.addCleanup(os.environ.pop, "GITHUB_STEP_SUMMARY", None)
        sys.argv = ["job1", "--base", "base", "--url", url, "--out", str(out), "--poll-interval", "0.01"]
        with contextlib.redirect_stdout(io.StringIO()) as log:
            code = job1.main()
        return code, out, log.getvalue(), summary.read_text() if summary.exists() else ""

    def test_only_added_or_changed_drafts_are_selected(self):
        self.assertEqual(job1.changed_drafts("base"), ["draft/new.md", "draft/team/edit.md"])

    def test_main_sends_a_temporary_key_and_records_the_draft(self):
        code, out, _, _ = self._run()
        self.assertEqual(code, 0)
        keys = sorted(recipe_draft.split(md)[0]["frontmatter_id"] for md, _ in FakeLM.sent)
        self.assertEqual(keys, ["a", "draft-new"])
        self.assertEqual({secret for _, secret in FakeLM.sent}, {"s"})
        self.assertEqual((out / "draft-new.path").read_text().strip(), "draft/new.md")
        self.assertEqual((out / "a.path").read_text().strip(), "draft/team/edit.md")

    def test_failed_steps_are_kept_and_reported_not_failed(self):
        code, out, log, summary = self._run({"draft-new": ["steps"]})
        self.assertEqual(code, 0)
        self.assertEqual(sorted(p.name for p in out.iterdir()),
                         ["a.json", "a.path", "draft-new.json", "draft-new.path"])
        saved = json.loads((out / "draft-new.json").read_text())
        self.assertEqual(saved["steps"][0]["errors"], STEP_ERRORS)
        self.assertNotIn("errors", saved["steps"][1])
        self.assertIn("2 passed, 0 failed", log)
        self.assertIn("- X: [vague] too vague", log)
        self.assertIn("::warning", log)
        self.assertIn("draft/new.md", summary)
        self.assertIn("too vague", summary)

    def test_every_draft_with_failed_steps_is_still_green(self):
        code, out, log, _ = self._run({"draft-new": ["steps"], "a": ["steps"]})
        self.assertEqual(code, 0)
        self.assertIn("2 passed, 0 failed", log)

    def test_a_refusal_is_a_partial_pass_and_keeps_only_what_passed(self):
        code, out, log, _ = self._run({"draft-new": ["refused"]})
        self.assertEqual(code, 0)
        self.assertEqual(sorted(p.name for p in out.iterdir()), ["a.json", "a.path"])
        self.assertIn("1 passed, 1 failed", log)
        self.assertIn("FAILED  draft/new.md  422 author_invalid", log)
        self.assertIn("missing: last_name", log)
        self.assertIn("::warning", log)

    def test_every_draft_refused_fails_the_job(self):
        code, out, log, _ = self._run({"draft-new": ["refused"], "a": ["refused"]})
        self.assertEqual(code, 1)
        self.assertFalse(out.exists())
        self.assertIn("0 passed, 2 failed", log)

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
