---
name: multi-threading-coverage-by-deal
description: |
  Use when a user mentions "multi-threading coverage by deal", or asks for related help. Number of distinct stakeholders engaged per deal — single-threaded deals close at materially lower rates per Gartner.
arguments: []
intempt:
  id: multi-threading-coverage-by-deal
  version: 1.0.0
  slashCommand: /multi-threading-coverage-by-deal
  group: Reports
  shortDescription: 'Number of distinct stakeholders engaged per deal: single-threaded deals close at materially lower rates per Gartner.'
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
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Multi-Threading Coverage by Deal".

        Series A: Event "deal_stage_changed", scope: per active deal_id, aggregation: Count Unique users from the user_ids property (the distinct stakeholders attached to the deal across all stage events)
        Series B: Same per-deal computation but counting only meeting_scheduled events linked to the deal (via deal_ids relation) — distinct users who actually attended a meeting
        Series C: Computed — Series A bucketed into "Single-threaded (1 contact)" / "Lightly threaded (2-3)" / "Multi-threaded (4-6)" / "Deeply threaded (7+)"
        Breakdown: By deal stage (open deals only, group by current stage from deal_stage_changed.new_stage)
        Time range: All open deals + last 90 days of closed deals
        Chart type: Stacked bar chart — bar per stage, segments showing the threading-bucket distribution

        Also include a parallel "win-rate by threading level" view:
        - For closed deals (deal_won + deal_lost) in the last 12 months, compute win rate by threading bucket
        - Surface: single-threaded deals win X%, multi-threaded deals win Y%, with the gap quantified

        Annotations:
        - Flag any open deals (especially in late-stage proposal/negotiation) that are still single-threaded — these are at acute risk and need multi-threading action by the AE.
        - Add the Gartner benchmark: B2B deals with 5+ engaged stakeholders close at 1.8× the rate of single-threaded deals.
        - Highlight the share of pipeline value (sum of deal amount) currently sitting in single-threaded deals — this is the dollar amount at risk.
        - Flag any deals where threading shrank vs. prior period (a stakeholder went silent — investigate champion-departure risk).

        Use case: the standard B2B sales hygiene report. AEs are notoriously single-threaded; this report makes the risk visible and quantifies it in dollars. Top-performing sales orgs make this their #1 weekly review.

        Taxonomy notes:
        - deal_stage_changed.user_ids is a relation (multi-value) carrying associated users.
        - meeting_scheduled.user_ids and meeting_scheduled.deal_ids together let us count meeting-attended stakeholders per deal.
        - Deal "current threading count" is computed across all events linked to the deal_id (deal_stage_changed, meeting_scheduled, call_completed, email_sent).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Multi-Threading Coverage by Deal

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Multi-Threading Coverage by Deal".

   Series A: Event "deal_stage_changed", scope: per active deal_id, aggregation: Count Unique users from the user_ids property (the distinct stakeholders attached to the deal across all stage events)
   Series B: Same per-deal computation but counting only meeting_scheduled events linked to the deal (via deal_ids relation) — distinct users who actually attended a meeting
   Series C: Computed — Series A bucketed into "Single-threaded (1 contact)" / "Lightly threaded (2-3)" / "Multi-threaded (4-6)" / "Deeply threaded (7+)"
   Breakdown: By deal stage (open deals only, group by current stage from deal_stage_changed.new_stage)
   Time range: All open deals + last 90 days of closed deals
   Chart type: Stacked bar chart — bar per stage, segments showing the threading-bucket distribution

   Also include a parallel "win-rate by threading level" view:
   - For closed deals (deal_won + deal_lost) in the last 12 months, compute win rate by threading bucket
   - Surface: single-threaded deals win X%, multi-threaded deals win Y%, with the gap quantified

   Annotations:
   - Flag any open deals (especially in late-stage proposal/negotiation) that are still single-threaded — these are at acute risk and need multi-threading action by the AE.
   - Add the Gartner benchmark: B2B deals with 5+ engaged stakeholders close at 1.8× the rate of single-threaded deals.
   - Highlight the share of pipeline value (sum of deal amount) currently sitting in single-threaded deals — this is the dollar amount at risk.
   - Flag any deals where threading shrank vs. prior period (a stakeholder went silent — investigate champion-departure risk).

   Use case: the standard B2B sales hygiene report. AEs are notoriously single-threaded; this report makes the risk visible and quantifies it in dollars. Top-performing sales orgs make this their #1 weekly review.

   Taxonomy notes:
   - deal_stage_changed.user_ids is a relation (multi-value) carrying associated users.
   - meeting_scheduled.user_ids and meeting_scheduled.deal_ids together let us count meeting-attended stakeholders per deal.
   - Deal "current threading count" is computed across all events linked to the deal_id (deal_stage_changed, meeting_scheduled, call_completed, email_sent).
   ```
