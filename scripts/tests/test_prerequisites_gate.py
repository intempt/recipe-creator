#!/usr/bin/env python3
"""scripts/prerequisites_gate.sh is what the write-back job runs before it reports
`prerequisites` green on its own commit, so it must run every step the workflow runs.
A step added to recipe-prerequisites.yml and not to the script fails here."""
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "recipe-prerequisites.yml"
SCRIPT = ROOT / "scripts" / "prerequisites_gate.sh"
# Steps the script leaves out on purpose (its header says why).
SKIPPED = ("ENGINE_READ_TOKEN", "pip install")


class GateMatchesWorkflow(unittest.TestCase):
    def test_every_workflow_step_is_in_the_script(self):
        steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["prerequisites"]["steps"]
        runs = [s["run"].strip() for s in steps if "run" in s]
        script = [ln.strip() for ln in SCRIPT.read_text().splitlines()]
        checked = 0
        for run in runs:
            if any(k in run for k in SKIPPED):
                continue
            if run.startswith("echo ") or "curl " in run:
                continue
            checked += 1
            for line in run.splitlines():
                self.assertIn(line.strip(), script, f"{line.strip()!r} is not in {SCRIPT.name}")
        self.assertGreaterEqual(checked, 15)

    def test_the_script_stops_on_the_first_failure(self):
        self.assertIn("set -euo pipefail", SCRIPT.read_text())


if __name__ == "__main__":
    unittest.main()
