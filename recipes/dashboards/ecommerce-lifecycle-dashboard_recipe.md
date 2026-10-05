---
name: ecommerce-lifecycle-dashboard
description: |
  Use when a user mentions "ecommerce lifecycle dashboard", asks for a crm / retention lead dashboard, or asks for related help. CRM / retention view: lifecycle distribution + migration, replenishment timing, discount cannibalization, and post-purchase paths.
arguments: []
intempt:
  id: ecommerce-lifecycle-dashboard
  version: 1.0.0
  slashCommand: /ecommerce-lifecycle-dashboard
  group: Dashboards
  shortDescription: "A single 'Ecommerce Lifecycle' dashboard canvas with cards for lifecycle distribution, migration, replenishment timing, discount cannibalization, and post-purchase paths."
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
        Create a Dash board (12-column composition canvas) titled "Ecommerce Lifecycle".

        Persona: CRM Lead, Retention Marketer, or Loyalty/Lifecycle Manager. Question answered: "How are customers progressing through their lifecycle, and where do I intervene?"

        Distinct from Customer 360: Customer 360 is the "who are my customers" overview; Lifecycle is the "how do I move them" operational view (migration, replenishment timing, discount mechanics, post-purchase touchpoints).

        Board-level configuration:
        - defaultDateRange: last_90_days
        - exclusionPeriod: incomplete_periods
        - visibility: project
        - boardFilters: none by default
        - boardBreakdowns: lifecycle_score (canonical 6-stage enum)

        Layout: 4 rows.

        Row 1 — Lifecycle health KPIs (heightPx: 200, four metric cards at widthUnits: 3):
        - Card 1: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in Champions"
        - Card 2: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in At Risk"
        - Card 3: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "Largest Migration Last 30d"
        - Card 4: Insights metric → source recipe: discount-impact-on-aov-and-margin, vizType: metric, titleOverride: "Net Revenue Impact of Discounts"

        Row 2 — Lifecycle distribution + migration (heightPx: 480, full-width single card at widthUnits: 12):
        - Card 1: Insights → source recipe: customer-lifecycle-distribution, displayMode: chart (stacked bar + migration flow side panel — the centerpiece)

        Row 3 — Operational levers: timing and discount mechanics (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram — informs replenishment journey timing)
        - Card 2: Insights → source recipe: discount-impact-on-aov-and-margin, displayMode: chart, vizType: bar (per-discount-code AOV impact and net revenue effect)

        Row 4 — Post-purchase journey (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Path → source recipe: post-conversion-onboarding-paths, displayMode: chart (what newly-converted customers do)
        - Card 2: Retention → source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort repeat-purchase by first-order category)

        Annotations:
        - Row 2 (lifecycle distribution + migration, full-width) is the strategic centerpiece.
        - Row 3 turns insight into operational levers.
        - Row 4 closes the loop: post-conversion paths + retention by category.

        Taxonomy notes:
        - Users.lifecycle_score is the canonical 6-stage enum.
        - All source recipes use canonical events: order_created, discount_applied, page_viewed, session_start, subscription_created.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---

# Ecommerce Lifecycle Dashboard

## Procedure

1. **Build Dashboard** [`create_dashboard`] — Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below. → produces: dashboard

   ```text
   Create a Dash board (12-column composition canvas) titled "Ecommerce Lifecycle".

   Persona: CRM Lead, Retention Marketer, or Loyalty/Lifecycle Manager. Question answered: "How are customers progressing through their lifecycle, and where do I intervene?"

   Distinct from Customer 360: Customer 360 is the "who are my customers" overview; Lifecycle is the "how do I move them" operational view (migration, replenishment timing, discount mechanics, post-purchase touchpoints).

   Board-level configuration:
   - defaultDateRange: last_90_days
   - exclusionPeriod: incomplete_periods
   - visibility: project
   - boardFilters: none by default
   - boardBreakdowns: lifecycle_score (canonical 6-stage enum)

   Layout: 4 rows.

   Row 1 — Lifecycle health KPIs (heightPx: 200, four metric cards at widthUnits: 3):
   - Card 1: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in Champions"
   - Card 2: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in At Risk"
   - Card 3: Insights metric → source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "Largest Migration Last 30d"
   - Card 4: Insights metric → source recipe: discount-impact-on-aov-and-margin, vizType: metric, titleOverride: "Net Revenue Impact of Discounts"

   Row 2 — Lifecycle distribution + migration (heightPx: 480, full-width single card at widthUnits: 12):
   - Card 1: Insights → source recipe: customer-lifecycle-distribution, displayMode: chart (stacked bar + migration flow side panel — the centerpiece)

   Row 3 — Operational levers: timing and discount mechanics (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram — informs replenishment journey timing)
   - Card 2: Insights → source recipe: discount-impact-on-aov-and-margin, displayMode: chart, vizType: bar (per-discount-code AOV impact and net revenue effect)

   Row 4 — Post-purchase journey (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Path → source recipe: post-conversion-onboarding-paths, displayMode: chart (what newly-converted customers do)
   - Card 2: Retention → source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort repeat-purchase by first-order category)

   Annotations:
   - Row 2 (lifecycle distribution + migration, full-width) is the strategic centerpiece.
   - Row 3 turns insight into operational levers.
   - Row 4 closes the loop: post-conversion paths + retention by category.

   Taxonomy notes:
   - Users.lifecycle_score is the canonical 6-stage enum.
   - All source recipes use canonical events: order_created, discount_applied, page_viewed, session_start, subscription_created.
   ```
