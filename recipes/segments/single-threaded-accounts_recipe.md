---
name: single-threaded-accounts
description: |
  Use when a user mentions "single-threaded accounts", or asks for related help. Multi-user companies where only 1 user is engaged — multi-threading risk for enterprise SaaS.
arguments: []
intempt:
  id: single-threaded-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Multi-user companies where only 1 user is engaged — multi-threading risk for enterprise SaaS."
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
        Create a segment called "Single-Threaded Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: employees > 50
        - AND Attribute: users_count = 1
        - AND Attribute: has_open_deal = true

        Description: Multi-user-sized companies (50+ employees) where only one user is engaged with our product, AND there's an active deal. Critical multi-threading risk — single-threaded enterprise deals lose at 2-3x the rate of multi-threaded deals. Trigger AE plays to identify and engage 2-3 additional stakeholders before deal close.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Single-Threaded Accounts

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Single-Threaded Accounts".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: employees > 50
   - AND Attribute: users_count = 1
   - AND Attribute: has_open_deal = true

   Description: Multi-user-sized companies (50+ employees) where only one user is engaged with our product, AND there's an active deal. Critical multi-threading risk — single-threaded enterprise deals lose at 2-3x the rate of multi-threaded deals. Trigger AE plays to identify and engage 2-3 additional stakeholders before deal close.
   ```

## Taxonomy notes

- employees, users_count, has_open_deal are canonical Accounts attributes.
- The 50-employee threshold filters to companies large enough that single-stakeholder engagement is genuinely risky (vs. small startups where one decision-maker is normal and expected).
- For larger enterprise focus, raise to employees > 200 or 500.
- The has_open_deal = true filter is the trigger — single-threaded with no deal isn't a risk yet, just a coverage gap. Single-threaded WITH a deal means active risk.
- Tier-1-account variant: layer with intent_level = "High" or score = "High" to focus on the highest-stakes single-threaded deals.
