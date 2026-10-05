---
id: support-tickets-vs-churn-correlation
title: Support volume versus churn
slash_command: /support-tickets-vs-churn-correlation
group: Reports
owner: intempt
curator: aman
summary: >-
  Compare weekly support ticket volume with weekly subscription cancellations to see how the counts change
  over time.
description: >-
  A report showing weekly counts of support tickets and subscription cancellations.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Line up tickets against churn"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Line up tickets against churn
    summary: >-
      Weekly ticket counts by priority against cancellations by reason over 12 weeks on a dual axis. Flags
      weeks where high priority tickets ran 50% above the 8 week average and checks whether ticket spikes
      lead churn spikes by the usual 2 to 4 weeks.
    builds: report
    description: |-
      Create an Insights report called "Support Volume vs Churn".
      Series A: Event "ticket_created", aggregation: Count, label: "Tickets"
      Series B: Event "subscription_cancelled", aggregation: Count, label: "Churns"
      Time granularity: Weekly
      Breakdown for Series A: By "priority" property on ticket_created (the canonical event has priority as a property)
      Breakdown for Series B: By "reason" property on subscription_cancelled (text: group by cleaned/tokenized reason categories)
      Time range: Last 12 weeks
      Compare: Previous period (prior 12 weeks)
      Chart type: Dual-axis chart: left axis tickets (stacked area by priority), right axis churns (lines by reason group)
      Annotations:
      - Highlight any week where high-priority tickets exceeded the trailing 8-week average by 50% or more.
      - For each spike in churns, surface the leading 2-week ticket volume: flag if elevated by more than 30% vs. baseline.
      Surface whether high-priority ticket spikes precede churn spikes (typical lag is 2-4 weeks). If correlation is strong, identify which subscription_cancelled.reason categories are most associated with prior support load.
      Taxonomy notes:
      - ticket_created is canonical (no "support_" prefix). Properties: ticket_id, priority, source_type, status, subject.
      - subscription_cancelled (British spelling) carries reason as a free-text field. Cluster reasons before breakdown.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Support volume versus churn

Compare weekly support ticket volume with weekly subscription cancellations to see how the counts change over time.

## Steps

1. **Line up tickets against churn** (builds report)

   Weekly ticket counts by priority against cancellations by reason over 12 weeks on a dual axis. Flags weeks where high priority tickets ran 50% above the 8 week average and checks whether ticket spikes lead churn spikes by the usual 2 to 4 weeks.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Line up tickets against churn"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
