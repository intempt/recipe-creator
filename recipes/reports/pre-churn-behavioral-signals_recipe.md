---
name: pre-churn-behavioral-signals
description: |
  Use when a user mentions "pre-churn behavioral signal identification", or asks for related help. Path to subscription_cancelled with precursor-event ranking by lift over baseline.
arguments: []
intempt:
  id: pre-churn-behavioral-signals
  version: 1.0.0
  slashCommand: /pre-churn-behavioral-signals
  group: Reports
  title: "Pre churn behaviour signals"
  shortDescription: "Shows what customers do in the month before they cancel, and which of those actions are genuinely unusual compared with customers who stay."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [path]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_paths_report
  procedure:
    - step: 1
      title: "Rank the signals before a cancel"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "The 7 steps before each cancellation in the 30 days leading up to it, across the last 90 days of cancellations and grouped by reason. Every precursor event is ranked by how much more often it appears than in a matched active cohort, flagging anything above 50%."
      prompt: |
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
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Pre churn behaviour signals

Shows what customers do in the month before they cancel, and which of those actions are genuinely unusual compared with customers who stay.

## What it does

1. **Rank the signals before a cancel** (`build_paths_report`)

   The 7 steps before each cancellation in the 30 days leading up to it, across the last 90 days of cancellations and grouped by reason. Every precursor event is ranked by how much more often it appears than in a matched active cohort, flagging anything above 50%.

## What you end up with

- **report** (report): Report produced by this recipe.
