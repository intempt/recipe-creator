# Start here

This repository is the Intempt recipe creator kit. A recipe is a markdown file that Blu,
Intempt's agent, runs inside a customer's workspace: find a segment, write an email, score
accounts. Published recipes appear in the Intempt Collective Marketplace on intempt.com
and in the console, marked **Install now** or **Coming soon**.

| You want to | Read |
|---|---|
| Understand what a recipe file must contain | [references/recipe-contract.md](./references/recipe-contract.md) |
| See what a step can build today | [references/entities.md](./references/entities.md) |
| Start a new recipe from a blank file | [RECIPE-TEMPLATE.md](./RECIPE-TEMPLATE.md) |
| Know where your files go | [PACKAGE-LAYOUT.md](./PACKAGE-LAYOUT.md) |
| Check your recipe before you open a pull request | [VALIDATION.md](./VALIDATION.md) |
| Submit it, and how publishing and earnings work | [SUBMITTING.md](./SUBMITTING.md) |
| Copy a recipe that already meets the bar | [examples/](./examples/) |

Writing with Claude Code? The `write-recipe` skill in `.claude/skills/` walks the same
contract step by step.

## The one idea that matters

Each step's `description` is the instruction the engine runs. It is not marketing copy and
it is not a summary. Write it the way you would type it into the console's Add step panel:
one thing, who it is about, the exact event or attribute names, every value written out.
The `summary` fields are what customers read.
