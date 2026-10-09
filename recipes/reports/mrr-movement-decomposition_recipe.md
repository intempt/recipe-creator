---
name: mrr-movement-decomposition
description: |
  Use when a user mentions "mrr movement decomposition", or asks for related help. The classic SaaS MRR waterfall: new, expansion, contraction, churn, reactivation per month. Requires computing the amount change on each subscription update.
arguments: []
intempt:
  id: mrr-movement-decomposition
  version: 1.0.0
  slashCommand: /mrr-movement-decomposition
  group: Reports
  title: "MRR movement waterfall"
  shortDescription: "Breaks each month's recurring revenue change into new, expansion, contraction, churn and reactivation, so you can see what is really driving growth."
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
  prerequisites:
    integrations:
      - { value: hubspot, severity: blocking, group: subscription-source }
      - { value: shopify, severity: blocking, group: subscription-source }
      - { value: stripe, severity: blocking, group: subscription-source }
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Break MRR into its five parts"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "A monthly waterfall over 12 months: new revenue from first subscriptions, expansion and contraction from the amount change on subscription updates, churn from cancellations and reactivation from resumed subscriptions, plus net new MRR and net revenue retention."
      prompt: |
        Create an Insights report called "MRR Movement Decomposition".

        This is the classic SaaS MRR waterfall. Compute the five movement categories per month:

        New MRR: Sum of the subscription amount on Subscription started events in the period for users who had no active subscription previously, unit: $
        Expansion MRR: From Subscription updated events: for each event, compute (new amount − prior amount on the same subscription). Sum the positive deltas where the change was a plan upgrade or a seat/quantity increase, unit: $
        Contraction MRR: Same Subscription updated computation; sum the negative deltas (will appear as negative values in the waterfall), unit: $
        Churned MRR: Sum of the prior subscription amount for each Subscription canceled event in the period (negative in the waterfall), unit: $
        Reactivation MRR: Sum of the subscription amount on Subscription resumed events where the user previously had a Subscription canceled in the prior 90 days, unit: $

        Net New MRR: New + Expansion + Contraction (negative) + Churned (negative) + Reactivation
        Net Revenue Retention (NRR): (Starting MRR + Expansion + Reactivation − Contraction − Churn) / Starting MRR × 100, unit: %

        Time granularity: Monthly
        Time range: Last 12 months
        Compare: Year-over-year
        Chart type: Waterfall chart per month (New, Expansion, Reactivation as positive stacks; Contraction, Churn as negative stacks; Net New as the connecting line), with a secondary line showing trailing 12-month NRR

        Annotations:
        - Add benchmarks: a healthy SaaS business has Expansion + Reactivation ≥ |Contraction + Churn| (NRR ≥ 100%).
        - Flag any month where Net New MRR went negative.
        - Flag any month where Churned MRR exceeded New MRR.
        - Top-quartile NRR is ≥ 110%; world-class is ≥ 120%.

        Deriving the movement split:
        - Expansion and Contraction are computed by comparing the new amount to the prior amount on each subscription update: positive deltas are expansion, negative deltas are contraction.
        - Reactivation is a resumed (or reactivated) subscription where the same customer had a recent cancellation.
        - This recipe needs subscription state-change events (started, updated, canceled, resumed) flowing reliably from the subscription integration. If subscription updates are sparse, the report degrades to New MRR + Churned MRR only: still valuable but missing the expansion/contraction decomposition.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# MRR movement waterfall

Breaks each month's recurring revenue change into new, expansion, contraction, churn and reactivation, so you can see what is really driving growth.

## Before you run it

- Connect hubspot
- Connect shopify
- Connect stripe

## What it does

1. **Break MRR into its five parts** (`build_insights_report`)

   A monthly waterfall over 12 months: new revenue from first subscriptions, expansion and contraction from the amount change on subscription updates, churn from cancellations and reactivation from resumed subscriptions, plus net new MRR and net revenue retention.

## What you end up with

- **report** (report): Report produced by this recipe.
