---
id: cold-outbound
title: Cold outbound sequence
slash_command: /cold-outbound
group: Journeys
owner: intempt
curator: somya
summary: Builds a target list from your ICP, runs a multi touch sequence with a booking link in it, and
  shows what pipeline came out.
description: >-
  Target list, multi-touch sequence, tailored content, deliverability protection.
version: 2.0.0
classification:
  product:
    - sales
  agent: outreach-rep
  mode:
    - b2b
  industry:
    - b2b-saas
    - media
  vertical:
    - sales-led
  complexity: advanced
  executionMode: live
  tags:
    - cold-outbound
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new segment, from step 1 "Build the target list"
    - A new designed email, from step 2 "Write the outbound emails"
    - A new journey, from step 3 "Run the touches, then break off"
    - A meeting action, from step 4 "Set up the booking link"
    - A new dashboard, from step 5 "Track replies and meetings"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the target list
    summary: >-
      Prospects matched to your ICP on company fit and intent signals.
    builds: segment
    description: >-
      Build target prospect list from ICP criteria (firmographic + intent signals).
  - id: s2
    title: Write the outbound emails
    summary: >-
      Cold email templates in your brand voice, with tokens for the details specific to each prospect.
    builds: email_html
    description: >-
      Generate personalized cold-outbound email templates with brand voice and prospect-specific personalization
      tokens. Use the result of "Build the target list".
    dependsOn:
      - s1
  - id: s3
    title: Run the touches, then break off
    summary: >-
      A multi touch sequence with a set cadence and breakup logic for prospects who stay silent.
    builds: journey
    description: >-
      Build a multi-touch outbound journey with appropriate cadence and break-up logic. Use the result
      of "Build the target list", "Write the outbound emails".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Set up the booking link
    summary: >-
      The link reps drop into outreach, with your availability and meeting types configured.
    builds: meeting
    description: >-
      Configure the booking link reps include in outreach, with availability and meeting-type config.
      Use the result of "Build the target list", "Write the outbound emails", "Run the touches, then break
      off".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Track replies and meetings
    summary: >-
      Outreach volume, reply rate, meetings booked, and the pipeline it contributed.
    builds: dashboard
    description: >-
      Compose a dashboard tracking outreach volume, reply rate, meeting-booked rate, and pipeline contribution.
      Use the result of "Build the target list", "Write the outbound emails", "Run the touches, then break
      off", "Set up the booking link".
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
  - key: scheduling_link
    producedByStep: s4
    type: scheduling_link
    description: Scheduling Link produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Cold outbound sequence

Builds a target list from your ICP, runs a multi touch sequence with a booking link in it, and shows what pipeline came out.

## Steps

1. **Build the target list** (builds segment)

   Prospects matched to your ICP on company fit and intent signals.

2. **Write the outbound emails** (builds email_html)

   Cold email templates in your brand voice, with tokens for the details specific to each prospect.

3. **Run the touches, then break off** (builds journey)

   A multi touch sequence with a set cadence and breakup logic for prospects who stay silent.

4. **Set up the booking link** (builds meeting)

   The link reps drop into outreach, with your availability and meeting types configured.

5. **Track replies and meetings** (builds dashboard)

   Outreach volume, reply rate, meetings booked, and the pipeline it contributed.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **scheduling_link** (scheduling_link): Scheduling Link produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new segment, from step 1 "Build the target list"
- A new designed email, from step 2 "Write the outbound emails"
- A new journey, from step 3 "Run the touches, then break off"
- A meeting action, from step 4 "Set up the booking link"
- A new dashboard, from step 5 "Track replies and meetings"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, meeting.
