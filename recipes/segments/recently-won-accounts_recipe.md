---
name: recently-won-accounts
description: |
  Use when a user mentions "recently-won accounts", or asks for related help. Accounts that closed a deal in last 90 days — onboarding cohort distinct from new-paying-customers.
arguments: []
intempt:
  id: recently-won-accounts
  version: 1.0.0
  slashCommand: /recently-won-accounts
  group: Segments
  shortDescription: 'Accounts that closed a deal in last 90 days: onboarding cohort distinct from new-paying-customers.'
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
        Create a segment called "Recently-Won Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: lifecycle_changed_at is within last 90 days
        - AND Attribute: account_lifecycle is "customer"
        - AND Attribute: has_open_deal = false

        Description: Accounts that became customers in the last 90 days — the post-deal-close onboarding cohort. Distinct from new-paying-customers (which is plan-tier-conversion at the User level). For B2B sales motion, the deal-close moment is the kickoff for CSM onboarding, implementation milestones, and time-to-value tracking.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Recently-Won Accounts

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Recently-Won Accounts".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: lifecycle_changed_at is within last 90 days
   - AND Attribute: account_lifecycle is "customer"
   - AND Attribute: has_open_deal = false

   Description: Accounts that became customers in the last 90 days — the post-deal-close onboarding cohort. Distinct from new-paying-customers (which is plan-tier-conversion at the User level). For B2B sales motion, the deal-close moment is the kickoff for CSM onboarding, implementation milestones, and time-to-value tracking.
   ```

## Taxonomy notes

- lifecycle_changed_at is canonical Accounts timestamp.
- account_lifecycle is canonical Accounts attribute (lifecycle stage enum).
- has_open_deal = false confirms no active deal still in flight (just-closed accounts have no NEW open deals).
- The 90-day window aligns with typical B2B onboarding cycles — implementation, integration, first business value. Adjust to your time-to-value: 30 days for fast PLG, 180 days for complex enterprise deployments.
- This segment intentionally does NOT use deal-stage signals (Deals are a separate object outside this bundle's scope). Lifecycle-stage transition is the V2.1-supported equivalent for "recently became a customer.
