---
description: Shows recurring revenue by plan over the last 12 months, with the month on month change and how each month compares with the same month last year.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - finance
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
