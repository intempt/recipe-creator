---
frontmatter_id: signup-activation-funnel
slash_command: /signup-activation-funnel
description: Emails a weekly digest of how many new signups come back, use the core feature and activate within two weeks,
  and which signup source produces the best ones.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Emails a weekly signup-to-activation digest: return, core-feature use and activation, by signup source, with slow-step
    and weak-source flags.'
  parameters:
  - name: core_feature_journey_id
    type: string
    label: Journey whose goal marks core feature use
    required: true
  - name: activation_journey_id
    type: string
    label: Journey whose goal marks activation
    required: true
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
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: user_created_event
    kind: event
    meaning: A new user account was created (signup)
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: journey_goal_completed_event
    kind: event
    meaning: A user completed a journey goal in a marketing or onboarding journey
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey in which the goal was completed
      optional: false
  - slot: signup_source_attribute
    kind: attribute
    meaning: The user's first-touch UTM source channel (signup source)
  steps:
  - id: s1
    builds: automation
    uses:
    - user_created_event
    - session_start_event
    - journey_goal_completed_event
    - signup_source_attribute
    - core_feature_journey_id
    - activation_journey_id
    - conversion_window
    - returned_window
    - comparison_period
    - activation_rate_benchmark
    - low_activation_threshold
    - high_activation_threshold
    - returned_median_threshold
    - core_feature_median_threshold
    - top_sources_count
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {user_created_event}
      in the last {comparison_period}, against the {comparison_period} before, within {conversion_window}: signed up; returned
      ({session_start_event} within {returned_window} of signup); used the core feature ({journey_goal_completed_event} with
      {journey_goal_completed_event.journey_id} equal to {core_feature_journey_id}); activated ({journey_goal_completed_event}
      with {journey_goal_completed_event.journey_id} equal to {activation_journey_id}). It writes: users at each step and
      step conversion % by {signup_source_attribute} (top {top_sources_count} sources); median time between steps; activation
      rate %, activated / signed up; the best-activating source at volume. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. It compares activation with {activation_rate_benchmark}%, flags sources
      under {low_activation_threshold}%, names sources over {high_activation_threshold}%, and flags median time to return
      above {returned_median_threshold} or to core use above {core_feature_median_threshold}. Nothing else is sent.'
---

# Signup to activation

Slash command: /signup-activation-funnel

## Step 1: Email the weekly activation digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did user created event in the last 14 d, against the 14 d before, within 14 d: signed up; returned (session start event within 24 h of signup); used the core feature (journey goal completed event with journey id equal to the journey whose goal marks core feature use); activated (journey goal completed event with journey id equal to the journey whose goal marks activation). It writes: users at each step and step conversion % by signup source attribute (top 6 sources); median time between steps; activation rate %, activated / signed up; the best-activating source at volume. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. It compares activation with 30%, flags sources under 15%, names sources over 40%, and flags median time to return above 24 h or to core use above 7 d. Nothing else is sent.
