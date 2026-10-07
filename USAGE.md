# USAGE: create, validate, deploy, update and delete a recipe

This page covers recipes made through `draft/`. A recipe made this way is two files:

```
recipes/<owner>/<frontmatter_id>/recipe.md     your prose, under a small front matter
recipes/<owner>/<frontmatter_id>/recipe.json   the checked recipe the deploy sends
```

**CI writes both of them, and you never write them.** You write a draft, CI checks it,
really runs it, and commits the two files for you.

## The rules

1. **`draft/` holds new or edited recipes only:** one `draft/<any-name>.md` per recipe. Any
   other file in `draft/` fails the `recipe-label` check.
2. **Never commit under `recipes/` yourself.** A pull request with a commit by a person
   that touches `recipes/` fails `recipe-label`. Only the write-back commit
   (`github-actions[bot]`) may change it.
3. **Pull requests go to `staging`.** A draft is checked only when a reviewer adds the
   `validate-recipes` label.
4. **`frontmatter_id` is unique across the whole repo,** for every owner. It is the recipe's key
   for deploy, update and delete.
5. **Deploys happen from `main` only,** by pushing a tag (see Deploy below).

## 1. A new recipe

Create `draft/<any-name>.md`. The file name does not matter, because CI chooses the key.

```markdown
---
description: "One sentence on what it does."   # optional; kept exactly as written
author:
  name: Beso                 # required
  last_name: Gugushvili      # required
  org_name: intempt          # the owner folder; leave out = intempt
  email: beso@intempt.com    # optional, like company, byline, linkedin_url, avatar_url
---
# Form Abandonment Nudge

## Step 1: Create Form Abandoners Segment

Create a segment called "Form Abandoners" for users. Base it on the "Change on" event …

## Step 2: Generate Nudge Banner Image

Generate a friendly, low-pressure "still there?" banner image …

## Step 3: Generate Nudge Email

Write a short, friendly nudge email for the "Form Abandoners" segment created in Step 1,
using the banner image generated in Step 2 …
```

- One `# Title`, then one `## Step N: <title>` per step, in plain prose.
- A step that uses an earlier step's result names that step: "the segment created in
  Step 1". A step may use only earlier steps.
- Write every value out: names, events, windows, tone. A vague step fails the check.
  [WRITING-STEPS.md](./WRITING-STEPS.md) has the long version.
- `org_name` is a folder name: lowercase letters, digits and single hyphens.
- Leave `frontmatter_id` out. CI picks it (see "How the key is chosen" below).

Open the pull request to `staging` with only that draft in it.

## 2. Validate

A reviewer adds the label **`validate-recipes`**. Until then `recipe-label` stays red and says so.
After that, these jobs run on every push to the pull request:

| Job | What it does | When it fails |
|---|---|---|
| `git-validate` | Reads your steps and checks each one against the engine (no workspace) | A step is vague, or uses a later step's output. The errors are listed per step |
| `git-validate-run` | Really runs the recipe in the CI project (org 1000 / project 6298). The entities it creates stay there | A step does not validate when it runs |
| `git-validate-writeback` | Writes `recipe.md` + `recipe.json`, deletes your draft, runs every prerequisites check on the result, commits as `github-actions[bot]`, and reports `recipe-label` and `prerequisites` green on that commit | The two files would disagree, or a check fails. Nothing is committed |

When a job fails, fix the draft and push again. The jobs run again while the label stays on.

**How the key is chosen.**
- **Owner:** `author.org_name`, else `intempt`.
- **`frontmatter_id`:** the slash command the engine reads from your title, without the `/`.
  If any recipe in the repo, of any owner, already uses it, CI adds `-2`, `-3`… and the
  slash command gets the same suffix.
- **`description`:** yours if you wrote one, otherwise generated.

What lands, in place of your draft:

```markdown
---
frontmatter_id: form-abandonment-nudge
slash_command: /form-abandonment-nudge
description: Nudges people who left a form unfinished.
author:
  name: Beso
  last_name: Gugushvili
  org_name: intempt
---

# Form Abandonment Nudge
…your prose, unchanged…
```

You can run the same checks locally before you push: `scripts/prerequisites_gate.sh`.

## 3. Merge

When the write-back commit is green, merge the pull request into `staging`. `staging`
reaches `main` by the usual promotion. A recipe can be deployed only after it is on `main`.

## 4. Deploy

Push a tag on a commit that is on `main`. The `recipe-deploy` workflow sends the matching
`recipe.json` to the platform, then deletes the tag so the same name can be pushed again.

```bash
git fetch origin main
git tag create/<person_id>/<frontmatter_id> origin/main
git push origin create/<person_id>/<frontmatter_id>
```

Or, with no tag, run the deploy by hand. It runs **only from `main`** (`--ref main`); started
from any other branch, including `staging`, it fails at once:

```bash
gh workflow run recipe-deploy -R intempt/recipe-creator --ref main -f action=create -f frontmatter_id=<frontmatter_id> -f person_id=<person_id>
gh workflow run recipe-deploy -R intempt/recipe-creator --ref main -f action=update -f frontmatter_id=<frontmatter_id>
gh run list -R intempt/recipe-creator --workflow recipe-deploy -L 1   # watch it
```

A manual run with nothing new on `main` for that recipe does nothing and ends green. Each
successful deploy (tag or manual) moves the tag `deployed/<frontmatter_id>` to the deployed
commit, and a delete removes it. So `create` and `update` skip when the recipe's
`recipe.json` is unchanged since that tag, and `delete` skips when there is no such tag. Tag
pushes are never skipped.

`<person_id>` is the Intempt user the recipe is created by. The deploy fails when:
- the commit is not on `main`
- no `recipes/*/*/recipe.json` has that `frontmatter_id`
- the platform already has that `frontmatter_id` (409): use `update/` instead

## 5. Update

1. Write a draft that names the recipe you are changing:

   ```markdown
   ---
   frontmatter_id: form-abandonment-nudge   # the existing key
   author:
     name: Beso
     last_name: Gugushvili
     org_name: intempt                      # must be the recipe's current owner
   ---
   # Form Abandonment Nudge
   …the whole recipe, as it should now read…
   ```

2. Validate and merge it as in steps 2 and 3. The key, the folder and the slash command
   stay the same; the prose, the description and the steps are replaced. A draft whose
   `frontmatter_id` names no recipe, a recipe of another owner, or one of the original
   hand-written recipes (front matter `id:`) is refused.
3. Once it is on `main`, deploy the change:

   ```bash
   git tag update/<frontmatter_id> origin/main && git push origin update/<frontmatter_id>
   ```

## 6. Delete

Remove the recipe from the platform:

```bash
git tag delete/<frontmatter_id> origin/main && git push origin delete/<frontmatter_id>
```

This needs no file, so it works even after the folder is gone. **Removing the folder from
the repo cannot go through a pull request today,** because a person's commit under `recipes/`
fails `recipe-label`. Ask a maintainer until a delete path is decided.

## What this page does not cover

The original hand-written recipes (front matter `id:`, no `recipe.json`) follow
[references/recipe-contract.md](./references/recipe-contract.md) and the checks in
`recipe-prerequisites.yml`. The `recipe-label` rule (no person's commit under `recipes/`)
applies to them as well.
