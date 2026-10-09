---
description: Shows which product categories get returned most, and which ones have got worse since last quarter.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
---

# Return rate by category

Slash command: /return-rate-by-category

## Step 1: Rank categories by returns

Create an Insights report called "Return Rate by Category".
Series A: Event "Order fulfilled", aggregation: Count
Series B: Event "Return requested", aggregation: Count
Formula: (B / A) × 100, unit: %, label: "Return Rate"
Breakdown: By product category: derive from Return requested.items joined to Products to find category, OR from the source order's items (Return requested carries order_id relation).
Time range: Last 90 days
Compare: Previous period (prior 90 days)
Chart type: Bar chart sorted by total return rate descending
Annotations:
- Flag any category where return rate jumped >5 percentage points vs. prior period.
- Surface top 5 categories by absolute return volume and top 5 by return rate (the lists are usually different and both matter).
Taxonomy notes:
- Return requested has items, order_id (relation), return_id, status. Items resolve to categories through the Products record object.
- Note: there is no canonical "return_reason" property on Return requested. Reason analysis would require joining with Order refunded (which has a reason text field) when the return is monetized.
