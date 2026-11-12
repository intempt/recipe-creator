---
frontmatter_id: compound-funnel-activated-and-paying
slash_command: /compound-funnel-activated-and-paying
description: Reports signups with activation and payment events so you can compare activated and paying groups. It does not filter for habitual use or a combined activated-and-paying condition.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows how many signed-up users reach activation, sustained use, and a paid subscription, broken down by traffic
    source, to compare activated and paying groups.
  parameters:
  - name: conversion_window
    type: duration
    label: Conversion window
    default: 30 d
    required: false
  - name: comparison_period
    type: duration
    label: Comparison period (prior period)
    default: 30 d
    required: false
  - name: habitual_use_count
    type: number
    label: Minimum journey goal completions for habitual use
    default: 3
    required: false
  - name: habitual_use_window
    type: duration
    label: Habitual use window
    default: 7 d
    required: false
  - name: low_step2_to_step4_threshold
    type: number
    label: Flag threshold for activated-to-paying conversion (%)
    default: 25
    required: false
  - name: low_step4_to_step1_threshold
    type: number
    label: Flag threshold for overall channel quality (%)
    default: 5
    required: false
  - name: high_step4_conversion_threshold
    type: number
    label: Highlight threshold for Step 4 conversion (%)
    default: 15
    required: false
  requirements:
  - slot: signup_event
    kind: event
    meaning: A user was created (signed up)
    properties:
    - name: utm_source
      type: string
      meaning: Traffic source of the user
      optional: true
  - slot: journey_goal_event
    kind: event
    meaning: A user completed a journey goal
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey the goal belongs to
      optional: false
    - name: goal_name
      type: string
      meaning: Name of the goal completed, such as the activation goal or the habitual use goal
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: customer_id
      type: string
      meaning: Identifier of the customer who started the subscription
      optional: false
    - name: trial_end
      type: date
      meaning: Date the trial ends, empty when the subscription is not a trial
      optional: true
  - slot: activation_journey
    kind: event
    meaning: The journey that defines activation by using the core feature
  - slot: utm_source_attribute
    kind: attribute
    meaning: The traffic source (UTM source) recorded on a user
  steps:
  - id: s1
    builds: report
    uses:
    - signup_event
    - journey_goal_event
    - activation_journey
    - subscription_started_event
    - utm_source_attribute
    - conversion_window
    - habitual_use_count
    - habitual_use_window
    - comparison_period
    - low_step2_to_step4_threshold
    - low_step4_to_step1_threshold
    - high_step4_conversion_threshold
    instruction: 'Create a Funnel report called "Activated AND Paying" over {signup_event}, {journey_goal_event} where the
      journey is {activation_journey} and the goal is "Activated", then users who completed {journey_goal_event} at least
      {habitual_use_count} times within {habitual_use_window} for the same user with goal "Habitual Use", then a compound
      step: the habitual use step was reached AND {subscription_started_event} exists for the same {subscription_started_event.customer_id}
      where {subscription_started_event.trial_end} is empty (a real paid subscription, not a trial). Set conversion window
      to {conversion_window}. Break down by {utm_source_attribute}. Compare to the previous {comparison_period}. For each
      step, also show median time-to-convert from the previous step and per-source conversion rate at each stage. Annotate:
      compare the Step 4 conversion rate against each condition alone (Activated alone, Paying alone) to show the activated-but-free
      and paying-but-inactive failure modes; flag any source where Step 2 to Step 4 conversion is below {low_step2_to_step4_threshold}%
      as an activated-to-paying issue; flag any source where Step 4 divided by Step 1 is below {low_step4_to_step1_threshold}%
      as an overall channel-quality issue; highlight sources where Step 4 conversion exceeds {high_step4_conversion_threshold}%.
      Show the activation-to-paywall conversion gap (Activated alone versus Activated AND Paying) as the difference between
      activation and real activation.'
---

# Activated and paying

Slash command: /compound-funnel-activated-and-paying

## Step 1: Count users who use and pay

Create a Funnel report called "Activated AND Paying".
Steps:
1. Event "User created": "Signed Up"
2. Event "Completed a journey goal" where journey_id matches the activation journey: "Activated" (uses core feature)
3. Event "Completed a journey goal" with frequency: 3+ occurrences within the same 7-day window for the same user: "Habitual Use"
4. Compound condition: Step 3 reached AND a Subscription started event exists for the same customer_id where trial_end is null (real paid subscription, not trial): "Activated AND Paying"
Conversion window: 30 days
Breakdown: By Users.UTM source
Compare: Previous period (prior 30 days)
For each step, also surface:
- Median time-to-convert from previous step
- Per-source conversion rate at each stage
Annotations:
- Compare the conversion rate at Step 4 vs. each individual condition alone (Activated alone, Paying alone). The gap reveals how much "activated but free" and "paying but inactive" exist as failure modes.
- Flag any source where Step 2 to Step 4 is below 25% (activated users not converting to paid: pricing or value-perception issue).
- Flag any source where Step 4 / Step 1 is below 5% (overall channel-quality issue).
- Highlight sources where Step 4 conversion exceeds 15%.
The activation-paywall conversion gap (Activated alone vs. Activated AND Paying) is the difference between vanity activation and real activation.
Taxonomy notes:
- "Habituated Use" and "Activated AND Paying" require Lovable to compute compound conditions from event sequences. The canonical events are all real (Completed a journey goal, Subscription started); the compounds are derived.
