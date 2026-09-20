---
name: multi-stakeholder-engaged-accounts
description: |
  Use when a user mentions "multi-stakeholder engaged accounts", or asks for related help. Accounts where 3+ users have been active in last 14 days — buying-committee signal for B2B.
arguments: []
intempt:
  id: multi-stakeholder-engaged-accounts
  version: 1.0.0
  slashCommand: /multi-stakeholder-engaged-accounts
  group: Segments
  shortDescription: 'Accounts where 3+ users have been active in last 14 days: buying-committee signal for B2B.'
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
  prerequisites:
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
        Create a segment called "Multi-Stakeholder Engaged Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: users_count >= 3
        - AND Event (across users in account): session_start occurred >= 5 times in last 14 days
        - AND Event (across users in account): page_viewed occurred >= 10 times in last 14 days

        Description: Accounts where 3+ users have been actively engaged in the last 14 days. The buying-committee signal — Salesforce reports B2B deals now involve an average of 11 stakeholders, so multi-user engagement at the account level is one of the strongest forward-looking indicators of an active buying cycle. Foundation for AE multi-threading plays and ABM coordination.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Multi-Stakeholder Engaged Accounts

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Multi-Stakeholder Engaged Accounts".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: users_count >= 3
   - AND Event (across users in account): session_start occurred >= 5 times in last 14 days
   - AND Event (across users in account): page_viewed occurred >= 10 times in last 14 days

   Description: Accounts where 3+ users have been actively engaged in the last 14 days. The buying-committee signal — Salesforce reports B2B deals now involve an average of 11 stakeholders, so multi-user engagement at the account level is one of the strongest forward-looking indicators of an active buying cycle. Foundation for AE multi-threading plays and ABM coordination.
   ```

## Taxonomy notes

- users_count is canonical Accounts attribute.
- session_start, page_viewed are canonical V2.1 events.
- The "across users in account" semantic aggregates events from all Users associated with the Account via primary_account_id or account_ids.
- The 3+ users threshold is a starter — for enterprise-focused merchants, raise to 5+ users (closer to the Salesforce average of 11 stakeholders for true buying-committee detection).
- Distinct from single-threaded-accounts (multi-threading risk segment) and pql-multi-user-account (PQL-specific). This segment captures GENERAL multi-stakeholder engagement, regardless of free/paid plan.
- For higher precision, layer with account_health = "healthy" (filter out at-risk accounts whose multi-user activity is panicked usage rather than expansion intent) or with has_open_deal = true (filter to active deals).
