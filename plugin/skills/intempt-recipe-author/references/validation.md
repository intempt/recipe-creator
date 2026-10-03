# Validation

## Checking one recipe

With the Intempt CLI:

```
intempt recipe validate <recipe.md>          # says valid, and Install now or Coming soon
intempt recipe validate <recipe.md> --json   # {valid, problems, availability, waitingOn, header}
```

| exit | Meaning |
|---|---|
| **0** | valid |
| **1** | the recipe has contract problems, or the file could not be read. The output lists why |
| **2** | the command was wrong: a missing file argument or an unknown flag |

Without the CLI, from a clone of this repository or the plugin's bundled copy (Python 3 and PyYAML):

```
python3 scripts/validate_recipes.py --lint <recipe.md>
```

| exit | Meaning |
|---|---|
| **0** | no contract problems. Lints are printed but do not fail |
| **1** | contract problems, listed on stderr |
| **2** | the command was wrong |

Both check that the folder equals the `id` and the parent folder equals `owner`, so keep the file
at `<owner>/<id>/recipe.md`.

## Lints

`--lint` marks descriptions the engine is likely to find vague. Treat every lint on an Install now
recipe as a defect: it is the difference between a step that runs and a step that waits for
someone to clarify it.

| Lint | Why it matters |
|---|---|
| bracket placeholder | `[Product]` points at nothing; the step check asks a person to fill it |
| rationale, not instruction | the step check reads every sentence as something to do |
| names another vendor | the engine cannot act on another product's concepts |
| segment never says who it is about | users or accounts is the first thing a segment needs |
| over 1200 chars | usually two steps written as one |

## What validation does not tell you

It checks the file is well formed, that `touches` is declared, and that descriptions avoid the
known vague shapes. It does not check that the events and attributes exist in anyone's project, that
the thresholds are the right ones, or that the recipe helps anyone.

## The whole repository

CI runs all of these on every pull request to `staging` and `main`:

```
python3 scripts/validate_recipes.py --lint              # the v2 contract, availability, lints
python3 scripts/validate_recipes.py --recipes examples --lint
python3 scripts/check_recipe_prerequisites.py           # every integration you name is declared
python3 scripts/check_recipe_identity.py                # ids and slash commands are unique
python3 scripts/rebuild_bodies.py --check               # each body matches its frontmatter
python3 scripts/render_entities_doc.py --check          # references/entities.md is current
python3 scripts/sync_plugin.py --check                  # the plugin's copies match the root
python3 scripts/build_artifacts.py --out /tmp/c --check # the public catalog builds, copy is clean
python3 scripts/tests/test_recipe_contract.py           # the contract's own tests
python3 scripts/tests/test_check_recipe_prerequisites.py
```
