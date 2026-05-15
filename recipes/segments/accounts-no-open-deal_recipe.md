---
name: accounts-no-open-deal
description: |
  Use when a user mentions "accounts with no open deal", or asks for related help. Healthy customer accounts with no current open deal — whitespace expansion opportunity.
arguments: []
intempt:
  id: accounts-no-open-deal
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Healthy customer accounts with no current open deal — whitespace expansion opportunity."
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
        Create a segment called "Accounts With No Open Deal".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: has_open_deal = false
        - AND Attribute: account_health = "healthy"
        - AND Attribute: users_count >= 3
        - AND Event: session_start (across users in account) occurred >= 5 times in last 30 days

        Description: Healthy active accounts with no open deal — ready for expansion conversation. Trigger AE whitespace task or executive outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Accounts With No Open Deal

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Accounts With No Open Deal".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: has_open_deal = false
   - AND Attribute: account_health = "healthy"
   - AND Attribute: users_count >= 3
   - AND Event: session_start (across users in account) occurred >= 5 times in last 30 days

   Description: Healthy active accounts with no open deal — ready for expansion conversation. Trigger AE whitespace task or executive outreach.
   ```

## Taxonomy notes

- has_open_deal is canonical Accounts attribute (boolean).
- account_health is canonical Accounts attribute (enum: healthy | at_risk | churning per V2.1 — no numeric account_health_score variant).
- users_count is canonical Accounts attribute.
- session_start is canonical event (replaces source template's "user_active" which is not a canonical event).
- For the "across users in account" semantic to evaluate correctly, the event aggregation rolls up session_start events from all Users associated with the Account via primary_account_id or account_ids.
