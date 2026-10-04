---
id: shopify-churn-risk-discount
title: Discount before a shopper lapses
slash_command: /shopify-churn-risk-discount
group: Workflows
owner: intempt
curator: trishik
summary: Sends a Shopify discount to customers whose buying rhythm has broken, judged against their own
  pattern rather than a fixed number of days.
description: >-
  Apply a Shopify discount to customers a churn signal has flagged, before they lapse rather than after.
version: 2.0.0
classification:
  product:
    - marketing
  agent: revops-automator
  mode:
    - ecommerce
  complexity: advanced
  executionMode: live
  tags:
    - shopify
    - discount
    - retention
prerequisites:
  integrations:
    - value: shopify
      severity: blocking
touches:
  reads:
    - Your Shopify connection
  writes:
    - A new segment, from step 1 "Spot a broken buying rhythm"
    - A new workflow, from step 2 "Apply the code, state the size"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Spot a broken buying rhythm
    summary: >-
      Customers whose gap since the last order is materially longer than their own established rhythm,
      rather than a fixed number of days that treats a monthly buyer and an annual one the same.
    builds: segment
    description: >-
      Create a segment of customers whose purchase cadence has broken: a gap materially longer than their
      own established rhythm, not a fixed number of days that treats a monthly buyer and an annual one
      the same.
  - id: s2
    title: Apply the code, state the size
    summary: >-
      The discount code is applied to each member, and the step states how many people that is before
      it runs, because a discount sent to the wrong segment is money already gone by the time anyone notices.
      Shopify's rejections come back word for word, since an expired code and an already applied code
      need different fixes.
    builds: workflow
    description: >-
      Create a workflow applying the discount code to each member. The step states the blast radius before
      it runs, because a discount applied to the wrong segment is money already gone by the time anyone
      notices. Shopify rejections come back verbatim: an expired code and an already-applied code call
      for different fixes. Use the result of "Spot a broken buying rhythm".
    dependsOn:
      - s1
outputs:
  - key: at_risk
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Discount before a shopper lapses

Sends a Shopify discount to customers whose buying rhythm has broken, judged against their own pattern rather than a fixed number of days.

## Steps

1. **Spot a broken buying rhythm** (builds segment)

   Customers whose gap since the last order is materially longer than their own established rhythm, rather than a fixed number of days that treats a monthly buyer and an annual one the same.

2. **Apply the code, state the size** (builds workflow)

   The discount code is applied to each member, and the step states how many people that is before it runs, because a discount sent to the wrong segment is money already gone by the time anyone notices. Shopify's rejections come back word for word, since an expired code and an already applied code need different fixes.

## What you end up with

- **at_risk** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## What this recipe touches

Reads:

- Your Shopify connection

Writes:

- A new segment, from step 1 "Spot a broken buying rhythm"
- A new workflow, from step 2 "Apply the code, state the size"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
