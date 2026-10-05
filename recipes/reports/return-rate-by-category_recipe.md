---
name: return-rate-by-category
description: |
  Use when a user mentions "return rate by category", or asks for related help. Return rate by product category with previous-period comparison and rising-rate flagging.
arguments: []
intempt:
  id: return-rate-by-category
  version: 1.0.0
  slashCommand: /return-rate-by-category
  group: Reports
  shortDescription: "A bar-chart Insights report showing return rate by product category over the last 90 days versus the prior 90 days, with rising categories flagged."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Return Rate by Category".

        Series A: Event "order_fulfilled", aggregation: Count
        Series B: Event "return_requested", aggregation: Count
        Formula: (B / A) × 100, unit: %, label: "Return Rate"
        Breakdown: By product category — derive from return_requested.items joined to Products to find category, OR from the source order's items (return_requested carries order_id relation).
        Time range: Last 90 days
        Compare: Previous period (prior 90 days)
        Chart type: Bar chart sorted by total return rate descending

        Annotations:
        - Flag any category where return rate jumped >5 percentage points vs. prior period.
        - Surface top 5 categories by absolute return volume and top 5 by return rate (the lists are usually different and both matter).

        Taxonomy notes:
        - return_requested has items, order_id (relation), return_id, status. Items resolve to categories through the Products record object.
        - Note: there is no canonical "return_reason" property on return_requested. Reason analysis would require joining with order_refunded (which has a reason text field) when the return is monetized.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Return Rate by Category

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Return Rate by Category".

   Series A: Event "order_fulfilled", aggregation: Count
   Series B: Event "return_requested", aggregation: Count
   Formula: (B / A) × 100, unit: %, label: "Return Rate"
   Breakdown: By product category — derive from return_requested.items joined to Products to find category, OR from the source order's items (return_requested carries order_id relation).
   Time range: Last 90 days
   Compare: Previous period (prior 90 days)
   Chart type: Bar chart sorted by total return rate descending

   Annotations:
   - Flag any category where return rate jumped >5 percentage points vs. prior period.
   - Surface top 5 categories by absolute return volume and top 5 by return rate (the lists are usually different and both matter).

   Taxonomy notes:
   - return_requested has items, order_id (relation), return_id, status. Items resolve to categories through the Products record object.
   - Note: there is no canonical "return_reason" property on return_requested. Reason analysis would require joining with order_refunded (which has a reason text field) when the return is monetized.
   ```
