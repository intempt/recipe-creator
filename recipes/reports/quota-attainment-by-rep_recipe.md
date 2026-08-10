---
name: quota-attainment-by-rep
description: |
  Use when a user mentions "quota attainment by rep", or asks for related help. Per-rep quota attainment (% of target hit) with trend, coverage ratio, and ranking — the headline sales-manager metric.
arguments: []
intempt:
  id: quota-attainment-by-rep
  version: 1.0.0
  slashCommand: /quota-attainment-by-rep
  group: Reports
  shortDescription: "Per-rep quota attainment (% of target hit) with trend, coverage ratio, and ranking — the headline sales-manager metric."
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
  prerequisites:
    integrations:
      - { value: hubspot, severity: blocking, group: crm }
      - { value: salesforce, severity: blocking, group: crm }
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
        Create an Insights report called "Quota Attainment by Rep".

        Series A: Sum of deal_won.amount per period, grouped by owner_id, unit: $, label: "Revenue Closed by Rep"
        Series B: Workspace-configured quota per rep per period, unit: $, label: "Quota Target"
          - Sourced from a per-rep quota attribute on the Users object OR from an external integration (HubSpot/Salesforce typically syncs this).
        Series C: Computed — Series A / Series B × 100, unit: %, label: "Quota Attainment %"
        Series D: Sum of all open-deal amounts (current pipeline) per rep / Series B = "Pipeline Coverage Ratio per Rep"
        Series E: Trailing-12-month rolling Series C per rep — the durable performance signal vs. period noise

        Time granularity: Quarterly (the standard quota period for B2B)
        Time range: Last 4 quarters + current quarter
        Breakdown: By owner_id (per-rep)
        Compare: Previous quarter AND same quarter prior year
        Chart type: Sortable horizontal bar chart per rep — bar = Series C (attainment %), with target line at 100%, annotation showing absolute closed revenue and quota; secondary view: trend chart per rep over last 4 quarters

        Sort modes:
        - By Quota Attainment (descending) → "Top Performers"
        - By Pipeline Coverage Ratio (ascending) → "At-Risk Reps" (low coverage = next-quarter shortfall)
        - By Revenue Trend (rolling-12mo) → "Consistent Performers"

        Annotations:
        - Color-code attainment: green ≥100%, yellow 80-99%, red <80%. Industry benchmark: top-quartile sales orgs have 60%+ of reps at ≥100% attainment; struggling teams have <40%.
        - Flag any rep at <50% quota attainment with <2:1 coverage ratio — acute performance risk; needs immediate manager intervention.
        - Flag the gap between top-performer and median: a 3x+ gap indicates skill/territory imbalance worth rebalancing.
        - Surface "ramp" reps (in their first 2 quarters) separately — they're not expected to hit full quota and shouldn't dilute the team-attainment percentage.
        - Highlight the top 3 reps by absolute revenue (not just %) — these are the deal-making heavyweights regardless of quota assignment.

        Use case: distinct from rep-activity-leaderboard (which is calls/emails leading indicators) — this is the lagging revenue outcome compared to assigned quota. Sales VPs use these together: activity diagnoses, attainment evaluates.

        Taxonomy notes:
        - deal_won.owner_id and deal_won.amount are canonical properties.
        - IMPORTANT — quota dependency: same caveat as forecast-vs-actual-quota — quota targets must be configured. Without quota data, Series B/C return null and the report degrades to absolute revenue-by-rep ranking only.
        - "Open deal amount" for Series D comes from the most-recent deal_stage_changed.amount per deal_id where new_stage is not in closed states.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Quota Attainment by Rep

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Quota Attainment by Rep".

   Series A: Sum of deal_won.amount per period, grouped by owner_id, unit: $, label: "Revenue Closed by Rep"
   Series B: Workspace-configured quota per rep per period, unit: $, label: "Quota Target"
     - Sourced from a per-rep quota attribute on the Users object OR from an external integration (HubSpot/Salesforce typically syncs this).
   Series C: Computed — Series A / Series B × 100, unit: %, label: "Quota Attainment %"
   Series D: Sum of all open-deal amounts (current pipeline) per rep / Series B = "Pipeline Coverage Ratio per Rep"
   Series E: Trailing-12-month rolling Series C per rep — the durable performance signal vs. period noise

   Time granularity: Quarterly (the standard quota period for B2B)
   Time range: Last 4 quarters + current quarter
   Breakdown: By owner_id (per-rep)
   Compare: Previous quarter AND same quarter prior year
   Chart type: Sortable horizontal bar chart per rep — bar = Series C (attainment %), with target line at 100%, annotation showing absolute closed revenue and quota; secondary view: trend chart per rep over last 4 quarters

   Sort modes:
   - By Quota Attainment (descending) → "Top Performers"
   - By Pipeline Coverage Ratio (ascending) → "At-Risk Reps" (low coverage = next-quarter shortfall)
   - By Revenue Trend (rolling-12mo) → "Consistent Performers"

   Annotations:
   - Color-code attainment: green ≥100%, yellow 80-99%, red <80%. Industry benchmark: top-quartile sales orgs have 60%+ of reps at ≥100% attainment; struggling teams have <40%.
   - Flag any rep at <50% quota attainment with <2:1 coverage ratio — acute performance risk; needs immediate manager intervention.
   - Flag the gap between top-performer and median: a 3x+ gap indicates skill/territory imbalance worth rebalancing.
   - Surface "ramp" reps (in their first 2 quarters) separately — they're not expected to hit full quota and shouldn't dilute the team-attainment percentage.
   - Highlight the top 3 reps by absolute revenue (not just %) — these are the deal-making heavyweights regardless of quota assignment.

   Use case: distinct from rep-activity-leaderboard (which is calls/emails leading indicators) — this is the lagging revenue outcome compared to assigned quota. Sales VPs use these together: activity diagnoses, attainment evaluates.

   Taxonomy notes:
   - deal_won.owner_id and deal_won.amount are canonical properties.
   - IMPORTANT — quota dependency: same caveat as forecast-vs-actual-quota — quota targets must be configured. Without quota data, Series B/C return null and the report degrades to absolute revenue-by-rep ranking only.
   - "Open deal amount" for Series D comes from the most-recent deal_stage_changed.amount per deal_id where new_stage is not in closed states.
   ```
