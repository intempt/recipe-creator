---
name: payment-failure-recovery-funnel
description: |
  Use when a user mentions "payment failure recovery funnel", or asks for related help. Dunning recovery funnel using canonical billing events with per-attempt success rate and revenue-at-risk.
arguments: []
intempt:
  id: payment-failure-recovery-funnel
  version: 1.0.0
  slashCommand: /payment-failure-recovery-funnel
  group: Reports
  title: "Payment recovery funnel"
  shortDescription: "Shows how much failed payment revenue you get back, which retry attempt recovers it, and how much is still at risk."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Follow failed payments to recovery"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A four step funnel over 14 days from a failed invoice payment to opening the recovery email, visiting billing and paying, split by retry attempt number, with the revenue at stake at each stage and a 70% recovery benchmark."
      prompt: |
        Create a Funnel report called "Payment Recovery Funnel".

        Steps:
        1. Event "Invoice payment failed": "Payment Failed"
        2. Event "Email opened" where the email is part of the dunning campaign (filter by the sent email's campaign matching the dunning template): "Opened Recovery Email"
        3. Event "View page" where the page URL contains "/billing" or "/account": "Visited Billing Page"
        4. Event "Invoice paid" within 14 days of step 1 (same customer): "Payment Recovered"

        Conversion window: 14 days
        Breakdown: By the attempt number on the failed invoice payment (1st attempt, 2nd, 3rd, 4th+)
        Compare: Previous period (prior 14 days)

        For each step, also surface:
        - Revenue at stake at this stage (sum of the amount due for users currently at this step)
        - Median time-to-recover for users who reach the final step

        Annotations:
        - Flag the recovery rate (Step 4 / Step 1) and benchmark against 70%.
        - Highlight which attempt number has the lowest recovery rate (later attempts typically recover at lower rates: informs when to escalate to manual outreach).

        Surface the total revenue recovered vs. revenue lost in the period.

        If you need to break failures down by reason, use the Charge failed event's failure code or failure message, since the failed invoice payment itself does not carry a failure reason.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Payment recovery funnel

Shows how much failed payment revenue you get back, which retry attempt recovers it, and how much is still at risk.

## What it does

1. **Follow failed payments to recovery** (`build_funnel_report`)

   A four step funnel over 14 days from a failed invoice payment to opening the recovery email, visiting billing and paying, split by retry attempt number, with the revenue at stake at each stage and a 70% recovery benchmark.

## What you end up with

- **report** (report): Report produced by this recipe.
