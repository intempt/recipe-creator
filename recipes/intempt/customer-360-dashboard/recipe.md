---
frontmatter_id: customer-360-dashboard
slash_command: /customer-360-dashboard
description: Displays the breakdown of customers across lifecycle stages and tracks repeat-purchase metrics on a centralized dashboard.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Gives a centralized dashboard of customers across six lifecycle stages, with migration, repeat-purchase timing,
    cohort lifetime value, and post-purchase first-session paths.
  parameters:
  - name: date_range
    type: enum
    label: Default date range
    default: last_90_days
    required: false
    options:
    - last_30_days
    - last_90_days
    - last_12_months
  - name: ltv_window
    type: string
    label: LTV window (cohort months)
    default: M6
    required: false
  requirements:
  - slot: lifecycle_distribution_insight
    kind: knowledge
    meaning: A customer lifecycle distribution insight that breaks customers down by the lifecycle score stages and shows
      stage migration
  - slot: ltv_cohort_insight
    kind: knowledge
    meaning: A first-purchase cohort lifetime value curve insight showing cumulative LTV per cohort
  - slot: retention_analysis
    kind: knowledge
    meaning: A purchase retention analysis that shows retention curves for cohorts by first-purchase month
  - slot: second_order_velocity_insight
    kind: knowledge
    meaning: A post-purchase second-order velocity insight showing days from first to second order
  - slot: post_conversion_paths
    kind: knowledge
    meaning: A post-conversion onboarding paths analysis showing what new paying customers do in their first session
  - slot: customer_placed_order
    kind: event
    meaning: A customer placed an order
    properties:
    - name: items
      type: text
      meaning: Items in the order
      optional: true
    - name: total_price
      type: number
      meaning: Total price of the order
      optional: true
  - slot: users_lifecycle_score
    kind: attribute
    meaning: The lifecycle score of a user with the six stages At risk, Needs attention, New customers, Promising, Regulars,
      Champions
  steps:
  - id: s1
    builds: dashboard
    uses:
    - date_range
    - users_lifecycle_score
    instruction: 'Create a Dash board (12-column composition canvas) titled "Customer 360". Set defaultDateRange to {date_range},
      exclusionPeriod to incomplete_periods, visibility to project, and boardFilters to none by default. Set boardBreakdowns
      to {users_lifecycle_score} using the six canonical stages (At risk, Needs attention, New customers, Promising, Regulars,
      Champions). Persona: CRM Lead, Lifecycle Marketer, or Retention/Loyalty Lead. Question answered: "Where are my customers
      in their lifecycle, and how do they progress?"'
---

# Customer lifecycle overview

Slash command: /customer-360-dashboard

## Step 1: Build the customer 360 board

Create a Dash board (12-column composition canvas) titled "Customer 360".
Persona: CRM Lead, Lifecycle Marketer, or Retention/Loyalty Lead. Question answered: "Where are my customers in their lifecycle, and how do they progress?"
Board-level configuration:
- defaultDateRange: last_90_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default
- boardBreakdowns: Lifecycle score (the canonical 6-stage Users-object enum: At risk, Needs attention, New customers, Promising, Regulars, Champions)
Layout: 4 rows.
Row 1: Lifecycle KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "Total Active Customers"
- Card 2: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in Champions + Regulars"
- Card 3: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in At Risk + Needs Attention"
- Card 4: Insights metric to source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (M6)"
Row 2: Lifecycle distribution and migration (heightPx: 440, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart (the stacked bar showing all 6 lifecycle stages with the migration view as a side panel)
Row 3: Repeat-purchase mechanics (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Retention to source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort by first-purchase month)
- Card 2: Insights to source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram of days from 1st to 2nd order: informs replenishment journey timing)
Row 4: Long-term value (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: first-purchase-cohort-ltv-curve, displayMode: chart, vizType: line (cumulative LTV per cohort member)
- Card 2: Path to source recipe: post-conversion-onboarding-paths, displayMode: chart (what new paying customers do in their first session: the post-purchase moment)
Annotations:
- Row 1 KPIs are filtered views of customer-lifecycle-distribution and first-purchase-cohort-ltv-curve: Lovable applies the Lifecycle score IN filter and renders the metric vizType.
- Row 2 (the full-width lifecycle distribution) is the dashboard's centerpiece. The single most important metric here is the migration view: "147 Regulars moved to At risk this month" is more actionable than any point-in-time percentage.
- Row 3 surfaces operational levers: the 2nd-order velocity histogram tells you the right replenishment-trigger delay per category.
- Row 4 closes the loop: which acquisition cohorts produce high-LTV customers, and what does the post-purchase moment look like for newly-converted customers.
Taxonomy notes:
- All source recipes use canonical events: Placed order (with items, total_price), Session start, View page.
- Users.Lifecycle score is the canonical 6-stage enum (At risk / Needs attention / New customers / Promising / Regulars / Champions). Do NOT introduce textbook RFM segment names like "Loyal," "VIP," "Hibernating," etc.
