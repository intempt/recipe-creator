# Package layout

```
recipes/
  intempt/                  recipes the Intempt team publishes
    cart-recovery/
      recipe.md
  <partner>/                one folder per Intempt Collective partner
    <recipe-id>/
      recipe.md
      references/           optional supporting notes for reviewers, never published
examples/
  intempt/<recipe-id>/recipe.md   recipes that meet the bar, to copy from
references/                 the contract and the entity list
scripts/                    the validator, the catalog build and the guards CI runs
```

Rules the validator enforces:

- The folder name equals the recipe `id`.
- The partner folder equals the recipe `owner`.
- One `recipe.md` per folder. The body under the frontmatter is generated; edit the
  frontmatter and run `python3 scripts/rebuild_bodies.py`.

A partner folder name is your Intempt Collective handle in kebab-case. Ask in the pull
request if you do not have one yet.
