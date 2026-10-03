# What each builder makes, and what its step must name

**Read [../../DETERMINISM.md](../../DETERMINISM.md) first, then exactly one family below.** The
table in [../entities.md](../entities.md) says which `builds` values exist; these pages say how to
write a step for each so the engine's step check derives the same thing every time.

| The step builds | `builds` | Read |
|---|---|---|
| a group of users or accounts | `segment` | [segments.md](segments.md) |
| a new event or a new attribute | `event`, `attribute` | [events-and-attributes.md](events-and-attributes.md) |
| an email | `email_html`, `email_plain` | [email.md](email.md) |
| a text, a push notification or a Slack message | `sms`, `push`, `slack` | [messaging.md](messaging.md) |
| an image | `image` | [images.md](images.md) |
| a brand avatar, pose, scene or design system | `avatar`, `pose`, `scene`, `design_system` | [brand-assets.md](brand-assets.md) |
| a JSON content asset | `json` | [content.md](content.md) |
| anything else | the Coming soon list | [coming-soon.md](coming-soon.md), generated |

**Before you agree to build it:** [../../NO-ENTITY-EXISTS.md](../../NO-ENTITY-EXISTS.md), the jobs
the engine cannot build yet. Read it during the conversation, not here.

## What every family has in common

These hold for every builder and are not repeated on each page.

- **The description is the only instruction.** The step check reads it once and derives the command,
  the entity, the arguments and `modelConfig` (`llm-wrapper` `step_check.py`). The file never
  carries them; the validator refuses a step with `command`, `entity`, `kind` or `arguments`.
- **A value the description states becomes `modelConfig`.** A value it leaves out becomes an
  argument the installer has to fill before the step runs, or a builder default nobody chose.
  Writing it out is the difference.
- **A description that points at nothing that exists is marked vague** and waits for a person
  (R36). For a segment this is checked against the installer's project.
- **An earlier step is named by its title and listed in `dependsOn`.** The step check wires the
  dependency from the wording; it refuses one that is not above this step (`needs_earlier_step`)
  or that makes the wrong kind of thing (`wrong_earlier_step`).
- **One step builds one thing.** Two things in one description is two steps.

## What these pages are, and are not

They quote real steps from `recipes/intempt/`, labelled with the recipe id and whether that recipe
is Install now or Coming soon. Where no recipe in the repository builds an entity yet, the page says
so instead of inventing an example. Every engine behaviour stated here traces to
`scripts/recipe_contract.py`, [../recipe-contract.md](../recipe-contract.md) or the `llm-wrapper`
files that table cites. If the engine disagrees with a page, the engine wins and the page is wrong.
