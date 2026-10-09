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
  title: "Support volume versus churn"
  shortDescription: "Puts weekly ticket volume next to cancellations to show whether support spikes tend to come before churn, and by how long."
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
      title: "Line up tickets against churn"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Weekly ticket counts by priority against cancellations by reason over 12 weeks on a dual axis. Flags weeks where high priority tickets ran 50% above the 8 week average and checks whether ticket spikes lead churn spikes by the usual 2 to 4 weeks."
      prompt: |
        Create an Insights report called "Support Volume vs Churn".

        Series A: Event "Ticket created", aggregation: Count, label: "Tickets"
        Series B: Event "Subscription canceled", aggregation: Count, label: "Churns"
        Time granularity: Weekly
        Breakdown for Series A: By ticket priority
        Breakdown for Series B: By cancellation reason (text: group by cleaned/tokenized reason categories)
        Time range: Last 12 weeks
        Compare: Previous period (prior 12 weeks)
        Chart type: Dual-axis chart: left axis tickets (stacked area by priority), right axis churns (lines by reason group)

        Annotations:
        - Highlight any week where high-priority tickets exceeded the trailing 8-week average by 50% or more.
        - For each spike in churns, surface the leading 2-week ticket volume: flag if elevated by more than 30% vs. baseline.

        Surface whether high-priority ticket spikes precede churn spikes (typical lag is 2-4 weeks). If correlation is strong, identify which cancellation reason categories are most associated with prior support load.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Support volume versus churn

Puts weekly ticket volume next to cancellations to show whether support spikes tend to come before churn, and by how long.

## What it does

1. **Line up tickets against churn** (`build_insights_report`)

   Weekly ticket counts by priority against cancellations by reason over 12 weeks on a dual axis. Flags weeks where high priority tickets ran 50% above the 8 week average and checks whether ticket spikes lead churn spikes by the usual 2 to 4 weeks.

## What you end up with

- **report** (report): Report produced by this recipe.
