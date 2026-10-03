---
id: cart-recovery
title: Abandoned cart recovery
slash_command: /cart-recovery
group: Journeys
owner: intempt
summary: Emails shoppers who left items behind, three times over three days, and measures how much revenue
  comes back.
description: >-
  Recover abandoned carts with a 3-touch sequence: segment, content, journey, A/B variants, dashboard,
  alert workflow.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - ecommerce
  complexity: advanced
  executionMode: live
  tags:
    - cart-recovery
steps:
  - id: s1
    title: Find who abandoned a cart
    summary: >-
      Anyone who abandoned a cart in the last 30 days and never placed that order.
    builds: segment
    description: >-
      Identify users with cart_abandoned event in last 30 days who have NOT placed an order for that cart.
  - id: s2
    title: Write the three emails
    summary: >-
      A reminder, then urgency with social proof, then a final notice with an optional discount, all in
      your brand voice.
    builds: email_html
    description: >-
      Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch
      2: urgency + social proof. Touch 3: final reminder optionally with discount. Use the result of "Find
      who abandoned a cart".
    dependsOn:
      - s1
  - id: s3
    title: Schedule the sequence
    summary: >-
      The three emails go out 1 hour, 24 hours and 72 hours after the cart was abandoned.
    builds: journey
    description: >-
      Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at
      1hr, 24hr, and 72hr after abandonment. Use the result of "Find who abandoned a cart", "Write the
      three emails".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Test subject lines and offers
    summary: >-
      A/B variants on the subject lines and on how big an incentive the last email carries.
    builds: experiment
    description: >-
      Add A/B variants on subject lines and incentive levels for the recovery journey. Use the result
      of "Find who abandoned a cart", "Write the three emails", "Schedule the sequence".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Track recovered revenue
    summary: >-
      Recovery rate, revenue recovered, and how long people take to come back.
    builds: dashboard
    description: >-
      Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the
      journey. Use the result of "Find who abandoned a cart", "Write the three emails", "Schedule the
      sequence", "Test subject lines and offers".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: Alert when it stops working
    summary: >-
      The team is told if the recovery rate falls below 15% over any 7 day window.
    builds: workflow
    description: >-
      Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. Use
      the result of "Find who abandoned a cart", "Write the three emails", "Schedule the sequence", "Test
      subject lines and offers", "Track recovered revenue".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
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
  - key: workflow
    producedByStep: s6
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Abandoned cart recovery

Emails shoppers who left items behind, three times over three days, and measures how much revenue comes back.

## Steps

1. **Find who abandoned a cart** (builds segment)

   Anyone who abandoned a cart in the last 30 days and never placed that order.

2. **Write the three emails** (builds email_html)

   A reminder, then urgency with social proof, then a final notice with an optional discount, all in your brand voice.

3. **Schedule the sequence** (builds journey)

   The three emails go out 1 hour, 24 hours and 72 hours after the cart was abandoned.

4. **Test subject lines and offers** (builds experiment)

   A/B variants on the subject lines and on how big an incentive the last email carries.

5. **Track recovered revenue** (builds dashboard)

   Recovery rate, revenue recovered, and how long people take to come back.

6. **Alert when it stops working** (builds workflow)

   The team is told if the recovery rate falls below 15% over any 7 day window.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, experiment, journey, workflow.
