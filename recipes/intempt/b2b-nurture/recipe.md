---
id: b2b-nurture
title: B2B lead nurture and routing
slash_command: /b2b-nurture
group: Journeys
owner: intempt
curator: somya
summary: Scores inbound leads, hands the sales ready ones to a rep with an owner and a task, and keeps
  the rest warm with content matched to how close they are.
description: >-
  Score leads, segment by readiness, route hot leads to sales, nurture the rest.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - b2b
  industry:
    - ai
    - b2b-saas
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - b2b-nurture
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new attribute, from step 1 "Score every lead"
    - A new segment, from step 2 "Split into hot, warm and cold"
    - A new workflow, from step 3 "Hand hot leads to a rep"
    - A new designed email, from step 4 "Write content for each bucket"
    - A new journey, from step 5 "Nurture at the right pace"
    - A new dashboard, from step 6 "Track handoffs and conversion"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score every lead
    summary: >-
      A qualification score built from company fit, intent signals and how deeply the person has engaged.
    builds: attribute
    description: >-
      Define a Qualification scoring attribute weighting firmographic fit, intent signals, and engagement
      depth.
  - id: s2
    title: Split into hot, warm and cold
    summary: >-
      Three buckets off that score: hot means sales ready, warm goes to nurture, cold is a long cycle.
    builds: segment
    description: >-
      Segment leads into hot (sales-ready), warm (nurture), and cold (long-cycle) buckets based on score.
      Use the result of "Score every lead".
    dependsOn:
      - s1
  - id: s3
    title: Hand hot leads to a rep
    summary: >-
      Hot leads get an owner assigned and a task created. Warm and cold leads go into the nurture journeys
      instead.
    builds: workflow
    description: >-
      Create a workflow routing hot leads to sales (assign owner, create task) and adding warm/cold leads
      to nurture journeys. Use the result of "Score every lead", "Split into hot, warm and cold".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Write content for each bucket
    summary: >-
      A demo offer for hot leads, case studies and an ROI calculator for warm ones, and education for
      cold ones.
    builds: email_html
    description: >-
      Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc, cold=education
      content. Use the result of "Score every lead", "Split into hot, warm and cold", "Hand hot leads
      to a rep".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Nurture at the right pace
    summary: >-
      One journey per bucket, each with the cadence and content that fits how ready the lead is.
    builds: journey
    description: >-
      Build per-segment nurture journeys with appropriate cadence and content. Use the result of "Score
      every lead", "Split into hot, warm and cold", "Hand hot leads to a rep", "Write content for each
      bucket".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: Track handoffs and conversion
    summary: >-
      Score distribution, how many hot leads actually reach sales, and how many nurtured leads turn into
      MQLs.
    builds: dashboard
    description: >-
      Compose a dashboard tracking score distribution, hot-lead handoff rate, and nurture-to-MQL conversion.
      Use the result of "Score every lead", "Split into hot, warm and cold", "Hand hot leads to a rep",
      "Write content for each bucket", "Nurture at the right pace".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
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
  - key: asset
    producedByStep: s4
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s5
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s6
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# B2B lead nurture and routing

Scores inbound leads, hands the sales ready ones to a rep with an owner and a task, and keeps the rest warm with content matched to how close they are.

## Steps

1. **Score every lead** (builds attribute)

   A qualification score built from company fit, intent signals and how deeply the person has engaged.

2. **Split into hot, warm and cold** (builds segment)

   Three buckets off that score: hot means sales ready, warm goes to nurture, cold is a long cycle.

3. **Hand hot leads to a rep** (builds workflow)

   Hot leads get an owner assigned and a task created. Warm and cold leads go into the nurture journeys instead.

4. **Write content for each bucket** (builds email_html)

   A demo offer for hot leads, case studies and an ROI calculator for warm ones, and education for cold ones.

5. **Nurture at the right pace** (builds journey)

   One journey per bucket, each with the cadence and content that fits how ready the lead is.

6. **Track handoffs and conversion** (builds dashboard)

   Score distribution, how many hot leads actually reach sales, and how many nurtured leads turn into MQLs.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new attribute, from step 1 "Score every lead"
- A new segment, from step 2 "Split into hot, warm and cold"
- A new workflow, from step 3 "Hand hot leads to a rep"
- A new designed email, from step 4 "Write content for each bucket"
- A new journey, from step 5 "Nurture at the right pace"
- A new dashboard, from step 6 "Track handoffs and conversion"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, workflow.
