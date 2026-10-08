#!/usr/bin/env python3
"""git_validate_run_recipes.py — job 2 of the draft/ flow: it runs each recipe job 1
passed, copies only the ones that validated to --out for job 3, and fails only when
every run failed."""
import contextlib
import io
import json
import os
import pathlib
import shutil
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import git_validate_run_recipes as job2


class FakeRun(BaseHTTPRequestHandler):
    fail: set = set()      # frontmatter_ids whose run does not validate
    refuse: set = set()    # frontmatter_ids whose start is refused

    def _answer(self, status, body):
        self.send_response(status)
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        recipe = json.loads(self.rfile.read(int(self.headers["Content-Length"])))["recipe"]
        key = recipe["frontmatter_id"]
        if key in FakeRun.refuse:
            return self._answer(422, {"detail": {"code": "bad_recipe", "message": "no"}})
        self._answer(200, {"chain_id": f"c-{key}"})

    def do_GET(self):
        key = self.path.split("?")[0].split("/")[-2]
        if key in FakeRun.fail:
            return self._answer(200, {"finished": True, "validated": False,
                                      "failed_step_id": "s1", "message": "boom"})
        self._answer(200, {"finished": True, "validated": True, "verdicts": [{"passed": True}]})

    def log_message(self, *a):
        pass


class Job2(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.checked = self.dir / "checked"
        self.checked.mkdir()
        for key in ("a", "b", "c"):
            (self.checked / f"{key}.json").write_text(json.dumps({"frontmatter_id": key}))
            (self.checked / f"{key}.path").write_text(f"draft/{key}.md\n")
        server = HTTPServer(("127.0.0.1", 0), FakeRun)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        self.url = f"http://127.0.0.1:{server.server_port}/v1/recipes/git_validate_run"
        os.environ["RECIPE_GIT_VALIDATE_SECRET"] = "s"
        self.addCleanup(os.environ.pop, "RECIPE_GIT_VALIDATE_SECRET", None)
        self.addCleanup(setattr, job2, "POLL_S", job2.POLL_S)
        job2.POLL_S = 0
        cfg = {"url": self.url[:-len("_run")], "org_id": 1, "project_id": 2, "person_id": 3}
        real = job2.git_validate_config.load
        job2.git_validate_config.load = lambda: cfg
        self.addCleanup(setattr, job2.git_validate_config, "load", real)

    def run_job(self, fail=(), refuse=()):
        FakeRun.fail, FakeRun.refuse = set(fail), set(refuse)
        out = self.dir / "validated"
        sys.argv = ["job2", str(self.checked), "--out", str(out), "--url", self.url]
        with contextlib.redirect_stdout(io.StringIO()) as log:
            code = job2.main()
        return code, out, log.getvalue()

    def test_a_partial_pass_is_green_and_hands_on_only_what_validated(self):
        code, out, log = self.run_job(fail={"b"}, refuse={"c"})
        self.assertEqual(code, 0)
        self.assertEqual(sorted(p.name for p in out.iterdir()), ["a.json", "a.path"])
        self.assertIn("1 passed, 2 failed", log)
        self.assertIn("FAILED  b  failed at s1: boom", log)
        self.assertIn("FAILED  c  422 bad_recipe: no", log)

    def test_every_run_failing_fails_the_job(self):
        code, out, log = self.run_job(fail={"a", "b"}, refuse={"c"})
        self.assertEqual(code, 1)
        self.assertFalse(out.exists())

    def test_all_passing_hands_on_all(self):
        code, out, _ = self.run_job()
        self.assertEqual(code, 0)
        self.assertEqual(len(list(out.iterdir())), 6)


if __name__ == "__main__":
    unittest.main()
