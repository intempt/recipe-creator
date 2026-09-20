---
name: winnable-churned-users
description: |
  Use when a user mentions "winnable churned users", or asks for related help. Recently churned users who showed engagement before churn: best win-back candidates.
arguments: []
intempt:
  id: winnable-churned-users
  version: 1.0.0
  slashCommand: /winnable-churned-users
  group: Segments
  title: 'Winnable churned users'
  shortDescription: 'People who cancelled in the last two months but used the product heavily before they left, the best odds for a win-back.'
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
      title: 'Build the win-back list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with a subscription cancellation in the last 60 days, lifetime value above zero, and 50 or more events on record.'
      prompt: |
        Create a segment called "Winnable Churned Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: subscription_cancelled occurred >= 1 time in last 60 days
        - AND Attribute: lifetime_value > 0
        - AND Attribute: total_events >= 50

        Description: Recently churned users with prior engagement (positive lifetime value, meaningful event volume during their active period). Best candidates for a win-back offer.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Winnable churned users

People who cancelled in the last two months but used the product heavily before they left, the best odds for a win-back.

## What it does

1. **Build the win-back list** (`create_segment`)

   Users with a subscription cancellation in the last 60 days, lifetime value above zero, and 50 or more events on record.

## What you end up with

- **segment** (segment): Segment created on /segments.
