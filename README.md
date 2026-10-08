# Intempt recipe creator

Write a recipe for the [Intempt](https://intempt.com) platform and submit it to the Intempt
Collective Marketplace.

A recipe is one markdown file, `recipe.md`. Its frontmatter lists steps; each step's `description`
is the instruction Blu, Intempt's agent, runs inside a customer's project with that person's own
access: build a segment, write an email, generate an image. A recipe that only works in your project
is not a recipe, it is a note to yourself, so everything the installer supplies is declared as an
input.

## Four ways in

| | Start from | Use when |
|---|---|---|
| **I have an idea** | a conversation | nothing is built yet |
| **From my Intempt workspace** | a segment or attribute you already built | it works in your project and you want others to install it. Read only |
| **I have a recipe.md** | a file you already have | it is written; you want it validated and submitted, or converted from the v1 format |
| **Something else** | tell the agent | it picks the closest route and says which |

All of them end the same way: a `recipe.md` you review, then you choose how it goes. Upload it at
[intempt.com/recipes/submit](https://intempt.com/recipes/submit), or have the agent send it with
`intempt recipe submit`, which previews first and cannot send without your explicit yes.

## Adding a recipe to this repository

You write one draft file. CI checks it, really runs it, and writes the published recipe for
you. Everything else is pull requests, two labels and one command run from `main`.

```
draft/<any-name>.md ──PR into staging──▶ label validate-recipes ──▶ CI checks, runs, writes
recipes/<owner>/<frontmatter_id>/ ──merge──▶ staging ──promotion PR + label ff-merge──▶ main
main ──gh workflow run recipe-deploy (create | update)──▶ the platform
main ──gh workflow run recipe-deploy (delete)──▶ archive PR into staging ──▶ main ──▶ removed from the platform
```

A published recipe is two files, and **CI writes both; you never do**:

```
recipes/<owner>/<frontmatter_id>/recipe.md     your prose, under a small front matter
recipes/<owner>/<frontmatter_id>/recipe.json   the checked recipe the deploy sends
```

A deleted recipe is not removed from the repo: it moves to `archived/<owner>/<frontmatter_id>/`
(see "Removing a recipe"). Nothing reads `archived/`; it is the record of what was deleted.

### The rules

1. **`draft/` holds new or edited recipes only:** one `draft/<any-name>.md` per recipe. Any
   other file in `draft/` fails the `recipe-label` check.
2. **Never commit under `recipes/` yourself.** A pull request with a commit by a person
   that touches `recipes/` fails `recipe-label`. Only `github-actions[bot]` may change it: the
   write-back commit, and the archive commit a **Delete** makes.
3. **Pull requests go to `staging`.** A draft is checked only when the `validate-recipes`
   label is on the pull request.
4. **`frontmatter_id` is unique across the whole repo,** for every owner. It is the recipe's key
   for create, update and delete.
5. **Create, update and delete run from `main` only.** Delete never touches the platform
   directly: it opens an archive pull request, and merging that to `main` removes the recipe.

### 1. Write the draft

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
- Leave `frontmatter_id` out for a new recipe. CI picks it (see "How the key is chosen" below).

You can run the same checks locally before you push: `scripts/prerequisites_gate.sh`.

### 2. Open the pull request and validate it

Open the pull request to `staging` with only that draft in it, and put the
**`validate-recipes`** label on it, either when you open it or later:

```bash
gh pr create -R intempt/recipe-creator --base staging --label validate-recipes --title "draft: <name>" --body "…"
gh pr edit <number> -R intempt/recipe-creator --add-label validate-recipes
```

Until the label is on, `recipe-label` stays red and says so. Then these jobs run:

| Job | What it does | When it fails |
|---|---|---|
| `git-validate` | Reads your steps and checks each one against the engine (no workspace) | A step is vague, or uses a later step's output. The errors are listed per step |
| `git-validate-run` | Really runs the recipe in the CI project (org 1000 / project 6298). The entities it creates stay there | A step does not validate when it runs |
| `git-validate-writeback` | Writes `recipe.md` + `recipe.json`, deletes your draft, runs every prerequisites check on the result, commits as `github-actions[bot]`, and reports `recipe-label` and `prerequisites` green on that commit | The two files would disagree, or a check fails. Nothing is committed |

When a job fails, fix the draft and push again. The jobs run again while the label stays on.
The bot's commit starts one more short round on its own; it finds no draft, so
`git-validate-run` and `git-validate-writeback` are skipped. That round is expected.

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

### 3. Merge into `staging`

When the write-back commit is green and the pull request is approved, merge it into `staging`.
Nothing reaches the platform yet.

### 4. Promote `staging` to `main`

Every push to `staging` opens (or updates) the promotion pull request "Merge Staging into
Main" (`staging` → `main`). Once it is approved on its current head commit, add the
**`ff-merge`** label:

```bash
gh pr edit <promotion-pr-number> -R intempt/recipe-creator --add-label ff-merge
```

A bot fast-forwards `main` to `staging` (no merge commit) and removes the label. If it refuses,
it comments why on the pull request; fix that and add the label again. Check it landed:

```bash
git fetch origin main && git log -1 --oneline origin/main
```

### 5. Create, update or delete it on the platform, from `main`

One command per action. It runs **only from `main`** (`--ref main`); started from any other
branch, including `staging`, it fails at once.

| Action | Command | Use when |
|---|---|---|
| **Create** | `gh workflow run recipe-deploy -R intempt/recipe-creator --ref main -f action=create -f frontmatter_id=<frontmatter_id> -f person_id=<person_id>` | The recipe is new on `main` |
| **Update** | `gh workflow run recipe-deploy -R intempt/recipe-creator --ref main -f action=update -f frontmatter_id=<frontmatter_id>` | An edited recipe reached `main` (see "Changing a recipe" below) |
| **Delete** | `gh workflow run recipe-deploy -R intempt/recipe-creator --ref main -f action=delete -f frontmatter_id=<frontmatter_id>` | The recipe should leave the platform. Opens an archive PR; the platform delete happens when it reaches `main` (see "Removing a recipe") |

Watch it: `gh run list -R intempt/recipe-creator --workflow recipe-deploy -L 1`.

- `<person_id>` is the Intempt user the recipe is created by.
- **Nothing new, nothing happens.** Each successful create or update moves the tag
  `deployed/<frontmatter_id>` to the deployed commit, and a successful platform delete removes
  it. So `create` and `update` do nothing (green, `UNCHANGED`) when the recipe's `recipe.json`
  has not changed since that tag.
- It fails when no `recipes/*/*/recipe.json` has that `frontmatter_id`, or when the platform
  already has that `frontmatter_id` on a `create` (409): use `update` instead.

The same three actions also run by pushing a tag on `main` (`delete/<frontmatter_id>` opens the
archive pull request, exactly like **Delete**). The workflow deletes the tag afterwards so the
name can be reused, and a tag push is never skipped:

```bash
git fetch origin main
git tag create/<person_id>/<frontmatter_id> origin/main && git push origin create/<person_id>/<frontmatter_id>
git tag update/<frontmatter_id> origin/main             && git push origin update/<frontmatter_id>
git tag delete/<frontmatter_id> origin/main             && git push origin delete/<frontmatter_id>
```

### Changing a recipe

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

2. Take it through steps 2 to 4. The key, the folder and the slash command stay the same; the
   prose, the description and the steps are replaced. A draft whose `frontmatter_id` names no
   recipe, a recipe of another owner, or one of the original hand-written recipes (front matter
   `id:`) is refused.
3. Run **Update** from step 5.

### Removing a recipe

Deleting is two steps, so the repo and the platform never disagree:

1. Run **Delete** from step 5. It does not touch the platform. It moves
   `recipes/<owner>/<slug>/` to `archived/<owner>/<slug>/` on a branch
   `archive/<frontmatter_id>` (a `github-actions[bot]` commit, so `recipe-label` accepts it) and
   opens a pull request into `staging`. `main` and `staging` are protected, so the move needs
   that pull request.
2. Approve and merge it. When it reaches `main`, `recipe-archive-delete` deletes every recipe
   the push moved into `archived/` from the platform and removes its `deployed/<frontmatter_id>`
   tag. A recipe with no such tag was never deployed and is only archived (`NOT DEPLOYED`).

`archived/` keeps every deleted recipe. Nothing reads it: create and update look in `recipes/`
only.

### Labels

Two pull-request labels start automation in this repo. No other label does: `bug`,
`documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`,
`question` and `wontfix` are GitHub's defaults and nothing reads them.

**`recipe-label` is not a label.** It is the name of a check (a job in
`.github/workflows/recipe-git-validate.yml`) that runs on every pull request to `staging`,
with or without labels. You cannot add it; it tells you whether `validate-recipes` is needed.

| Label | Added by | Starts | What it changes |
|---|---|---|---|
| `validate-recipes` | A reviewer or the author, on a pull request into `staging` | `.github/workflows/recipe-git-validate.yml` (`pull_request`, on `opened` with the label or `labeled`): `git-validate` → `git-validate-run` → `git-validate-writeback` | Creates entities in the CI project (org 1000 / project 6298) by really running the recipe, then pushes a `github-actions[bot]` commit to the PR branch that writes `recipes/<owner>/<frontmatter_id>/recipe.md` + `recipe.json` and deletes the draft |
| `ff-merge` | A person with write access, on the promotion pull request (`staging` → `main`, "Merge Staging into Main") | `.github/workflows/ff-merge.yml` (`pull_request_target`, on `labeled`), which calls `intempt/.github/.github/workflows/ff-merge.yml@main` | Fast-forwards `main` to the pull request's `staging` head, pushed by the ff-merge bot app. No merge commit |

**The archive pull request needs no label.** A **Delete** (`recipe-deploy`) opens it as
`github-actions[bot]`: `archive: <frontmatter_id>`, branch `archive/<frontmatter_id>` into
`staging`, moving `recipes/<owner>/<slug>/` to `archived/<owner>/<slug>/`. It is opened with the
workflow token, so no check starts on it. When it reaches `main`,
`.github/workflows/recipe-archive-delete.yml` (`push` to `main`, paths `archived/**`) deletes
the recipe from the platform and removes `deployed/<frontmatter_id>`.

**`validate-recipes`, in more detail.**
- Only pull requests into `staging` run it; the workflow has no other branch.
- While it stays on, every push reruns the three jobs.
- Removing it stops the git Validate jobs on later pushes. `recipe-label` reruns, and stays
  red while a draft is still in the tree. Once the write-back has landed, removing it changes
  nothing.
- Adding or removing *another* label while `validate-recipes` is on reruns `git-validate`
  (the job ignores a `labeled` event for a different label, but not an `unlabeled` one).
- A pull request from a fork gets no write-back: `git-validate-writeback` skips it with a notice.

**`ff-merge`, in more detail.**
- The promotion pull request is opened by `.github/workflows/autopr.yaml` (as
  `github-actions`) on every push to `staging`.
- The bot refuses unless: the pull request is open, its head is this repo's `staging` (not a
  fork), its base is `main`, the person who added the label has write or admin access, and
  there is an approval on the current head commit with no outstanding "changes requested".
  It also refuses when `main` has commits `staging` lacks.
- Whatever the result, the bot removes the label afterwards. On a refusal it comments the
  reason on the pull request. To try again, add the label again.
- Removing the label yourself does nothing; only `labeled` is handled.

### Not covered here

The original hand-written recipes (front matter `id:`, no `recipe.json`) follow
[references/recipe-contract.md](./references/recipe-contract.md) and the checks in
`recipe-prerequisites.yml`. The `recipe-label` rule (no person's commit under `recipes/`)
applies to them as well.

## Start here

**[START-HERE.md](./START-HERE.md)**: install, then create the recipe. If you are pasting a link to
someone, paste that one.

The rest is reference, in the order you will want it:

1. [PREREQUISITES.md](./PREREQUISITES.md): the Intempt CLI, signing in, the plugin.
2. Your route: [workflows/idea-to-recipe.md](./workflows/idea-to-recipe.md),
   [workflows/workspace-to-recipe.md](./workflows/workspace-to-recipe.md) or
   [workflows/existing-recipe.md](./workflows/existing-recipe.md).
3. [WRITING-STEPS.md](./WRITING-STEPS.md): read this before writing any step. The test, the vague
   rule, and before and after examples from this repository. [DETERMINISM.md](./DETERMINISM.md) is
   the reasoning behind it: what the engine derives from a step, and the seven rules that pin it.
4. [NO-ENTITY-EXISTS.md](./NO-ENTITY-EXISTS.md): read this while you are still talking. The jobs the
   engine cannot build yet, and how they become Coming soon instead of being faked.
5. [references/recipe-contract.md](./references/recipe-contract.md): what the file must contain.
6. [references/entities.md](./references/entities.md): what a step can build, generated from the recipes,
   and [references/entities/](./references/entities/README.md): one page per builder, with good and bad
   steps.
7. [RECIPE-TEMPLATE.md](./RECIPE-TEMPLATE.md) and [PACKAGE-LAYOUT.md](./PACKAGE-LAYOUT.md).
8. [VALIDATION.md](./VALIDATION.md), then [SUBMITTING.md](./SUBMITTING.md).

**This repository is an installable plugin.** In Claude Code:

```
/plugin marketplace add intempt/recipe-creator
/plugin install intempt-recipe-creator@intempt-recipe-creator
```

The skill lives at [plugin/skills/intempt-recipe-creator/](./plugin/skills/intempt-recipe-creator/):
the whole flow, its own validator and the worked example, so it runs with no network.

## Install now and Coming soon

Every step declares what it `builds`. A recipe whose steps all build something the engine supports
today is **Install now**; the rest are **Coming soon**, and the catalog says which builder each is
waiting on. The counts are in [references/entities.md](./references/entities.md), generated from
the recipes.

## Where finished recipes live

- **[examples/](./examples/README.md)** is a curated set to copy from, chosen because it meets the
  bar. Its README says what each one teaches.
- **`recipes/<owner>/<id>/`** holds published recipes. `recipes/intempt/` holds the recipes the
  Intempt team publishes. New ones arrive through `draft/` and are written by CI, never by hand
  ([Adding a recipe](#adding-a-recipe-to-this-repository)); the original hand-written ones follow
  [references/recipe-contract.md](./references/recipe-contract.md).
- **`draft/`** holds drafts waiting in an open pull request, and nothing else. It is empty on
  `staging` and `main`.

When a customer installs a recipe, Intempt makes a copy in their project. That copy is theirs to
edit and never changes underneath them.

## If your agent cannot read this repository

Some sandboxes cannot fetch a GitHub page. Tell the agent to fetch the raw file instead:

```
curl -fsSL https://raw.githubusercontent.com/intempt/recipe-creator/main/START-HERE.md
```

If that also returns nothing, the sandbox has no network at all. Install the plugin instead: it
carries this procedure, the validator and the example, and loads from disk.

**The tell that your agent gave up and improvised:** it names no files from this repository. Ask
which files it read.

## Three things that will save you a rejected submission

**Your project's names do not travel.** A journey id, a form, a list, a value only your project
holds: each becomes an `inputs` row the installer supplies, with what happens when it is missing.

**Every step says who, what and when.** Users or accounts, the exact event or attribute, every
threshold and window written out. A step the engine finds vague does not run; it waits for someone
to clarify it. [WRITING-STEPS.md](./WRITING-STEPS.md) is the bar.

**Say what you did not check.** If a threshold is your judgment rather than something measured, put
it under `does_not_claim`. A recipe that declares nothing cannot be trusted or corrected.

## Licence

MIT. See [LICENSE](./LICENSE). You keep the copyright in a recipe you submit; accepted recipes are
published under MIT with your attribution preserved.
