---
name: vip-customers-high-ltv
description: |
  Use when a user mentions "vip customers: high lifetime value", or asks for related help. Highest-value customers by lifetime spend. Concrete numeric threshold (no percentile placeholder).
arguments: []
intempt:
  id: vip-customers-high-ltv
  version: 1.0.0
  slashCommand: /vip-customers-high-ltv
  group: Segments
  title: 'VIP customers'
  shortDescription: 'Customers who have spent 1,000 or more across repeat orders, the base list for rewards, early access, and concierge support.'
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
      title: 'Build the VIP list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with lifetime value of 1,000 or more and 2 or more orders.'
      prompt: |
        Create a segment called "VIP Customers".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: lifetime_value >= 1000
        - AND Event: order_created occurred >= 2 times

        Description: High lifetime-value customers with repeat purchase history. Foundation segment for VIP rewards, exclusive product access, and concierge support.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# VIP customers

Customers who have spent 1,000 or more across repeat orders, the base list for rewards, early access, and concierge support.

## What it does

1. **Build the VIP list** (`create_segment`)

   Users with lifetime value of 1,000 or more and 2 or more orders.

## What you end up with

- **segment** (segment): Segment created on /segments.
