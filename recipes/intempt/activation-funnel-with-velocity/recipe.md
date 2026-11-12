---
frontmatter_id: activation-funnel-with-velocity
slash_command: /activation-funnel-with-velocity
description: Shows where new users drop out across key onboarding steps to pinpoint activation bottlenecks.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows where new users drop out across key onboarding steps and how long each step takes, to pinpoint activation
    bottlenecks and stuck users.
  parameters:
  - name: conversion_window
    type: duration
    label: Funnel conversion window
    default: 14 d
    required: false
  - name: comparison_window
    type: duration
    label: Comparison period (prior period)
    default: 14 d
    required: false
  - name: first_return_window
    type: duration
    label: Max time from signup to first return session
    default: 24 h
    required: false
  - name: habituation_goal_count
    type: number
    label: Goal completions required for habituated activation
    default: 3
    required: false
  - name: habituation_window
    type: duration
    label: Window for habituation goal completions after core feature
    default: 7 d
    required: false
  - name: benchmark_setup_time
    type: duration
    label: 'Benchmark: signup to setup complete'
    default: 24 h
    required: false
  - name: p75_flag_threshold
    type: duration
    label: Flag steps whose p75 time-to-convert exceeds
    default: 7 d
    required: false
  - name: stall_rate_flag_threshold
    type: number
    label: Flag steps with 72h stall rate above (%)
    default: 60
    required: false
  - name: velocity_reduction_pct
    type: number
    label: Time-to-convert reduction scenario (%)
    default: 50
    required: false
  requirements:
  - slot: signup_event
    kind: event
    meaning: A new user account was created
  - slot: session_event
    kind: event
    meaning: A user started a session in the product
  - slot: journey_goal_event
    kind: event
    meaning: A user completed a journey goal
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey the goal belongs to
      optional: false
  - slot: setup_journey
    kind: knowledge
    meaning: The identifier of the onboarding setup journey
  - slot: core_feature_journey
    kind: knowledge
    meaning: The identifier of the core-feature journey
  - slot: activation_journey
    kind: knowledge
    meaning: The identifier of the activation journey
  - slot: utm_source_attribute
    kind: attribute
    meaning: The UTM source the user came from
  steps:
  - id: s1
    builds: report
    uses:
    - signup_event
    - session_event
    - journey_goal_event
    - setup_journey
    - core_feature_journey
    - activation_journey
    - utm_source_attribute
    - conversion_window
    - comparison_window
    - first_return_window
    - habituation_goal_count
    - habituation_window
    - benchmark_setup_time
    - p75_flag_threshold
    - stall_rate_flag_threshold
    - velocity_reduction_pct
    instruction: 'Create a funnel report named "Activation with Step Velocity" with these steps in order: (1) {signup_event}
      labeled "Signed Up"; (2) {session_event} within {first_return_window} of the signup step, labeled "First Return"; (3)
      {journey_goal_event} where journey_id matches {setup_journey}, labeled "Completed Setup"; (4) {journey_goal_event} where
      journey_id matches {core_feature_journey}, labeled "Used Core Feature"; (5) {journey_goal_event} where journey_id matches
      {activation_journey}, requiring at least {habituation_goal_count} occurrences within {habituation_window} following
      step 4, labeled "Activated (Habituated)". The habituation rule counts journey goal completions per user grouped by user
      over that window. Set the conversion window to {conversion_window}. Break down by {utm_source_attribute}. Compare against
      the prior {comparison_window}. For each step show conversion rate plus median time-to-convert from the previous step,
      75th-percentile time-to-convert, and stall rate (share of users at the step who have not advanced) after 24 hours, 72
      hours, and 7 days. Annotations: show {benchmark_setup_time} as the benchmark for signup to setup complete (activation
      gold standard). Flag any step whose p75 time-to-convert exceeds {p75_flag_threshold}. Flag any step whose 72-hour stall
      rate is above {stall_rate_flag_threshold}%. Highlight the step where a {velocity_reduction_pct}% reduction in time-to-convert
      would produce the largest downstream activation lift.'
---

# Activation funnel with velocity

Slash command: /activation-funnel-with-velocity

## Step 1: Time each step to activation

Create a Funnel report called "Activation with Step Velocity".
Steps:
1. Event "User created": "Signed Up"
2. Event "Session start" within 24h of User created: "First Return"
3. Event "Completed a journey goal" where journey_id matches the setup journey: "Completed Setup"
4. Event "Completed a journey goal" where journey_id matches the core-feature journey: "Used Core Feature"
5. Event "Completed a journey goal" where journey_id matches the activation journey, with frequency: Occurred date appears 3+ times in the 7 days following step 4: "Activated (Habituated)"
Conversion window: 14 days
Breakdown: By Users.UTM source
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
- "Habituated" Step 5 requires Lovable to compute the "3+ goal completions in 7 days" rule from Completed a journey goal timestamps grouped by user.
