---
name: shopify-churn-risk-discount
description: Use when a user mentions "churn risk discount", "win back discount shopify", "discount lapsing customers", or asks for related help. Apply a Shopify discount to customers a churn signal has flagged, before they lapse rather than after.
arguments: []
intempt:
  id: shopify-churn-risk-discount
  title: "Discount before a shopper lapses"
  version: 1.0.0
  slashCommand: /shopify-churn-risk-discount
  group: Workflows
  shortDescription: "Sends a Shopify discount to customers whose buying rhythm has broken, judged against their own pattern rather than a fixed number of days."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: revops-automator
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [shopify, discount, retention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
  procedure:
    - step: 1
      title: "Spot a broken buying rhythm"
      command: create_segment
      produces: segment
      bindsAs: at_risk
      description: "Customers whose gap since the last order is materially longer than their own established rhythm, rather than a fixed number of days that treats a monthly buyer and an annual one the same."
      prompt: 'Create a segment of customers whose purchase cadence has broken: a gap materially longer than their own established rhythm, not a fixed number of days that treats a monthly buyer and an annual one the same.'
    - step: 2
      title: "Apply the code, state the size"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - at_risk
      description: "The discount code is applied to each member, and the step states how many people that is before it runs, because a discount sent to the wrong segment is money already gone by the time anyone notices. Shopify's rejections come back word for word, since an expired code and an already applied code need different fixes."
      prompt: 'Create a workflow applying the discount code to each member. The step states the blast radius before it runs, because a discount applied to the wrong segment is money already gone by the time anyone notices. Shopify rejections come back verbatim: an expired code and an already-applied code call for different fixes.'
  outputs:
    - { name: at_risk, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Discount before a shopper lapses

Sends a Shopify discount to customers whose buying rhythm has broken, judged against their own pattern rather than a fixed number of days.

## Before you run it

- Connect shopify

## What it does

1. **Spot a broken buying rhythm** (`create_segment`)

   Customers whose gap since the last order is materially longer than their own established rhythm, rather than a fixed number of days that treats a monthly buyer and an annual one the same.

2. **Apply the code, state the size** (`create_workflow`)

   The discount code is applied to each member, and the step states how many people that is before it runs, because a discount sent to the wrong segment is money already gone by the time anyone notices. Shopify's rejections come back word for word, since an expired code and an already applied code need different fixes.

## What you end up with

- **at_risk** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
