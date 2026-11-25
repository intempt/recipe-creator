---
frontmatter_id: activation-funnel-with-velocity
slash_command: /activation-funnel-with-velocity
description: Builds a segment of new users stalled before setup and emails a weekly digest of where new users drop out across
  onboarding steps and how long each step takes.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of where new users drop out across onboarding steps and how long each takes, and builds
    a segment of new users stuck before setup.
  parameters:
  - name: conversion_window
    type: duration
    label: Signup window followed
    default: 14 d
    required: false
  - name: first_return_window
    type: duration
    label: Window for the first return
    default: 24 h
    required: false
  - name: habituation_goal_count
    type: number
    label: Activation events that count as habit
    default: 3
    required: false
  - name: habituation_window
    type: duration
    label: Window for those activation events
    default: 7 d
    required: false
  - name: stall_after
    type: duration
    label: Time after signup without setup that counts as stalled
    default: 72 h
    required: false
  - name: p75_flag_threshold
    type: duration
    label: Slow step flag (75th percentile time)
    default: 7 d
    required: false
  - name: stall_rate_flag_threshold
    type: number
    label: Stall rate that flags a step (%)
    default: 60
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: signup_event
    kind: event
    meaning: A new user account was created
  - slot: session_event
    kind: event
    meaning: A user started a session in the product
  - slot: setup_completed_event
    kind: event
    meaning: A user completed onboarding setup
  - slot: core_feature_event
    kind: event
    meaning: A user used the product's core feature
  - slot: activation_event
    kind: event
    meaning: A user reached the product's activation milestone
  - slot: utm_source_attribute
    kind: attribute
    meaning: The UTM source the user came from
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - signup_event
    - setup_completed_event
    - conversion_window
    - stall_after
    instruction: Build a new segment of users named "Stalled New Users". A user is in it when they did {signup_event} in the
      last {conversion_window} and more than {stall_after} ago, and did not do {setup_completed_event} at any time.
  - id: s2
    builds: automation
    uses:
    - s1
    - signup_event
    - session_event
    - setup_completed_event
    - core_feature_event
    - activation_event
    - utm_source_attribute
    - conversion_window
    - first_return_window
    - habituation_goal_count
    - habituation_window
    - stall_after
    - p75_flag_threshold
    - stall_rate_flag_threshold
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {signup_event}
      in the last {conversion_window} and in the {conversion_window} before, through these steps in order: signed up; did
      {session_event} within {first_return_window} of signup; did {setup_completed_event}; did {core_feature_event}; did {activation_event}
      at least {habituation_goal_count} times within {habituation_window} after their first {core_feature_event}. It writes
      these figures for both windows: users at each step and conversion % from the step before; median and 75th percentile
      time from the step before; % of users at each step not advanced after {stall_after}; final conversion split by {utm_source_attribute};
      users in the segment from "Find new users stalled before setup". The first line names any step whose 75th percentile
      time is over {p75_flag_threshold} or whose stall % is above {stall_rate_flag_threshold}%. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Activation funnel with velocity

Slash command: /activation-funnel-with-velocity

## Step 1: Find new users stalled before setup

Build a new segment of users named "Stalled New Users". A user is in it when they did signup event in the last 14 d and more than 72 h ago, and did not do setup completed event at any time.

## Step 2: Email the weekly activation digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did signup event in the last 14 d and in the 14 d before, through these steps in order: signed up; did session event within 24 h of signup; did setup completed event; did core feature event; did activation event at least 3 times within 7 d after their first core feature event. It writes these figures for both windows: users at each step and conversion % from the step before; median and 75th percentile time from the step before; % of users at each step not advanced after 72 h; final conversion split by utm source attribute; users in the segment from "Find new users stalled before setup". The first line names any step whose 75th percentile time is over 7 d or whose stall % is above 60%. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
