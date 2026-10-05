---
name: support-tickets-vs-churn-correlation
description: |
  Use when a user mentions "support tickets vs churn correlation", or asks for related help. Dual-axis support ticket volume vs subscription cancellations with priority decomposition and lead-lag.
arguments: []
intempt:
  id: support-tickets-vs-churn-correlation
  version: 1.0.0
  slashCommand: /support-tickets-vs-churn-correlation
  group: Reports
  shortDescription: "Generate an insights report comparing weekly support ticket creation against subscription cancellations broken down by priority and reason."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
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
        Create an Insights report called "Support Volume vs Churn".

        Series A: Event "ticket_created", aggregation: Count, label: "Tickets"
        Series B: Event "subscription_cancelled", aggregation: Count, label: "Churns"
        Time granularity: Weekly
        Breakdown for Series A: By "priority" property on ticket_created (the canonical event has priority as a property)
        Breakdown for Series B: By "reason" property on subscription_cancelled (text — group by cleaned/tokenized reason categories)
        Time range: Last 12 weeks
        Compare: Previous period (prior 12 weeks)
        Chart type: Dual-axis chart — left axis tickets (stacked area by priority), right axis churns (lines by reason group)

        Annotations:
        - Highlight any week where high-priority tickets exceeded the trailing 8-week average by 50% or more.
        - For each spike in churns, surface the leading 2-week ticket volume — flag if elevated by more than 30% vs. baseline.

        Surface whether high-priority ticket spikes precede churn spikes (typical lag is 2-4 weeks). If correlation is strong, identify which subscription_cancelled.reason categories are most associated with prior support load.

        Taxonomy notes:
        - ticket_created is canonical (no "support_" prefix). Properties: ticket_id, priority, source_type, status, subject.
        - subscription_cancelled (British spelling) carries reason as a free-text field. Cluster reasons before breakdown.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Support Tickets vs Churn Correlation

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Support Volume vs Churn".

   Series A: Event "ticket_created", aggregation: Count, label: "Tickets"
   Series B: Event "subscription_cancelled", aggregation: Count, label: "Churns"
   Time granularity: Weekly
   Breakdown for Series A: By "priority" property on ticket_created (the canonical event has priority as a property)
   Breakdown for Series B: By "reason" property on subscription_cancelled (text — group by cleaned/tokenized reason categories)
   Time range: Last 12 weeks
   Compare: Previous period (prior 12 weeks)
   Chart type: Dual-axis chart — left axis tickets (stacked area by priority), right axis churns (lines by reason group)

   Annotations:
   - Highlight any week where high-priority tickets exceeded the trailing 8-week average by 50% or more.
   - For each spike in churns, surface the leading 2-week ticket volume — flag if elevated by more than 30% vs. baseline.

   Surface whether high-priority ticket spikes precede churn spikes (typical lag is 2-4 weeks). If correlation is strong, identify which subscription_cancelled.reason categories are most associated with prior support load.

   Taxonomy notes:
   - ticket_created is canonical (no "support_" prefix). Properties: ticket_id, priority, source_type, status, subject.
   - subscription_cancelled (British spelling) carries reason as a free-text field. Cluster reasons before breakdown.
   ```
