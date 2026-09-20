---
name: repeat-buyers
description: |
  Use when a user mentions "repeat buyers", or asks for related help. Customers who have made 3+ purchases in the last 90 days with meaningful spend.
arguments: []
intempt:
  id: repeat-buyers
  version: 1.0.0
  slashCommand: /repeat-buyers
  group: Segments
  title: 'Repeat buyers'
  shortDescription: 'Customers who have ordered three or more times this quarter and spent real money, the right list for loyalty perks and review requests.'
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
      title: 'Build the repeat-buyer list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with 3 or more orders in the last 90 days and lifetime value of 100 or more.'
      prompt: |
        Create a segment called "Repeat Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred >= 3 times in last 90 days
        - AND Attribute: lifetime_value >= 100

        Description: Repeat customers with meaningful spend. Priority for loyalty rewards, replenishment campaigns, and review requests.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Repeat buyers

Customers who have ordered three or more times this quarter and spent real money, the right list for loyalty perks and review requests.

## What it does

1. **Build the repeat-buyer list** (`create_segment`)

   Users with 3 or more orders in the last 90 days and lifetime value of 100 or more.

## What you end up with

- **segment** (segment): Segment created on /segments.
