---
name: mid-market-accounts
description: |
  Use when a user mentions "mid-market accounts (100-1000 employees)", or asks for related help. Mid-sized companies (100-1000 employees) — inside-sales / scaled-AE routing.
arguments: []
intempt:
  id: mid-market-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Mid-sized companies (100-1000 employees) — inside-sales / scaled-AE routing."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [b2b, saas]
    object: accounts
    complexity: standard
    executionMode: live
    tags: [accounts-segment]
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
        Create a segment called "Mid-Market Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: employees >= 100
        - AND Attribute: employees < 1000

        Description: Companies with 100-1000 employees. Foundation for inside-sales / scaled-AE routing — these accounts get standardized playbooks, semi-personalized campaigns, and shorter sales cycles than enterprise. Universal B2B routing pattern.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Mid-Market Accounts (100-1000 Employees)

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Mid-Market Accounts".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: employees >= 100
   - AND Attribute: employees < 1000

   Description: Companies with 100-1000 employees. Foundation for inside-sales / scaled-AE routing — these accounts get standardized playbooks, semi-personalized campaigns, and shorter sales cycles than enterprise. Universal B2B routing pattern.
   ```

## Taxonomy notes

- employees is canonical Accounts attribute.
- The 100-1000 range is the canonical mid-market definition. Adjust the lower bound (50, 200) and upper bound (500, 2000) per merchant's segmentation.
- Pair with intent_level (High → priority routing) or account_health (healthy → expansion targeting) for more nuanced mid-market plays.
- This is one of three account-size segments (alongside enterprise-accounts and smb-accounts) that together form the universal B2B sales-motion-routing foundation.
