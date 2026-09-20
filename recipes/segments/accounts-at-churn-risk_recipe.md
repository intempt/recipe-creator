---
name: accounts-at-churn-risk
description: |
  Use when a user mentions "accounts at churn risk", or asks for related help. Active accounts showing health deterioration — CSM intervention needed.
arguments: []
intempt:
  id: accounts-at-churn-risk
  version: 1.0.1
  slashCommand: /accounts-at-churn-risk
  group: Segments
  shortDescription: 'Active accounts showing health deterioration: CSM intervention needed.'
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
        Create a segment called "Accounts At Churn Risk".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: account_health = "at_risk"
        - AND Attribute: has_renewal_deal = false
        - AND Attribute: account_lifetime_value > 0
        - AND Attribute: users_count >= 1

        Description: Active accounts flagged at-risk by the platform's health-scoring with positive lifetime value (proven paid customer) and no active renewal deal in flight. CSM intervention priority — these are recoverable churn risks where someone has paid before and isn't currently in renewal motion.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Accounts At Churn Risk

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Accounts At Churn Risk".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: account_health = "at_risk"
   - AND Attribute: has_renewal_deal = false
   - AND Attribute: account_lifetime_value > 0
   - AND Attribute: users_count >= 1

   Description: Active accounts flagged at-risk by the platform's health-scoring with positive lifetime value (proven paid customer) and no active renewal deal in flight. CSM intervention priority — these are recoverable churn risks where someone has paid before and isn't currently in renewal motion.
   ```

## Taxonomy notes

- account_health is canonical Accounts attribute (string enum: healthy | at_risk | churning). Per scoring constraint, this uses the enum bucket — never the numeric account_health_score variant.
- has_renewal_deal is canonical Accounts boolean (V2.1). The has_renewal_deal = false filter ensures the segment captures accounts where no renewal motion is currently active (vs. accounts where the renewal is already in flight under AE/CSM ownership).
- account_lifetime_value is canonical Accounts numeric — the account-level aggregate of paid revenue. The "> 0" filter excludes never-paid accounts (those are different cohorts — typically prospects or evaluators).
- users_count >= 1 confirms there's at least one user to intervene with (accounts with no users are stale CRM records, not churn-risk targets).
- Distinct from accounts-no-open-deal (whitespace expansion target) — at-risk accounts need defensive intervention, not expansion plays.
- For more nuanced renewal targeting, pair with renewal-window-90-day on the Users side to get the intersection of (account at risk) AND (subscription renewing soon).
