---
name: lead-customer-sales
description: |
  Use when a user mentions "lead to customer (sales)", or asks for related help. Sales pipeline funnel using deal stage changes and meeting events with stage velocity and forecasted revenue.
arguments: []
intempt:
  id: lead-customer-sales
  version: 1.0.0
  slashCommand: /lead-customer-sales
  group: Reports
  title: "Lead to customer"
  shortDescription: "Shows how many demo requests turn into booked meetings, completed demos, proposals and closed deals, and which lead sources actually convert."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [b2b]
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
      title: "Trace demo requests to closed deals"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A five step funnel over 60 days from a demo request form to a scheduled meeting, a meeting that actually happened, a proposal stage change and a won deal, split by the top 8 lead sources, with median time between stages and forecast revenue per stage."
      prompt: |
        Create a Funnel report called "Lead to Customer".

        Steps:
        1. Event "Form submitted" where the form matches a demo-request form: "Requested Demo"
           (alternative: Deal created with stage matching "Discovery" or similar)
        2. Event "Meeting scheduled" linked to the user: "Scheduled Demo"
        3. Event "Meeting scheduled" that was not canceled and whose end time is in the past (i.e. the meeting actually happened): "Completed Demo"
        4. Event "Deal stage changed" where the new stage matches a "Proposal" pattern: "Proposal Sent"
        5. Event "Deal won": "Deal Closed"

        Conversion window: 60 days
        Breakdown: By the first-touch lead source on the user record. Top 8 sources.
        Compare: Previous period (prior 60 days)

        For each step, also surface:
        - Median time-to-convert from previous step (stage velocity)
        - Per-source conversion rate at each stage
        - Forecast revenue: Sum of the current deal amount for deals currently at this stage × historical conversion-to-won rate

        Annotations:
        - Flag the lead source with highest end-to-end win rate AND volume: invest more there.
        - Flag any stage where median velocity exceeded 14 days (deal-stalled signal).
        - Highlight any source with rising volume but falling win rate (lead-quality erosion).

        Surface the projected closed-won revenue for the period based on current pipeline volumes.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Lead to customer

Shows how many demo requests turn into booked meetings, completed demos, proposals and closed deals, and which lead sources actually convert.

## What it does

1. **Trace demo requests to closed deals** (`build_funnel_report`)

   A five step funnel over 60 days from a demo request form to a scheduled meeting, a meeting that actually happened, a proposal stage change and a won deal, split by the top 8 lead sources, with median time between stages and forecast revenue per stage.

## What you end up with

- **report** (report): Report produced by this recipe.
