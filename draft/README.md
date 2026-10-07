# draft/ — how a recipe gets into this repo

You write a recipe as prose in `draft/<any-name>.md` and open a pull request to `staging`.
You never write under `recipes/`: CI writes it from your draft. A pull request whose
commits change `recipes/` by hand fails the `recipe-label` check.

## The draft

```markdown
---
frontmatter_id: form-abandonment-nudge   # ONLY to edit an existing recipe — leave out for a new one
description: "One sentence on what it does." # optional; kept exactly as written
author:
  name: Beso            # required
  last_name: Gugushvili # required
  org_name: intempt     # the owner folder; left out = intempt
  email: beso@intempt.com  # optional, like company, byline, linkedin_url, avatar_url
---
# Form Abandonment Nudge

## Step 1: Create Form Abandoners Segment

Create a segment called "Form Abandoners" for users. …

## Step 2: …
```

One `## Step N: <title>` section per step, in plain prose. A step that uses an earlier
step's result names that step ("the segment created in Step 1").

## What happens to it

1. A reviewer adds the `validate-recipes` label. Until then `recipe-label` stays red.
2. **git-validate** reads the steps and checks each one (a step must use earlier
   outputs correctly and must not be vague). Failures are listed per step.
3. **git-validate-run** really runs the recipe in the CI project.
4. **git-validate-writeback** commits, as `github-actions[bot]`:
   - `recipes/<org_name>/<frontmatter_id>/recipe.md`: your prose under a front matter
     of `frontmatter_id`, `slash_command`, `description` and `author`
   - `recipes/<org_name>/<frontmatter_id>/recipe.json`: what the deploy sends
   - your draft, deleted

   and reports `recipe-label` and `prerequisites` green on that commit.

## The key

- **New recipe:** `frontmatter_id` is the slash command the model reads from your title,
  without the `/`. When any recipe in the repo (any owner) already uses it, CI adds
  `-2`, `-3`… and the slash command gets the same suffix.
- **Edit:** put the recipe's `frontmatter_id` in the draft. Key, folder and slash command
  stay; `org_name` must be the recipe's owner.
