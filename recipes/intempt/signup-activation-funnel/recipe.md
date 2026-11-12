---
frontmatter_id: signup-activation-funnel
slash_command: /signup-activation-funnel
description: Shows how many new signups come back, use the core feature and activate within two weeks, and which signup source produces the best ones.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a signup-to-activation funnel that shows return, core-feature use and two-week activation, broken down by
    signup source with flags.
  parameters:
  - name: conversion_window
    type: duration
    label: Conversion window
    default: 14 d
    required: false
  - name: returned_window
    type: duration
    label: Return window after signup
    default: 24 h
    required: false
  - name: comparison_period
    type: duration
    label: Comparison period (previous period)
    default: 14 d
    required: false
  - name: activation_rate_benchmark
    type: number
    label: Activation rate benchmark (%)
    default: 30
    required: false
  - name: low_activation_threshold
    type: number
    label: Flag sources with activation rate below (%)
    default: 15
    required: false
  - name: high_activation_threshold
    type: number
    label: Highlight sources with activation rate above (%)
    default: 40
    required: false
  - name: returned_median_threshold
    type: duration
    label: Max median time to 'Returned After Signup' before flag
    default: 24 h
    required: false
  - name: core_feature_median_threshold
    type: duration
    label: Max median time to 'Used Core Feature' before flag
    default: 7 d
    required: false
  - name: top_sources_count
    type: number
    label: Number of top signup sources to break down
    default: 6
    required: false
  requirements:
  - slot: user_created_event
    kind: event
    meaning: A new user account was created (signup)
    properties:
    - name: user_id
      type: string
      meaning: Identifier of the user who signed up
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
    properties:
    - name: user_id
      type: string
      meaning: Identifier of the user who started the session
      optional: false
  - slot: journey_goal_completed_event
    kind: event
    meaning: A user completed a journey goal in a marketing or onboarding journey
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey in which the goal was completed
      optional: false
    - name: user_id
      type: string
      meaning: Identifier of the user who completed the goal
      optional: false
    - name: occurred_date
      type: date
      meaning: Date and time the goal was completed
      optional: false
  - slot: onboarding_journey
    kind: knowledge
    meaning: The onboarding/activation journey whose ID identifies the core feature goal
  - slot: activation_journey
    kind: knowledge
    meaning: The activation journey whose ID identifies the activation goal
  - slot: signup_source_attribute
    kind: attribute
    meaning: The user's first-touch UTM source channel (signup source)
  - slot: signup_timestamp_attribute
    kind: attribute
    meaning: The date and time the user signed up (signup_at)
  steps:
  - id: s1
    builds: report
    uses:
    - user_created_event
    - session_start_event
    - journey_goal_completed_event
    - onboarding_journey
    - activation_journey
    - signup_source_attribute
    - signup_timestamp_attribute
    - conversion_window
    - returned_window
    - comparison_period
    - activation_rate_benchmark
    - low_activation_threshold
    - high_activation_threshold
    - returned_median_threshold
    - core_feature_median_threshold
    - top_sources_count
    instruction: 'Create a funnel report named "Signup to Activation" with a conversion window of {conversion_window}. Steps:
      (1) {user_created_event} labeled "Signed Up"; (2) {session_start_event} within {returned_window} of the signup event,
      labeled "Returned After Signup"; (3) {journey_goal_completed_event} where journey_id matches {onboarding_journey}, labeled
      "Used Core Feature"; (4) {journey_goal_completed_event} where journey_id matches {activation_journey} and occurred_date
      minus {signup_timestamp_attribute} is at most {conversion_window}, labeled "Activated". Break down by {signup_source_attribute},
      showing the top {top_sources_count} channels (organic, paid_search, paid_social, content, referral, direct). Compare
      against the previous {comparison_period}. For each step, show median and 75th-percentile time-to-convert from the previous
      step and per-source conversion rate at each stage. Annotations: add a benchmark that activation rate (Activated / Signed
      Up) of {activation_rate_benchmark}% is typical for PLG SaaS; flag any source whose activation rate is below {low_activation_threshold}%
      as poor lead quality or onboarding mismatch; flag any step where median time-to-convert exceeds {returned_median_threshold}
      for "Returned After Signup" or {core_feature_median_threshold} for "Used Core Feature"; highlight sources whose activation
      rate is above {high_activation_threshold}%. Identify the signup source that produces the highest-activating users at
      sufficient volume.'
---

# Signup to activation

Slash command: /signup-activation-funnel

## Step 1: Follow signups to activation

Create a Funnel report called "Signup to Activation".
Steps:
1. Event "User created": "Signed Up"
2. Event "Session start" within 24 hours of User created: "Returned After Signup" (proxy for engagement after creation)
3. Event "Completed a journey goal" where journey_id matches the onboarding/activation journey: "Used Core Feature"
4. Event "Completed a journey goal" where journey_id matches the activation journey AND Occurred date - signup_at <= 14 days: "Activated"
Conversion window: 14 days
Breakdown: By Users.UTM source (signup source: top 6 channels: organic, paid_search, paid_social, content, referral, direct)
Compare: Previous period (prior 14 days)
For each step, also surface:
- Median and 75th-percentile time-to-convert from previous step
- Per-source conversion rate at each stage
Annotations:
- Add benchmark: activation rate (Step 4 / Step 1) of 30% is typical PLG SaaS.
- Flag any source with activation rate <15% (poor lead quality or onboarding mismatch).
- Flag any step where median time-to-convert exceeds 24 hours for "Returned After Signup" or 7 days for "Used Core Feature".
- Highlight sources with activation rate >40%.
Identify which signup source produces the highest-activating users at sufficient volume.
Taxonomy notes:
- User created and Completed a journey goal are canonical. Completed a journey goal carries journey_id, Occurred date, user_id.
- "signup_completed", "onboarding_started" as standalone events do not exist; the activation journey itself emits Completed a journey goal when the user hits the activation goal.
- Users.UTM source is the canonical first-touch source attribute.
