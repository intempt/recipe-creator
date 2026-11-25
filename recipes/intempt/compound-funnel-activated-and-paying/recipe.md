---
frontmatter_id: compound-funnel-activated-and-paying
slash_command: /compound-funnel-activated-and-paying
description: Builds the segment of users who are both activated and paying, and emails a weekly digest of how many signups
  reach activation, habitual use and a paid subscription, by traffic source.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds an activated-and-paying users segment and emails a weekly digest of signups reaching activation, habitual
    use and a paid subscription, by traffic source.
  parameters:
  - name: conversion_window
    type: duration
    label: Signup window followed
    default: 30 d
    required: false
  - name: habitual_use_count
    type: number
    label: Activation events that count as habitual use
    default: 3
    required: false
  - name: habitual_use_window
    type: duration
    label: Window for habitual use
    default: 7 d
    required: false
  - name: low_step2_to_step4_threshold
    type: number
    label: Activated-to-paying rate flagged as low (%)
    default: 25
    required: false
  - name: low_step4_to_step1_threshold
    type: number
    label: Signup-to-activated-and-paying rate flagged as low (%)
    default: 5
    required: false
  - name: high_step4_conversion_threshold
    type: number
    label: Signup-to-activated-and-paying rate highlighted (%)
    default: 15
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: signup_event
    kind: event
    meaning: A user was created (signed up)
    properties:
    - name: utm_source
      type: string
      meaning: Traffic source of the signup
      optional: false
  - slot: activation_event
    kind: event
    meaning: A user reached activation by using the core feature
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: trial_end
      type: string
      meaning: End of the trial, empty for a paid subscription
      optional: false
  steps:
  - id: s1
    builds: segment
    uses:
    - activation_event
    - subscription_started_event
    - habitual_use_count
    - habitual_use_window
    instruction: Build a new segment of users named "Activated and Paying Users". A user is in it when they did {activation_event}
      at least {habitual_use_count} times in the last {habitual_use_window}, and did {subscription_started_event} with {subscription_started_event.trial_end}
      empty at any time.
  - id: s2
    builds: automation
    uses:
    - s1
    - signup_event
    - activation_event
    - subscription_started_event
    - conversion_window
    - habitual_use_count
    - habitual_use_window
    - low_step2_to_step4_threshold
    - low_step4_to_step1_threshold
    - high_step4_conversion_threshold
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {signup_event}
      in the last {conversion_window} and in the {conversion_window} before, and writes for both windows, overall and per
      {signup_event.utm_source}: signups; activated (did {activation_event}); habitual (did {activation_event} at least {habitual_use_count}
      times within {habitual_use_window}); activated and paying (habitual and did {subscription_started_event} with {subscription_started_event.trial_end}
      empty); activated but not paying; paying but not activated; the users in the segment from "Find activated and paying
      users" now. It flags sources where activated to activated-and-paying is below {low_step2_to_step4_threshold}%, sources
      where signups to activated-and-paying is below {low_step4_to_step1_threshold}%, and highlights sources above {high_step4_conversion_threshold}%.
      Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Activated and paying

Slash command: /compound-funnel-activated-and-paying

## Step 1: Find activated and paying users

Build a new segment of users named "Activated and Paying Users". A user is in it when they did activation event at least 3 times in the last 7 d, and did subscription started event with trial end empty at any time.

## Step 2: Email the weekly activated-and-paying digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did signup event in the last 30 d and in the 30 d before, and writes for both windows, overall and per utm source: signups; activated (did activation event); habitual (did activation event at least 3 times within 7 d); activated and paying (habitual and did subscription started event with trial end empty); activated but not paying; paying but not activated; the users in the segment from "Find activated and paying users" now. It flags sources where activated to activated-and-paying is below 25%, sources where signups to activated-and-paying is below 5%, and highlights sources above 15%. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
