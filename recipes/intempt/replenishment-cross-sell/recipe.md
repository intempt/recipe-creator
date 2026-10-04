---
id: replenishment-cross-sell
title: Replenishment and cross sell
slash_command: /replenishment-cross-sell
group: Journeys
owner: intempt
curator: somya
summary: Reminds people to reorder before they run out, at the pace they actually get through it, and
  suggests what pairs with it.
description: >-
  Reorder reminders for consumable products + cross-sell complementary items + referral nudges.
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
    - replenishment-cross-sell
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new segment, from step 1 "Work out when they run out"
    - A new designed email, from step 2 "Write the reorder reminder"
    - A new journey, from step 3 "Remind before they run dry"
    - A new product recommendation, from step 4 "Pick what pairs with it"
    - A new A/B experiment, from step 5 "Test when to cross sell"
    - A new dashboard, from step 6 "Track reorders and attach rate"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Work out when they run out
    summary: >-
      Shoppers coming up on their usual reorder window, worked out from what they have bought before.
    builds: segment
    description: >-
      Identify users approaching their typical reorder window for consumable products based on purchase
      history.
  - id: s2
    title: Write the reorder reminder
    summary: >-
      An email timed to their own consumption pattern, with a one click reorder link.
    builds: email_html
    description: >-
      Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder
      link. Use the result of "Work out when they run out".
    dependsOn:
      - s1
  - id: s3
    title: Remind before they run dry
    summary: >-
      Reminders sent at intervals ahead of the point they run out.
    builds: journey
    description: >-
      Build a journey sending reorder reminders at appropriate intervals before depletion. Use the result
      of "Work out when they run out", "Write the reorder reminder".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Pick what pairs with it
    summary: >-
      Cross sell recommendations built from what that customer has bought before.
    builds: recommendation
    description: >-
      Generate cross-sell recommendations for complementary products based on the customer's purchase
      history. Use the result of "Work out when they run out", "Write the reorder reminder", "Remind before
      they run dry".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Test when to cross sell
    summary: >-
      A/B variants putting the cross sell inside the reorder email or in a separate one.
    builds: experiment
    description: >-
      Add A/B variants on cross-sell timing (with-reorder vs separate-touch). Use the result of "Work
      out when they run out", "Write the reorder reminder", "Remind before they run dry", "Pick what pairs
      with it".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: Track reorders and attach rate
    summary: >-
      How many people reorder, how often the cross sell attaches, and the 12 month value of repeat buyers.
    builds: dashboard
    description: >-
      Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase
      value. Use the result of "Work out when they run out", "Write the reorder reminder", "Remind before
      they run dry", "Pick what pairs with it", "Test when to cross sell".
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
  - key: recommendation
    producedByStep: s4
    type: recommendation
    description: Recommendation produced by this recipe.
  - key: experiment
    producedByStep: s5
    type: experiment
    description: Experiment produced by this recipe.
  - key: dashboard
    producedByStep: s6
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Replenishment and cross sell

Reminds people to reorder before they run out, at the pace they actually get through it, and suggests what pairs with it.

## Steps

1. **Work out when they run out** (builds segment)

   Shoppers coming up on their usual reorder window, worked out from what they have bought before.

2. **Write the reorder reminder** (builds email_html)

   An email timed to their own consumption pattern, with a one click reorder link.

3. **Remind before they run dry** (builds journey)

   Reminders sent at intervals ahead of the point they run out.

4. **Pick what pairs with it** (builds recommendation)

   Cross sell recommendations built from what that customer has bought before.

5. **Test when to cross sell** (builds experiment)

   A/B variants putting the cross sell inside the reorder email or in a separate one.

6. **Track reorders and attach rate** (builds dashboard)

   How many people reorder, how often the cross sell attaches, and the 12 month value of repeat buyers.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new segment, from step 1 "Work out when they run out"
- A new designed email, from step 2 "Write the reorder reminder"
- A new journey, from step 3 "Remind before they run dry"
- A new product recommendation, from step 4 "Pick what pairs with it"
- A new A/B experiment, from step 5 "Test when to cross sell"
- A new dashboard, from step 6 "Track reorders and attach rate"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, experiment, journey, recommendation.
