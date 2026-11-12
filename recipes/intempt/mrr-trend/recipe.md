---
frontmatter_id: mrr-trend
slash_command: /mrr-trend
description: Shows recurring revenue by plan over the last 12 months, with the month on month change and how each month compares with the same month last year.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows monthly recurring revenue by plan over the last 12 months, with month-on-month change, year-over-year comparison,
    and flags for contraction and mix shifts.
  parameters:
  - name: time_range
    type: duration
    label: Time range to chart
    default: 12 mo
    required: false
  - name: yoy_share_shift_threshold
    type: number
    label: YoY plan share shift threshold (percentage points)
    default: 5
    required: false
  - name: growth_average_window
    type: duration
    label: Trailing growth average window
    default: 3 mo
    required: false
  - name: recurring_type_value
    type: text
    label: Revenue completed type value that marks recurring revenue
    default: subscription
    required: false
  requirements:
  - slot: revenue_completed_event
    kind: event
    meaning: A customer completed a revenue payment
    properties:
    - name: amount
      type: number
      meaning: Payment amount in dollars
      optional: false
    - name: customer_id
      type: text
      meaning: Identifier of the paying customer
      optional: false
    - name: type
      type: text
      meaning: Revenue type, indicating whether the payment is recurring subscription revenue
      optional: false
    - name: source
      type: text
      meaning: Where the revenue payment originated
      optional: true
  - slot: invoice_paid_event
    kind: event
    meaning: A customer's invoice was paid through the payment processor
    properties:
    - name: amount_paid_cents
      type: number
      meaning: Amount paid on the invoice in cents
      optional: false
    - name: customer_id
      type: text
      meaning: Identifier of the paying customer
      optional: false
    optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription to a plan
    properties:
    - name: plan
      type: text
      meaning: Name of the subscription plan tier the customer started
      optional: false
    - name: customer_id
      type: text
      meaning: Identifier of the subscribing customer
      optional: false
  steps:
  - id: s1
    builds: report
    uses:
    - revenue_completed_event
    - invoice_paid_event
    - subscription_started_event
    - time_range
    - yoy_share_shift_threshold
    - growth_average_window
    - recurring_type_value
    instruction: 'Create an Insights report titled "Monthly Recurring Revenue Trend" showing monthly recurring revenue over
      {time_range}, with monthly granularity. Series A is the sum of {revenue_completed_event.amount} for {revenue_completed_event}
      where {revenue_completed_event.type} equals "{recurring_type_value}", labeled "MRR" in dollars. If {revenue_completed_event}
      recurring type is not configured in the workspace, use {invoice_paid_event} instead, summing {invoice_paid_event.amount_paid_cents}
      divided by 100 to get dollars. Break Series A down by plan: attribute each paying customer to the plan from their most
      recent active {subscription_started_event.plan}, matched on customer id. Render Series A as a stacked area chart. Series
      B is the month-over-month net new MRR, computed as current month MRR minus previous month MRR, labeled "Net New MRR"
      in dollars, shown as a secondary line. Add a dotted year-over-year overlay comparing each month with the same month
      of the prior year. Annotations: show the absolute MRR for the most recent month as a callout; show the month-over-month
      growth rate as a percentage and the trailing {growth_average_window} average growth rate; flag any month where Net New
      MRR is negative as contraction; highlight any plan whose share of MRR shifted by more than {yoy_share_shift_threshold}
      percentage points year over year. Do not use a subscription_payment event, which does not exist in the taxonomy.'
---

# Monthly recurring revenue trend

Slash command: /mrr-trend

## Step 1: Chart MRR by plan each month

Create an Insights report called "Monthly Recurring Revenue Trend".
Series A: Event "Revenue completed" where type indicates a recurring payment (or "Invoice paid" if Invoice paid is the canonical recurring revenue marker in this workspace), aggregation: Sum of "amount" property, unit: $, label: "MRR"
 - For Revenue completed, filter by type indicating subscription/recurring revenue.
 - For Invoice paid as fallback, aggregate amount_paid_cents and divide by 100 to get $.
Series B: Computed: month-over-month MRR delta (current month MRR − previous month MRR), unit: $, label: "Net New MRR"
Time granularity: Monthly
Breakdown for Series A: By Plan: for Revenue completed users, the Plan comes from their Subscription started event (most recent active subscription). Render as stacked area.
Time range: Last 12 months
Compare: Year-over-year (same month previous year, dotted overlay)
Chart type: Stacked area chart for Series A with Series B as a secondary line
Annotations:
- Add the absolute MRR figure for the most recent month as a callout.
- Add the month-over-month growth rate (%) and the trailing 3-month average growth rate.
- Flag any month where net new MRR went negative (contraction).
- Highlight any plan tier whose share of MRR shifted by more than 5 percentage points YoY.
Taxonomy notes:
- Revenue completed has amount, customer_id, type, source: use type to filter for recurring revenue.
- Invoice paid (Stripe) has amount_paid_cents: use as primary if Revenue completed type-discrimination is not configured.
- Plan comes from Subscription started: join to user's most-recent active subscription to attribute the MRR.
- "subscription_payment" as an event does not exist in the canonical taxonomy.
