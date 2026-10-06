---
id: win-back
title: Lapsed customer win back
slash_command: /win-back
group: Journeys
owner: intempt
curator: somya
summary: Sorts lapsed customers by how long they have been gone and escalates the offer with the gap,
  from a gentle nudge to an exclusive deal.
description: >-
  Tiered re-engagement for lapsed users: segment by recency, content per tier, journey, retention measurement.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - all
  industry:
    - ai
    - b2b-saas
    - ecommerce
    - finance
    - media
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - win-back
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new segment, from step 1 "Sort lapsed users by the gap"
    - A new designed email, from step 2 "Write content per tier"
    - A new journey, from step 3 "Escalate the offer by tier"
    - A new report, from step 4 "Measure who comes back"
    - A new A/B experiment, from step 5 "Test what brings them back"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Sort lapsed users by the gap
    summary: >-
      Three tiers: inactive 30 to 60 days, 60 to 120 days, and 120 days or more.
    builds: segment
    description: >-
      Segment lapsed users into tiers: 30-60 days inactive, 60-120 days inactive, 120+ days inactive.
  - id: s2
    title: Write content per tier
    summary: >-
      Gentle for the recently lapsed, a reminder of the value for the middle tier, and an exclusive offer
      for the long gone.
    builds: email_html
    description: >-
      Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive
      offer for deep-lapsed. Use the result of "Sort lapsed users by the gap".
    dependsOn:
      - s1
  - id: s3
    title: Escalate the offer by tier
    summary: >-
      One journey with an arm per tier, each with its own touches and a bigger incentive the longer they
      have been away.
    builds: journey
    description: >-
      Build a multi-arm journey routing each tier through appropriate touches with escalating incentives.
      Use the result of "Sort lapsed users by the gap", "Write content per tier".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Measure who comes back
    summary: >-
      Re-engagement rate per tier over the 90 days after the journey.
    builds: report
    description: >-
      Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey.
      Use the result of "Sort lapsed users by the gap", "Write content per tier", "Escalate the offer
      by tier".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Test what brings them back
    summary: >-
      A/B variants on the incentive: a discount, a free gift, or no incentive at all.
    builds: experiment
    description: >-
      Add A/B variants on incentive type (discount vs free gift vs value-only). Use the result of "Sort
      lapsed users by the gap", "Write content per tier", "Escalate the offer by tier", "Measure who comes
      back".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
  - key: report
    producedByStep: s4
    type: report
    description: Report produced by this recipe.
  - key: experiment
    producedByStep: s5
    type: experiment
    description: Experiment produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Lapsed customer win back

Sorts lapsed customers by how long they have been gone and escalates the offer with the gap, from a gentle nudge to an exclusive deal.

## Steps

1. **Sort lapsed users by the gap** (builds segment)

   Three tiers: inactive 30 to 60 days, 60 to 120 days, and 120 days or more.

2. **Write content per tier** (builds email_html)

   Gentle for the recently lapsed, a reminder of the value for the middle tier, and an exclusive offer for the long gone.

3. **Escalate the offer by tier** (builds journey)

   One journey with an arm per tier, each with its own touches and a bigger incentive the longer they have been away.

4. **Measure who comes back** (builds report)

   Re-engagement rate per tier over the 90 days after the journey.

5. **Test what brings them back** (builds experiment)

   A/B variants on the incentive: a discount, a free gift, or no incentive at all.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new segment, from step 1 "Sort lapsed users by the gap"
- A new designed email, from step 2 "Write content per tier"
- A new journey, from step 3 "Escalate the offer by tier"
- A new report, from step 4 "Measure who comes back"
- A new A/B experiment, from step 5 "Test what brings them back"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build experiment, journey, report.
