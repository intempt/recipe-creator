---
id: user-retention-weekly
title: Weekly user retention
slash_command: /user-retention-weekly
group: Reports
owner: intempt
curator: aman
summary: Shows what share of each week's signups are still coming back at weeks 1, 4 and 12, and which
  acquisition sources hold up best.
description: >-
  Weekly cohort retention with W1/W4/W12 benchmarks and acquisition-source comparison.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
    - media
  vertical: []
  complexity: quick
  executionMode: live
  tags:
    - retention
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Track weekly signup cohorts"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track weekly signup cohorts
    summary: >-
      Weekly cohorts anchored on signup over 12 weeks, measuring who starts a session in later weeks,
      split by acquisition source. Benchmarks week 1 at 40%, week 4 at 25% and week 12 at 15%, and flags
      cohorts down more than 5 points.
    builds: report
    description: |-
      Create a Retention report called "Weekly User Retention".
      Anchor event: user_created
      Return event: session_start
      Cohort granularity: Weekly
      Time range: Last 12 weeks (require cohorts to have completed full 12-week return window where possible)
      Breakdown: By Users.utm_source (acquisition source)
      Compare: Previous period (prior 12 weeks of cohorts)
      Chart type: Retention curve (line per cohort) plus cohort table with W1 / W4 / W12 columns
      Annotations:
      - Add horizontal benchmarks: W1 retention 40% (B2B SaaS median), W4 25%, W12 15%.
      - Flag any cohort where W1 retention dropped >5 percentage points vs. the prior cohort.
      - Highlight the source with the strongest W12 retention (highest-quality acquisition channel).
      - Identify whether retention curves are flattening over time (good (natural retention forming a plateau) or continuously decaying (bad) no stable user base forming).
      Surface the source-by-source retention gap at W4: the moment by which most low-quality signups have churned out.
      Taxonomy notes:
      - user_created and session_start are canonical. Users.utm_source is the canonical first-touch attribute.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Weekly user retention

Shows what share of each week's signups are still coming back at weeks 1, 4 and 12, and which acquisition sources hold up best.

## Steps

1. **Track weekly signup cohorts** (builds report)

   Weekly cohorts anchored on signup over 12 weeks, measuring who starts a session in later weeks, split by acquisition source. Benchmarks week 1 at 40%, week 4 at 25% and week 12 at 15%, and flags cohorts down more than 5 points.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Track weekly signup cohorts"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
