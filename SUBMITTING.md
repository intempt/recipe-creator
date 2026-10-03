# Submitting a recipe

1. Fork the repository and branch from `staging`.
2. Add `recipes/<your-partner-folder>/<recipe-id>/recipe.md`. Start from
   [RECIPE-TEMPLATE.md](./RECIPE-TEMPLATE.md).
3. Run everything in [VALIDATION.md](./VALIDATION.md).
4. Open a pull request against `staging`, never `main`. Say what the recipe does for a
   customer, which integrations it needs, and which company you are submitting for.
5. A maintainer reviews it. Recipes run inside other people's workspaces, so review covers
   safety as well as quality.
6. Merged to `staging`, it reaches the internal catalog. Promotion to `main` publishes it
   to the Intempt Collective Marketplace.

## Earnings

Recipe creators in the Intempt Collective earn on published recipes that other teams run.
The track, the rate and how payouts work are on [intempt.com/partner](https://intempt.com/partner#build)
and in the Intempt Collective Terms.

## Safety review

- A step runs with the invoking person's own access. It can never escalate, but it can make
  their access do something they did not intend. Say exactly what each step changes.
- Do not put a URL in a description unless the recipe truly needs to reach that host.
- Declare every integration a recipe names under `prerequisites.integrations`.
