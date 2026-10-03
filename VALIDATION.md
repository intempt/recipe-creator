# Validation

Run these before you push. CI runs the same ones on every pull request.

```
python3 scripts/validate_recipes.py --lint              # the v2 contract, availability, quality lints
python3 scripts/validate_recipes.py --lint recipes/<partner>/<id>/recipe.md   # one recipe, lints listed
python3 scripts/check_recipe_prerequisites.py           # every integration you name is declared
python3 scripts/check_recipe_identity.py                # ids and slash commands are unique
python3 scripts/rebuild_bodies.py --check               # the body matches the frontmatter
python3 scripts/render_entities_doc.py --check          # references/entities.md is current
python3 scripts/build_artifacts.py --out /tmp/c --check # the public catalog builds, copy is clean
python3 scripts/tests/test_recipe_contract.py           # the contract's own tests
```

`validate_recipes.py` fails on a contract problem. Its `--lint` warnings do not fail the
build; they mark descriptions the engine is likely to find vague:

| Lint | Why it matters |
|---|---|
| bracket placeholder | `[Product]` points at nothing; the step check asks a person to fill it |
| rationale, not instruction | the step check reads every sentence as something to do |
| names another vendor | the engine cannot act on another product's concepts |
| segment never says who it is about | users or accounts is the first thing a segment needs |
| over 1200 chars | usually two steps written as one |
