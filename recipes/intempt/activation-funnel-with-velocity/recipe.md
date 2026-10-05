---
id: activation-funnel-with-velocity
title: Activation funnel with velocity
slash_command: /activation-funnel-with-velocity
group: Reports
owner: intempt
curator: aman
summary: >-
  Shows where new users drop out across key onboarding steps to pinpoint activation bottlenecks.
description: >-
  Activation funnel report: identifies conversion drop-offs across onboarding milestones.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: quick
  executionMode: live
  tags:
    - funnel
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Time each step to activation"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Time each step to activation
    summary: >-
      A five step funnel from signup to habitual use inside a 14 day window, split by signup source. Each
      step carries median and 75th percentile time to convert plus the share of users still stuck after
      24 hours, 72 hours and 7 days.
    builds: report
    description: |-
      Create a Funnel report called "Activation with Step Velocity".
      Steps:
      1. Event "user_created": "Signed Up"
      2. Event "session_start" within 24h of user_created: "First Return"
      3. Event "goal_completed_in_journey" where journey_id matches the setup journey: "Completed Setup"
      4. Event "goal_completed_in_journey" where journey_id matches the core-feature journey: "Used Core Feature"
      5. Event "goal_completed_in_journey" where journey_id matches the activation journey, with frequency: occurred_at appears 3+ times in the 7 days following step 4: "Activated (Habituated)"
      Conversion window: 14 days
      Breakdown: By Users.utm_source
      Compare: Previous period (prior 14 days)
      For each step, in addition to conversion rate, surface:
      - Median time-to-convert from previous step
      - 75th-percentile time-to-convert
      - Stall rate: % of users at this step who have NOT advanced after 24h, after 72h, after 7 days
      Annotations:
      - Add benchmarks: median signup to setup-complete ≤ 24 hours is the activation gold standard.
      - Flag any step where p75 time-to-convert exceeds 7 days (long tail of stalled users).
      - Flag any step where the stall-rate-at-72h is above 60%.
      - Highlight the step where reducing time-to-convert by 50% would have the biggest downstream activation lift.
      Velocity is the activation lever: drop-off tells you where users die, velocity tells you where they're stuck.
      Taxonomy notes:
      - "Habituated" Step 5 requires Lovable to compute the "3+ goal completions in 7 days" rule from goal_completed_in_journey timestamps grouped by user.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Activation funnel with velocity

Shows where new users drop out across key onboarding steps to pinpoint activation bottlenecks.

## Steps

1. **Time each step to activation** (builds report)

   A five step funnel from signup to habitual use inside a 14 day window, split by signup source. Each step carries median and 75th percentile time to convert plus the share of users still stuck after 24 hours, 72 hours and 7 days.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Time each step to activation"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
