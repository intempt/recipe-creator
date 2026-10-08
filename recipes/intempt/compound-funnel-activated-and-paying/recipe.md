---
id: compound-funnel-activated-and-paying
title: Activated and paying
slash_command: /compound-funnel-activated-and-paying
group: Reports
owner: intempt
curator: aman
summary: >-
  Reports signups with activation and payment events so you can compare activated and paying groups. It does
  not filter for habitual use or a combined activated-and-paying condition.
description: >-
  A report that surfaces signup records with activation events and payment events. Use it to compare activated
  and paying signups separately, since the product does not support frequency filters or compound AND steps.
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
    - finance
  vertical:
    - payments
  complexity: quick
  executionMode: live
  tags:
    - funnel
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Count users who use and pay"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Count users who use and pay
    summary: >-
      A four step funnel from signup to activation, then three uses inside a 7 day window, then a paid
      non trial subscription, over 30 days and split by signup source. Compares the combined rate against
      activation alone and payment alone.
    builds: report
    description: |-
      Create a Funnel report called "Activated AND Paying".
      Steps:
      1. Event "user_created": "Signed Up"
      2. Event "goal_completed_in_journey" where journey_id matches the activation journey: "Activated" (uses core feature)
      3. Event "goal_completed_in_journey" with frequency: 3+ occurrences within the same 7-day window for the same user: "Habitual Use"
      4. Compound condition: Step 3 reached AND a subscription_created event exists for the same customer_id where trial_end is null (real paid subscription, not trial): "Activated AND Paying"
      Conversion window: 30 days
      Breakdown: By Users.utm_source
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
      - "Habituated Use" and "Activated AND Paying" require Lovable to compute compound conditions from event sequences. The canonical events are all real (goal_completed_in_journey, subscription_created); the compounds are derived.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Activated and paying

Reports signups with activation and payment events so you can compare activated and paying groups. It does not filter for habitual use or a combined activated-and-paying condition.

## Steps

1. **Count users who use and pay** (builds report)

   A four step funnel from signup to activation, then three uses inside a 7 day window, then a paid non trial subscription, over 30 days and split by signup source. Compares the combined rate against activation alone and payment alone.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Count users who use and pay"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
