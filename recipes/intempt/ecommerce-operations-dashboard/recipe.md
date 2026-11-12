---
frontmatter_id: ecommerce-operations-dashboard
slash_command: /ecommerce-operations-dashboard
description: Answers whether orders are shipping on time and where return spikes occur by tracking fulfillment rates, returns, and refunds by product.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Gives operations teams a 30-day dashboard showing whether orders ship on time and where returns and refunds cluster
    by product category.
  parameters:
  - name: dateRange
    type: string
    label: Default date range
    default: last_30_days
  - name: exclusionPeriod
    type: string
    label: Exclusion period (data lag)
    default: today
  - name: fulfillmentTargetPct
    type: number
    label: Fulfillment rate alert threshold (%)
    default: 90
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: order_id
      type: string
      meaning: Identifier of the order
      optional: false
    - name: product_category
      type: string
      meaning: Category of the items in the order
      optional: true
  - slot: order_fulfilled_event
    kind: event
    meaning: An order was fulfilled and shipped
    properties:
    - name: order_id
      type: string
      meaning: Identifier of the order
      optional: false
  - slot: order_refunded_event
    kind: event
    meaning: An order was refunded
    properties:
    - name: order_id
      type: string
      meaning: Identifier of the order
      optional: false
    - name: product_category
      type: string
      meaning: Category of the refunded product
      optional: true
  - slot: order_cancelled_event
    kind: event
    meaning: An order was cancelled
    properties:
    - name: order_id
      type: string
      meaning: Identifier of the order
      optional: false
  - slot: ticket_created_event
    kind: event
    meaning: A customer support ticket was created
  - slot: checkout_step_event
    kind: event
    meaning: A customer progressed through a checkout step
    properties:
    - name: checkout_step
      type: string
      meaning: Name of the checkout step reached
      optional: false
  - slot: operations_dashboard_destination
    kind: destination
    meaning: Project space where the operations dashboard is stored and shared with project members
    optional: true
    channel: hubspot
  steps:
  - id: s1
    builds: dashboard
    uses:
    - placed_order_event
    - order_fulfilled_event
    - order_refunded_event
    - order_cancelled_event
    - ticket_created_event
    - checkout_step_event
    - dateRange
    - exclusionPeriod
    - fulfillmentTargetPct
    - operations_dashboard_destination
    instruction: 'Create a 12-column dashboard titled "E-commerce Operations" with project visibility, default date range
      {dateRange}, and an exclusion period of {exclusionPeriod} because operations data lags by hours. Leave board filters
      empty and apply a product_category breakdown, derived from the items in each order, to every card where it applies.
      Build four rows. Row 1 (height 200 px) holds four metric cards, each 3 units wide: ''Orders (30d)'' from the order status
      flow of {placed_order_event}, {order_fulfilled_event}, {order_refunded_event} and {order_cancelled_event}; ''Fulfillment
      Rate'' from the same order status flow, where a value below {fulfillmentTargetPct}% signals a backlog or capacity issue;
      ''Return Rate (30d)'' from the return rate by category; ''Refund Rate (30d)'' from the refund rate by product and category.
      Row 2 (height 400 px) holds two cards, each 6 units wide: a stacked column chart of the order status flow over time
      showing created, fulfilled, refunded and cancelled counts, and a bar histogram with a cumulative line of time-to-ship,
      computed as the difference between the {order_fulfilled_event} created date and the {placed_order_event} created date,
      joined on order_id. Row 3 (height 440 px) holds two 6-unit bar charts: return rate by category and refund rate by product
      and category. Categories with both high return and high refund rates are the inventory-quality problem areas. Row 4
      (height 400 px) holds two 6-unit cards: a funnel-steps chart of per-step checkout friction using {checkout_step_event.checkout_step},
      and a path chart of the paths that precede {ticket_created_event}. Keep the cards non-overlapping and distinct from
      the revenue dashboard, which covers the order-placement stage only.'
---

# Fulfillment, returns and refunds

Slash command: /ecommerce-operations-dashboard

## Step 1: Build the operations board

Create a Dash board (12-column composition canvas) titled "E-commerce Operations".
Persona: Operations Lead, Fulfillment Manager, or Customer Service Lead. Question answered: "Is the post-purchase machine working? Where are quality issues hiding?"
Distinct from the E-commerce Revenue Dashboard: Revenue is "are we selling" (top of order); Operations is "are we delivering" (bottom of order through return). Zero card overlap.
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: today (operations data lags by hours)
- visibility: project
- boardFilters: none by default
- boardBreakdowns: product_category (derived from items): pushed down to applicable cards
Layout: 4 rows.
Row 1: Operational KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: order-status-flow, vizType: metric, titleOverride: "Orders (30d)"
- Card 2: Insights metric to source recipe: order-status-flow, vizType: metric, titleOverride: "Fulfillment Rate"
- Card 3: Insights metric to source recipe: return-rate-by-category, vizType: metric, titleOverride: "Return Rate (30d)"
- Card 4: Insights metric to source recipe: refund-rate-by-product-and-category, vizType: metric, titleOverride: "Refund Rate (30d)"
Row 2: Order flow (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: order-status-flow, displayMode: chart, vizType: stacked_column (created/fulfilled/refunded/cancelled distribution over time)
- Card 2: Insights to source recipe: time-to-ship-distribution, displayMode: chart, vizType: bar (histogram with cumulative line)
Row 3: Quality issues (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: return-rate-by-category, displayMode: chart, vizType: bar
- Card 2: Insights to source recipe: refund-rate-by-product-and-category, displayMode: chart, vizType: bar
Row 4: Pre-purchase friction and support (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Funnel to source recipe: checkout-form-friction, displayMode: chart, vizType: funnel_steps (per-checkout-step friction)
- Card 2: Path to source recipe: support-deflection-paths, displayMode: chart (paths preceding Ticket created: operational quality intelligence)
Annotations:
- Row 1 Card 2 ("Fulfillment Rate") is the operational headline. <90% indicates a backlog or capacity issue.
- Row 2 surfaces the operational tempo (Card 1: order flow over time) and ship-time distribution (Card 2: how fast are we actually shipping). The histogram is more useful than just "average ship time" because it surfaces the long tail.
- Row 3 surfaces post-purchase quality (categories with high return AND high refund rates are the inventory-quality problem children); Row 4 surfaces pre-purchase friction and support load.
Taxonomy notes:
- All source recipes are taxonomy-grounded. order-status-flow and time-to-ship-distribution are new v5 recipes designed specifically for this dashboard's operational use case (replacing earlier inline custom specs).
- Placed order, Order fulfilled, Order refunded, Order cancelled are all canonical events.
- Time-to-ship is computed from (Order fulfilled.Created date − Placed order.Created date) joined on order_id.
