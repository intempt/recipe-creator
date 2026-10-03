# Package layout

A recipe is one file:

```
<owner>/<recipe-id>/recipe.md
```

Write it there in your own working directory. The validator checks that the folder name equals the
recipe `id` and that the parent folder equals `owner`, your Intempt Collective handle in kebab-case.

The body under the frontmatter is generated from it. Edit the frontmatter only.

## This repository

```
recipes/<author>/<recipe-id>/recipe.md   published recipes, written only when a submission is approved
examples/intempt/<recipe-id>/recipe.md    recipes chosen to copy from
references/                               the contract and the entity list
workflows/                                the three routes in
plugin/                                   the intempt-recipe-author plugin
scripts/                                  the validator, the catalog build and the guards CI runs
```
