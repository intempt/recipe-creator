---
description: Shows what each rep actually did last month, calls, emails, meetings and tasks, next to the revenue they closed.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - b2b-saas
  - finance
---

# Rep activity leaderboard

Slash command: /rep-activity-leaderboard

## Step 1: Tie rep activity to revenue

Create an Insights report called "Rep Activity Leaderboard".
Series A: Event "Call completed" OR "call_logged", aggregation: Count grouped by owner_id, label: "Calls"
Series B: Event "Messaged email" where direction = outbound (sent emails), aggregation: Count grouped by created_by (the rep), label: "Outbound Emails"
Series C: Event "Meeting scheduled" where canceled_at is null, aggregation: Count grouped by created_by, label: "Meetings Booked"
Series D: Event "Task completed", aggregation: Count grouped by assignee_id, label: "Tasks Completed"
Series E: Sum of Deal won.amount grouped by owner_id (rep's revenue contribution in period), unit: $, label: "Revenue Closed"
Series F: Computed: Series E / Series A × 100, label: "Revenue per 100 Calls"
 - The Gong-popularized leading-indicator metric: ties activity volume to revenue outcomes.
Time range: Last 30 days
Breakdown: By owner_id (per-rep, sortable leaderboard)
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
Taxonomy notes:
- Call completed and call_logged are both canonical (varies by integration: HubSpot/Salesforce typically emit Call completed with metadata; manually-logged calls emit call_logged).
- Messaged email.direction is a canonical property; outbound emails have direction = "outbound".
- Meeting scheduled.canceled_at being null means the meeting wasn't canceled. End_time being in the past indicates it actually occurred.
- Task completed.assignee_id is the rep responsible for the task.
- "Rep" identification varies by event:
 - Call completed: created_by
 - Messaged email: created_by
 - Meeting scheduled: created_by
 - Task completed: assignee_id
 - Deal won: owner_id
 These should all resolve to the same Users object (owner_id is a canonical user-attribute): Lovable's translation layer must unify these for per-rep aggregation.
