---
frontmatter_id: mrr-movement-decomposition
slash_command: /mrr-movement-decomposition
description: Reports monthly recurring revenue movement by summing new and churned MRR from subscription data. Shows gross additions and losses by month.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Builds a monthly MRR waterfall over the last 12 months that splits recurring revenue movement into new, expansion,
    contraction, churn and reactivation, with NRR trend.
  parameters:
  - name: time_granularity
    type: enum
    label: Time granularity
    default: monthly
    required: false
    options:
    - monthly
  - name: time_range
    type: duration
    label: Time range
    default: 12 mo
    required: false
  - name: reactivation_window
    type: duration
    label: Reactivation lookback window
    default: 90 d
    required: false
  - name: comparison_period
    type: enum
    label: Comparison period
    default: year_over_year
    required: false
    options:
    - none
    - month_over_month
    - year_over_year
  requirements:
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: amount
      type: number
      meaning: Recurring amount of the new subscription
      optional: false
    - name: customer_id
      type: string
      meaning: Identifier of the customer
      optional: false
  - slot: subscription_updated_event
    kind: event
    meaning: A customer's subscription was changed
    properties:
    - name: amount
      type: number
      meaning: New recurring amount after the change
      optional: false
    - name: prior_amount
      type: number
      meaning: Recurring amount before the change
      optional: false
    - name: subscription_id
      type: string
      meaning: Identifier of the subscription
      optional: false
    - name: changed_fields
      type: text
      meaning: Which subscription fields changed
      optional: false
    - name: plan_items
      type: text
      meaning: New plan state after the change
      optional: true
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: prior_amount
      type: number
      meaning: Recurring amount of the subscription before cancellation
      optional: false
    - name: customer_id
      type: string
      meaning: Identifier of the customer
      optional: false
  - slot: subscription_resumed_event
    kind: event
    meaning: A customer resumed a previously paused or canceled subscription
    properties:
    - name: amount
      type: number
      meaning: Recurring amount when resumed
      optional: false
    - name: customer_id
      type: string
      meaning: Identifier of the customer
      optional: false
  - slot: active_subscription_status
    kind: attribute
    meaning: Whether a customer currently has an active subscription
  - slot: mrr_waterfall_report
    kind: knowledge
    meaning: Output report showing the MRR movement waterfall
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - subscription_started_event
    - subscription_updated_event
    - subscription_canceled_event
    - subscription_resumed_event
    - active_subscription_status
    - time_range
    - time_granularity
    - reactivation_window
    - comparison_period
    instruction: 'Create an Insights report called "MRR Movement Decomposition". Compute five monthly MRR movement categories
      over the {time_range} window at {time_granularity} granularity. New MRR: sum of {subscription_started_event.amount}
      for customers with no active subscription beforehand. Expansion MRR: from {subscription_updated_event} events, compute
      the delta of {subscription_updated_event.amount} minus {subscription_updated_event.prior_amount} per subscription_id,
      and sum the positive deltas where {subscription_updated_event.changed_fields} indicates a plan upgrade or seat/quantity
      increase. Contraction MRR: same delta computation, summing negative deltas (shown as negative values). Churned MRR:
      sum of {subscription_canceled_event.prior_amount} per cancellation (shown as negative). Reactivation MRR: sum of {subscription_resumed_event.amount}
      where the same {subscription_canceled_event.customer_id} had a cancellation within {reactivation_window}. Net New MRR
      = New + Expansion + Contraction + Churned + Reactivation. Net Revenue Retention (%) = (Starting MRR + Expansion + Reactivation
      − Contraction − Churn) / Starting MRR × 100. Compare using {comparison_period}. Chart as a waterfall per month: New,
      Expansion and Reactivation as positive stacks; Contraction and Churn as negative stacks; Net New as the connecting line;
      add a secondary line with trailing 12-month NRR.'
---

# MRR movement waterfall

Slash command: /mrr-movement-decomposition

## Step 1: Break MRR into its five parts

Create an Insights report called "MRR Movement Decomposition".
This is the canonical SaaS MRR waterfall. Compute the five movement categories per month:
New MRR: Sum of Subscription started.amount in the period for users who had no active subscription previously, unit: $
Expansion MRR: From Subscription updated events: for each event, compute (new amount − prior subscription amount on the same subscription_id). Sum the positive deltas where changed_fields indicates plan upgrade or seat/quantity increase, unit: $
Contraction MRR: Same Subscription updated computation; sum the negative deltas (will appear as negative values in the waterfall), unit: $
Churned MRR: Sum of the prior subscription amount for each Subscription canceled event in the period (negative in the waterfall), unit: $
Reactivation MRR: Sum of subscription_resumed.amount where the user previously had a Subscription canceled in the prior 90 days, unit: $
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
- The canonical Intempt taxonomy does NOT have separate subscription_upgraded, subscription_downgraded, or subscription_reactivated events. The available subscription state-change events are: Subscription started, Subscription updated, Subscription canceled, subscription_paused, subscription_resumed, subscription_expired, subscription_activated.
- Expansion / Contraction split must be computed by Lovable's translation layer from Subscription updated by comparing new vs. prior subscription amount. The changed_fields property indicates what changed; plan_items carries the new state.
- Reactivation is computed as subscription_resumed (or subscription_activated) where the same customer_id had a recent Subscription canceled.
- This recipe requires the workspace to have these subscription state-change events flowing reliably from Stripe / HubSpot / Shopify subscription integrations. If Subscription updated is sparse, the report degrades to New MRR + Churned MRR only: still valuable but missing the expansion/contraction decomposition.
