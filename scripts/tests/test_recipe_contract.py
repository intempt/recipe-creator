#!/usr/bin/env python3
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from recipe_contract import availability, validate

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


if __name__ == "__main__":
    unittest.main(verbosity=1)
