---
name: pipeline-value-snapshot
description: |
  Use when a user mentions "pipeline value snapshot", or asks for related help. Current open-pipeline value with stage decomposition, weighted forecast, and concentration risk surfacing.
arguments: []
intempt:
  id: pipeline-value-snapshot
  version: 1.0.0
  slashCommand: /pipeline-value-snapshot
  group: Reports
  title: "Pipeline value snapshot"
  shortDescription: "Shows what your open pipeline is worth today, stage by stage, alongside a forecast weighted by how often each stage actually closes."
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
      title: "Value open pipeline by stage"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Total open deal value grouped by current stage, plus a forecast weighting each deal by its stage's win rate from the last 180 days of closed deals, compared with the same snapshot 30 days ago. Flags any stage holding more than 40% of the pipeline."
      prompt: |
        Create an Insights report called "Pipeline Value Snapshot".

        Series A: Event "Deal stage changed", scope: most-recent state per deal where the new stage is in open stages (not in closed-won, closed-lost, or equivalent terminal stages), aggregation: Sum of the deal amount, unit: $, label: "Open Pipeline Value"
        Series B: Same as A but with each deal's amount weighted by historical close-rate of its current stage (compute the historical win-rate per stage from trailing-180d closed deals, then multiply each open deal's amount by its current stage's win-rate), label: "Weighted Forecast"
        Series C: Computed: Series A grouped by stage / Series A total × 100, unit: %, label: "Pipeline Concentration by Stage"

        Time range: Current snapshot
        Compare: Previous snapshot 30 days ago (point-in-time pipeline shift)
        Breakdown for the chart view: By the current stage of each open deal
        Chart type: Horizontal bar chart per stage with Series A as the bar value, Series B as a secondary mark/line, and the previous-snapshot value as a dotted overlay

        Annotations:
        - Add the pipeline-value-to-quota ratio if the workspace has a quota target configured (otherwise skip).
        - Flag if >40% of pipeline value is concentrated in late stages (proposal/negotiation): execution risk if any major deal slips.
        - Flag if >40% of pipeline value is concentrated in early stages (qualification/discovery): pipeline thin on near-term close-able deals.
        - Highlight the largest single deal in the pipeline (by the deal's amount): single-deal concentration risk.
        - Add a 30-day delta callout: "Pipeline grew/shrank by $X (Y%) vs. 30 days ago. Net change driven primarily by [stage_X movement / new deals / closed deals]."

        Use case: the headline pipeline metric every sales VP and CRO looks at first thing each morning. Distinct from deal-velocity-by-stage (which is about how fast deals move): this is about how much money is currently in motion and where it sits.

        Open versus closed stage classification depends on the project's deal stage setup. By convention, closed stages are those whose name contains won, lost, or closed.

        Weighted forecast computation requires historical deal data. If trailing-180d closed-deal volume is insufficient (fewer than 50 deals), use a fallback weighting (early-stage 10%, mid 30%, late 70%) and flag the imprecision.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Pipeline value snapshot

Shows what your open pipeline is worth today, stage by stage, alongside a forecast weighted by how often each stage actually closes.

## What it does

1. **Value open pipeline by stage** (`build_insights_report`)

   Total open deal value grouped by current stage, plus a forecast weighting each deal by its stage's win rate from the last 180 days of closed deals, compared with the same snapshot 30 days ago. Flags any stage holding more than 40% of the pipeline.

## What you end up with

- **report** (report): Report produced by this recipe.
