---
frontmatter_id: cohort-acquisition-ltv-dashboard
author:
  name: Intempt
  last_name: Technologies
  org_name: intempt
---
# Cohort LTV by acquisition channel

## Step 1: Build the cohort LTV board

Create a Dash board (12-column composition canvas) titled "Cohort Acquisition LTV".
Persona: a performance marketer running paid acquisition, or a founder evaluating channel quality. Question answered: which acquisition cohorts produce lifetime value worth keeping, where should spend scale, and which channels acquire customers who retain versus buy once and leave.
Board-level configuration:
- defaultDateRange: last_12_months, since lifetime value is inherently long-term and shorter ranges miss the cohort tail
- exclusionPeriod: incomplete_periods, since recent cohorts have not had time to mature
- visibility: project
- boardFilters: none by default
- boardBreakdowns: UTM source, pushed down throughout as the acquisition-channel dimension
Layout: 4 rows.
Row 1: Cohort headline KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (Month 6)"
- Card 2: Insights metric to source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (Month 12)"
- Card 3: Retention metric to source recipe: purchase-retention, vizType: metric, titleOverride: "Month 3 Repeat Purchase Rate"
- Card 4: Insights metric to source recipe: post-purchase-second-order-velocity, vizType: metric, titleOverride: "Median Days to Second Order"
Row 2: Cohort LTV curves by channel (heightPx: 480, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: first-purchase-cohort-ltv-curve, displayMode: chart, vizType: line, multi-line by cohort, X axis months since first purchase, Y axis cumulative revenue per cohort member, broken down by acquisition channel via UTM source.
Row 3: Repeat-purchase mechanics (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Retention to source recipe: purchase-retention, displayMode: chart, vizType: retention_curve, cohort by first-purchase month, repeat-purchase percent over time, by first-order category
- Card 2: Insights to source recipe: post-purchase-second-order-velocity, displayMode: chart, histogram of days from first to second order, to inform replenishment journey timing per category
Row 4: Channel revenue and lifecycle context (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: revenue-by-channel, displayMode: chart, vizType: bar, current revenue split per channel
- Card 2: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart, per-channel customer-lifecycle distribution
Annotations:
- The two Row 1 lifetime-value figures are read alongside customer acquisition cost, which this dashboard does not compute: acquisition cost must be brought in separately to judge unit economics.
- Row 2 is the strategic centerpiece: a channel whose cohort line climbs steeply accumulates revenue fast and is acquiring customers worth keeping; a channel whose line stays flat is acquiring one-time buyers.
- Row 3's retention curve shows which product categories suit a subscribe-and-reorder offer, meaning those with a high month-3 repeat rate, versus which are one-time-purchase categories.
- Row 4 ties it together: a channel with high current revenue but a lifecycle mix weighted toward At risk customers is a leading indicator of future revenue erosion on that channel.
- Recommended cadence: monthly. Cohort lifetime value moves slowly; a weekly read mostly shows noise.
Taxonomy notes:
- All source recipes use canonical events: Placed order with items, total_price, customer_id; Session start; View page.
- Users.UTM source is the canonical first-touch acquisition channel.
- Users.Lifecycle score is the canonical six-stage lifecycle enum: At risk, Needs attention, New customers, Promising, Regulars, Champions.

## Step 2: Flag channels worth more or less spend

Create a workflow called "Cohort LTV Monthly Channel Review" that runs on the same monthly cadence the board is read on. For any channel whose Month 6 average lifetime value is in the bottom quartile of tracked channels for 2 consecutive months, create a task for the performance marketing owner recommending that channel's spend be reviewed, with the cohort curve attached. For any channel in the top quartile for 2 consecutive months, create a separate task recommending its spend be considered for an increase. Use the result of "Build the cohort LTV board".
