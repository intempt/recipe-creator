---
id: welcome-series
title: Welcome series
slash_command: /welcome-series
group: Journeys
owner: intempt
summary: Introduces your brand to new subscribers over their first week in four emails, and tests the
  subject lines and the opening offer.
description: >-
  First-touch sequence for new subscribers: segment, content, journey, A/B variants, performance dashboard.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - all
  complexity: advanced
  executionMode: live
  tags:
    - welcome-series
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new segment, from step 1 "Find new subscribers"
    - A new designed email, from step 2 "Write the four emails"
    - A new journey, from step 3 "Send across the first week"
    - A new A/B experiment, from step 4 "Test subject lines and offer"
    - A new dashboard, from step 5 "Track the first purchase"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find new subscribers
    summary: >-
      Anyone who subscribed in the last 30 days and has not had a welcome email yet.
    builds: segment
    description: >-
      Identify users who subscribed within the last 30 days and have not received a welcome email yet.
  - id: s2
    title: Write the four emails
    summary: >-
      A sequence introducing the brand, the product and what it is for, in your brand voice.
    builds: email_html
    description: >-
      Generate a 4-email welcome sequence introducing the brand, product, and value props using brand
      voice. Use the result of "Find new subscribers".
    dependsOn:
      - s1
  - id: s3
    title: Send across the first week
    summary: >-
      The four emails go out straight away, then after a day, after three days, and after a week.
    builds: journey
    description: >-
      Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription.
      Use the result of "Find new subscribers", "Write the four emails".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Test subject lines and offer
    summary: >-
      A/B variants on the subject lines and on whether the welcome offer appears at all.
    builds: experiment
    description: >-
      Add A/B variants on subject lines and welcome offer presence. Use the result of "Find new subscribers",
      "Write the four emails", "Send across the first week".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Track the first purchase
    summary: >-
      Opens, clicks, conversion, and how long a new subscriber takes to buy.
    builds: dashboard
    description: >-
      Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase
      from the welcome journey. Use the result of "Find new subscribers", "Write the four emails", "Send
      across the first week", "Test subject lines and offer".
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
  - key: experiment
    producedByStep: s4
    type: experiment
    description: Experiment produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Welcome series

Introduces your brand to new subscribers over their first week in four emails, and tests the subject lines and the opening offer.

## Steps

1. **Find new subscribers** (builds segment)

   Anyone who subscribed in the last 30 days and has not had a welcome email yet.

2. **Write the four emails** (builds email_html)

   A sequence introducing the brand, the product and what it is for, in your brand voice.

3. **Send across the first week** (builds journey)

   The four emails go out straight away, then after a day, after three days, and after a week.

4. **Test subject lines and offer** (builds experiment)

   A/B variants on the subject lines and on whether the welcome offer appears at all.

5. **Track the first purchase** (builds dashboard)

   Opens, clicks, conversion, and how long a new subscriber takes to buy.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new segment, from step 1 "Find new subscribers"
- A new designed email, from step 2 "Write the four emails"
- A new journey, from step 3 "Send across the first week"
- A new A/B experiment, from step 4 "Test subject lines and offer"
- A new dashboard, from step 5 "Track the first purchase"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, experiment, journey.
