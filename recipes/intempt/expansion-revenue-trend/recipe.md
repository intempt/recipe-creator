---
frontmatter_id: expansion-revenue-trend
slash_command: /expansion-revenue-trend
description: Shows month over month MRR change per subscription from Subscription updated change events, comparing each subscription's amount before and after the update.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows month-over-month expansion revenue per subscription from plan upgrades and seat increases, and how much it
    equals as a share of new MRR.
  parameters:
  - name: window
    type: duration
    label: Time range to analyze
    default: 12 mo
    required: false
  - name: healthy_threshold
    type: number
    label: Healthy expansion as % of new MRR
    default: 30
    required: false
  - name: best_in_class_threshold
    type: number
    label: Best-in-class expansion as % of new MRR
    default: 50
    required: false
  - name: stall_decline_threshold
    type: number
    label: MoM expansion decline that flags a stall (%)
    default: 15
    required: false
  requirements:
  - slot: subscription_updated_event
    kind: event
    meaning: A customer's subscription was updated
    properties:
    - name: subscription_id
      type: string
      meaning: Identifier of the subscription that changed
      optional: false
    - name: changed_fields
      type: text
      meaning: Names of the subscription fields that changed, such as plan or line items
      optional: false
    - name: plan_items
      type: text
      meaning: Plan line items with price, quantity and product after the update
      optional: false
    - name: amount
      type: number
      meaning: Subscription amount after the update
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: subscription_id
      type: string
      meaning: Identifier of the new subscription
      optional: false
    - name: amount
      type: number
      meaning: Starting subscription amount
      optional: false
    - name: plan
      type: string
      meaning: Starting plan tier used to break down results
      optional: false
  - slot: revenue_event
    kind: event
    meaning: A customer payment was completed or an invoice was paid
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - subscription_updated_event
    - subscription_started_event
    - window
    - healthy_threshold
    - best_in_class_threshold
    - stall_decline_threshold
    instruction: 'Create an Insights report called "Expansion Revenue Trend" showing month-over-month MRR change per subscription
      from {subscription_updated_event} events, comparing each subscription''s amount before and after the update. Series
      A "Upgrade Revenue": from {subscription_updated_event}, where {subscription_updated_event.changed_fields} indicates
      a plan change (contains "plan_id" or "plan_items" with a higher-priced target in {subscription_updated_event.plan_items});
      for each event compare the new {subscription_updated_event.amount} with the prior amount on the same {subscription_updated_event.subscription_id};
      sum positive deltas, unit $. Series B "Seat / Quantity Expansion Revenue": from {subscription_updated_event}, where
      {subscription_updated_event.changed_fields} indicates a quantity increase in {subscription_updated_event.plan_items};
      sum positive amount deltas, unit $. Series C "Expansion as % of New MRR": (A + B) divided by new MRR in the period times
      100, unit %, where new MRR is the sum of {subscription_started_event.amount} in the period. Granularity monthly over
      {window}, compare year-over-year, breakdown by starting plan tier using {subscription_started_event.plan}. Chart: stacked
      bars for A and B, Series C as a line on a secondary axis. Annotate benchmarks: expansion as % of new MRR at or above
      {healthy_threshold} is healthy and at or above {best_in_class_threshold} is best-in-class. Flag any month where total
      expansion revenue declined month over month by more than {stall_decline_threshold}% as a stalling expansion engine.
      Highlight whether upgrade-driven or seat-driven expansion dominates and whether the mix is shifting. Negative deltas
      count as contraction and are excluded from expansion totals.'
---

# Expansion revenue trend

Slash command: /expansion-revenue-trend

## Step 1: Split upgrades from seat growth

Create an Insights report called "Expansion Revenue Trend".
Series A: Event "Subscription updated" where changed_fields indicates a plan upgrade (parsed from the changed_fields text property: e.g. contains "plan_id" or "plan_items" with a higher-priced target), aggregation: Sum of the resulting subscription amount delta
 Computation: for each Subscription updated event, compare new amount vs. prior amount on the same subscription_id. Positive delta with plan change = upgrade. Sum positive deltas, unit: $, label: "Upgrade Revenue".
Series B: Event "Subscription updated" where changed_fields indicates seat/quantity increase (e.g. plan_items quantity went up), aggregation: Sum of positive amount delta, unit: $, label: "Seat / Quantity Expansion Revenue"
Series C: Computed: (A + B) / new_mrr_in_period × 100, unit: %, label: "Expansion as % of New MRR"
 where new_mrr = sum of Subscription started.amount in the period
Time granularity: Monthly
Breakdown: By Plan: show which starting plan tiers produce the most expansion
Time range: Last 12 months
Compare: Year-over-year
Chart type: Stacked bar for A and B with Series C as a line on a secondary axis
Annotations:
- Add benchmarks: expansion as % of new MRR ≥ 30% is healthy; ≥ 50% is best-in-class.
- Flag any month where total expansion revenue declined MoM by more than 15% (expansion engine stalling).
- Highlight whether upgrade-driven expansion or seat-driven expansion dominates, and whether the mix is shifting.
Taxonomy notes:
- The canonical taxonomy has Subscription updated with a changed_fields text property and a plan_items property (flattenable to price_id, quantity, product). It does NOT have separate subscription_upgraded / subscription_downgraded events.
- Computing upgrade vs downgrade requires comparing new vs prior subscription state: operationally this means: when Subscription updated fires, look up the prior Subscription started.amount and compute the delta. Positive delta = expansion, negative = contraction.
- "subscription_payment" is not a canonical event. Use Revenue completed or Invoice paid for actual revenue capture.
