---
name: one-time-buyers-at-risk
description: |
  Use when a user mentions "one-time buyers at risk", or asks for related help. Customers who made one purchase but have not returned in 60+ days.
arguments: []
intempt:
  id: one-time-buyers-at-risk
  version: 1.0.0
  slashCommand: /one-time-buyers-at-risk
  group: Segments
  title: 'One-time buyers going cold'
  shortDescription: 'Customers who bought once, have not been back in two months, and are not trending well, so you can give them a reason to return.'
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
      title: 'Build the one-time-buyer list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with exactly 1 order all time, no activity for 60 days or more, and a lifecycle score other than Regulars or Promising.'
      prompt: |
        Create a segment called "One-Time Buyers At Risk".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred = 1 time (all time)
        - AND Attribute: days_since_last_activity >= 60
        - AND Attribute: lifecycle_score is not in ["Regulars", "Promising"]

        Description: Single-purchase customers who haven't returned in over 60 days and aren't on a healthy lifecycle trajectory. Re-engagement opportunity: second-purchase incentive recommended.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# One-time buyers going cold

Customers who bought once, have not been back in two months, and are not trending well, so you can give them a reason to return.

## What it does

1. **Build the one-time-buyer list** (`create_segment`)

   Users with exactly 1 order all time, no activity for 60 days or more, and a lifecycle score other than Regulars or Promising.

## What you end up with

- **segment** (segment): Segment created on /segments.
