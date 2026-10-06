---
id: quota-attainment-by-rep
title: Quota attainment by rep
slash_command: /quota-attainment-by-rep
group: Reports
owner: intempt
curator: aman
summary: >-
  See revenue by rep to compare each rep's closed revenue over the selected period.
description: >-
  A per-rep view of closed revenue for comparing sales results.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
  industry:
    - b2b-saas
    - finance
  vertical: []
  complexity: quick
  executionMode: live
  tags:
    - insights
prerequisites:
  integrations:
    - value: hubspot
      severity: blocking
      group: crm
    - value: salesforce
      severity: blocking
      group: crm
touches:
  reads:
    - Your HubSpot connection
    - Your Salesforce connection
  writes:
    - A new report, from step 1 "Rank reps on quota hit"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Rank reps on quota hit
    summary: >-
      Closed won revenue per rep against their quota for the last 4 quarters and the current one, shown
      as attainment percentage with a target line at 100%, plus pipeline coverage per rep and a rolling
      12 month attainment figure.
    builds: report
    description: |-
      Create an Insights report called "Quota Attainment by Rep".
      Series A: Sum of deal_won.amount per period, grouped by owner_id, unit: $, label: "Revenue Closed by Rep"
      Series B: Workspace-configured quota per rep per period, unit: $, label: "Quota Target"
       - Sourced from a per-rep quota attribute on the Users object OR from an external integration (HubSpot/Salesforce typically syncs this).
      Series C: Computed: Series A / Series B × 100, unit: %, label: "Quota Attainment %"
      Series D: Sum of all open-deal amounts (current pipeline) per rep / Series B = "Pipeline Coverage Ratio per Rep"
      Series E: Trailing-12-month rolling Series C per rep: the durable performance signal vs. period noise
      Time granularity: Quarterly (the standard quota period for B2B)
      Time range: Last 4 quarters + current quarter
      Breakdown: By owner_id (per-rep)
      Compare: Previous quarter AND same quarter prior year
      Chart type: Sortable horizontal bar chart per rep: bar = Series C (attainment %), with target line at 100%, annotation showing absolute closed revenue and quota; secondary view: trend chart per rep over last 4 quarters
      Sort modes:
      - By Quota Attainment (descending) to "Top Performers"
      - By Pipeline Coverage Ratio (ascending) to "At-Risk Reps" (low coverage = next-quarter shortfall)
      - By Revenue Trend (rolling-12mo) to "Consistent Performers"
      Annotations:
      - Color-code attainment: green ≥100%, yellow 80-99%, red <80%. Industry benchmark: top-quartile sales orgs have 60%+ of reps at ≥100% attainment; struggling teams have <40%.
      - Flag any rep at <50% quota attainment with <2:1 coverage ratio: acute performance risk; needs immediate manager intervention.
      - Flag the gap between top-performer and median: a 3x+ gap indicates skill/territory imbalance worth rebalancing.
      - Surface "ramp" reps (in their first 2 quarters) separately: they're not expected to hit full quota and shouldn't dilute the team-attainment percentage.
      - Highlight the top 3 reps by absolute revenue (not just %): these are the deal-making heavyweights regardless of quota assignment.
      Use case: distinct from rep-activity-leaderboard (which is calls/emails leading indicators): this is the lagging revenue outcome compared to assigned quota. Sales VPs use these together: activity diagnoses, attainment evaluates.
      Taxonomy notes:
      - deal_won.owner_id and deal_won.amount are canonical properties.
      - IMPORTANT (quota dependency: same caveat as forecast-vs-actual-quota) quota targets must be configured. Without quota data, Series B/C return null and the report degrades to absolute revenue-by-rep ranking only.
      - "Open deal amount" for Series D comes from the most-recent deal_stage_changed.amount per deal_id where new_stage is not in closed states.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Quota attainment by rep

See revenue by rep to compare each rep's closed revenue over the selected period.

## Steps

1. **Rank reps on quota hit** (builds report)

   Closed won revenue per rep against their quota for the last 4 quarters and the current one, shown as attainment percentage with a target line at 100%, plus pipeline coverage per rep and a rolling 12 month attainment figure.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Your HubSpot connection
- Your Salesforce connection

Writes:

- A new report, from step 1 "Rank reps on quota hit"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
