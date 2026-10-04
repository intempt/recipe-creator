# Jobs the engine cannot build yet

**Read this during the conversation, not after drafting.** If someone says "and then put them in a
journey" and the engine cannot build a journey, that has to come up while you are still talking.
Found afterwards, the draft already promises something imaginary and the repair is a rewrite.

## What the engine builds today

The `builds` values on the Install now list in [references/entities.md](entities.md):
segments, events, attributes, emails, SMS, push and Slack messages, images, JSON content, and brand
avatars, poses, scenes and design systems. A recipe whose every step builds one of these is
**Install now**.

## What it cannot build yet

Everything on the Coming soon list in [references/entities.md](entities.md), which is
generated from `COMING_SOON_ENTITIES` in `scripts/recipe_contract.py`. The ones people ask for most:

- **Journeys.** Turned off in the engine on 2026-09-21. "Send this email when they enter the
  segment" is a journey.
- **Reports and dashboards.** Funnels, retention, paths and the dashboards that hold them.
- **Workflows.** Anything scheduled or triggered that runs without a person.
- **Experiments and website personalization.**
- **Product recommendations, landing pages, videos and custom agents.**

## Jobs that look buildable and are not

- **Scoring.** There is no scoring builder. A score is an `attribute`, and an AI attribute can hold
  one, but say exactly what goes into it and how each value is reached. "Score accounts by fit" is
  not a step; "an attribute on accounts that is High when employees is 50 to 500 and industry is
  SaaS, otherwise Low" is.
- **Dedupe and merge.** No step merges or deletes users or accounts. A recipe can build a segment
  of likely duplicates for a person to review. It cannot resolve them.
- **Sending.** Building an email is not sending it. Without a journey, a recipe produces the email
  and the segment, and a person sends.
- **Anything in another product.** A step acts inside Intempt. "Update the deal in the CRM" is not a
  step, even when the CRM is connected.

## What to do when the job needs one of these

1. Say so in the conversation, in one sentence, naming the builder.
2. Keep the step and give it the real `builds` value, for example `journey`. Do not swap in an
   Install now entity that does something different so the recipe looks runnable.
3. The recipe is then **Coming soon**, and the catalog says which builder it is waiting on. When the
   engine ships that builder, it flips to Install now with no change to your file.
4. If the rest is useful on its own, offer a second, smaller recipe with only the Install now steps.
   Two honest recipes beat one that waits on four builders.
