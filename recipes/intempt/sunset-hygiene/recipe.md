---
id: sunset-hygiene
title: Sunset inactive subscribers
slash_command: /sunset-hygiene
group: Journeys
owner: intempt
curator: somya
summary: Gives subscribers who have ignored six months of email one chance to say they still want it,
  then stops mailing them to protect deliverability.
description: >-
  Re-engage long-unengaged users, then suppress them for deliverability protection.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - all
  complexity: advanced
  executionMode: live
  tags:
    - sunset-hygiene
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new segment, from step 1 "Find who stopped reading"
    - A new designed email, from step 2 "Write the last chance email"
    - A new journey, from step 3 "Send it, then wait 14 days"
    - A new workflow, from step 4 "Suppress anyone who ignores it"
    - A new dashboard, from step 5 "Watch your deliverability"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find who stopped reading
    summary: >-
      Subscribers who have not opened or clicked anything in 180 days or more.
    builds: segment
    description: >-
      Identify subscribers who have not opened or clicked any email in 180+ days.
  - id: s2
    title: Write the last chance email
    summary: >-
      One email asking them to confirm they still want to hear from you, with a clear opt in.
    builds: email_html
    description: >-
      Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA. Use
      the result of "Find who stopped reading".
    dependsOn:
      - s1
  - id: s3
    title: Send it, then wait 14 days
    summary: >-
      The email goes out and the journey waits a fortnight for a response.
    builds: journey
    description: >-
      Build a 2-touch journey sending the final-attempt email and waiting 14 days for response. Use the
      result of "Find who stopped reading", "Write the last chance email".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Suppress anyone who ignores it
    summary: >-
      After the 14 days, everyone who did not respond is added to the suppression list.
    builds: workflow
    description: >-
      Create a workflow automatically adding non-responders to the suppression list after the 14-day window.
      Use the result of "Find who stopped reading", "Write the last chance email", "Send it, then wait
      14 days".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Watch your deliverability
    summary: >-
      Send rate, open rate, complaints, bounces and inbox placement.
    builds: dashboard
    description: >-
      Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce
      rate, inbox-placement. Use the result of "Find who stopped reading", "Write the last chance email",
      "Send it, then wait 14 days", "Suppress anyone who ignores it".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
  - key: workflow
    producedByStep: s4
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Sunset inactive subscribers

Gives subscribers who have ignored six months of email one chance to say they still want it, then stops mailing them to protect deliverability.

## Steps

1. **Find who stopped reading** (builds segment)

   Subscribers who have not opened or clicked anything in 180 days or more.

2. **Write the last chance email** (builds email_html)

   One email asking them to confirm they still want to hear from you, with a clear opt in.

3. **Send it, then wait 14 days** (builds journey)

   The email goes out and the journey waits a fortnight for a response.

4. **Suppress anyone who ignores it** (builds workflow)

   After the 14 days, everyone who did not respond is added to the suppression list.

5. **Watch your deliverability** (builds dashboard)

   Send rate, open rate, complaints, bounces and inbox placement.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new segment, from step 1 "Find who stopped reading"
- A new designed email, from step 2 "Write the last chance email"
- A new journey, from step 3 "Send it, then wait 14 days"
- A new workflow, from step 4 "Suppress anyone who ignores it"
- A new dashboard, from step 5 "Watch your deliverability"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, workflow.
