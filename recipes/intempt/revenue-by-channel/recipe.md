---
frontmatter_id: revenue-by-channel
slash_command: /revenue-by-channel
description: Shows which channels brought in revenue over the last 30 days, each channel's share, and how the mix has shifted since last year.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows which acquisition channels brought in revenue over the last 30 days, each channel's share, and how the channel
    mix has shifted versus last year.
  parameters:
  - name: time_window
    type: duration
    label: Analysis time range
    default: 30 d
    required: false
  - name: top_n_channels
    type: number
    label: Number of top channels shown before grouping the rest as Other
    default: 8
    required: false
  - name: mix_shift_threshold_pp
    type: number
    label: Share shift (percentage points YoY) that flags a channel
    default: 5
    required: false
  requirements:
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order value of the placed order
      optional: false
  - slot: utm_source_attribute
    kind: attribute
    meaning: The user's first-touch UTM source recorded on the user record
  steps:
  - id: s1
    builds: report
    uses:
    - order_placed_event
    - utm_source_attribute
    - time_window
    - top_n_channels
    - mix_shift_threshold_pp
    instruction: 'Create an Insights report titled "Revenue by Acquisition Channel". Series A: count of {order_placed_event}
      aggregated as sum of {order_placed_event.total_price}, unit $, labeled "Revenue". Series B: Series A divided by total
      revenue times 100, unit %, labeled "Share of Revenue". Break down by {utm_source_attribute} to attribute each order
      to a channel; show the top {top_n_channels} channels by revenue and group the remainder as "Other". Time range: last
      {time_window}. Compare against the previous period (prior {time_window}) and the same period last year. Show Series
      A as a horizontal bar chart with the period comparison overlaid; show Series B share over time as a separate small-multiple
      area chart. Annotate each channel bar with absolute revenue and year-over-year percentage change. Flag any channel whose
      share of revenue shifted by {mix_shift_threshold_pp} or more percentage points year over year as a mix shift. Highlight
      channels whose revenue grew but whose share declined (growing slower than overall), and channels whose revenue declined
      while share stayed stable (overall slowdown rather than channel-specific).'
---

# Revenue by acquisition channel

Slash command: /revenue-by-channel

## Step 1: Split revenue by channel

Create an Insights report called "Revenue by Acquisition Channel".
Series A: Event "Placed order", aggregation: Sum of "total_price" property, unit: $, label: "Revenue"
Series B: Computed: Series A / total revenue × 100, unit: %, label: "Share of Revenue"
Breakdown: By UTM source: use the User.UTM source attribute (Users object has UTM source as a User-scope text attribute) to attribute each order to a channel. Top 8 by revenue, group remainder as "Other".
Time range: Last 30 days
Compare: Previous period (prior 30 days) AND year-over-year (same 30 days last year)
Chart type: Horizontal bar chart for Series A with overlaid period comparison; separate small-multiple area chart for share-of-revenue over time
Annotations:
- Add absolute revenue and YoY % change next to each channel bar.
- Flag any channel whose share of revenue shifted by 5+ percentage points YoY (mix shift).
- Highlight channels with revenue growth but declining share (growing slower than overall) and channels with declining revenue but stable share (overall slowdown, not channel-specific).
The mix-shift view is what reveals whether the business is becoming more or less channel-concentrated.
Taxonomy notes:
- Users.UTM source is a real text attribute; per-order channel attribution uses the User's first-touch UTM source as authored on the user record.
- Placed order.total_price is the order value (Shopify-sourced). "order_total" is not a real property.
