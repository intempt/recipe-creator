---
name: multi-product-buyers
description: |
  Use when a user mentions "multi-product buyers", or asks for related help. Customers who have purchased across multiple distinct products: cross-sell-ready cohort.
arguments: []
intempt:
  id: multi-product-buyers
  version: 1.0.0
  slashCommand: /multi-product-buyers
  group: Segments
  title: 'Multi-product buyers'
  shortDescription: 'Customers who have bought more than once and spent a meaningful amount, so cross-sell offers reach people with broad interest.'
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
      title: 'Build the repeat-spend list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with 2 or more orders in the last 180 days and lifetime value of 200 or more.'
      prompt: |
        Create a segment called "Multi-Product Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred >= 2 times in last 180 days
        - AND Attribute: lifetime_value >= 200

        Description: Customers with multiple orders and meaningful spend. Cross-sell-ready cohort: broader product affinity than single-category buyers.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Multi-product buyers

Customers who have bought more than once and spent a meaningful amount, so cross-sell offers reach people with broad interest.

## What it does

1. **Build the repeat-spend list** (`create_segment`)

   Users with 2 or more orders in the last 180 days and lifetime value of 200 or more.

## What you end up with

- **segment** (segment): Segment created on /segments.
