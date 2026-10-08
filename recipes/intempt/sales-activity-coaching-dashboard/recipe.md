---
id: sales-activity-coaching-dashboard
title: Rep activity and coaching
slash_command: /sales-activity-coaching-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: >-
  Shows sales rep activity volume for calls, emails and meetings alongside the revenue it produced, so
  managers can identify coaching needs and performance differences.
description: >-
  Sales Manager dashboard: rep calls, emails and meetings, revenue per call efficiency, and win-loss patterns.
  A coaching view built from activity and revenue data.
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
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the rep leaderboard"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the rep leaderboard
    summary: >-
      Calls, emails and meetings per rep with revenue per call, ranked, alongside win and loss patterns
      and deal hygiene.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Sales Activity & Coaching".
      Persona: Sales Manager or frontline-coach. Question answered: "Which reps need coaching? What patterns differentiate top performers from the rest?"
      Distinct from Sales Pipeline (deal-focused, operational) and Sales Forecasting (period commitment). Sales Activity & Coaching is per-rep frontline-management: the dashboard a manager opens when planning weekly 1:1s.
      Board-level configuration:
      - defaultDateRange: last_30_days
      - exclusionPeriod: none
      - visibility: project
      - boardFilters: none by default; managers typically filter to owner_id IN (their direct reports) at runtime
      - boardBreakdowns: owner_id: pushed down throughout
      Layout: 4 rows.
      Row 1: Activity volume KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: rep-activity-leaderboard, vizType: metric, titleOverride: "Total Calls (Team, 30d)"
      - Card 2: Insights metric to source recipe: rep-activity-leaderboard, vizType: metric, titleOverride: "Total Meetings Booked"
      - Card 3: Insights metric to source recipe: rep-activity-leaderboard, vizType: metric, titleOverride: "Team Revenue per 100 Calls"
      - Card 4: Insights metric to source recipe: quota-attainment-by-rep, vizType: metric, titleOverride: "% Reps at ≥100% Attainment"
      Row 2: The leaderboard (heightPx: 520, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: rep-activity-leaderboard, displayMode: table (the sortable per-rep activity + revenue table: the centerpiece coaching artifact). Sort modes: Top Performers (revenue), Most Active (calls), Most Efficient (revenue per call), Rising/Falling Stars (week-over-week change).
      Row 3: Win-loss patterns (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: win-loss-analysis, displayMode: chart, vizType: bar (won vs. lost by source: ICP fit signal)
      - Card 2: Insights to source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (which stages slow deals down: coaching focus areas)
      Row 4: Strategic deal hygiene (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: multi-threading-coverage-by-deal, displayMode: chart, vizType: stacked_bar (single-threaded deals are coaching opportunities: Gartner data shows they close at 50% lower rates)
      - Card 2: Insights to source recipe: quota-attainment-by-rep, displayMode: chart, vizType: bar (per-rep attainment with team-average benchmark)
      Annotations:
      - Row 1's "Revenue per 100 Calls" is the Gong-popularized leading-indicator metric. Below team-average × 0.5 indicates serious efficiency issue; coach the rep on qualification or talk tracks.
      - Row 2 (the leaderboard, full-width) is the dashboard's centerpiece. Manager workflow: open before weekly 1:1s, sort by "Rising/Falling Stars" to spot trend changes, then drill into specific reps for coaching topics.
      - Row 3 shifts from individual to pattern: which deal types/sources lose? Which stages stall? These are team-level coaching topics, not 1:1 topics.
      - Row 4 surfaces deal-hygiene issues that compound: single-threaded deals are pure coaching gold (advise the rep to multi-thread before proposal stage). Per-rep attainment with team-average overlay surfaces both the bottom (intervention) and top (replicate) of the distribution.
      - Recommended cadence: read this dashboard before weekly 1:1s and Friday team standups. The rising-stars sort changes weekly; the patterns view changes monthly.
      Taxonomy notes:
      - rep-activity-leaderboard pulls from call_completed, call_logged, messaged_email (direction=outbound), meeting_scheduled, task_completed, deal_won: all canonical events.
      - "Rep" identification is unified across events through created_by / assignee_id / owner_id resolving to the same Users object (owner_id is canonical).
      - quota-attainment-by-rep depends on workspace-level quota target configuration: see that recipe's notes.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Rep activity and coaching

Shows sales rep activity volume for calls, emails and meetings alongside the revenue it produced, so managers can identify coaching needs and performance differences.

## Steps

1. **Build the rep leaderboard** (builds dashboard)

   Calls, emails and meetings per rep with revenue per call, ranked, alongside win and loss patterns and deal hygiene.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the rep leaderboard"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
