---
name: recently-churned-users
description: |
  Use when a user mentions "recently churned users (30 days)", or asks for related help. Users who cancelled their subscription in the last 30 days: fast win-back cohort.
arguments: []
intempt:
  id: recently-churned-users
  version: 1.0.0
  slashCommand: /recently-churned-users
  group: Segments
  title: 'Recently cancelled customers'
  shortDescription: 'Customers who cancelled in the last month, while the reason is fresh and a win-back still has a chance.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas]
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
      title: 'Build the recent-cancel list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with a subscription cancellation in the last 30 days and lifetime value above zero.'
      prompt: |
        Create a segment called "Recently Churned Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: subscription_cancelled occurred >= 1 time in last 30 days
        - AND Attribute: lifetime_value > 0

        Description: Users who cancelled in the last 30 days with prior paid history. Fast win-back cohort: easier to recover than older churned users while feedback is still fresh.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Recently cancelled customers

Customers who cancelled in the last month, while the reason is fresh and a win-back still has a chance.

## What it does

1. **Build the recent-cancel list** (`create_segment`)

   Users with a subscription cancellation in the last 30 days and lifetime value above zero.

## What you end up with

- **segment** (segment): Segment created on /segments.
