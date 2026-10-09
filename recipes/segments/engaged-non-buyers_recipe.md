---
name: engaged-non-buyers
description: |
  Use when a user mentions "engaged non-buyers", or asks for related help. Highly engaged visitors who have never made a purchase: first-purchase targeting cohort.
arguments: []
intempt:
  id: engaged-non-buyers
  version: 1.0.0
  slashCommand: /engaged-non-buyers
  group: Segments
  title: 'Engaged visitors who never bought'
  shortDescription: 'People who use your site a lot but have never placed an order, so you can aim a first-purchase offer at them.'
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
      title: 'Build the non-buyer list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Known users with 10 or more events, zero orders all time, activity in the last 7 days, and an email on file.'
      prompt: |
        Create a segment called "Engaged Non-Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: Total events >= 10
        - AND Event: Placed order occurred 0 times (all time)
        - AND Attribute: Days since last activity <= 7
        - AND Attribute: email is not empty

        Description: Identified users who engage frequently but have never purchased. First-purchase incentive cohort: typically responds well to a first-order discount or product-discovery campaign.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Engaged visitors who never bought

People who use your site a lot but have never placed an order, so you can aim a first-purchase offer at them.

## What it does

1. **Build the non-buyer list** (`create_segment`)

   Known users with 10 or more events, zero orders all time, activity in the last 7 days, and an email on file.

## What you end up with

- **segment** (segment): Segment created on /segments.
