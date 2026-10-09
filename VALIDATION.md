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

## Injection and portability

`validate_recipes.py` runs two scans on every file and reports what they find as contract problems.
Both also run on their own:

```
python3 scripts/injection.py <recipe.md or folder>     # text aimed at the agent, the engine or a reviewer
python3 scripts/portability.py <recipe.md or folder>   # values that only exist in your workspace
```

| exit | Meaning |
|---|---|
| **0** | nothing found |
| **1** | findings, each with where it is (`steps.s2.description`), the line, the text and the fix |
| **2** | the command was wrong, no recipe.md was found, or (injection only) the pattern file failed its pin |

**Injection** blocks: an instruction to ignore earlier instructions, a new role for the agent, a
system-prompt or chat-template marker, text addressed to a reviewer or a scanner, an instruction to
run without approval or to keep something from the installer, a request for a credential, an
invisible or direction-changing character, a long encoded blob, an HTML comment in the body other
than the generated marker, an HTML comment in a step that carries an instruction, and a link in a
description to a host outside intempt.com. The patterns live in `scripts/fixtures/injection_patterns.json`
as data. `scripts/fixtures/SUITE_SHA256` pins that file, and the scan refuses to run when the two
disagree, so a change to the rules is always a reviewed change to both.

**Portability** blocks: a UUID, a numeric id of 9 digits or more, an opaque id (a cuid, a 24-character
hex id, a prefixed id with a digit in it), an email address outside the reserved example domains (`example.com`, `.org`, `.net`), a link into
`app.intempt.com` or any URL with an org, project or workspace in its path, and a segment, journey,
form or list id written as a value (`segment id 4821`). Naming a property such as `journey_id` is
fine; giving it a value is not. The fix is always an `inputs` row: what the installer supplies, what
happens without it, and the step saying "the journey chosen for this run".

## Normalising

```
python3 scripts/normalise_recipe.py <recipe.md or folder>          # rewrite in place
python3 scripts/normalise_recipe.py --check <recipe.md or folder>  # exit 1 if any file would change
```

LF line endings, no trailing whitespace, top-level and step keys in the order
[RECIPE-TEMPLATE.md](./RECIPE-TEMPLATE.md) and [references/recipe-contract.md](./references/recipe-contract.md)
use, and the body regenerated from the frontmatter. It never changes a frontmatter value; if
reordering would, it refuses and names the file.

## Packaging

`python3 scripts/package_recipe.py <recipe.md> --out <dir>` runs the contract and both scans, and
writes the submission bundle only when all of them pass. [PACKAGE-LAYOUT.md](./PACKAGE-LAYOUT.md)
says what is in it.

## What validation does not tell you

It checks the file is well formed, that `touches` is declared, and that descriptions avoid the
known vague shapes. It does not check that the events and attributes exist in anyone's project, that
the thresholds are the right ones, or that the recipe helps anyone.

## The whole repository

CI runs all of these on every pull request to `staging` and `main`:

```
python3 scripts/validate_recipes.py --lint              # the v2 contract, availability, lints, both scans
python3 scripts/validate_recipes.py --recipes examples --lint
python3 scripts/injection.py recipes examples          # prompt injection
python3 scripts/portability.py recipes examples        # workspace-only values
python3 scripts/normalise_recipe.py --check recipes examples
python3 scripts/check_recipe_identity.py                # ids and slash commands are unique
python3 scripts/rebuild_bodies.py --check               # each body matches its frontmatter
python3 scripts/render_entities_doc.py --check          # references/entities.md is current
python3 scripts/sync_plugin.py --check                  # the plugin's copies match the root
python3 scripts/build_artifacts.py --out /tmp/c --check # the public catalog builds, copy is clean
python3 scripts/tests/test_recipe_contract.py           # the contract's own tests
for t in scripts/tests/test_*.py; do python3 "$t" || exit 1; done   # every script's tests
```
