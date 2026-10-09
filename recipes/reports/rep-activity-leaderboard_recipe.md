---
name: rep-activity-leaderboard
description: |
  Use when a user mentions "rep activity leaderboard", or asks for related help. Per-rep sales activity (calls, emails, meetings, tasks) with revenue-correlation and quota-attainment overlay.
arguments: []
intempt:
  id: rep-activity-leaderboard
  version: 1.0.0
  slashCommand: /rep-activity-leaderboard
  group: Reports
  title: "Rep activity leaderboard"
  shortDescription: "Shows what each rep actually did last month, calls, emails, meetings and tasks, next to the revenue they closed."
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
      title: "Tie rep activity to revenue"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Per rep over the last 30 days: calls, outbound emails, meetings booked and tasks completed, alongside closed won revenue and revenue per 100 calls, compared with the prior 30 days and sortable on any column."
      prompt: |
        Create an Insights report called "Rep Activity Leaderboard".

        Series A: Event "Call completed" OR "Call logged", aggregation: Count grouped by the rep, label: "Calls"
        Series B: Event "Messaged email" where direction = outbound (sent emails), aggregation: Count grouped by the rep, label: "Outbound Emails"
        Series C: Event "Meeting scheduled" where the meeting was not canceled, aggregation: Count grouped by the rep, label: "Meetings Booked"
        Series D: Event "Task completed", aggregation: Count grouped by the assigned rep, label: "Tasks Completed"
        Series E: Sum of the Deal won amount grouped by the rep (rep's revenue contribution in period), unit: $, label: "Revenue Closed"
        Series F: Computed: Series E / Series A × 100, label: "Revenue per 100 Calls"
          - The Gong-popularized leading-indicator metric: ties activity volume to revenue outcomes.

        Time range: Last 30 days
        Breakdown: By rep (per-rep, sortable leaderboard)
        Compare: Previous period (prior 30 days)
        Chart type: Sortable table (the leaderboard) with rep name, all activity counts, revenue closed, and the activity-to-revenue ratios. Plus a secondary chart showing activity volume distribution per rep (stacked bar).

        Sort modes (toggle):
        - By Revenue Closed (descending) to "Top Performers"
        - By Calls (descending) to "Most Active"
        - By Revenue per 100 Calls (descending) to "Most Efficient"
        - By Activity Velocity (week-over-week change) to "Rising / Falling Stars"

        Annotations:
        - Flag reps with high activity (top quartile in calls/emails) but low revenue (bottom quartile): coaching opportunity, likely qualification or close-rate issue.
        - Flag reps with low activity (bottom quartile) but high revenue (top quartile): outliers worth understanding (might be working strategic accounts, or might be inheriting deals).
        - Highlight any rep whose activity dropped >30% week-over-week (engagement drop: disengagement or PTO; flag for manager check-in).
        - Surface team averages alongside each metric (so any rep can see how they compare).
        - Add the trailing-week revenue-per-call benchmark; below team-average × 0.5 indicates serious efficiency issue.

        Use case: the canonical sales-manager weekly review. Activity metrics are leading indicators (per Gong); revenue is the lagging outcome. Reading them together surfaces both the "rising stars" (activity climbing, revenue about to follow) and the "coaching opportunities" (activity high but revenue stuck).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Rep activity leaderboard

Shows what each rep actually did last month, calls, emails, meetings and tasks, next to the revenue they closed.

## Before you run it

- Connect hubspot
- Connect salesforce

## What it does

1. **Tie rep activity to revenue** (`build_insights_report`)

   Per rep over the last 30 days: calls, outbound emails, meetings booked and tasks completed, alongside closed won revenue and revenue per 100 calls, compared with the prior 30 days and sortable on any column.

## What you end up with

- **report** (report): Report produced by this recipe.
