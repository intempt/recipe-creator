---
name: second-purchase-window
description: |
  Use when a user mentions "second-purchase window", or asks for related help. First-time buyers in the critical 1-30 day window after their first order. 50% of all repeat purchases happen here.
arguments: []
intempt:
  id: second-purchase-window
  version: 1.0.0
  slashCommand: /second-purchase-window
  group: Segments
  title: 'First-time buyers in the repeat window'
  shortDescription: 'Customers who bought for the first time in the last month, the period when most second purchases happen.'
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
      title: 'Build the second-purchase list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with exactly 1 order all time, placed within the last 30 days.'
      prompt: |
        Create a segment called "Second-Purchase Window".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred = 1 time (all time)
        - AND Event: order_created occurred >= 1 time in last 30 days

        Description: Customers who just bought for the first time and are in the highest-conversion repurchase window. 50.3% of all repeat purchases happen in the first 30 days post-purchase, yet most brands suppress recent buyers from campaigns. This segment fixes that by giving you a clean cohort to target with personalized cross-sells, "complete-the-set" offers, and second-purchase nudges (not discount blasts: handwritten-style notes outperform).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# First-time buyers in the repeat window

Customers who bought for the first time in the last month, the period when most second purchases happen.

## What it does

1. **Build the second-purchase list** (`create_segment`)

   Users with exactly 1 order all time, placed within the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
