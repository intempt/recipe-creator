# JSON content

| `builds` | What it makes | Install now |
|---|---|---|
| `json` | a JSON content asset | yes |

## What the builder makes

A structured content asset saved in the installer's project as JSON. Pick it when the output is data
other content reads, not copy a person reads: copy belongs in `email_html`, `email_plain`, `sms`,
`push` or `slack`. The generic `content` entity is a different thing and is Coming soon; do not
use it for email ([email.md](email.md)).

## A good description names

- every key the JSON must have, by name;
- the type and the allowed values of each;
- how many items, when it is a list;
- where each value comes from: an earlier step by its title with `dependsOn`, or a value written out.

## Good and bad, from `recipes/intempt/`

No recipe in this repository builds `json` yet, so there is no real step to quote. Write to the list
above; a description that lists its keys is one the step check cannot read two ways.

## What belongs in `inputs`

- a schema or a key list the installer's own system expects;
- any identifier that only exists in their stack. `scripts/portability.py` blocks UUIDs, long
  numeric ids and opaque ids written into a recipe.

## Common lint failures

| Lint | Seen as | Fix |
|---|---|---|
| bracket placeholder | `{"name": "[Product]"}` | the value, or an `inputs` row |
| over 1200 chars | a whole payload pasted into the step | list the keys and rules instead |

The engine's import rules say never to write anything in curly braces (`md_import.py` RULES), and
the validator refuses `{{` outright. Describe the keys in words; do not paste a JSON object into the
step.
