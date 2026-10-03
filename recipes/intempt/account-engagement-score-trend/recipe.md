---
id: account-engagement-score-trend
title: Account engagement score trend
slash_command: /account-engagement-score-trend
group: Reports
owner: intempt
summary: Scores each account on how many of its users are active and how much they do, weekly, so you
  can see which accounts are pulling away and which are going quiet.
description: >-
  Account-level engagement (rolled up from all users on the account) tracked over time: identifies expansion
  vs. churn-risk accounts.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
  complexity: quick
  executionMode: live
  tags:
    - insights
steps:
  - id: s1
    title: Score account engagement weekly
    summary: >-
      A weekly engagement score per account over the last 12 weeks, built from the distinct users who
      started a session plus overall click volume, for the top 30 accounts. Flags accounts down more than
      30% in the last 4 weeks and accounts up more than 50%.
    builds: report
    description: |-
      Create an Insights report called "Account Engagement Score Trend".
      Series A: Event "session_start", aggregation: Count Unique Users: rolled up by Users.primary_account_id (so each account's score = number of distinct users from that account who emitted a session_start in the period)
      Series B: Event "click_on", aggregation: Count, rolled up by Users.primary_account_id (raw activity volume per account)
      Series C: Computed engagement score per account = (Series A × 5) + (Series B × 0.1): a weighted blend giving each account a single number reflecting both breadth (distinct users) and depth (activity volume)
      Time granularity: Weekly
      Time range: Last 12 weeks
      Breakdown: By Account record (top 30 accounts by current engagement score)
      Compare: Previous period (prior 12 weeks)
      Chart type: Multi-line chart with one line per account, plus a heatmap small-multiple showing score change week-over-week
      Annotations:
      - Flag accounts whose engagement score dropped >30% in the last 4 weeks vs. trailing 8-week baseline (acute disengagement: churn risk).
      - Flag accounts whose engagement score grew >50% in the last 4 weeks (expansion candidates: sales should reach out).
      - Flag accounts where Series A (distinct users) is shrinking but Series B (activity) is stable: the account is consolidating to a smaller power-user group; risky if that user departs (single-threaded account).
      - Highlight the top 5 accounts by absolute engagement score AND the top 5 by week-over-week growth rate: different lists, both worth sales attention.
      Use case: the canonical B2B account-health view. Single-user metrics miss the real story in B2B; an account where 1 user is hyperactive while 20 others ignore the product is at risk despite high "activity." This recipe rolls up to the account level.
      Taxonomy notes:
      - Users.primary_account_id is the canonical relation linking users to accounts.
      - The Accounts object has 58 attributes including engagement-score relation possibilities.
      - session_start and click_on are canonical engagement signals.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Account engagement score trend

Scores each account on how many of its users are active and how much they do, weekly, so you can see which accounts are pulling away and which are going quiet.

## Steps

1. **Score account engagement weekly** (builds report)

   A weekly engagement score per account over the last 12 weeks, built from the distinct users who started a session plus overall click volume, for the top 30 accounts. Flags accounts down more than 30% in the last 4 weeks and accounts up more than 50%.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
