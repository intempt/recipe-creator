---
id: pipeline-value-snapshot
title: Pipeline value snapshot
slash_command: /pipeline-value-snapshot
group: Reports
owner: intempt
curator: aman
summary: >-
  Shows the value of your open pipeline today by summing your deal events, broken out by stage.
description: >-
  Open pipeline value built from summed deal events, with a stage breakdown.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
  industry:
    - b2b-saas
  vertical:
    - sales-led
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Value open pipeline by stage"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Value open pipeline by stage
    summary: >-
      Total open deal value grouped by current stage, plus a forecast weighting each deal by its stage's
      win rate from the last 180 days of closed deals, compared with the same snapshot 30 days ago. Flags
      any stage holding more than 40% of the pipeline.
    builds: report
    description: |-
      Create an Insights report called "Pipeline Value Snapshot".
      Series A: Event "deal_stage_changed", scope: most-recent state per deal_id where new_stage is in open stages (not in closed_won, closed_lost, or equivalent terminal stages), aggregation: Sum of "amount", unit: $, label: "Open Pipeline Value"
      Series B: Same as A but with each deal's amount weighted by historical close-rate of its current stage (compute the historical win-rate per stage from trailing-180d closed deals, then multiply each open deal's amount by its current stage's win-rate), label: "Weighted Forecast"
      Series C: Computed: Series A grouped by new_stage / Series A total × 100, unit: %, label: "Pipeline Concentration by Stage"
      Time range: Current snapshot
      Compare: Previous snapshot 30 days ago (point-in-time pipeline shift)
      Breakdown for the chart view: By new_stage (current stage of each open deal)
      Chart type: Horizontal bar chart per stage with Series A as the bar value, Series B as a secondary mark/line, and the previous-snapshot value as a dotted overlay
      Annotations:
      - Add the pipeline-value-to-quota ratio if the workspace has a quota target configured (otherwise skip).
      - Flag if >40% of pipeline value is concentrated in late stages (proposal/negotiation): execution risk if any major deal slips.
      - Flag if >40% of pipeline value is concentrated in early stages (qualification/discovery): pipeline thin on near-term close-able deals.
      - Highlight the largest single deal in the pipeline (by deal_created.amount): single-deal concentration risk.
      - Add a 30-day delta callout: "Pipeline grew/shrank by $X (Y%) vs. 30 days ago. Net change driven primarily by [stage_X movement / new deals / closed deals]."
      Use case: the headline pipeline metric every sales VP and CRO looks at first thing each morning. Distinct from deal-velocity-by-stage (which is about how fast deals move): this is about how much money is currently in motion and where it sits.
      Taxonomy notes:
      - deal_stage_changed carries amount, new_stage, previous_stage, deal_id, currency.
      - "Open" vs "Closed" stage classification depends on the project's lead/deal stage configuration. Standard convention: closed stages are those whose name matches /won|lost|closed/i.
      - Weighted forecast computation requires historical deal data; if trailing-180d closed-deal volume is insufficient (<50 deals), use a fallback weighting (early-stage 10%, mid 30%, late 70%) and flag the imprecision.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Pipeline value snapshot

Shows the value of your open pipeline today by summing your deal events, broken out by stage.

## Steps

1. **Value open pipeline by stage** (builds report)

   Total open deal value grouped by current stage, plus a forecast weighting each deal by its stage's win rate from the last 180 days of closed deals, compared with the same snapshot 30 days ago. Flags any stage holding more than 40% of the pipeline.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Value open pipeline by stage"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
