---
name: account-engagement-score-trend
description: |
  Use when a user mentions "account engagement score trend", or asks for related help. Account-level engagement (rolled up from all users on the account) tracked over time: identifies expansion vs. churn-risk accounts.
arguments: []
intempt:
  id: account-engagement-score-trend
  version: 1.0.0
  slashCommand: /account-engagement-score-trend
  group: Reports
  title: "Account engagement score trend"
  shortDescription: "Scores each account on how many of its users are active and how much they do, weekly, so you can see which accounts are pulling away and which are going quiet."
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
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Score account engagement weekly"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "A weekly engagement score per account over the last 12 weeks, built from the distinct users who started a session plus overall click volume, for the top 30 accounts. Flags accounts down more than 30% in the last 4 weeks and accounts up more than 50%."
      prompt: |
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
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Account engagement score trend

Scores each account on how many of its users are active and how much they do, weekly, so you can see which accounts are pulling away and which are going quiet.

## What it does

1. **Score account engagement weekly** (`build_insights_report`)

   A weekly engagement score per account over the last 12 weeks, built from the distinct users who started a session plus overall click volume, for the top 30 accounts. Flags accounts down more than 30% in the last 4 weeks and accounts up more than 50%.

## What you end up with

- **report** (report): Report produced by this recipe.
