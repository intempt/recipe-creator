# Package layout

A recipe is one file:

```
<owner>/<recipe-id>/recipe.md
```

Write it there in your own working directory. The validator checks that the folder name equals the
recipe `id` and that the parent folder equals `owner`, your Intempt Collective handle in kebab-case.

The body under the frontmatter is generated from it. Edit the frontmatter only.

## What a submission sends

The website form and `intempt recipe submit` take the raw `recipe.md`, at most 250 KB. To see
exactly what would be sent, and check it the way review will:

```
python3 scripts/package_recipe.py <owner>/<id>/recipe.md --out <dir>
```

It runs the contract, the injection scan and the portability scan, and writes nothing unless all
three pass. Then `<dir>` holds the `recipe.md`, byte for byte, and a `manifest.json` with its `id`,
`owner`, `curator`, `version`, `sha256`, `bytes`, `availability` and `waitingOn`, plus the versions
of the two scans that cleared it. The manifest has no timestamp, so the same file always produces
the same manifest.

## This repository

```
recipes/<author>/<recipe-id>/recipe.md   published recipes, written only when a submission is approved
examples/intempt/<recipe-id>/recipe.md    recipes chosen to copy from; examples/README.md says what each teaches
DETERMINISM.md                            what the engine derives from a step, and the rules that pin it
references/                               the contract and the entity list
references/entities/                      one page per builder family, with good and bad steps
workflows/                                the three routes in
plugin/                                   the intempt-recipe-creator plugin
scripts/                                  the validator, the scans, the catalog build and the guards CI runs
scripts/fixtures/                         the injection patterns, pinned by SUITE_SHA256
NOTICE, LICENSE                           what licence covers what
```
