---
name: repeat-cart-abandoners
description: |
  Use when a user mentions "repeat cart abandoners", or asks for related help. Users who have abandoned checkout 2+ times in the last 30 days without purchasing.
arguments: []
intempt:
  id: repeat-cart-abandoners
  version: 1.0.0
  slashCommand: /repeat-cart-abandoners
  group: Segments
  title: 'Repeat cart abandoners'
  shortDescription: 'People who have walked away from checkout twice or more this month without buying, usually a sign of friction or price resistance.'
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
      title: 'Build the repeat-abandoner list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users who abandoned checkout 2 or more times in the last 30 days and placed no order in that period.'
      prompt: |
        Create a segment called "Repeat Cart Abandoners".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: Abandoned checkout occurred >= 2 times in last 30 days
        - AND Event: Placed order occurred 0 times in last 30 days

        Description: Users who repeatedly abandon checkout: likely friction or price sensitivity. Trigger differentiated recovery offers (different from first-time abandoners).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Repeat cart abandoners

People who have walked away from checkout twice or more this month without buying, usually a sign of friction or price resistance.

## What it does

1. **Build the repeat-abandoner list** (`create_segment`)

   Users who abandoned checkout 2 or more times in the last 30 days and placed no order in that period.

## What you end up with

- **segment** (segment): Segment created on /segments.
