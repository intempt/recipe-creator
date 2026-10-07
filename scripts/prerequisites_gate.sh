#!/usr/bin/env bash
# Every runnable step of .github/workflows/recipe-prerequisites.yml, in its order.
#
# The write-back job (recipe-git-validate.yml, job 3) commits with GITHUB_TOKEN, and a
# GITHUB_TOKEN push starts no workflow — so `prerequisites` never runs on the bot's
# commit. Job 3 runs THIS on the tree it is about to commit, and only then reports
# `prerequisites` green on that commit. tests/test_prerequisites_gate.py fails when a
# step is added to the workflow and not here.
#
# Left out: the engine drift check (it needs ENGINE_READ_TOKEN, and the commit only adds
# recipes, never the entity list) and `pip install pyyaml` (the caller installs it).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/tests/test_check_recipe_prerequisites.py
python3 scripts/check_recipe_prerequisites.py
python3 scripts/build_artifacts.py --out /tmp/catalog --check
python3 scripts/tests/test_recipe_contract.py
for t in scripts/tests/test_*.py; do python3 "$t" || exit 1; done
python3 scripts/injection.py recipes examples
python3 scripts/portability.py recipes examples
python3 scripts/normalise_recipe.py --check recipes examples
python3 scripts/validate_recipes.py --lint
python3 scripts/validate_recipes.py --recipes examples --lint && python3 scripts/rebuild_bodies.py --recipes examples --check
python3 scripts/render_entities_doc.py --check
python3 scripts/check_recipe_identity.py
python3 scripts/check_recipe_consistency.py
python3 scripts/rebuild_bodies.py --check
python3 scripts/sync_plugin.py --check
python3 plugin/skills/intempt-recipe-creator/scripts/validate_recipes.py --lint --recipes plugin/skills/intempt-recipe-creator/references/examples
python3 plugin/skills/intempt-recipe-creator/scripts/injection.py plugin/skills/intempt-recipe-creator/references/examples && python3 plugin/skills/intempt-recipe-creator/scripts/portability.py plugin/skills/intempt-recipe-creator/references/examples
echo "prerequisites: every step passed"
