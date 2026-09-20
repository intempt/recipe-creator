---
name: replenishment-ready
description: |
  Use when a user mentions "replenishment-ready customers", or asks for related help. Customers approaching their typical re-order cycle. 8-15% conversion on replenishment reminders vs 1-3% on general promos.
arguments: []
intempt:
  id: replenishment-ready
  version: 1.0.0
  slashCommand: /replenishment-ready
  group: Segments
  title: 'Customers due to re-order'
  shortDescription: 'Customers whose last order was one to two months ago and who are about due for another, the moment a running-low reminder lands best.'
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
      title: 'Build the replenishment list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users who have ordered at least once, last ordered 30 to 60 days ago, and have not ordered in the last 30 days.'
      prompt: |
        Create a segment called "Replenishment-Ready".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred >= 1 time (all time)
        - AND Event: order_created occurred 0 times in last 30 days
        - AND Event: order_created occurred >= 1 time between 30 and 60 days ago

        Description: Customers whose last purchase was 30-60 days ago and who are due for re-purchase based on typical consumption cycles. Trigger replenishment reminder ("Running low?") timed to product depletion. Replenishment messaging consistently outperforms generic promotion by 5-10x.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Customers due to re-order

Customers whose last order was one to two months ago and who are about due for another, the moment a running-low reminder lands best.

## What it does

1. **Build the replenishment list** (`create_segment`)

   Users who have ordered at least once, last ordered 30 to 60 days ago, and have not ordered in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
