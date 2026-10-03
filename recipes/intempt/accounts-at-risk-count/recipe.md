---
id: accounts-at-risk-count
title: Accounts at risk
slash_command: /accounts-at-risk-count
group: Reports
owner: intempt
summary: Counts the accounts whose usage has dropped far enough to be a churn risk, tracks that count
  weekly, and puts a dollar figure on the revenue attached to them.
description: >-
  Count and trend of accounts whose engagement has declined materially: the canonical CS early-warning
  headline metric.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
    - saas
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Count accounts going quiet"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Count accounts going quiet
    summary: >-
      A weekly count of accounts where active users fell 30% or more against the prior 8 weeks, or the
      main user has not logged in for 14 days, or a high priority ticket was raised in the last 30 days.
      Adds a watch list for 10% to 30% drops and the subscription revenue at risk.
    builds: report
    description: |-
      Create an Insights report called "Accounts at Risk".
      Definition of "at risk":
      An account (Users.primary_account_id) qualifies as at-risk if ALL of the following hold for the trailing 4 weeks vs. the prior 8-week baseline:
       - Distinct active users in the account dropped by ≥30% (count of unique users from the account who emitted a session_start)
       - OR the dominant user (most-active user on the account) has emitted zero session_start events in the last 14 days (champion-departure proxy)
       - OR the account's primary_user_id has emitted ≥1 ticket_created with priority = high or P1 in the last 30 days
      Series A: Count Unique values of primary_account_id satisfying the at-risk criteria, time granularity: Weekly snapshot, label: "Accounts at Risk"
      Series B: Count Unique values of primary_account_id NOT satisfying the criteria but whose engagement dropped 10: 30% (early-warning band), label: "Accounts to Watch"
      Series C: Sum of subscription amount (most-recent active subscription_created.amount) across at-risk accounts: the dollar revenue at risk, unit: $, label: "Revenue at Risk"
      Time range: Last 12 weeks
      Breakdown: By primary_account_id segment if the project has account-tier metadata (Enterprise / Mid-Market / SMB) on the Accounts object; otherwise by trailing-30d engagement-volume bucket
      Compare: Previous period (prior 12 weeks)
      Chart type: Stacked area chart for Series A and B over time, with Series C ($) as a secondary line on a right axis
      Annotations:
      - Flag any week where Series A grew by ≥20% vs. the trailing 4-week average (acute risk spike: investigate what happened that week).
      - Surface the top 5 accounts currently in Series A by subscription amount (highest-value at-risk accounts get priority CSM action).
      - Flag if Series A as % of total active accounts exceeds 15% (broad-base health issue, not isolated account problems).
      - Highlight the dominant trigger: which of the three at-risk criteria fires most often? If "distinct users dropped" dominates, the issue is account-level disengagement; if "champion departure" dominates, the issue is single-threading; if "high-priority tickets" dominates, the issue is product quality.
      Use case: the canonical CS headline metric. Most CS teams maintain this list manually in a spreadsheet; this recipe automates it. Distinct from account-engagement-score-trend (which is the per-account engagement timeline): this is the count headline.
      Taxonomy notes:
      - session_start, ticket_created are canonical events. Users.primary_account_id is the canonical account-level relation.
      - "Champion" identification = the user with the highest count of session_start events on the account in the trailing 30 days. "Departure" = zero session_start events from that user in the last 14 days.
      - ticket_created.priority is a real property; the "high-priority" classification depends on the project's priority enum (typically P1, P2, P3, P4 or High/Medium/Low).
      - Subscription amount lookup: the account's primary_user_id's most-recent active subscription_created.amount, summed across users on the account if the workspace has multi-subscription accounts.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accounts at risk

Counts the accounts whose usage has dropped far enough to be a churn risk, tracks that count weekly, and puts a dollar figure on the revenue attached to them.

## Steps

1. **Count accounts going quiet** (builds report)

   A weekly count of accounts where active users fell 30% or more against the prior 8 weeks, or the main user has not logged in for 14 days, or a high priority ticket was raised in the last 30 days. Adds a watch list for 10% to 30% drops and the subscription revenue at risk.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Count accounts going quiet"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
