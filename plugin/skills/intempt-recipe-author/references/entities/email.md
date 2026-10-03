# Email

| `builds` | What it makes | Install now |
|---|---|---|
| `email_html` | a designed marketing email (HTML) | yes |
| `email_plain` | a plain-text email | yes |

## What the builders make

An email saved as content in the installer's project. **Building an email is not sending it**
([../../NO-ENTITY-EXISTS.md](../no-entity-exists.md)): sending to a segment is a journey, which is
Coming soon. A recipe produces the email and the segment, and a person sends. Say so under
`touches.never`.

Pick the entity the step really builds. The step check's own rule is that an email step builds an
email type, never the generic `content` (`step_check.py` instructions).

## A good description names

- who it is for, by the earlier step's title: "the users in 'Find trials ending this week'", with
  that step in `dependsOn`;
- the subject line rule: its length and what it must say;
- the length of the body, in sentences;
- what each sentence or block says;
- the call to action: the button label, and what it links to;
- the tone, and what is ruled out ("No discount").

## Good

No recipe in `recipes/intempt/` is Install now with an email step yet; they all wait on a journey.
The kit's own example builds one, [../../examples/intempt/trial-expiring-nudge/recipe.md](../examples/intempt/trial-expiring-nudge/recipe.md)
step 2:

```
Write a designed email for the users in "Find trials ending this week".
Subject line under 50 characters that names the day the trial ends.
Three sentences in the brand voice: the trial ends on their end_date, their data stays
if they upgrade, and one button labelled "Keep my workspace" that links to the billing page.
No discount.
```

The billing page differs per customer, so it is an `inputs` row in that recipe.

## Bad, from `recipes/intempt/`

`competitor-mention-detected-response` step 3 (Coming soon). The lint reports a bracket placeholder:

```
... 'Helpful comparison: [Product] vs [Competitor] from your team's perspective' ...
'Want to talk? [CSM name] would like to understand what's not working' ...
```

`[Product]`, `[Competitor]` and `[CSM name]` point at nothing. The step also writes four emails, one
per intent, which is four steps.

`b2b-nurture` step 4 (Coming soon) is lint-clean and still too vague to build the same thing twice:

```
Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc,
cold=education content.
```

Three emails in one step, and no length, subject, tone or call to action for any of them.

## What belongs in `inputs`

- a link that differs per customer: the billing page, the booking page, a help article;
- a sender name or signature, when the recipe should not choose one.

## Common lint failures

| Lint | Seen as | Fix |
|---|---|---|
| bracket placeholder | `[Product]`, `[CSM name]` | write the value, or make it an `inputs` row |
| over 1200 chars | one step writing an email per tier or per intent | one email per step |
| rationale, not instruction | why the email works | delete it; the step is the email |

`scripts/portability.py` blocks a real email address in the copy; use `you@example.com` for a
placeholder in markup.
