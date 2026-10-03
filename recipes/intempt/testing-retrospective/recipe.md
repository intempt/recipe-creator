---
id: testing-retrospective
title: Quarterly experiment retrospective
slash_command: /testing-retrospective
group: Dashboards
owner: intempt
summary: 'Pulls every experiment you ran last quarter into one review: what won, what lost, what the results
  have in common, and what to test next.'
description: >-
  Quarterly experiment review and roadmap for next testing cycle.
version: 2.0.0
classification:
  product:
    - marketing
  agent: experience-optimizer
  mode:
    - all
  complexity: standard
  executionMode: live
  tags:
    - testing-retrospective
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

Pulls every experiment you ran last quarter into one review: what won, what lost, what the results have in common, and what to test next.

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

## Availability

Coming soon: waiting on the engine to build dashboard, report.
