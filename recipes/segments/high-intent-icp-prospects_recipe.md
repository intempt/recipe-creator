---
name: high-intent-icp-prospects
description: |
  Use when a user mentions "high-intent icp prospects", or asks for related help. ICP-matching accounts with active intent signals (pricing + docs visited recently).
arguments: []
intempt:
  id: high-intent-icp-prospects
  version: 1.0.0
  slashCommand: /high-intent-icp-prospects
  group: Segments
  shortDescription: "ICP-matching accounts with active intent signals (pricing + docs visited recently)."
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
        Create a segment called "High-Intent ICP Prospects".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: employees is between 50 and 1000
        - AND Attribute: industry is one of ["SaaS", "Technology", "Fintech", "Financial Services"]
        - AND Event (via users in account): page_viewed where page_url contains "/pricing" occurred >= 1 time in last 7 days
        - AND Event (via users in account): page_viewed where page_url contains "/docs" occurred >= 1 time in last 7 days
        - AND Attribute: has_open_deal = false

        Description: ICP-matching accounts with hot buying signals this week. Highest-priority cohort for SDR outreach — pre-qualified and actively researching.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# High-Intent ICP Prospects

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "High-Intent ICP Prospects".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: employees is between 50 and 1000
   - AND Attribute: industry is one of ["SaaS", "Technology", "Fintech", "Financial Services"]
   - AND Event (via users in account): page_viewed where page_url contains "/pricing" occurred >= 1 time in last 7 days
   - AND Event (via users in account): page_viewed where page_url contains "/docs" occurred >= 1 time in last 7 days
   - AND Attribute: has_open_deal = false

   Description: ICP-matching accounts with hot buying signals this week. Highest-priority cohort for SDR outreach — pre-qualified and actively researching.
   ```

## Taxonomy notes

- employees, industry are canonical Accounts attributes (replaces source template's "employee_count" with the canonical attribute name).
- page_viewed.page_url is the canonical event property (replaces source template's "page" property name).
- has_open_deal is canonical.
- The "via users in account" semantic aggregates page_viewed events from all Users associated with the Account.
- This segment compounds with ICP Match Accounts to produce hot prospects — but the intent component (recent pricing+docs visits) makes it actionable on a daily cadence rather than the broader ICP segment.
