---
name: net-new-prospects
description: |
  Use when a user mentions "net-new prospects", or asks for related help. Recently identified accounts with minimal engagement — SDR first-touch foundation.
arguments: []
intempt:
  id: net-new-prospects
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Create a /segments account segment named 'Net-New Prospects' for accounts created in the last 7 days with ≤5 events, lifecycle prospect, and no open deal."
  availability: available
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
        Create a segment called "Net-New Prospects".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: created_at is within last 7 days
        - AND Attribute: total_events <= 5
        - AND Attribute: account_lifecycle = "prospect"
        - AND Attribute: has_open_deal = false

        Description: Accounts identified in the last 7 days with minimal engagement so far. Foundation for SDR first-touch sequences — these are the freshest entries to your TAL or your inbound feed, deserving immediate qualification within ICP-fit and intent-strength frameworks.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Net-New Prospects

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Net-New Prospects".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: created_at is within last 7 days
   - AND Attribute: total_events <= 5
   - AND Attribute: account_lifecycle = "prospect"
   - AND Attribute: has_open_deal = false

   Description: Accounts identified in the last 7 days with minimal engagement so far. Foundation for SDR first-touch sequences — these are the freshest entries to your TAL or your inbound feed, deserving immediate qualification within ICP-fit and intent-strength frameworks.
   ```

## Taxonomy notes

- created_at is canonical Accounts timestamp.
- total_events is canonical Accounts numeric.
- account_lifecycle and has_open_deal are canonical Accounts attributes.
- The total_events <= 5 filter captures truly net-new — accounts with substantial event volume have already been engaged and belong in active-research or surge cohorts.
- For inbound-routing variant, pair with icp-match-accounts (route net-new ICP-fit to SDR queue) and active-research-surge-accounts (route net-new HIGH-intent directly to AE).
- Refresh frequently — net-new prospects age out of this segment quickly (7-day window is short by design).
