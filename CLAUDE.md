# CLAUDE.md

Public, source-available recipes for the Intempt platform. Recipes are templates Blu
executes inside a customer's project using that person's own access.

## Writing or editing a recipe

Use the `write-recipe` skill in `.claude/skills/write-recipe/`. It owns the frontmatter
schema, the copy rules, the safety rules and the pull request flow. Do not restate them
here: one copy, in the skill.

## Before you push

```
python3 scripts/check_recipe_prerequisites.py    # declares every integration it names
python3 scripts/check_recipe_identity.py         # id unique, matches filename, slash unique
python3 scripts/build_artifacts.py --out /tmp/c --check   # customer-facing copy is clean
```

All three run in CI on pull requests to `staging` and `main`.

## Branches

`staging` is the default branch and where contributions land. `main` is fast-forward only
from `staging`; there are no pull requests to `main`. Merging to `staging` publishes the
catalog for internal testing, promotion to `main` publishes it to customers.

## Counts

Never write a recipe count into a document by hand. Three files once claimed 256, 292 and
302 for the same corpus. `README.md` generates its table, and anything else should read:

```
find recipes -name '*.md' | wc -l
```

## Scripts

| | |
|---|---|
| `build_artifacts.py` | builds the public catalog from the `.md` sources. The `--check` mode is the copy gate |
| `check_recipe_identity.py` | id and slash-command uniqueness, id matches filename |
| `check_recipe_prerequisites.py` | a recipe naming an integration must declare it |
| `convert_ts_to_md.py` | one-time migration from an older TypeScript format. Kept for provenance, not part of any flow |
