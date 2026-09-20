---
name: failed-payment-accounts
description: |
  Use when a user mentions "failed-payment users", or asks for related help. Users with payment failure in last 14 days — dunning/recovery cohort.
arguments: []
intempt:
  id: failed-payment-accounts
  version: 1.0.0
  slashCommand: /failed-payment-accounts
  group: Segments
  shortDescription: 'Users with payment failure in last 14 days: dunning/recovery cohort.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas, ecommerce]
    object: users
    complexity: standard
    executionMode: live
    tags: [users-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: stripe, severity: blocking }
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
        Create a segment called "Failed-Payment Users".

        Object: Users

        Rules (any condition matches — joined by OR):
        - Event: payment_failed occurred >= 1 time in last 14 days
        - OR Event: invoice_payment_failed occurred >= 1 time in last 14 days
        - OR Event: billing_failed occurred >= 1 time in last 14 days
        - OR Event: charge_failed occurred >= 1 time in last 14 days

        Description: Users with one or more payment failures in the last 14 days. Dunning-recovery cohort with the highest immediate-revenue ROI of any segment. Trigger an automated card-update email sequence; for high-LTV failures, escalate to manual CSM/AE outreach with a personal touch.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Failed-Payment Users

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Failed-Payment Users".

   Object: Users

   Rules (any condition matches — joined by OR):
   - Event: payment_failed occurred >= 1 time in last 14 days
   - OR Event: invoice_payment_failed occurred >= 1 time in last 14 days
   - OR Event: billing_failed occurred >= 1 time in last 14 days
   - OR Event: charge_failed occurred >= 1 time in last 14 days

   Description: Users with one or more payment failures in the last 14 days. Dunning-recovery cohort with the highest immediate-revenue ROI of any segment. Trigger an automated card-update email sequence; for high-LTV failures, escalate to manual CSM/AE outreach with a personal touch.
   ```

## Taxonomy notes

- payment_failed, invoice_payment_failed, billing_failed, charge_failed are all canonical V2.1 events (Stripe-sourced) with rich properties (amount_cents, decline_code, failure_code, etc.).
- The OR-joined rule structure captures any kind of payment failure — different payment processors and contract types fire different events.
- The 14-day window matches typical dunning retry cadence (Stripe defaults: retry at days 1, 3, 5, 7 after initial fail, then mark as past_due).
- For higher-value escalation, layer with lifetime_value > <threshold> to identify high-LTV failures that warrant manual intervention beyond the standard dunning email sequence.
- Distinct from subscription_cancelled (which is voluntary churn) — failed payments are involuntary churn that's typically recoverable with simple card-update flows.
