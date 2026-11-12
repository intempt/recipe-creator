---
frontmatter_id: ecommerce-lifecycle-dashboard
slash_command: /ecommerce-lifecycle-dashboard
description: Shows lifecycle distribution, when shoppers reorder, and whether discount codes add revenue or eat into it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Gives the team a lifecycle board showing how customers move between stages, when they reorder, and whether discount
    codes add or cut revenue.
  parameters:
  - name: dateRange
    type: enum
    label: Default date range
    default: last_90_days
    required: false
    options:
    - last_30_days
    - last_90_days
    - last_365_days
  - name: migrationWindow
    type: duration
    label: Migration look-back window
    default: 30 d
    required: false
  - name: boardVisibility
    type: enum
    label: Board visibility
    default: project
    required: false
    options:
    - project
    - private
  requirements:
  - slot: lifecycle_distribution_insight
    kind: knowledge
    meaning: A customer lifecycle distribution analysis across the six lifecycle score stages with stage migration flows
  - slot: discount_impact_insight
    kind: knowledge
    meaning: A discount impact analysis showing average order value and margin effect per discount code
  - slot: second_order_velocity_insight
    kind: knowledge
    meaning: An analysis of the time between a customer's first and second order
  - slot: post_conversion_paths_insight
    kind: knowledge
    meaning: An analysis of what newly converted customers do after their first purchase
  - slot: purchase_retention_insight
    kind: knowledge
    meaning: A cohort repeat-purchase retention analysis by first-order category
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: discount_code
      type: text
      meaning: Discount code applied to the order
      optional: true
  - slot: discount_applied_event
    kind: event
    meaning: A customer applied a discount code
  - slot: lifecycle_score_attribute
    kind: attribute
    meaning: The customer's lifecycle score stage (six-stage enum)
  steps:
  - id: s1
    builds: dashboard
    uses:
    - dateRange
    - boardVisibility
    - lifecycle_score_attribute
    instruction: 'Create a 12-column dashboard titled "Ecommerce Lifecycle" with visibility {boardVisibility}, default date
      range {dateRange}, incomplete periods excluded, no board filters by default, and breakdown by {lifecycle_score_attribute}
      using the six-stage enum. Lay it out in 4 rows: a row of four 200px metric cards, a full-width 480px lifecycle distribution
      chart, a row of two 400px operational cards, and a row of two 400px post-purchase cards.'
---

# Ecommerce lifecycle and retention

Slash command: /ecommerce-lifecycle-dashboard

## Step 1: Build the lifecycle board

Create a Dash board (12-column composition canvas) titled "Ecommerce Lifecycle".
Persona: CRM Lead, Retention Marketer, or Loyalty/Lifecycle Manager. Question answered: "How are customers progressing through their lifecycle, and where do I intervene?"
Distinct from Customer 360: Customer 360 is the "who are my customers" overview; Lifecycle is the "how do I move them" operational view (migration, replenishment timing, discount mechanics, post-purchase touchpoints).
Board-level configuration:
- defaultDateRange: last_90_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default
- boardBreakdowns: Lifecycle score (canonical 6-stage enum)
Layout: 4 rows.
Row 1: Lifecycle health KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in Champions"
- Card 2: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in At Risk"
- Card 3: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "Largest Migration Last 30d"
- Card 4: Insights metric to source recipe: discount-impact-on-aov-and-margin, vizType: metric, titleOverride: "Net Revenue Impact of Discounts"
Row 2: Lifecycle distribution + migration (heightPx: 480, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart (stacked bar + migration flow side panel: the centerpiece)
Row 3: Operational levers: timing and discount mechanics (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram: informs replenishment journey timing)
- Card 2: Insights to source recipe: discount-impact-on-aov-and-margin, displayMode: chart, vizType: bar (per-discount-code AOV impact and net revenue effect)
Row 4: Post-purchase journey (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Path to source recipe: post-conversion-onboarding-paths, displayMode: chart (what newly-converted customers do)
- Card 2: Retention to source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort repeat-purchase by first-order category)
Annotations:
- Row 2 (lifecycle distribution + migration, full-width) is the strategic centerpiece.
- Row 3 turns insight into operational levers.
- Row 4 closes the loop: post-conversion paths + retention by category.
Taxonomy notes:
- Users.Lifecycle score is the canonical 6-stage enum.
- All source recipes use canonical events: Placed order, discount_applied, View page, Session start, Subscription started.
