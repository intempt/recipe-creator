---
name: vip-customers-high-ltv
description: |
  Use when a user mentions "vip customers — high lifetime value", or asks for related help. Highest-value customers by lifetime spend. Concrete numeric threshold (no percentile placeholder).
arguments: []
intempt:
  id: vip-customers-high-ltv
  version: 1.0.0
  slashCommand: /vip-customers-high-ltv
  group: Segments
  shortDescription: "Highest-value customers by lifetime spend. Concrete numeric threshold (no percentile placeholder)."
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
      title: "Configure Segment Rule"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Open the segment authoring surface, name the segment, and apply the rule below."
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

# VIP Customers — High Lifetime Value

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "VIP Customers".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: lifetime_value >= 1000
   - AND Event: order_created occurred >= 2 times

   Description: High lifetime-value customers with repeat purchase history. Foundation segment for VIP rewards, exclusive product access, and concierge support.
   ```

## Taxonomy notes

- lifetime_value is canonical Users attribute (currency).
- The $1000 threshold is a starting point. Merchants should tune to their P90 customer lifetime-value benchmark — typical 7-figure DTC stores set this between $500 and $5000 depending on AOV.
- Source template proposed "lifetime_value > [top 10% threshold for project]" which is not a real rule (segment rules need concrete numeric values). This recipe substitutes a starter threshold and notes the merchant must adjust to their actual P90.
