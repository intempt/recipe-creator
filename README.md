# Intempt Recipes

The recipe creator kit for the [Intempt](https://intempt.com) platform, and the source of
every recipe in the Intempt Collective Marketplace. A recipe is a markdown file that Blu,
Intempt's agent, runs inside a customer's workspace using that person's own access.

**New here? Read [START-HERE.md](./START-HERE.md).**

```
recipes/<partner>/<recipe-id>/recipe.md   one folder per Intempt Collective partner
examples/                                 recipes that meet the bar, to copy from
references/recipe-contract.md             what a recipe file must contain, and why
references/entities.md                    what a step can build today, and what is coming
scripts/                                  the validator, the catalog build and the CI guards
```

## Install now and Coming soon

Every step declares what it `builds`. A recipe whose steps all build something the engine
supports today is **Install now**; the rest are **Coming soon**, and the catalog says which
engine builder each one is waiting on. Counts live in
[references/entities.md](./references/entities.md), generated from the recipes.

## How a recipe reaches customers

1. A pull request against `staging` adds or edits `recipes/<partner>/<id>/recipe.md`.
2. CI validates it against the contract the engine reads (`scripts/validate_recipes.py`).
3. Merged to `staging`, the catalog is published for internal testing.
4. Promotion to `main` publishes it to customers on intempt.com and in the console.

When a customer installs a recipe, Intempt makes a copy in their workspace. That copy is
theirs to edit and never changes underneath them.

## Licence

Source-available, not open source. You may read these, run them on Intempt, and
contribute. You may not redistribute them or use them to build a competing
product. See [LICENSE](./LICENSE).

Contributing grants Intempt a licence to publish your contribution. Partner
revenue share, where it applies, is a separate written agreement.
