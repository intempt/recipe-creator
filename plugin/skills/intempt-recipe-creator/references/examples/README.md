# Examples

Recipes that meet the bar in [references/recipe-contract.md](../recipe-contract.md) and
[DETERMINISM.md](../determinism.md). Copy one, rename the folder and the `id`, and change every value.

Three of them are **published recipes**, copied byte for byte from `recipes/intempt/`; a test fails
if a copy drifts from its source. One is **written for this kit** and is not in the catalog. The
difference is stated because your recipe has to make the same kind of distinction in
`does_not_claim`: an example that claims more than it has shown teaches the wrong lesson.

| Example | Provenance | Shape | Read it for |
|---|---|---|---|
| [trial-expiring-nudge](intempt/trial-expiring-nudge/recipe.md) | written for this kit | `segment`, then `email_html` with `dependsOn` | how one step uses another step's result |
| [demo-requested-accounts](intempt/demo-requested-accounts/recipe.md) | published recipe | one `segment` about accounts | users versus accounts, and a form that only the installer has |
| [acquisition-channel-cohort](intempt/acquisition-channel-cohort/recipe.md) | published recipe | one `segment` about users | a value with a default that the installer can replace |
| [ad-variants](intempt/ad-variants/recipe.md) | published recipe | one `image` | an attached file as an input, and what is decided at run time |

All four are Install now. No published recipe has an Install now `segment` followed by an
`email_html` step yet, which is why the first example is written for the kit rather than copied.

## What each one teaches

**`trial-expiring-nudge`: name the earlier step, never point at it.** Step 2 says "the users in
'Find trials ending this week'" and lists `s1` in `dependsOn`. It never writes `{{steps.s1}}`, and
it never says "that segment": the step check wires the dependency from the title. Every window is
written out (next 7 days, last 14 days) and both windows are owned up to under `does_not_claim`,
because nothing measured them. The billing link differs per customer, so it is an `inputs` row with
what happens when it is missing.

**`demo-requested-accounts`: say who, and mean it.** The first words are "a segment of accounts".
The condition then says how a user-level event rolls up: "the users in the account together did
the submit_on event". A segment that says neither users nor accounts is the first thing the step
check marks vague. The demo form is the installer's, so the step says "the demo request form chosen
for this run" and the `inputs` row says the step waits until one is chosen.

**`acquisition-channel-cohort`: a default is still a value.** The step names `"google"` and
`"cpc"` outright, so the step check has something that exists to resolve. The `inputs` row tells
the installer they can supply another pair, and that google and cpc are used if they do not. This
recipe is the after half of the placeholder example in [WRITING-STEPS.md](../writing-steps.md):
the before version said `utm_source = "<source>"` and pointed at nothing.

**`ad-variants`: an image step with an attached file.** The step says "the ad image attached to
this run", lists exactly six variants and the one thing each changes, and says nothing about a model
or a pipeline. What the new headline or palette will be is decided when the step runs, and
`does_not_claim` says so rather than implying the recipe chose them.

## If your idea overlaps one of these

Build it anyway, and say in your `description` what yours does differently. Overlapping recipes are
fine; one that does the same job without saying so makes the catalog harder to choose from.
