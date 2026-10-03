# Getting started with Intempt recipes

> This file is written to be handed to your coding agent. Point it here and ask it to create an
> Intempt recipe with you. Installing the plugin, signing in where a route needs it, and writing the
> file are all things the agent does by following the steps below.

A recipe is a markdown file that Blu, Intempt's agent, runs inside a customer's project with that
person's own access: build a segment, write an email, generate an image. Published recipes appear in
the Intempt Collective Marketplace on intempt.com and in the console, marked **Install now** or
**Coming soon**.

## Two prompts, not one

Install is a separate job from doing the work. Send these as two messages:

```
1.  Set up the Intempt recipe creator by following the steps in
    https://github.com/intempt/recipe-creator

2.  Create an Intempt recipe
```

**Do not put this repository's URL in the second prompt.** A URL is an instruction to fetch. Given
the link, an agent fetches these files and rebuilds the procedure from them instead of invoking the
installed `intempt-recipe-author` skill, which is slower and worse than the skill it already has.
Install first, then ask for the work.

**If you are the agent reading this because you were handed the URL:** check whether
`intempt-recipe-author` is available to you as a skill. If it is, invoke it and stop reading this
file. Only if it is genuinely unavailable do you continue here, and then read the other files **raw**:

```
curl -fsSL https://raw.githubusercontent.com/intempt/recipe-creator/main/<NAME>
```

Over HTTP a relative link resolves to nothing, so fetch each file by name when you need it.

## Install

| Host | Install |
|---|---|
| **Claude Code** | `/plugin marketplace add intempt/recipe-creator` then `/plugin install intempt-recipe-author@intempt-recipe-creator`, from inside Claude Code |
| **Codex** | `codex plugin marketplace add intempt/recipe-creator`, then open **Plugins** and install **intempt-recipe-author** |
| **Cursor** | Add `https://github.com/intempt/recipe-creator` as a plugin marketplace and install **intempt-recipe-author** |

If the skill will not load by name after installing, restart the host. Some hosts register a new
plugin only on start.

No install has been run end to end yet; that happens once the repository is public. The Claude Code
manifests pass `claude plugin validate`. The Codex and Cursor manifests follow the shapes other
published plugins use, and are untested. If one fails, the curl fallback above still works.

[PREREQUISITES.md](./PREREQUISITES.md) covers the Intempt CLI, signing in and updating the plugin.

## The order of work

### 1. The route comes first, and it is asked

> **Where are you starting from?**

| Answer | Route |
|---|---|
| **I have an idea** | [workflows/idea-to-recipe.md](./workflows/idea-to-recipe.md). No sign-in, no CLI |
| **From my Intempt workspace** | sign in, then [workflows/workspace-to-recipe.md](./workflows/workspace-to-recipe.md). Read only |
| **I have a recipe.md** | [workflows/existing-recipe.md](./workflows/existing-recipe.md). No sign-in |
| **Something else** | say what, and the agent picks the closest route and tells you which |

The route is never guessed from what the agent can see. Only you know where you are starting from.

### 2. Sign in only if the route needs it

The workspace route reads your project, so it needs `intempt login` and `intempt whoami`. The other
routes never touch your project and ask for nothing.

### 3. A full draft before any question

The agent writes the whole `recipe.md` first: every step, every value, the touches block, the inputs.
People correct a document far better than they answer questions about one.

### 4. At most three questions, one per message

A question is asked only when the answer changes what gets written: a threshold with no stated
reason, a value that only you know, an edge the draft cannot settle. Saying "draft it" ends the
questions and the rest are written as `does_not_claim` lines.

### 5. Validate

```
intempt recipe validate <file> --json
```

or, without the CLI, `python3 scripts/validate_recipes.py --lint <file>`. See
[VALIDATION.md](./VALIDATION.md).

### 6. One stop, with both ways to submit

One message: where the file is, that it validated, whether it is Install now or Coming soon, and
both ways to submit:

- the form at [intempt.com/recipes/submit](https://intempt.com/recipes/submit), or
- `intempt recipe submit <file>` from the session, which previews what would be sent and sends only
  after your explicit yes.

"Not now" is a complete answer. [SUBMITTING.md](./SUBMITTING.md) has the rest.

## Ways this goes wrong

- **Your agent names no files from this repository.** Ask which files it read. A confident plan with
  no filenames means it fell back to a generic workflow, and its recipe will look right and fail the
  contract. Stop it and fix access first.
- **The recipe states an insight you never said.** That is the failure, not a bonus. A generated
  insight reads better than a real one and is worth less, because somebody will act on it.
- **A clean validation gets read as a verdict.** Validation checks the file is well formed and that
  descriptions avoid the known vague shapes. It does not check that your events exist in anyone's
  project, that the thresholds are right, or that the recipe helps anyone.
