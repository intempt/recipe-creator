---
name: high-cart-value-abandoners
description: |
  Use when a user mentions "high-cart-value abandoners", or asks for related help. Cart abandoners with high cart value: priority recovery cohort distinct from frequency-based abandoners.
arguments: []
intempt:
  id: high-cart-value-abandoners
  version: 1.0.0
  slashCommand: /high-cart-value-abandoners
  group: Segments
  title: 'High-value cart abandoners'
  shortDescription: 'People who walked away from an expensive cart in the last week and have not bought since, so you chase the baskets worth chasing.'
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
      title: 'Build the big-cart list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users who abandoned a cart worth 200 or more in the last 7 days and have placed no order in those 7 days.'
      prompt: |
        Create a segment called "High-Cart-Value Abandoners".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: cart_abandoned where total_amount >= 200 occurred >= 1 time in last 7 days
        - AND Event: order_created occurred 0 times in last 7 days

        Description: Cart abandoners whose abandoned cart value is high: priority recovery cohort. Worth more attention (and a potentially higher-effort intervention like a personal email or SMS) than low-cart-value abandoners. Distinct from repeat-cart-abandoners (which targets by frequency, not value).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# High-value cart abandoners

People who walked away from an expensive cart in the last week and have not bought since, so you chase the baskets worth chasing.

## What it does

1. **Build the big-cart list** (`create_segment`)

   Users who abandoned a cart worth 200 or more in the last 7 days and have placed no order in those 7 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
