---
name: accounts-at-risk-count
description: |
  Use when a user mentions "accounts at risk", or asks for related help. Count and trend of accounts whose engagement has declined materially — the canonical CS early-warning headline metric.
arguments: []
intempt:
  id: accounts-at-risk-count
  version: 1.0.0
  slashCommand: /accounts-at-risk-count
  group: Reports
  shortDescription: "Count and trend of accounts whose engagement has declined materially — the canonical CS early-warning headline metric."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [b2b, saas]
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
        Create an Insights report called "Accounts at Risk".

        Definition of "at risk":
        An account (Users.primary_account_id) qualifies as at-risk if ALL of the following hold for the trailing 4 weeks vs. the prior 8-week baseline:
          - Distinct active users in the account dropped by ≥30% (count of unique users from the account who emitted a session_start)
          - OR the dominant user (most-active user on the account) has emitted zero session_start events in the last 14 days (champion-departure proxy)
          - OR the account's primary_user_id has emitted ≥1 ticket_created with priority = high or P1 in the last 30 days

        Series A: Count Unique values of primary_account_id satisfying the at-risk criteria, time granularity: Weekly snapshot, label: "Accounts at Risk"
        Series B: Count Unique values of primary_account_id NOT satisfying the criteria but whose engagement dropped 10–30% (early-warning band), label: "Accounts to Watch"
        Series C: Sum of subscription amount (most-recent active subscription_created.amount) across at-risk accounts — the dollar revenue at risk, unit: $, label: "Revenue at Risk"

        Time range: Last 12 weeks
        Breakdown: By primary_account_id segment if the project has account-tier metadata (Enterprise / Mid-Market / SMB) on the Accounts object; otherwise by trailing-30d engagement-volume bucket
        Compare: Previous period (prior 12 weeks)
        Chart type: Stacked area chart for Series A and B over time, with Series C ($) as a secondary line on a right axis

        Annotations:
        - Flag any week where Series A grew by ≥20% vs. the trailing 4-week average (acute risk spike — investigate what happened that week).
        - Surface the top 5 accounts currently in Series A by subscription amount (highest-value at-risk accounts get priority CSM action).
        - Flag if Series A as % of total active accounts exceeds 15% (broad-base health issue, not isolated account problems).
        - Highlight the dominant trigger: which of the three at-risk criteria fires most often? If "distinct users dropped" dominates, the issue is account-level disengagement; if "champion departure" dominates, the issue is single-threading; if "high-priority tickets" dominates, the issue is product quality.

        Use case: the canonical CS headline metric. Most CS teams maintain this list manually in a spreadsheet; this recipe automates it. Distinct from account-engagement-score-trend (which is the per-account engagement timeline) — this is the count headline.

        Taxonomy notes:
        - session_start, ticket_created are canonical events. Users.primary_account_id is the canonical account-level relation.
        - "Champion" identification = the user with the highest count of session_start events on the account in the trailing 30 days. "Departure" = zero session_start events from that user in the last 14 days.
        - ticket_created.priority is a real property; the "high-priority" classification depends on the project's priority enum (typically P1, P2, P3, P4 or High/Medium/Low).
        - Subscription amount lookup: the account's primary_user_id's most-recent active subscription_created.amount, summed across users on the account if the workspace has multi-subscription accounts.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Accounts at Risk

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Accounts at Risk".

   Definition of "at risk":
   An account (Users.primary_account_id) qualifies as at-risk if ALL of the following hold for the trailing 4 weeks vs. the prior 8-week baseline:
     - Distinct active users in the account dropped by ≥30% (count of unique users from the account who emitted a session_start)
     - OR the dominant user (most-active user on the account) has emitted zero session_start events in the last 14 days (champion-departure proxy)
     - OR the account's primary_user_id has emitted ≥1 ticket_created with priority = high or P1 in the last 30 days

   Series A: Count Unique values of primary_account_id satisfying the at-risk criteria, time granularity: Weekly snapshot, label: "Accounts at Risk"
   Series B: Count Unique values of primary_account_id NOT satisfying the criteria but whose engagement dropped 10–30% (early-warning band), label: "Accounts to Watch"
   Series C: Sum of subscription amount (most-recent active subscription_created.amount) across at-risk accounts — the dollar revenue at risk, unit: $, label: "Revenue at Risk"

   Time range: Last 12 weeks
   Breakdown: By primary_account_id segment if the project has account-tier metadata (Enterprise / Mid-Market / SMB) on the Accounts object; otherwise by trailing-30d engagement-volume bucket
   Compare: Previous period (prior 12 weeks)
   Chart type: Stacked area chart for Series A and B over time, with Series C ($) as a secondary line on a right axis

   Annotations:
   - Flag any week where Series A grew by ≥20% vs. the trailing 4-week average (acute risk spike — investigate what happened that week).
   - Surface the top 5 accounts currently in Series A by subscription amount (highest-value at-risk accounts get priority CSM action).
   - Flag if Series A as % of total active accounts exceeds 15% (broad-base health issue, not isolated account problems).
   - Highlight the dominant trigger: which of the three at-risk criteria fires most often? If "distinct users dropped" dominates, the issue is account-level disengagement; if "champion departure" dominates, the issue is single-threading; if "high-priority tickets" dominates, the issue is product quality.

   Use case: the canonical CS headline metric. Most CS teams maintain this list manually in a spreadsheet; this recipe automates it. Distinct from account-engagement-score-trend (which is the per-account engagement timeline) — this is the count headline.

   Taxonomy notes:
   - session_start, ticket_created are canonical events. Users.primary_account_id is the canonical account-level relation.
   - "Champion" identification = the user with the highest count of session_start events on the account in the trailing 30 days. "Departure" = zero session_start events from that user in the last 14 days.
   - ticket_created.priority is a real property; the "high-priority" classification depends on the project's priority enum (typically P1, P2, P3, P4 or High/Medium/Low).
   - Subscription amount lookup: the account's primary_user_id's most-recent active subscription_created.amount, summed across users on the account if the workspace has multi-subscription accounts.
   ```
