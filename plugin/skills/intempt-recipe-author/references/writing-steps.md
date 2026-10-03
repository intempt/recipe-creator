# Writing steps the engine can run

**The test fits in one sentence: could two competent people type this description into the Add step
panel and get different things?** If yes, the step describes what you meant rather than instructing
anyone.

A step's `description` is the one instruction the engine runs (`llm-wrapper` `orchestrator.py`
`step_text()`). The step check reads it once and derives the command, the entity and the arguments
(`step_check.py`). Nothing else in the file tells it what to do.

## Every step names

1. **Who.** Users or accounts. A segment without it is vague.
2. **The exact event, attribute and value**, as it exists in the project: the `order_created` event,
   the `plan_name` attribute, the value `"trial"`.
3. **The window.** "In the last 14 days", "between 60 and 90 days ago", "at any time". Never
   "recently".
4. **Every threshold.** "1000 or more", "exactly 1", "more than 0".
5. **One thing.** One segment, one email, one image. "Build a segment and email it" is two steps.
6. **An earlier step by its title**, when it uses that step's result, listed in `dependsOn`.

## The vague rule

The step check marks a description vague when it points at something that does not exist
(`step_check.py` R36). A vague step does not run; it waits for a person to clarify. So:

- No placeholders: `[Product]`, `<Channel Name>`, `{{steps.s1}}`. Name the earlier step by its title
  and write the value out.
- Nothing only you have: a journey id, a form name, a list. Make it an `inputs` row and say "the
  activation journey chosen for this run".
- No rationale. "This is the highest-ROI cohort" is read as something to do.
- No other vendors' names, and no model or pipeline names. The engine picks the model.

`python3 scripts/validate_recipes.py --lint` reports placeholders, rationale, vendor names,
segments that never say who, and descriptions over 1200 characters.

## Bad and good, from this repository

**A segment** (`at-risk-vips`), before:

```
Create a segment called "At-Risk VIPs".
Object: Users
Rules (all conditions joined by AND):
- Attribute: lifetime_value >= 1000
- AND Attribute: days_since_last_activity is between 45 and 90
...
Description: High-LTV customers who are going quiet: the Klaviyo "Needs Attention" RFM cohort.
Most expensive cohort to lose; strongest ROI for personalized win-back outreach.
```

After:

```
Build a segment of users named "At-Risk VIPs".
A user is in the segment only when all of these are true:
- their lifetime_value attribute is 1000 or more
- their days_since_last_activity attribute is between 45 and 90
- they did the order_created event 2 or more times, at any time
- they did not do the order_created event in the last 45 days
```

The rationale and the vendor name are gone. The window on every event is written out.

**A placeholder** (`acquisition-channel-cohort`), before: `utm_source = "<source>"`. After: the
description uses `"google"` and `"cpc"`, and an `inputs` row says the installer can supply another
pair, and that google and cpc are used if they do not.

**An image** (`upscale`), before:

```
Upscale the image to 4x resolution.
Pure detail enhancement only. Same composition, same colors, same subject.
Pipeline: fal-ai/clarity-upscaler, scale: 4
```

After:

```
Upscale the image attached to this run to 4 times its width and height.
Enhance detail only: keep the composition, colours and subject the same, and do not re-render the subject.
```

The pipeline line named a vendor and a model the engine does not take instructions about.

## Before you keep a step, ask it out loud

- Who is this about?
- Which event or attribute, spelled how?
- Over what window?
- What happens if the installer's project does not have it? (That is a `prerequisites` entry or an
  `inputs` row.)
- Is every sentence something to do?
