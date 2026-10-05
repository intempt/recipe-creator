---
name: customer-360-dashboard
description: |
  Use when a user mentions "customer 360 dashboard", asks for a crm / lifecycle lead dashboard, or asks for related help. CRM / Lifecycle view: lifecycle stage distribution, repeat-purchase mechanics, LTV by acquisition cohort.
arguments: []
intempt:
  id: customer-360-dashboard
  version: 1.0.0
  slashCommand: /customer-360-dashboard
  group: Dashboards
  shortDescription: "Build a Customer 360 dashboard canvas with lifecycle stage distribution, repeat-purchase, and LTV by acquisition cohort cards."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: standard
    executionMode: live
    tags: [dashboard]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_dashboard
  procedure:
    - step: 1
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below."
      prompt: |
        Create a Dash board (12-column composition canvas) titled "Customer 360".

        Persona: CRM Lead, Lifecycle Marketer, or Retention/Loyalty Lead. Question answered: "Where are my customers in their lifecycle, and how do they progress?"

        Board-level configuration:
        - defaultDateRange: last_90_days
        - exclusionPeriod: incomplete_periods
        - visibility: project
        - boardFilters: none by default
        - boardBreakdowns: lifecycle_score (the canonical 6-stage Users-object enum: At risk, Needs attention, New customers, Promising, Regulars, Champions)

        Layout: 4 rows.

        Row 1 — Lifecycle KPIs (heightPx: 200, four metric cards at widthUnits: 3):
        - Card 1: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "Total Active Customers"
        - Card 2: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in Champions + Regulars"
        - Card 3: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in At Risk + Needs Attention"
        - Card 4: Insights metric → source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (M6)"

        Row 2 — Lifecycle distribution and migration (heightPx: 440, full-width single card at widthUnits: 12):
        - Card 1: Insights → source recipe: customer-lifecycle-distribution, displayMode: chart (the stacked bar showing all 6 lifecycle stages with the migration view as a side panel)

        Row 3 — Repeat-purchase mechanics (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Retention → source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort by first-purchase month)
        - Card 2: Insights → source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram of days from 1st to 2nd order — informs replenishment journey timing)

        Row 4 — Long-term value (heightPx: 440, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: first-purchase-cohort-ltv-curve, displayMode: chart, vizType: line (cumulative LTV per cohort member)
        - Card 2: Path → source recipe: post-conversion-onboarding-paths, displayMode: chart (what new paying customers do in their first session — the post-purchase moment)

        Annotations:
        - Row 1 KPIs are filtered views of customer-lifecycle-distribution and first-purchase-cohort-ltv-curve — Lovable applies the lifecycle_score IN filter and renders the metric vizType.
        - Row 2 (the full-width lifecycle distribution) is the dashboard's centerpiece. The single most important metric here is the migration view: "147 Regulars moved to At risk this month" is more actionable than any point-in-time percentage.
        - Row 3 surfaces operational levers: the 2nd-order velocity histogram tells you the right replenishment-trigger delay per category.
        - Row 4 closes the loop: which acquisition cohorts produce high-LTV customers, and what does the post-purchase moment look like for newly-converted customers.

        Taxonomy notes:
        - All source recipes use canonical events: order_created (with items, total_price), session_start, page_viewed.
        - Users.lifecycle_score is the canonical 6-stage enum (At risk / Needs attention / New customers / Promising / Regulars / Champions). Do NOT introduce textbook RFM segment names like "Loyal," "VIP," "Hibernating," etc.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---

# Customer 360 Dashboard

## Procedure

1. **Build Dashboard** [`create_dashboard`] — Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below. → produces: dashboard

   ```text
   Create a Dash board (12-column composition canvas) titled "Customer 360".

   Persona: CRM Lead, Lifecycle Marketer, or Retention/Loyalty Lead. Question answered: "Where are my customers in their lifecycle, and how do they progress?"

   Board-level configuration:
   - defaultDateRange: last_90_days
   - exclusionPeriod: incomplete_periods
   - visibility: project
   - boardFilters: none by default
   - boardBreakdowns: lifecycle_score (the canonical 6-stage Users-object enum: At risk, Needs attention, New customers, Promising, Regulars, Champions)

   Layout: 4 rows.

   Row 1 — Lifecycle KPIs (heightPx: 200, four metric cards at widthUnits: 3):
   - Card 1: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "Total Active Customers"
   - Card 2: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in Champions + Regulars"
   - Card 3: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in At Risk + Needs Attention"
   - Card 4: Insights metric → source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (M6)"

   Row 2 — Lifecycle distribution and migration (heightPx: 440, full-width single card at widthUnits: 12):
   - Card 1: Insights → source recipe: customer-lifecycle-distribution, displayMode: chart (the stacked bar showing all 6 lifecycle stages with the migration view as a side panel)

   Row 3 — Repeat-purchase mechanics (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Retention → source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort by first-purchase month)
   - Card 2: Insights → source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram of days from 1st to 2nd order — informs replenishment journey timing)

   Row 4 — Long-term value (heightPx: 440, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: first-purchase-cohort-ltv-curve, displayMode: chart, vizType: line (cumulative LTV per cohort member)
   - Card 2: Path → source recipe: post-conversion-onboarding-paths, displayMode: chart (what new paying customers do in their first session — the post-purchase moment)

   Annotations:
   - Row 1 KPIs are filtered views of customer-lifecycle-distribution and first-purchase-cohort-ltv-curve — Lovable applies the lifecycle_score IN filter and renders the metric vizType.
   - Row 2 (the full-width lifecycle distribution) is the dashboard's centerpiece. The single most important metric here is the migration view: "147 Regulars moved to At risk this month" is more actionable than any point-in-time percentage.
   - Row 3 surfaces operational levers: the 2nd-order velocity histogram tells you the right replenishment-trigger delay per category.
   - Row 4 closes the loop: which acquisition cohorts produce high-LTV customers, and what does the post-purchase moment look like for newly-converted customers.

   Taxonomy notes:
   - All source recipes use canonical events: order_created (with items, total_price), session_start, page_viewed.
   - Users.lifecycle_score is the canonical 6-stage enum (At risk / Needs attention / New customers / Promising / Regulars / Champions). Do NOT introduce textbook RFM segment names like "Loyal," "VIP," "Hibernating," etc.
   ```
