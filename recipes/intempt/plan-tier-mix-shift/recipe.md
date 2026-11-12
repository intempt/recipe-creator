---
frontmatter_id: plan-tier-mix-shift
slash_command: /plan-tier-mix-shift
description: Shows how revenue is spread across plans over time and whether revenue mix is drifting up market or down market.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows how revenue and customers spread across subscription plans month by month, flagging shifts toward higher
    or lower tiers and divergences between revenue and customer mix.
  parameters:
  - name: time_range
    type: duration
    label: Time range to analyze
    default: 12 mo
    required: false
  - name: shift_threshold_pp
    type: number
    label: Revenue share shift flag threshold (percentage points, YoY)
    default: 5
    required: false
  - name: comparison_period
    type: enum
    label: Comparison period
    default: year_over_year
    required: false
    options:
    - year_over_year
    - month_over_month
  requirements:
  - slot: revenue_event
    kind: event
    meaning: A customer completed a revenue payment
    properties:
    - name: amount
      type: number
      meaning: Payment amount in dollars
      optional: false
    - name: revenue_type
      type: string
      meaning: Type of revenue, such as recurring
      optional: true
  - slot: invoice_paid_event
    kind: event
    meaning: A customer's invoice was paid
    properties:
    - name: amount
      type: number
      meaning: Invoice amount in dollars
      optional: false
    optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: plan
      type: string
      meaning: Subscription plan tier
      optional: false
    - name: subscription_id
      type: string
      meaning: Unique subscription identifier
      optional: false
    - name: status
      type: string
      meaning: Subscription status
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: subscription_id
      type: string
      meaning: Unique subscription identifier
      optional: false
  - slot: subscription_expired_event
    kind: event
    meaning: A customer's subscription expired
    properties:
    - name: subscription_id
      type: string
      meaning: Unique subscription identifier
      optional: false
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - revenue_event
    - invoice_paid_event
    - subscription_started_event
    - subscription_canceled_event
    - subscription_expired_event
    - time_range
    - shift_threshold_pp
    - comparison_period
    instruction: 'Create an Insights report titled "Plan-Tier Mix Shift". Series A: count of {revenue_event} filtered to revenue
      type recurring (fall back to {invoice_paid_event} if no recurring revenue type exists), aggregated as sum of {revenue_event.amount}
      in dollars. Series B: count of distinct users with an active subscription at each month-end, where a subscription is
      active if a {subscription_started_event} exists with status in active states and no later {subscription_canceled_event}
      or {subscription_expired_event} exists for the same {subscription_started_event.subscription_id} before that month-end.
      Series C: Series A broken down by plan divided by total Series A times 100, in percent, labeled "% of Revenue by Plan".
      Series D: Series B broken down by plan divided by total Series B times 100, in percent, labeled "% of Customers by Plan".
      Use monthly granularity over {time_range}, breaking down by plan resolved from each user''s most recent active {subscription_started_event.plan}.
      Compare with {comparison_period}. Chart as two stacked area charts side by side: Series C and Series D. Annotate each
      plan with its start and end share and the percentage-point change. Flag any plan whose revenue share shifted by more
      than {shift_threshold_pp} percentage points. Highlight where revenue mix and customer mix diverge: a higher tier rising
      as a share of revenue while flat as a share of customers signals rising average revenue per account from pricing or
      positioning; the opposite pattern, customer mix moving up-market while revenue mix stays flat, signals discounting eroding
      the up-market thesis.'
---

# Plan tier mix shift

Slash command: /plan-tier-mix-shift

## Step 1: Compare revenue and customer mix

Create an Insights report called "Plan-Tier Mix Shift".
Series A: Event "Revenue completed" filtered to recurring revenue type (or Invoice paid as fallback), aggregation: Sum of "amount", unit: $
Series B: Count of users with an active subscription at month-end (active = has Subscription started with status in active states, no subsequent Subscription canceled or subscription_expired before the month-end)
Series C: Computed: Series A by plan / total Series A × 100, unit: %, label: "% of Revenue by Plan"
Series D: Computed: Series B by plan / total Series B × 100, unit: %, label: "% of Customers by Plan"
Time granularity: Monthly
Breakdown: By Plan (resolved from each user's most-recent active Subscription started.Plan)
Time range: Last 12 months
Compare: Year-over-year
Chart type: Two stacked area charts side-by-side: Series C (revenue mix) and Series D (customer mix)
Annotations:
- For each plan, label start-of-period and end-of-period share with the change in percentage points.
- Flag any plan whose share of revenue shifted by >5 percentage points YoY.
- Highlight any divergence between revenue mix and customer mix (e.g., higher tier growing as % of revenue but flat as % of customers = ARPA going up = pricing/positioning working).
- Flag the opposite divergence (customer mix shifting up-market but revenue mix flat = discounting eroding the up-market thesis).
This is one of the most consequential questions for SaaS pricing/positioning teams.
Taxonomy notes:
- Plan is on Subscription started. Active subscription status is determined by absence of a later Subscription canceled / subscription_expired for the same subscription_id.
