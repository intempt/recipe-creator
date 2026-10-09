---
description: Compare weekly support ticket volume with weekly subscription cancellations to see how the counts change over time.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - finance
  - media
---

# Support volume versus churn

Slash command: /support-tickets-vs-churn-correlation

## Step 1: Line up tickets against churn

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
