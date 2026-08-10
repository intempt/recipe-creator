---
name: mrr-movement-decomposition
description: |
  Use when a user mentions "mrr movement decomposition", or asks for related help. The canonical SaaS MRR waterfall — new, expansion, contraction, churn, reactivation per month. Requires subscription_updated delta-computation.
arguments: []
intempt:
  id: mrr-movement-decomposition
  version: 1.0.0
  slashCommand: /mrr-movement-decomposition
  group: Reports
  shortDescription: "The canonical SaaS MRR waterfall — new, expansion, contraction, churn, reactivation per month. Requires subscription_updated delta-computation."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: hubspot, severity: blocking }
      - { value: shopify, severity: blocking }
      - { value: stripe, severity: blocking }
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "MRR Movement Decomposition".

        This is the canonical SaaS MRR waterfall. Compute the five movement categories per month:

        New MRR: Sum of subscription_created.amount in the period for users who had no active subscription previously, unit: $
        Expansion MRR: From subscription_updated events — for each event, compute (new amount − prior subscription amount on the same subscription_id). Sum the positive deltas where changed_fields indicates plan upgrade or seat/quantity increase, unit: $
        Contraction MRR: Same subscription_updated computation; sum the negative deltas (will appear as negative values in the waterfall), unit: $
        Churned MRR: Sum of the prior subscription amount for each subscription_cancelled event in the period (negative in the waterfall), unit: $
        Reactivation MRR: Sum of subscription_resumed.amount where the user previously had a subscription_cancelled in the prior 90 days, unit: $

        Net New MRR: New + Expansion + Contraction (negative) + Churned (negative) + Reactivation
        Net Revenue Retention (NRR): (Starting MRR + Expansion + Reactivation − Contraction − Churn) / Starting MRR × 100, unit: %

        Time granularity: Monthly
        Time range: Last 12 months
        Compare: Year-over-year
        Chart type: Waterfall chart per month (New, Expansion, Reactivation as positive stacks; Contraction, Churn as negative stacks; Net New as the connecting line), with a secondary line showing trailing 12-month NRR

        Annotations:
        - Add benchmarks: a healthy SaaS business has Expansion + Reactivation ≥ |Contraction + Churn| (NRR ≥ 100%).
        - Flag any month where Net New MRR went negative.
        - Flag any month where Churned MRR exceeded New MRR.
        - Top-quartile NRR is ≥ 110%; world-class is ≥ 120%.

        Taxonomy notes:
        - The canonical Intempt taxonomy does NOT have separate subscription_upgraded, subscription_downgraded, or subscription_reactivated events. The available subscription state-change events are: subscription_created, subscription_updated, subscription_cancelled, subscription_paused, subscription_resumed, subscription_expired, subscription_activated.
        - Expansion / Contraction split must be computed by Lovable's translation layer from subscription_updated by comparing new vs. prior subscription amount. The changed_fields property indicates what changed; plan_items carries the new state.
        - Reactivation is computed as subscription_resumed (or subscription_activated) where the same customer_id had a recent subscription_cancelled.
        - This recipe requires the workspace to have these subscription state-change events flowing reliably from Stripe / HubSpot / Shopify subscription integrations. If subscription_updated is sparse, the report degrades to New MRR + Churned MRR only — still valuable but missing the expansion/contraction decomposition.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# MRR Movement Decomposition

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "MRR Movement Decomposition".

   This is the canonical SaaS MRR waterfall. Compute the five movement categories per month:

   New MRR: Sum of subscription_created.amount in the period for users who had no active subscription previously, unit: $
   Expansion MRR: From subscription_updated events — for each event, compute (new amount − prior subscription amount on the same subscription_id). Sum the positive deltas where changed_fields indicates plan upgrade or seat/quantity increase, unit: $
   Contraction MRR: Same subscription_updated computation; sum the negative deltas (will appear as negative values in the waterfall), unit: $
   Churned MRR: Sum of the prior subscription amount for each subscription_cancelled event in the period (negative in the waterfall), unit: $
   Reactivation MRR: Sum of subscription_resumed.amount where the user previously had a subscription_cancelled in the prior 90 days, unit: $

   Net New MRR: New + Expansion + Contraction (negative) + Churned (negative) + Reactivation
   Net Revenue Retention (NRR): (Starting MRR + Expansion + Reactivation − Contraction − Churn) / Starting MRR × 100, unit: %

   Time granularity: Monthly
   Time range: Last 12 months
   Compare: Year-over-year
   Chart type: Waterfall chart per month (New, Expansion, Reactivation as positive stacks; Contraction, Churn as negative stacks; Net New as the connecting line), with a secondary line showing trailing 12-month NRR

   Annotations:
   - Add benchmarks: a healthy SaaS business has Expansion + Reactivation ≥ |Contraction + Churn| (NRR ≥ 100%).
   - Flag any month where Net New MRR went negative.
   - Flag any month where Churned MRR exceeded New MRR.
   - Top-quartile NRR is ≥ 110%; world-class is ≥ 120%.

   Taxonomy notes:
   - The canonical Intempt taxonomy does NOT have separate subscription_upgraded, subscription_downgraded, or subscription_reactivated events. The available subscription state-change events are: subscription_created, subscription_updated, subscription_cancelled, subscription_paused, subscription_resumed, subscription_expired, subscription_activated.
   - Expansion / Contraction split must be computed by Lovable's translation layer from subscription_updated by comparing new vs. prior subscription amount. The changed_fields property indicates what changed; plan_items carries the new state.
   - Reactivation is computed as subscription_resumed (or subscription_activated) where the same customer_id had a recent subscription_cancelled.
   - This recipe requires the workspace to have these subscription state-change events flowing reliably from Stripe / HubSpot / Shopify subscription integrations. If subscription_updated is sparse, the report degrades to New MRR + Churned MRR only — still valuable but missing the expansion/contraction decomposition.
   ```
