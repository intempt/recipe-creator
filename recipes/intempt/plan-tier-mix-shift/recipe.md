---
description: Shows how revenue is spread across plans over time and whether revenue mix is drifting up market or down market.
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

# Plan tier mix shift

Slash command: /plan-tier-mix-shift

## Step 1: Compare revenue and customer mix

Create an Insights report called "Plan-Tier Mix Shift".
Series A: Event "revenue_completed" filtered to recurring revenue type (or invoice_paid as fallback), aggregation: Sum of "amount", unit: $
Series B: Count of users with an active subscription at month-end (active = has subscription_created with status in active states, no subsequent subscription_cancelled or subscription_expired before the month-end)
Series C: Computed: Series A by plan / total Series A × 100, unit: %, label: "% of Revenue by Plan"
Series D: Computed: Series B by plan / total Series B × 100, unit: %, label: "% of Customers by Plan"
Time granularity: Monthly
Breakdown: By plan_name (resolved from each user's most-recent active subscription_created.plan_name)
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
- plan_name is on subscription_created. Active subscription status is determined by absence of a later subscription_cancelled / subscription_expired for the same subscription_id.
