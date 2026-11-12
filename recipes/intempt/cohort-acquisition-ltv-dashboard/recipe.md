---
frontmatter_id: cohort-acquisition-ltv-dashboard
slash_command: /cohort-acquisition-ltv-dashboard
description: Monitor acquisition performance with line plots of selected metrics over calendar time. Use the trends to see how measures such as revenue or repeat purchases change over time.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows how customer lifetime value by acquisition channel and first-purchase cohort develops over time, with repeat-purchase
    timing and lifecycle context for scaling decisions.
  parameters:
  - name: defaultDateRange
    type: string
    label: Default date range
    default: last_12_months
  - name: exclusionPeriod
    type: enum
    label: Exclude incomplete periods
    default: incomplete_periods
    options:
    - incomplete_periods
    - none
  - name: visibility
    type: enum
    label: Dashboard visibility
    default: project
    options:
    - project
    - private
  - name: m6LtvCacMultiple
    type: number
    label: Healthy M6 LTV to CAC multiple
    default: 1.5
  - name: m12LtvCacMultiple
    type: number
    label: Top-quartile M12 LTV to CAC multiple
    default: 3
  - name: subscribeRetentionThreshold
    type: string
    label: M3 repeat rate suggesting subscribe-and-save
    default: 30%
  - name: oneTimeRetentionThreshold
    type: string
    label: M3 repeat rate suggesting one-time purchase category
    default: 10%
  - name: recommendedCadence
    type: string
    label: Recommended review cadence
    default: monthly
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: items
      type: text
      meaning: Items in the order
      optional: false
    - name: total_price
      type: number
      meaning: Total order price
      optional: false
    - name: customer_id
      type: string
      meaning: Customer identifier
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A customer started a session
    optional: true
  - slot: view_page_event
    kind: event
    meaning: A customer viewed a page
    optional: true
  - slot: utm_source_attribute
    kind: attribute
    meaning: The customer's first-touch UTM source acquisition channel
  - slot: lifecycle_score_attribute
    kind: attribute
    meaning: The customer's lifecycle stage (At risk, Needs attention, New customers, Promising, Regulars, Champions)
  - slot: first_order_category_attribute
    kind: attribute
    meaning: The product category of the customer's first order
    optional: true
  steps:
  - id: s1
    builds: dashboard
    uses:
    - placed_order_event
    - session_start_event
    - view_page_event
    - utm_source_attribute
    - lifecycle_score_attribute
    - first_order_category_attribute
    - defaultDateRange
    - exclusionPeriod
    - visibility
    - m6LtvCacMultiple
    - m12LtvCacMultiple
    - subscribeRetentionThreshold
    - oneTimeRetentionThreshold
    - recommendedCadence
    instruction: 'Create a Dash board with a 12-column composition canvas titled "Cohort Acquisition LTV". Set the default
      date range to {defaultDateRange}, exclude {exclusionPeriod}, and set visibility to {visibility}. Use no board filters
      by default. Set the board breakdown to {utm_source_attribute} and push it down throughout the board. Lay out four rows.
      Row 1 (height 200 px): four metric cards at 3 width units each. Card 1: insights metric from the first-purchase cohort
      LTV curve, vizType metric, title "Average LTV (M6)". Card 2: insights metric from the first-purchase cohort LTV curve,
      vizType metric, title "Average LTV (M12)". Card 3: retention metric from purchase retention, vizType metric, title "M3
      Repeat Purchase Rate". Card 4: insights metric from post-purchase second-order velocity, vizType metric, title "Median
      Days to 2nd Order". Row 2 (height 480 px): one full-width card at 12 width units. Insights from the first-purchase cohort
      LTV curve, displayMode chart, vizType line. Each line is a cohort defined by first-purchase month, X-axis is months
      since first purchase, Y-axis is cumulative revenue per cohort member, broken down by {utm_source_attribute}. Row 3 (height
      440 px): two cards at 6 width units. Card 1: retention curve from purchase retention, displayMode chart, vizType retention_curve,
      cohorts by first-purchase month showing repeat-purchase percentage over time, by {first_order_category_attribute}. Card
      2: insights from post-purchase second-order velocity, displayMode chart, histogram of days from first to second order,
      per category. Row 4 (height 440 px): two cards at 6 width units. Card 1: insights from revenue by channel, displayMode
      chart, vizType bar, current revenue split per channel. Card 2: insights from customer lifecycle distribution, displayMode
      chart, lifecycle distribution per channel using {lifecycle_score_attribute} against {utm_source_attribute}. Reading
      guide: M6 LTV at or above {m6LtvCacMultiple} times CAC is healthy and M12 LTV at or above {m12LtvCacMultiple} times
      CAC is top quartile; CAC must be computed externally. In the cohort curve, steep slopes mark quality acquisition channels
      and flat slopes mark one-and-done buyers. In the retention curve, categories above {subscribeRetentionThreshold} M3
      repeat suit subscribe-and-save, and categories below {oneTimeRetentionThreshold} M3 repeat are one-time purchases. Use
      the second-order histogram to set replenishment trigger delays per category. A channel with high current revenue but
      mostly At Risk customers signals revenue erosion. Review this dashboard {recommendedCadence}.'
