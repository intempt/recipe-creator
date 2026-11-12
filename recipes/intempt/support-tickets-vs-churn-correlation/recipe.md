---
frontmatter_id: support-tickets-vs-churn-correlation
slash_command: /support-tickets-vs-churn-correlation
description: Compare weekly support ticket volume with weekly subscription cancellations to see how the counts change over time.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Compares weekly support ticket volume with weekly subscription cancellations, flags unusual spikes, and checks
    whether high-priority ticket surges come before churn spikes.
  parameters:
  - name: time_range
    type: duration
    label: Time range to compare
    default: 12 w
    required: false
  - name: spike_threshold_pct
    type: number
    label: High-priority ticket spike threshold (% above trailing average)
    default: 50
    required: false
  - name: trailing_window_weeks
    type: number
    label: Trailing average window (weeks)
    default: 8
    required: false
  - name: churn_spike_lead_threshold_pct
    type: number
    label: Leading ticket volume elevation threshold (%)
    default: 30
    required: false
  requirements:
  - slot: ticket_created_event
    kind: event
    meaning: A customer support ticket was created
    properties:
    - name: priority
      type: text
      meaning: Priority level of the ticket
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: reason
      type: text
      meaning: Free-text reason given for the cancellation, clustered into reason categories
      optional: false
  steps:
  - id: s1
    builds: report
    uses:
    - ticket_created_event
    - subscription_canceled_event
    - time_range
    - spike_threshold_pct
    - trailing_window_weeks
    - churn_spike_lead_threshold_pct
    instruction: 'Create an Insights report called "Support Volume vs Churn". Series A: count of {ticket_created_event} labeled
      "Tickets". Series B: count of {subscription_canceled_event} labeled "Churns". Use weekly time granularity over the last
      {time_range}, and compare against the previous period of the same length. Break down Series A by {ticket_created_event.priority}.
      Break down Series B by cluster of {subscription_canceled_event.reason} into cleaned, tokenized reason categories before
      breakdown. Chart type: dual-axis; left axis shows tickets as a stacked area by priority, right axis shows churns as
      lines by reason group. Annotations: highlight any week where high-priority tickets exceed the trailing {trailing_window_weeks}-week
      average by {spike_threshold_pct}% or more. For each churn spike, show the leading 2-week ticket volume and flag it if
      elevated by more than {churn_spike_lead_threshold_pct}% versus baseline. Surface whether high-priority ticket spikes
      precede churn spikes (typical lag 2-4 weeks). If the correlation is strong, identify which churn reason categories are
      most associated with prior support load.'
---

# Support volume versus churn

Slash command: /support-tickets-vs-churn-correlation

## Step 1: Line up tickets against churn

Create an Insights report called "Support Volume vs Churn".
Series A: Event "Ticket created", aggregation: Count, label: "Tickets"
Series B: Event "Subscription canceled", aggregation: Count, label: "Churns"
Time granularity: Weekly
Breakdown for Series A: By "priority" property on Ticket created (the canonical event has priority as a property)
Breakdown for Series B: By "reason" property on Subscription canceled (text: group by cleaned/tokenized reason categories)
Time range: Last 12 weeks
Compare: Previous period (prior 12 weeks)
Chart type: Dual-axis chart: left axis tickets (stacked area by priority), right axis churns (lines by reason group)
Annotations:
- Highlight any week where high-priority tickets exceeded the trailing 8-week average by 50% or more.
- For each spike in churns, surface the leading 2-week ticket volume: flag if elevated by more than 30% vs. baseline.
Surface whether high-priority ticket spikes precede churn spikes (typical lag is 2-4 weeks). If correlation is strong, identify which Subscription canceled.reason categories are most associated with prior support load.
Taxonomy notes:
- Ticket created is canonical (no "support_" prefix). Properties: ticket_id, priority, source_type, status, subject.
- Subscription canceled (British spelling) carries reason as a free-text field. Cluster reasons before breakdown.
