---
id: trial-activation-funnel
title: Trial activation funnel
slash_command: /trial-activation-funnel
group: Reports
owner: intempt
summary: Shows how far trial users get through setup and core feature use before the trial ends, and which
  sources bring trials that activate.
description: >-
  Trial milestone funnel using subscription_created (trial), session_start, and journey-goal events.
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
    - A new report, from step 1 "Track trials through setup"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track trials through setup
    summary: >-
      A five step funnel over 14 days from trial start to a return session within 24 hours, a completed
      setup goal, core feature use and full activation, split by signup source. Flags under 50% reaching
      setup on day one and core use taking over 48 hours.
    builds: report
    description: |-
      Create a Funnel report called "Trial Activation Funnel".
      Steps:
      1. Event "subscription_created" where trial_end and trial_start are populated: "Started Trial"
      2. Event "session_start" by the same user within 24h of step 1: "First Return Session"
      3. Event "goal_completed_in_journey" where journey_id matches the integration/setup journey: "Completed Setup Goal"
      4. Event "goal_completed_in_journey" where journey_id matches the core-feature-use journey: "Used Core Feature"
      5. Event "goal_completed_in_journey" where journey_id matches the full-activation journey AND occurred within 14 days of trial start: "Fully Activated"
      Conversion window: 14 days
      Breakdown: By Users.utm_source
      Compare: Previous period (prior 14 days)
      For each step, also surface:
      - Median time-to-convert from previous step
      - Per-source conversion rate at each stage
      Annotations:
      - Flag if the % of trials that hit Step 3 within 24 hours is below 50%: first-day setup is a strong activation predictor.
      - Flag if median time from Step 1 to Step 4 exceeds 48 hours: the time-to-value benchmark for self-serve PLG.
      - Flag any source where Step 5 (full activation) rate is below 15%.
      - Highlight sources where Step 5 rate exceeds 35%.
      Surface the single highest-leverage step to optimize: largest drop-off × largest downstream lift on Step 5.
      Taxonomy notes:
      - "integration_connected" and "onboarding_started" as standalone events do not exist. Setup milestones are tracked via goal_completed_in_journey events emitted by the relevant onboarding journey.
      - Each onboarding milestone (setup, core-feature use, full activation) corresponds to a different journey_id in the project's journey configuration.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Trial activation funnel

Shows how far trial users get through setup and core feature use before the trial ends, and which sources bring trials that activate.

## Steps

1. **Track trials through setup** (builds report)

   A five step funnel over 14 days from trial start to a return session within 24 hours, a completed setup goal, core feature use and full activation, split by signup source. Flags under 50% reaching setup on day one and core use taking over 48 hours.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Track trials through setup"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
