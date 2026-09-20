---
name: high-frequency-buyers
description: |
  Use when a user mentions "high-frequency buyers", or asks for related help. Customers who purchase 4+ times per quarter: most loyal cohort.
arguments: []
intempt:
  id: high-frequency-buyers
  version: 1.0.0
  slashCommand: /high-frequency-buyers
  group: Segments
  title: 'High-frequency buyers'
  shortDescription: 'Customers who order at least four times a quarter, so loyalty perks and early access go to the people who buy most often.'
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
      title: 'Build the frequent-buyer list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with 4 or more orders in the last 90 days.'
      prompt: |
        Create a segment called "High-Frequency Buyers".

        Object: Users

        Rules:
        - Event: order_created occurred >= 4 times in last 90 days

        Description: High-frequency buyers: the most loyal cohort. Priority for loyalty program enrollment, early access, and brand-ambassador outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# High-frequency buyers

Customers who order at least four times a quarter, so loyalty perks and early access go to the people who buy most often.

## What it does

1. **Build the frequent-buyer list** (`create_segment`)

   Users with 4 or more orders in the last 90 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
