---
name: ecommerce-operations-dashboard
description: |
  Use when a user mentions "e-commerce operations dashboard", asks for a operations / fulfillment lead dashboard, or asks for related help. Ops / fulfillment view: order flow, fulfillment rate, returns, refunds, and quality issues by product.
arguments: []
intempt:
  id: ecommerce-operations-dashboard
  version: 1.0.0
  slashCommand: /ecommerce-operations-dashboard
  group: Dashboards
  shortDescription: "Create an e-commerce operations dashboard tracking post-purchase order flow, fulfillment rates, returns, and refunds."
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
        Create a Dash board (12-column composition canvas) titled "E-commerce Operations".

        Persona: Operations Lead, Fulfillment Manager, or Customer Service Lead. Question answered: "Is the post-purchase machine working? Where are quality issues hiding?"

        Distinct from the E-commerce Revenue Dashboard: Revenue is "are we selling" (top of order); Operations is "are we delivering" (bottom of order through return). Zero card overlap.

        Board-level configuration:
        - defaultDateRange: last_30_days
        - exclusionPeriod: today (operations data lags by hours)
        - visibility: project
        - boardFilters: none by default
        - boardBreakdowns: product_category (derived from items) — pushed down to applicable cards

        Layout: 4 rows.

        Row 1 — Operational KPIs (heightPx: 200, four metric cards at widthUnits: 3):
        - Card 1: Insights metric → source recipe: order-status-flow, vizType: metric, titleOverride: "Orders (30d)"
        - Card 2: Insights metric → source recipe: order-status-flow, vizType: metric, titleOverride: "Fulfillment Rate"
        - Card 3: Insights metric → source recipe: return-rate-by-category, vizType: metric, titleOverride: "Return Rate (30d)"
        - Card 4: Insights metric → source recipe: refund-rate-by-product-and-category, vizType: metric, titleOverride: "Refund Rate (30d)"

        Row 2 — Order flow (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: order-status-flow, displayMode: chart, vizType: stacked_column (created/fulfilled/refunded/cancelled distribution over time)
        - Card 2: Insights → source recipe: time-to-ship-distribution, displayMode: chart, vizType: bar (histogram with cumulative line)

        Row 3 — Quality issues (heightPx: 440, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: return-rate-by-category, displayMode: chart, vizType: bar
        - Card 2: Insights → source recipe: refund-rate-by-product-and-category, displayMode: chart, vizType: bar

        Row 4 — Pre-purchase friction and support (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Funnel → source recipe: checkout-form-friction, displayMode: chart, vizType: funnel_steps (per-checkout-step friction)
        - Card 2: Path → source recipe: support-deflection-paths, displayMode: chart (paths preceding ticket_created — operational quality intelligence)

        Annotations:
        - Row 1 Card 2 ("Fulfillment Rate") is the operational headline. <90% indicates a backlog or capacity issue.
        - Row 2 surfaces the operational tempo (Card 1: order flow over time) and ship-time distribution (Card 2: how fast are we actually shipping). The histogram is more useful than just "average ship time" because it surfaces the long tail.
        - Row 3 surfaces post-purchase quality (categories with high return AND high refund rates are the inventory-quality problem children); Row 4 surfaces pre-purchase friction and support load.

        Taxonomy notes:
        - All source recipes are taxonomy-grounded. order-status-flow and time-to-ship-distribution are new v5 recipes designed specifically for this dashboard's operational use case (replacing earlier inline custom specs).
        - order_created, order_fulfilled, order_refunded, order_cancelled are all canonical events.
        - Time-to-ship is computed from (order_fulfilled.created_at − order_created.created_at) joined on order_id.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---

# E-commerce Operations Dashboard

## Procedure

1. **Build Dashboard** [`create_dashboard`] — Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below. → produces: dashboard

   ```text
   Create a Dash board (12-column composition canvas) titled "E-commerce Operations".

   Persona: Operations Lead, Fulfillment Manager, or Customer Service Lead. Question answered: "Is the post-purchase machine working? Where are quality issues hiding?"

   Distinct from the E-commerce Revenue Dashboard: Revenue is "are we selling" (top of order); Operations is "are we delivering" (bottom of order through return). Zero card overlap.

   Board-level configuration:
   - defaultDateRange: last_30_days
   - exclusionPeriod: today (operations data lags by hours)
   - visibility: project
   - boardFilters: none by default
   - boardBreakdowns: product_category (derived from items) — pushed down to applicable cards

   Layout: 4 rows.

   Row 1 — Operational KPIs (heightPx: 200, four metric cards at widthUnits: 3):
   - Card 1: Insights metric → source recipe: order-status-flow, vizType: metric, titleOverride: "Orders (30d)"
   - Card 2: Insights metric → source recipe: order-status-flow, vizType: metric, titleOverride: "Fulfillment Rate"
   - Card 3: Insights metric → source recipe: return-rate-by-category, vizType: metric, titleOverride: "Return Rate (30d)"
   - Card 4: Insights metric → source recipe: refund-rate-by-product-and-category, vizType: metric, titleOverride: "Refund Rate (30d)"

   Row 2 — Order flow (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: order-status-flow, displayMode: chart, vizType: stacked_column (created/fulfilled/refunded/cancelled distribution over time)
   - Card 2: Insights → source recipe: time-to-ship-distribution, displayMode: chart, vizType: bar (histogram with cumulative line)

   Row 3 — Quality issues (heightPx: 440, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: return-rate-by-category, displayMode: chart, vizType: bar
   - Card 2: Insights → source recipe: refund-rate-by-product-and-category, displayMode: chart, vizType: bar

   Row 4 — Pre-purchase friction and support (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Funnel → source recipe: checkout-form-friction, displayMode: chart, vizType: funnel_steps (per-checkout-step friction)
   - Card 2: Path → source recipe: support-deflection-paths, displayMode: chart (paths preceding ticket_created — operational quality intelligence)

   Annotations:
   - Row 1 Card 2 ("Fulfillment Rate") is the operational headline. <90% indicates a backlog or capacity issue.
   - Row 2 surfaces the operational tempo (Card 1: order flow over time) and ship-time distribution (Card 2: how fast are we actually shipping). The histogram is more useful than just "average ship time" because it surfaces the long tail.
   - Row 3 surfaces post-purchase quality (categories with high return AND high refund rates are the inventory-quality problem children); Row 4 surfaces pre-purchase friction and support load.

   Taxonomy notes:
   - All source recipes are taxonomy-grounded. order-status-flow and time-to-ship-distribution are new v5 recipes designed specifically for this dashboard's operational use case (replacing earlier inline custom specs).
   - order_created, order_fulfilled, order_refunded, order_cancelled are all canonical events.
   - Time-to-ship is computed from (order_fulfilled.created_at − order_created.created_at) joined on order_id.
   ```
