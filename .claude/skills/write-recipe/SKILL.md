---
name: write-recipe
description: Use when writing, editing, converting, or reviewing an Intempt recipe in this repository. Covers the recipe.md v2 contract the engine reads, how to write step descriptions the engine can run, Install now versus Coming soon, the validators, and the pull request flow.
---

# Writing an Intempt recipe

For creating a recipe to submit, use the `intempt-recipe-author` plugin skill in
`plugin/skills/`. This skill is for maintaining the recipes already in this repository.

A recipe is a template Blu runs inside a customer's workspace, using **their** access. Two
audiences read it, and they read different fields:

| Audience | Reads | Wants |
|---|---|---|
| A customer on the Marketplace | `title`, `summary`, step `title` and step `summary` | plain language, the concrete rule |
| The engine | step `description`, `dependsOn`, `builds` | one exact instruction per step |

The schema is [references/recipe-contract.md](../../../references/recipe-contract.md).
Read it first; this skill is the procedure, not a second copy of the schema.

## 1. Decide what the recipe builds

List the things it makes, one per step. Look each up in
[references/entities.md](../../../references/entities.md):

- every step on the Install now list: the recipe is runnable today;
- any step on the Coming soon list: it publishes as Coming soon until that builder ships.

Prefer splitting a big idea into an Install now recipe and a Coming soon one over a single
recipe that waits on four builders.

## 2. Create the folder

```
recipes/<partner>/<recipe-id>/recipe.md
```

Start from [RECIPE-TEMPLATE.md](../../../RECIPE-TEMPLATE.md). Check the id and slash command
are free:

```
ls recipes/*/ | grep -x <recipe-id>
grep -rh "^slash_command:" recipes/ | sort | uniq -d
```

## 3. Write each step's description

This is the field the engine runs, and the one the engine's step check judges. Write it as you
would type it into the console's Add step panel:

- one thing per step;
- who it is about: users or accounts;
- the exact event and attribute names as they exist in the project;
- every value written out: thresholds, windows, schedule, tone, length;
- an earlier step named by its title, and listed in `dependsOn`;
- no `{{...}}`, no `[Placeholder]`, no rationale, no other vendors' names.

Bad: `Generate per-tier email content. GREEN (expansion-leaning content ...). The account-as-unit aggregation is the differentiator.`
Good: `Write a designed email for the accounts in "Group paying accounts by tier" whose tier is green. Two sentences on what high-growth accounts do next and one button to book a call.`

## 4. Declare what it touches

Every recipe needs `touches` with `reads`, `writes` and `never`. Add `inputs` for anything the
installer supplies and `does_not_claim` for what nothing checked. See the contract.

## 5. Write the customer copy

- `title`: a real name, never the id.
- `summary`: what the customer gets, one sentence, under 200 characters. Never list the
  objects it builds.
- step `title`: the action, under 40 characters.
- step `summary`: the concrete rule in plain words.
- No em-dashes, en-dashes or arrow glyphs anywhere a customer reads.

## 6. Validate

```
python3 scripts/rebuild_bodies.py
python3 scripts/validate_recipes.py --lint recipes/<partner>/<recipe-id>/recipe.md
python3 scripts/check_recipe_prerequisites.py
python3 scripts/check_recipe_identity.py
python3 scripts/build_artifacts.py --out /tmp/c --check
```

Fix every contract problem. Treat every lint on an Install now recipe as a defect: it is
the difference between a step that runs and a step that asks the customer to clarify.

## 7. Open the pull request

Against **`staging`**, never `main`.

```
git checkout -b feature/<short-name>
git add recipes/<partner>/<recipe-id>/
git commit
gh pr create --base staging
```

Say what the recipe does for a customer, which integrations it needs, whether it is Install
now or Coming soon, and which company you are submitting for.

## Red flags in your own draft

| If you wrote | Reconsider |
|---|---|
| `command`, `entity`, `kind`, `prompt` or `bindsAs` | delete them; the engine derives them |
| a step that builds two things | split it |
| a description that could describe any recipe | put the real rule and values in it |
| `{{...}}` or `[Product]` | name the step by its title, write the value out |
| a summary listing objects built | say what the customer gets |
| an em-dash | colon, full stop, or comma |
| a URL in a description | does the recipe truly need to reach that host |
