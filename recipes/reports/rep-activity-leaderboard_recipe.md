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
  shortDescription: "Per-rep sales activity (calls, emails, meetings, tasks) with revenue-correlation and quota-attainment overlay."
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
      - { value: hubspot, severity: blocking }
      - { value: salesforce, severity: blocking }
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
        Create an Insights report called "Rep Activity Leaderboard".

        Series A: Event "call_completed" OR "call_logged", aggregation: Count grouped by owner_id, label: "Calls"
        Series B: Event "messaged_email" where direction = outbound (sent emails), aggregation: Count grouped by created_by (the rep), label: "Outbound Emails"
        Series C: Event "meeting_scheduled" where canceled_at is null, aggregation: Count grouped by created_by, label: "Meetings Booked"
        Series D: Event "task_completed", aggregation: Count grouped by assignee_id, label: "Tasks Completed"
        Series E: Sum of deal_won.amount grouped by owner_id (rep's revenue contribution in period), unit: $, label: "Revenue Closed"
        Series F: Computed — Series E / Series A × 100, label: "Revenue per 100 Calls"
          - The Gong-popularized leading-indicator metric: ties activity volume to revenue outcomes.

        Time range: Last 30 days
        Breakdown: By owner_id (per-rep, sortable leaderboard)
        Compare: Previous period (prior 30 days)
        Chart type: Sortable table (the leaderboard) with rep name, all activity counts, revenue closed, and the activity-to-revenue ratios. Plus a secondary chart showing activity volume distribution per rep (stacked bar).

        Sort modes (toggle):
        - By Revenue Closed (descending) → "Top Performers"
        - By Calls (descending) → "Most Active"
        - By Revenue per 100 Calls (descending) → "Most Efficient"
        - By Activity Velocity (week-over-week change) → "Rising / Falling Stars"

        Annotations:
        - Flag reps with high activity (top quartile in calls/emails) but low revenue (bottom quartile) — coaching opportunity, likely qualification or close-rate issue.
        - Flag reps with low activity (bottom quartile) but high revenue (top quartile) — outliers worth understanding (might be working strategic accounts, or might be inheriting deals).
        - Highlight any rep whose activity dropped >30% week-over-week (engagement drop — disengagement or PTO; flag for manager check-in).
        - Surface team averages alongside each metric (so any rep can see how they compare).
        - Add the trailing-week revenue-per-call benchmark; below team-average × 0.5 indicates serious efficiency issue.

        Use case: the canonical sales-manager weekly review. Activity metrics are leading indicators (per Gong); revenue is the lagging outcome. Reading them together surfaces both the "rising stars" (activity climbing, revenue about to follow) and the "coaching opportunities" (activity high but revenue stuck).

        Taxonomy notes:
        - call_completed and call_logged are both canonical (varies by integration: HubSpot/Salesforce typically emit call_completed with metadata; manually-logged calls emit call_logged).
        - messaged_email.direction is a canonical property; outbound emails have direction = "outbound".
        - meeting_scheduled.canceled_at being null means the meeting wasn't canceled. End_time being in the past indicates it actually occurred.
        - task_completed.assignee_id is the rep responsible for the task.
        - "Rep" identification varies by event:
          - call_completed: created_by
          - messaged_email: created_by
          - meeting_scheduled: created_by
          - task_completed: assignee_id
          - deal_won: owner_id
          These should all resolve to the same Users object (owner_id is a canonical user-attribute) — Lovable's translation layer must unify these for per-rep aggregation.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Rep Activity Leaderboard

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Rep Activity Leaderboard".

   Series A: Event "call_completed" OR "call_logged", aggregation: Count grouped by owner_id, label: "Calls"
   Series B: Event "messaged_email" where direction = outbound (sent emails), aggregation: Count grouped by created_by (the rep), label: "Outbound Emails"
   Series C: Event "meeting_scheduled" where canceled_at is null, aggregation: Count grouped by created_by, label: "Meetings Booked"
   Series D: Event "task_completed", aggregation: Count grouped by assignee_id, label: "Tasks Completed"
   Series E: Sum of deal_won.amount grouped by owner_id (rep's revenue contribution in period), unit: $, label: "Revenue Closed"
   Series F: Computed — Series E / Series A × 100, label: "Revenue per 100 Calls"
     - The Gong-popularized leading-indicator metric: ties activity volume to revenue outcomes.

   Time range: Last 30 days
   Breakdown: By owner_id (per-rep, sortable leaderboard)
   Compare: Previous period (prior 30 days)
   Chart type: Sortable table (the leaderboard) with rep name, all activity counts, revenue closed, and the activity-to-revenue ratios. Plus a secondary chart showing activity volume distribution per rep (stacked bar).

   Sort modes (toggle):
   - By Revenue Closed (descending) → "Top Performers"
   - By Calls (descending) → "Most Active"
   - By Revenue per 100 Calls (descending) → "Most Efficient"
   - By Activity Velocity (week-over-week change) → "Rising / Falling Stars"

   Annotations:
   - Flag reps with high activity (top quartile in calls/emails) but low revenue (bottom quartile) — coaching opportunity, likely qualification or close-rate issue.
   - Flag reps with low activity (bottom quartile) but high revenue (top quartile) — outliers worth understanding (might be working strategic accounts, or might be inheriting deals).
   - Highlight any rep whose activity dropped >30% week-over-week (engagement drop — disengagement or PTO; flag for manager check-in).
   - Surface team averages alongside each metric (so any rep can see how they compare).
   - Add the trailing-week revenue-per-call benchmark; below team-average × 0.5 indicates serious efficiency issue.

   Use case: the canonical sales-manager weekly review. Activity metrics are leading indicators (per Gong); revenue is the lagging outcome. Reading them together surfaces both the "rising stars" (activity climbing, revenue about to follow) and the "coaching opportunities" (activity high but revenue stuck).

   Taxonomy notes:
   - call_completed and call_logged are both canonical (varies by integration: HubSpot/Salesforce typically emit call_completed with metadata; manually-logged calls emit call_logged).
   - messaged_email.direction is a canonical property; outbound emails have direction = "outbound".
   - meeting_scheduled.canceled_at being null means the meeting wasn't canceled. End_time being in the past indicates it actually occurred.
   - task_completed.assignee_id is the rep responsible for the task.
   - "Rep" identification varies by event:
     - call_completed: created_by
     - messaged_email: created_by
     - meeting_scheduled: created_by
     - task_completed: assignee_id
     - deal_won: owner_id
     These should all resolve to the same Users object (owner_id is a canonical user-attribute) — Lovable's translation layer must unify these for per-rep aggregation.
   ```
