---
id: testing-retrospective
title: Quarterly experiment retrospective
slash_command: /testing-retrospective
group: Dashboards
owner: intempt
curator: sid
summary: >-
  Builds a quarterly retrospective dashboard tracking exposure events, conversion metrics, and engagement
  trends across your testing periods.
description: >-
  Quarterly retrospective dashboard tracking conversion events and engagement trends across testing periods.
version: 2.0.0
classification:
  product:
    - marketing
  agent: experience-optimizer
  mode:
    - all
  industry:
    - ai
    - b2b-saas
    - ecommerce
    - finance
    - media
  vertical: []
  complexity: standard
  executionMode: live
  tags:
    - testing-retrospective
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Compile the quarter's results"
    - A new report, from step 2 "Find the patterns that repeat"
    - A new dashboard, from step 3 "Track cadence and impact"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Compile the quarter's results
    summary: >-
      Every experiment run in the period sorted into winners, losers and inconclusive.
    builds: report
    description: >-
      Compile results across all experiments run in the period: winners, losers, inconclusive.
  - id: s2
    title: Find the patterns that repeat
    summary: >-
      Which kinds of hypothesis won, which traffic sources behaved differently, and which surfaces performed
      best.
    builds: report
    description: >-
      Generate insights report extracting patterns: which hypothesis families won, which traffic sources
      differed, best surfaces. Use the result of "Compile the quarter's results".
    dependsOn:
      - s1
  - id: s3
    title: Track cadence and impact
    summary: >-
      How many tests you ran, what share of them won, and the revenue those wins produced.
    builds: dashboard
    description: >-
      Compose a dashboard summarizing testing cadence, win rate, and revenue impact. Use the result of
      "Compile the quarter's results", "Find the patterns that repeat".
    dependsOn:
      - s1
      - s2
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Reports produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Quarterly experiment retrospective

Builds a quarterly retrospective dashboard tracking exposure events, conversion metrics, and engagement trends across your testing periods.

## Steps

1. **Compile the quarter's results** (builds report)

   Every experiment run in the period sorted into winners, losers and inconclusive.

2. **Find the patterns that repeat** (builds report)

   Which kinds of hypothesis won, which traffic sources behaved differently, and which surfaces performed best.

3. **Track cadence and impact** (builds dashboard)

   How many tests you ran, what share of them won, and the revenue those wins produced.

## What you end up with

- **report** (report): Reports produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Compile the quarter's results"
- A new report, from step 2 "Find the patterns that repeat"
- A new dashboard, from step 3 "Track cadence and impact"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, report.
