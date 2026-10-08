---
description: Shows which channels brought in revenue over the last 30 days, each channel's share, and how the mix has shifted since last year.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
  - finance
---

# Revenue by acquisition channel

Slash command: /revenue-by-channel

## Step 1: Split revenue by channel

Create an Insights report called "Revenue by Acquisition Channel".
Series A: Event "order_created", aggregation: Sum of "total_price" property, unit: $, label: "Revenue"
Series B: Computed: Series A / total revenue × 100, unit: %, label: "Share of Revenue"
Breakdown: By utm_source: use the User.utm_source attribute (Users object has utm_source as a User-scope text attribute) to attribute each order to a channel. Top 8 by revenue, group remainder as "Other".
Time range: Last 30 days
Compare: Previous period (prior 30 days) AND year-over-year (same 30 days last year)
Chart type: Horizontal bar chart for Series A with overlaid period comparison; separate small-multiple area chart for share-of-revenue over time
Annotations:
- Add absolute revenue and YoY % change next to each channel bar.
- Flag any channel whose share of revenue shifted by 5+ percentage points YoY (mix shift).
- Highlight channels with revenue growth but declining share (growing slower than overall) and channels with declining revenue but stable share (overall slowdown, not channel-specific).
The mix-shift view is what reveals whether the business is becoming more or less channel-concentrated.
Taxonomy notes:
- Users.utm_source is a real text attribute; per-order channel attribution uses the User's first-touch utm_source as authored on the user record.
- order_created.total_price is the order value (Shopify-sourced). "order_total" is not a real property.
