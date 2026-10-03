---
id: pre-churn-behavioral-signals
title: Pre churn behaviour signals
slash_command: /pre-churn-behavioral-signals
group: Reports
owner: intempt
summary: Shows what customers do in the month before they cancel, and which of those actions are genuinely
  unusual compared with customers who stay.
description: >-
  Path to subscription_cancelled with precursor-event ranking by lift over baseline.
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
    - path
steps:
  - id: s1
    title: Rank the signals before a cancel
    summary: >-
      The 7 steps before each cancellation in the 30 days leading up to it, across the last 90 days of
      cancellations and grouped by reason. Every precursor event is ranked by how much more often it appears
      than in a matched active cohort, flagging anything above 50%.
    builds: report
    description: |-
      Create a Path report called "Pre-Churn Behavioral Signals".
      Anchor event: subscription_cancelled
      Direction: backward (looking back from the cancellation event)
      Depth: 7 steps backward
      Window: 30 days before cancellation
      Loop compression: on
      Time range: Last 90 days of cancellations
      Breakdown: By the cancellation reason: subscription_cancelled.reason is a free-text property; cluster reasons before breakdown (e.g. price, fit, feature-gap, churn-without-reason).
      Surface both the top paths (most common precursor sequences) AND a precursor-event ranking:
      Precursor-event ranking computation:
      - For each canonical event type that occurs in the 30 days before cancellation:
       - Compute its frequency in the pre-churn window (cancelled cohort)
       - Compute its frequency in the same 30-day window for a control cohort (active subscribers, matched on plan_name and tenure since subscription_created)
       - Lift = (frequency in churned cohort − frequency in control cohort) / frequency in control cohort × 100
      - Surface the top 10 events by lift
      Annotations:
      - Flag any event whose lift exceeds 50% (occurs >1.5× more often in pre-churn period than in matched active cohort).
      - Surface the median time between the highest-lift event and the cancellation: this is the intervention window.
      - Highlight any "ticket_created" events in the top precursors: high-priority operational issues.
      - Highlight any "invoice_payment_failed" events: distinct from product-fit churn; require dunning remediation.
      Surface the 3 strongest behavioral leading indicators of churn and the typical intervention window.
      Taxonomy notes:
      - subscription_cancelled is canonical; reason is a free-text property requiring clustering.
      - Path engine ranks all canonical events that appear in the backward-window. The "support_ticket_created" event is actually called ticket_created.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Pre churn behaviour signals

Shows what customers do in the month before they cancel, and which of those actions are genuinely unusual compared with customers who stay.

## Steps

1. **Rank the signals before a cancel** (builds report)

   The 7 steps before each cancellation in the 30 days leading up to it, across the last 90 days of cancellations and grouped by reason. Every precursor event is ranked by how much more often it appears than in a matched active cohort, flagging anything above 50%.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
