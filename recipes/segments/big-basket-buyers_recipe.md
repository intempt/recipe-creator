---
name: big-basket-buyers
description: |
  Use when a user mentions "big-basket buyers", or asks for related help. Customers with high average order value: premium-bundle and upsell-targeting cohort.
arguments: []
intempt:
  id: big-basket-buyers
  version: 1.0.0
  slashCommand: /big-basket-buyers
  group: Segments
  title: 'Big basket buyers'
  shortDescription: 'Customers who spend heavily on every single order, so premium bundles and higher tiers go to people who already buy big.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [ecommerce]
    object: users
    complexity: standard
    executionMode: live
    tags: [users-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the big-basket list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Customers with an average order value of 150 or more, 2 or more orders all time, and lifetime value of 300 or more.'
      prompt: |
        Create a segment called "Big-Basket Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: Average order value >= 150
        - AND Event: Placed order occurred >= 2 times (all time)
        - AND Attribute: Lifetime value >= 300

        Description: Customers who buy at higher AOV per order. Distinct from VIPs (which is by lifetime spend). Big-basket buyers may have fewer orders but consistently spend big on each: the right cohort for premium product launches, bundle offers, and "spend more, save more" tier promotions.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Big basket buyers

Customers who spend heavily on every single order, so premium bundles and higher tiers go to people who already buy big.

## What it does

1. **Build the big-basket list** (`create_segment`)

   Customers with an average order value of 150 or more, 2 or more orders all time, and lifetime value of 300 or more.

## What you end up with

- **segment** (segment): Segment created on /segments.
