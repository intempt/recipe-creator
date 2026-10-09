---
name: multi-threading-coverage-by-deal
description: |
  Use when a user mentions "multi-threading coverage by deal", or asks for related help. Number of distinct stakeholders engaged per deal: single-threaded deals close at materially lower rates per Gartner.
arguments: []
intempt:
  id: multi-threading-coverage-by-deal
  version: 1.0.0
  slashCommand: /multi-threading-coverage-by-deal
  group: Reports
  title: "Multi threading coverage"
  shortDescription: "Shows how many people you are actually talking to inside each open deal, and how win rates compare between single threaded and multi threaded deals."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [b2b]
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
      title: "Count contacts on each deal"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Distinct stakeholders per open deal, bucketed as single threaded, lightly threaded, multi threaded or deeply threaded and grouped by current stage, with win rates per bucket from the last 12 months of closed deals. Flags late stage deals still on one contact."
      prompt: |
        Create an Insights report called "Multi-Threading Coverage by Deal".

        Series A: Deal stage changed events, scope: per active deal, aggregation: Count unique associated users (the distinct stakeholders attached to the deal across all stage events)
        Series B: Same per-deal computation but counting only Meeting scheduled events linked to the deal (via the associated deals relation): distinct users who actually attended a meeting
        Series C: Computed: Series A bucketed into "Single-threaded (1 contact)" / "Lightly threaded (2-3)" / "Multi-threaded (4-6)" / "Deeply threaded (7+)"
        Breakdown: By deal stage (open deals only, group by current stage from the Deal stage changed new stage)
        Time range: All open deals + last 90 days of closed deals
        Chart type: Stacked bar chart: bar per stage, segments showing the threading-bucket distribution

        Also include a parallel "win-rate by threading level" view:
        - For closed deals (Deal won plus Deal lost) in the last 12 months, compute win rate by threading bucket
        - Surface: single-threaded deals win X%, multi-threaded deals win Y%, with the gap quantified

        Annotations:
        - Flag any open deals (especially in late-stage proposal/negotiation) that are still single-threaded: these are at acute risk and need multi-threading action by the AE.
        - Add the Gartner benchmark: B2B deals with 5+ engaged stakeholders close at 1.8× the rate of single-threaded deals.
        - Highlight the share of pipeline value (sum of deal amount) currently sitting in single-threaded deals: this is the dollar amount at risk.
        - Flag any deals where threading shrank vs. prior period (a stakeholder went silent: investigate champion-departure risk).

        Use case: the standard B2B sales hygiene report. AEs are notoriously single-threaded; this report makes the risk visible and quantifies it in dollars. Top-performing sales orgs make this their #1 weekly review.

        A deal's current threading count is computed across all events linked to the deal: stage changes, meetings scheduled, calls completed and emails sent.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Multi threading coverage

Shows how many people you are actually talking to inside each open deal, and how win rates compare between single threaded and multi threaded deals.

## What it does

1. **Count contacts on each deal** (`build_insights_report`)

   Distinct stakeholders per open deal, bucketed as single threaded, lightly threaded, multi threaded or deeply threaded and grouped by current stage, with win rates per bucket from the last 12 months of closed deals. Flags late stage deals still on one contact.

## What you end up with

- **report** (report): Report produced by this recipe.
