#!/usr/bin/env python3
import pathlib
import subprocess
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from support import SCRIPTS, cleanup, example_text, write_recipe

import portability

STEP_ONE = "      Build a segment of users named \"Trials ending this week\".\n"


def with_step_one_line(extra):
    return example_text().replace(STEP_ONE, STEP_ONE + "      " + extra + "\n", 1)


def kinds(findings):
    return {f["kind"] for f in findings}


class Portability(unittest.TestCase):
    def scan(self, text):
        path = write_recipe(text)
        try:
            return portability.scan_file(path)
        finally:
            cleanup(path)

    def test_the_worked_example_has_no_findings(self):
        self.assertEqual(self.scan(example_text()), [])

    def test_a_uuid_is_flagged_and_the_fix_is_an_inputs_row(self):
        found = self.scan(with_step_one_line("Only users in segment 3f2b8c1e-9a4d-4e2b-8f1a-6c7d5e4b3a21."))
        self.assertIn("uuid", kinds(found))
        hit = next(f for f in found if f["kind"] == "uuid")
        self.assertEqual(hit["where"], "steps.s1.description")
        self.assertIn("inputs", hit["fix"])

    def test_a_long_numeric_id_is_flagged(self):
        self.assertIn("numeric_id", kinds(self.scan(with_step_one_line("Use list 4815162342 for the audience."))))

    def test_a_threshold_is_not_an_id(self):
        self.assertEqual(self.scan(with_step_one_line("Only users whose lifetime_value attribute is 1000000 or more.")), [])

    def test_a_cuid_is_flagged(self):
        self.assertIn("opaque_id", kinds(self.scan(with_step_one_line("Use cjld2cjxh0000qzrmn831i7rn as the source."))))

    def test_a_24_character_hex_object_id_is_flagged(self):
        self.assertIn("opaque_id", kinds(self.scan(with_step_one_line("Use 507f1f77bcf86cd799439011 as the source."))))

    def test_a_real_email_address_is_flagged(self):
        self.assertIn("email", kinds(self.scan(with_step_one_line("Send the list to jane@acme-corp.com."))))

    def test_an_example_domain_email_is_allowed(self):
        self.assertEqual(self.scan(with_step_one_line("The placeholder reads you@example.com.")), [])

    def test_an_app_intempt_link_is_flagged(self):
        self.assertIn("workspace_link", kinds(self.scan(with_step_one_line("Copy https://app.intempt.com/segments/81234 as the base."))))

    def test_an_org_or_project_name_in_a_url_is_flagged(self):
        self.assertIn("workspace_link", kinds(self.scan(with_step_one_line("Read https://api.intempt.com/v1/acme-prod/projects/web-main/events."))))

    def test_a_hardcoded_segment_or_journey_id_is_flagged(self):
        self.assertIn("entity_id", kinds(self.scan(with_step_one_line("Exclude segment id 4821."))))
        self.assertIn("entity_id", kinds(self.scan(with_step_one_line("Only where journey_id = jrn_77a."))))

    def test_naming_an_id_property_without_a_value_is_allowed(self):
        line = "Only users who did goal_completed_in_journey with a journey_id equal to the activation journey chosen for this run."
        self.assertEqual(self.scan(with_step_one_line(line)), [])

    def test_the_cli_exits_1_on_a_finding_and_0_when_clean(self):
        bad = write_recipe(with_step_one_line("Exclude segment id 4821."))
        good = write_recipe(example_text())
        try:
            run_bad = subprocess.run([sys.executable, str(SCRIPTS / "portability.py"), str(bad)], capture_output=True, text=True)
            run_good = subprocess.run([sys.executable, str(SCRIPTS / "portability.py"), str(good)], capture_output=True, text=True)
            self.assertEqual(run_bad.returncode, 1, run_bad.stdout + run_bad.stderr)
            self.assertIn("inputs", run_bad.stdout)
            self.assertEqual(run_good.returncode, 0, run_good.stdout + run_good.stderr)
        finally:
            cleanup(bad)
            cleanup(good)


if __name__ == "__main__":
    unittest.main(verbosity=1)
