---
name: accounts-at-risk-count
description: |
  Use when a user mentions "accounts at risk", or asks for related help. Count and trend of accounts whose engagement has declined materially: the canonical CS early-warning headline metric.
arguments: []
intempt:
  id: accounts-at-risk-count
  version: 1.0.0
  slashCommand: /accounts-at-risk-count
  group: Reports
  title: "Accounts at risk"
  shortDescription: "Counts the accounts whose usage has dropped far enough to be a churn risk, tracks that count weekly, and puts a dollar figure on the revenue attached to them."
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
      title: "Count accounts going quiet"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "A weekly count of accounts where active users fell 30% or more against the prior 8 weeks, or the main user has not logged in for 14 days, or a high priority ticket was raised in the last 30 days. Adds a watch list for 10% to 30% drops and the subscription revenue at risk."
      prompt: |
        Create an Insights report called "Accounts at Risk".

        Definition of "at risk":
        An account qualifies as at-risk if ALL of the following hold for the trailing 4 weeks vs. the prior 8-week baseline:
          - Distinct active users in the account dropped by ≥30% (count of unique users from the account who started a session)
          - OR the dominant user (most-active user on the account) has started zero sessions in the last 14 days (champion-departure proxy)
          - OR the account's main user has raised ≥1 support ticket with priority = high or P1 in the last 30 days

        Series A: Count Unique accounts satisfying the at-risk criteria, time granularity: Weekly snapshot, label: "Accounts at Risk"
        Series B: Count Unique accounts NOT satisfying the criteria but whose engagement dropped 10: 30% (early-warning band), label: "Accounts to Watch"
        Series C: Sum of subscription amount (the most-recent active subscription amount) across at-risk accounts: the dollar revenue at risk, unit: $, label: "Revenue at Risk"

        Time range: Last 12 weeks
        Breakdown: By account segment if the project has account-tier metadata (Enterprise / Mid-Market / SMB) on the account; otherwise by trailing-30d engagement-volume bucket
        Compare: Previous period (prior 12 weeks)
        Chart type: Stacked area chart for Series A and B over time, with Series C ($) as a secondary line on a right axis

        Annotations:
        - Flag any week where Series A grew by ≥20% vs. the trailing 4-week average (acute risk spike: investigate what happened that week).
        - Surface the top 5 accounts currently in Series A by subscription amount (highest-value at-risk accounts get priority CSM action).
        - Flag if Series A as % of total active accounts exceeds 15% (broad-base health issue, not isolated account problems).
        - Highlight the dominant trigger: which of the three at-risk criteria fires most often? If "distinct users dropped" dominates, the issue is account-level disengagement; if "champion departure" dominates, the issue is single-threading; if "high-priority tickets" dominates, the issue is product quality.

        Use case: the canonical CS headline metric. Most CS teams maintain this list manually in a spreadsheet; this recipe automates it. Distinct from account-engagement-score-trend (which is the per-account engagement timeline): this is the count headline.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Accounts at risk

Counts the accounts whose usage has dropped far enough to be a churn risk, tracks that count weekly, and puts a dollar figure on the revenue attached to them.

## What it does

1. **Count accounts going quiet** (`build_insights_report`)

   A weekly count of accounts where active users fell 30% or more against the prior 8 weeks, or the main user has not logged in for 14 days, or a high priority ticket was raised in the last 30 days. Adds a watch list for 10% to 30% drops and the subscription revenue at risk.

## What you end up with

- **report** (report): Report produced by this recipe.
