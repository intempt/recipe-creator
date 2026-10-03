---
id: lead-qualification
title: Lead qualification and handoff
slash_command: /lead-qualification
group: Journeys
owner: intempt
summary: Scores inbound leads, sends the sales ready ones round robin to a rep with the context attached,
  and puts the rest into nurture.
description: >-
  Score leads, segment, route hot leads to sales, nurture the rest.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
  complexity: advanced
  executionMode: live
  tags:
    - lead-qualification
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new attribute, from step 1 "Score every lead"
    - A new segment, from step 2 "Split into hot, warm and cold"
    - A new workflow, from step 3 "Route hot leads round robin"
    - A new journey, from step 4 "Nurture warm and cold leads"
    - A new dashboard, from step 5 "Track handoff to opportunity"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score every lead
    summary: >-
      A qualification score weighing company fit, intent and engagement.
    builds: attribute
    description: >-
      Define a Qualification attribute weighting firmographic fit, intent, and engagement.
  - id: s2
    title: Split into hot, warm and cold
    summary: >-
      Three tiers off that score.
    builds: segment
    description: >-
      Segment leads into hot/warm/cold tiers based on qualification score. Use the result of "Score every
      lead".
    dependsOn:
      - s1
  - id: s3
    title: Route hot leads round robin
    summary: >-
      Hot leads are handed round robin to a rep on the team, with a task created that carries the context.
    builds: workflow
    description: >-
      Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks
      with context. Use the result of "Score every lead", "Split into hot, warm and cold".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Nurture warm and cold leads
    summary: >-
      A journey for each of the other two tiers, at a cadence that suits how far off they are.
    builds: journey
    description: >-
      Build nurture journeys for warm and cold leads with appropriate cadence. Use the result of "Score
      every lead", "Split into hot, warm and cold", "Route hot leads round robin".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Track handoff to opportunity
    summary: >-
      Lead volume, score distribution, how many reach a rep, and how many turn into opportunities.
    builds: dashboard
    description: >-
      Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      Use the result of "Score every lead", "Split into hot, warm and cold", "Route hot leads round robin",
      "Nurture warm and cold leads".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: journey
    producedByStep: s4
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Lead qualification and handoff

Scores inbound leads, sends the sales ready ones round robin to a rep with the context attached, and puts the rest into nurture.

## Steps

1. **Score every lead** (builds attribute)

   A qualification score weighing company fit, intent and engagement.

2. **Split into hot, warm and cold** (builds segment)

   Three tiers off that score.

3. **Route hot leads round robin** (builds workflow)

   Hot leads are handed round robin to a rep on the team, with a task created that carries the context.

4. **Nurture warm and cold leads** (builds journey)

   A journey for each of the other two tiers, at a cadence that suits how far off they are.

5. **Track handoff to opportunity** (builds dashboard)

   Lead volume, score distribution, how many reach a rep, and how many turn into opportunities.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new attribute, from step 1 "Score every lead"
- A new segment, from step 2 "Split into hot, warm and cold"
- A new workflow, from step 3 "Route hot leads round robin"
- A new journey, from step 4 "Nurture warm and cold leads"
- A new dashboard, from step 5 "Track handoff to opportunity"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, workflow.
