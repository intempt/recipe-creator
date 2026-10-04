#!/usr/bin/env python3
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from recipe_contract import INTEMPT_CURATORS, availability, curator_for_group, render_body, validate

PATH = pathlib.Path("recipes/intempt/vip-users/recipe.md")


def recipe(**overrides):
    base = {
        "id": "vip-users",
        "title": "VIP users",
        "slash_command": "/vip-users",
        "group": "Segments",
        "owner": "intempt",
        "summary": "Users who spent over 500 in the last 90 days.",
        "steps": [
            {"id": "s1", "title": "Find VIP users", "summary": "Big spenders.", "builds": "segment",
             "description": "Build a segment of users whose total purchase amount in the last 90 days is over 500."},
            {"id": "s2", "title": "Write a thank-you email", "summary": "A thank-you note.", "builds": "email_html",
             "description": "Write a thank-you email to the users in Find VIP users.", "dependsOn": ["s1"]},
        ],
        "outputs": [{"key": "vips", "producedByStep": "s1", "type": "segment"}],
        "touches": {
            "reads": ["The order_completed event"],
            "writes": ["A new segment", "A new email"],
            "never": ["Nothing runs until you approve the plan in Blu."],
        },
    }
    base.update(overrides)
    return base


class Contract(unittest.TestCase):
    def test_a_well_formed_recipe_has_no_problems(self):
        self.assertEqual(validate(PATH, recipe()), [])

    def test_a_recipe_whose_steps_all_build_engine_entities_is_install_now(self):
        self.assertEqual(availability(recipe()), ("install_now", []))

    def test_a_recipe_with_one_unbuildable_step_is_coming_soon_and_names_the_builder(self):
        r = recipe()
        r["steps"][1]["builds"] = "journey"
        self.assertEqual(availability(r), ("coming_soon", ["journey"]))

    def test_curly_braces_in_a_description_are_refused(self):
        r = recipe()
        r["steps"][1]["description"] = "Email {{steps.s1.title}}."
        self.assertTrue(any("curly braces" in p for p in validate(PATH, r)))

    def test_depending_on_a_later_step_is_refused(self):
        r = recipe()
        r["steps"][0]["dependsOn"] = ["s2"]
        self.assertTrue(any("not an earlier step" in p for p in validate(PATH, r)))

    def test_engine_owned_fields_in_the_file_are_refused(self):
        r = recipe()
        r["steps"][0]["command"] = "create_segment"
        self.assertTrue(any("unknown field 'command'" in p for p in validate(PATH, r)))

    def test_step_ids_must_run_s1_s2_in_order(self):
        r = recipe()
        r["steps"][1]["id"] = "s5"
        self.assertTrue(any("id must be s2" in p for p in validate(PATH, r)))

    def test_the_folder_must_equal_the_id(self):
        self.assertTrue(any("folder" in p for p in validate(pathlib.Path("recipes/intempt/other/recipe.md"), recipe())))

    def test_the_owner_must_equal_the_partner_folder(self):
        self.assertTrue(any("partner folder" in p for p in validate(pathlib.Path("recipes/acme/vip-users/recipe.md"), recipe())))

    def test_an_output_must_name_a_step(self):
        r = recipe(outputs=[{"key": "vips", "producedByStep": "s9"}])
        self.assertTrue(any("producedByStep" in p for p in validate(PATH, r)))

    def test_an_unknown_entity_is_refused(self):
        r = recipe()
        r["steps"][0]["builds"] = "hologram"
        self.assertTrue(any("not a known entity" in p for p in validate(PATH, r)))

    def test_a_bad_slash_command_is_refused(self):
        self.assertTrue(any("slash_command" in p for p in validate(PATH, recipe(slash_command="VIP Users"))))

    def test_touches_is_required(self):
        r = recipe()
        del r["touches"]
        self.assertTrue(any("touches is required" in p for p in validate(PATH, r)))

    def test_touches_needs_reads_writes_and_never(self):
        r = recipe()
        del r["touches"]["never"]
        self.assertTrue(any("touches.never" in p for p in validate(PATH, r)))

    def test_touches_refuses_an_unknown_key(self):
        r = recipe()
        r["touches"]["deletes"] = ["everything"]
        self.assertTrue(any("unknown key 'deletes'" in p for p in validate(PATH, r)))

    def test_an_empty_touches_list_is_refused(self):
        r = recipe()
        r["touches"]["reads"] = []
        self.assertTrue(any("touches.reads must be a non-empty list" in p for p in validate(PATH, r)))

    def test_an_input_row_needs_all_three_fields(self):
        r = recipe(inputs=[{"input": "Spend threshold", "what_the_installer_supplies": "A number"}])
        self.assertTrue(any("if_missing is required" in p for p in validate(PATH, r)))

    def test_a_complete_input_row_and_claims_list_are_accepted(self):
        r = recipe(
            inputs=[{"input": "Spend threshold", "what_the_installer_supplies": "A number", "if_missing": "500 is used"}],
            does_not_claim=["The 500 threshold comes from the author, not from your data."],
        )
        self.assertEqual(validate(PATH, r), [])

    def test_an_em_dash_in_a_declaration_is_refused(self):
        r = recipe(does_not_claim=["It works \u2014 always."])
        self.assertTrue(any("em-dash" in p for p in validate(PATH, r)))

    def test_the_body_renders_touches_inputs_and_claims(self):
        r = recipe(
            inputs=[{"input": "Spend threshold", "what_the_installer_supplies": "A number", "if_missing": "500 is used"}],
            does_not_claim=["Nothing checks the threshold against your data."],
        )
        body = render_body(r)
        self.assertIn("## What this recipe touches", body)
        self.assertIn("- The order_completed event", body)
        self.assertIn("Never:", body)
        self.assertIn("| Spend threshold | A number | 500 is used |", body)
        self.assertIn("## What this recipe does not claim", body)
        self.assertLess(body.index("## What this recipe touches"), body.index("## Availability"))

    def test_the_body_leaves_out_sections_that_were_not_declared(self):
        body = render_body(recipe())
        self.assertNotIn("## Declared inputs", body)
        self.assertNotIn("## What this recipe does not claim", body)

    def test_a_known_intempt_curator_is_accepted(self):
        self.assertEqual(validate(PATH, recipe(curator="somya")), [])

    def test_a_curator_that_is_not_kebab_case_is_refused(self):
        self.assertTrue(any("curator" in p and "kebab-case" in p for p in validate(PATH, recipe(curator="Somya Nayak"))))

    def test_an_intempt_recipe_with_an_unknown_curator_is_refused(self):
        self.assertTrue(any("curator 'bob'" in p for p in validate(PATH, recipe(curator="bob"))))

    def test_a_partner_recipe_may_name_its_own_curator(self):
        path = pathlib.Path("recipes/acme/vip-users/recipe.md")
        self.assertEqual(validate(path, recipe(owner="acme", curator="jane-doe")), [])

    def test_curator_is_optional(self):
        self.assertEqual(validate(PATH, recipe()), [])

    def test_every_marketplace_group_has_exactly_one_intempt_curator(self):
        groups = [g for gs in INTEMPT_CURATORS.values() for g in gs]
        self.assertEqual(len(groups), len(set(groups)))
        self.assertEqual(curator_for_group("Segments"), "harish")
        self.assertEqual(curator_for_group("Creative"), "aurobind")
        self.assertEqual(curator_for_group("A group nobody curates"), "sid")


if __name__ == "__main__":
    unittest.main(verbosity=1)
