---
frontmatter_id: mrr-trend
slash_command: /mrr-trend
description: This recipe builds a monthly report on recurring revenue, broken down by plan, and then watches it for problems. It is for revenue, finance and growth teams who want to be told when revenue shrinks or the plan mix shifts.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
prerequisites:
  integrations:
    - { value: stripe, severity: blocking }
    - { value: slack, severity: recommended }
---

# Monthly recurring revenue trend

## Step 1: Chart MRR by plan each month

Create an Insights report called "Monthly Recurring Revenue Trend".
Series A: Event "Revenue completed" where type indicates a recurring payment (or "Invoice paid" if Invoice paid is the canonical recurring revenue marker in this workspace), aggregation: Sum of "amount" property, unit: $, label: "MRR"
 - For Revenue completed, filter by type indicating subscription/recurring revenue.
 - For Invoice paid as fallback, aggregate amount_paid_cents and divide by 100 to get $.
Series B: Computed: month-over-month MRR delta (current month MRR minus previous month MRR), unit: $, label: "Net New MRR"
Time granularity: Monthly
Breakdown for Series A: By Plan: for Revenue completed users, the Plan comes from their Subscription started event (most recent active subscription). Render as stacked area.
Time range: Last 12 months
Compare: Year-over-year (same month previous year, dotted overlay)
Chart type: Stacked area chart for Series A with Series B as a secondary line
Annotations:
- Add the absolute MRR figure for the most recent month as a callout.
- Add the month-over-month growth rate (percent) and the trailing 3-month average growth rate.
- Flag any month where net new MRR went negative (contraction).
- Highlight any plan tier whose share of MRR shifted by more than 5 percentage points year over year.
Taxonomy notes:
- Revenue completed has amount, customer_id, type, source: use type to filter for recurring revenue.
- Invoice paid (Stripe) has amount_paid_cents: use as primary if Revenue completed type-discrimination is not configured.
- Plan comes from Subscription started: join to the user's most-recent active subscription to attribute the MRR.
- "subscription_payment" as an event does not exist in the canonical taxonomy.

## Step 2: Alert the revenue owner on contraction

Create a workflow called "MRR Contraction Alert" that runs on the same monthly schedule as "Chart MRR by plan each month". When that month's Net New MRR is negative, or any plan tier's share of MRR moved by more than 5 percentage points month over month, post a Slack message to the revenue team channel naming the dollar amount of the contraction, the plan tiers involved, and a link to the report. In the same run, create a task assigned to the revenue owner, due within 3 business days, titled with the calendar month and the words "MRR contraction", with the contraction amount and affected plan tiers in the task description. When Net New MRR is positive and no tier moved by more than 5 percentage points, the workflow ends without posting or creating a task. Use the result of "Chart MRR by plan each month".