---

# Cohort LTV by acquisition channel

Slash command: /cohort-acquisition-ltv-dashboard

## Step 1: Build the cohort LTV board

Create a Dash board (12-column composition canvas) titled "Cohort Acquisition LTV".
Persona: Performance Marketer running paid acquisition, or DTC Founder evaluating channel quality. Question answered: "Which acquisition cohorts produce LTV worth keeping? Where should I scale spend? Which channels acquire customers who retain vs. one-and-done?"
This dashboard is universally cited as the #1 dashboard for $20M+ DTC brands across Common Thread Collective, Conjura, Lifetimely, and Peel. Distinct from Customer 360 (overall customer-base observational) and Ecommerce Revenue (top-line): Cohort LTV is acquisition-month-cohort × revenue curve, with channel decomposition that ties acquisition cost back to long-term value.
Board-level configuration:
- defaultDateRange: last_12_months (LTV is inherently long-term; shorter ranges miss the cohort tail)
- exclusionPeriod: incomplete_periods (recent cohorts haven't had time to mature)
- visibility: project
- boardFilters: none by default
- boardBreakdowns: UTM source: pushed down throughout (the canonical acquisition-channel dimension)
Layout: 4 rows.
Row 1: Cohort headline KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (M6)"
- Card 2: Insights metric to source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (M12)"
- Card 3: Retention metric to source recipe: purchase-retention, vizType: metric, titleOverride: "M3 Repeat Purchase Rate"
- Card 4: Insights metric to source recipe: post-purchase-second-order-velocity, vizType: metric, titleOverride: "Median Days to 2nd Order"
Row 2: Cohort LTV curves by channel (heightPx: 480, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: first-purchase-cohort-ltv-curve, displayMode: chart, vizType: line (multi-line: each line = a cohort, X-axis = months since first purchase, Y-axis = cumulative revenue per cohort member, broken down by acquisition channel via UTM source). The strategic centerpiece: answers "which channels acquire customers worth keeping."
Row 3: Repeat-purchase mechanics (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Retention to source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort by first-purchase month: repeat-purchase % over time, by first-order category)
- Card 2: Insights to source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram of days from 1st to 2nd order: informs replenishment journey timing per category)
Row 4: Channel revenue and lifecycle context (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: revenue-by-channel, displayMode: chart, vizType: bar (current revenue split per channel: context for the LTV view)
- Card 2: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart (per-channel customer-lifecycle distribution: answers "which channels acquire Champions vs. At Risk customers")
Annotations:
- Row 1's two LTV KPIs (M6 + M12) are the canonical DTC scaling metrics. M6 LTV ≥ 1.5× CAC = healthy unit economics; M12 LTV ≥ 3× CAC = top-quartile. Without ad-spend integration in canonical taxonomy, this dashboard surfaces LTV; CAC must be computed externally and combined.
- Row 2 (Cohort LTV curves, full-width) is the strategic centerpiece. Reading it: each line is a cohort defined by first-purchase month; the line's slope tells you how fast each cohort accumulates revenue. Channels with steep curves (rapid cumulative revenue) acquire quality customers; channels with flat curves (low cumulative revenue) acquire one-and-done buyers.
- Row 3 surfaces operational levers:
 - Card 1 (retention curve) shows replenishment patterns by category: categories with steep retention curves (>30% M3 repeat) are candidates for subscribe-and-save or autoship; flat curves (<10% M3) are one-time-purchase categories
 - Card 2 (second-order velocity histogram) tells you the right delay for replenishment journey triggers per category: generic 30-day or 60-day delays often miss the actual median.
- Row 4 ties it together: which channels are currently producing revenue (Card 1), and what customer types are they acquiring (Card 2). A channel with high current revenue but acquiring mostly At Risk segments is a leading indicator of revenue erosion.
- Recommended cadence: read this dashboard monthly. Cohort LTV is slow-moving: weekly views over-rotate on noise.
Taxonomy notes:
- All source recipes use canonical events: Placed order (with items, total_price, customer_id), Session start, View page.
- Users.UTM source is the canonical first-touch acquisition channel.
- Users.Lifecycle score is the canonical 6-stage lifecycle enum (At risk / Needs attention / New customers / Promising / Regulars / Champions).
- This dashboard does NOT include CAC or ROAS metrics because ad-spend events are not in canonical taxonomy V2.1. It surfaces LTV cohort quality; CAC must be computed externally and combined for full unit economics analysis.
