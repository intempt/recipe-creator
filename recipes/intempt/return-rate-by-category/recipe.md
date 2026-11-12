---
frontmatter_id: return-rate-by-category
slash_command: /return-rate-by-category
description: Shows which product categories get returned most, and which ones have got worse since last quarter.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows which product categories get returned most and which have worsened since last quarter, as a return-rate report
    with flagged jumps and top-5 lists.
  parameters:
  - name: time_window
    type: duration
    label: Analysis time window
    default: 90 d
    required: false
  - name: comparison_window
    type: duration
    label: Comparison period
    default: 90 d
    required: false
  - name: jump_threshold_pp
    type: number
    label: Flag jump threshold (percentage points)
    default: 5
    required: false
  - name: top_n
    type: number
    label: Number of top categories to surface
    default: 5
    required: false
  requirements:
  - slot: order_fulfilled_event
    kind: event
    meaning: A customer's order was fulfilled
    properties:
    - name: order_id
      type: string
      meaning: Identifier of the fulfilled order
      optional: false
  - slot: return_requested_event
    kind: event
    meaning: A customer requested a return of an order
    properties:
    - name: return_id
      type: string
      meaning: Identifier of the return request
      optional: false
    - name: order_id
      type: string
      meaning: Order the return belongs to
      optional: false
    - name: status
      type: string
      meaning: Current status of the return request
      optional: true
    - name: items
      type: text
      meaning: Items included in the return
      optional: false
  - slot: products_catalog
    kind: product_feed
    meaning: Product catalog containing each product's category
  steps:
  - id: s1
    builds: report
    uses:
    - order_fulfilled_event
    - return_requested_event
    - products_catalog
    - time_window
    - comparison_window
    - jump_threshold_pp
    - top_n
    instruction: 'Create an Insights report titled "Return Rate by Category". Series A: count of {order_fulfilled_event}.
      Series B: count of {return_requested_event}. Formula: (B / A) × 100, unit %, label "Return Rate". Break down by product
      category, resolving each return''s {return_requested_event.items} to a category through {products_catalog}, or else
      through the source order''s items linked by {return_requested_event.order_id}. Time range: last {time_window}. Compare
      against the previous period of {comparison_window}. Chart type: bar chart sorted by return rate descending. Annotations:
      flag any category whose return rate rose by more than {jump_threshold_pp} percentage points versus the prior period.
      Surface the top {top_n} categories by absolute return volume and the top {top_n} by return rate, since the two lists
      usually differ. Note: no canonical return reason property exists on the return event; reason analysis would require
      joining the refund record when a return is monetized.'
---

# Return rate by category

Slash command: /return-rate-by-category

## Step 1: Rank categories by returns

Create an Insights report called "Return Rate by Category".
Series A: Event "Order fulfilled", aggregation: Count
Series B: Event "Return requested", aggregation: Count
Formula: (B / A) × 100, unit: %, label: "Return Rate"
Breakdown: By product category: derive from Return requested.items joined to Products to find category, OR from the source order's items (Return requested carries order_id relation).
Time range: Last 90 days
Compare: Previous period (prior 90 days)
Chart type: Bar chart sorted by total return rate descending
Annotations:
- Flag any category where return rate jumped >5 percentage points vs. prior period.
- Surface top 5 categories by absolute return volume and top 5 by return rate (the lists are usually different and both matter).
Taxonomy notes:
- Return requested has items, order_id (relation), return_id, status. Items resolve to categories through the Products record object.
- Note: there is no canonical "return_reason" property on Return requested. Reason analysis would require joining with Order refunded (which has a reason text field) when the return is monetized.
