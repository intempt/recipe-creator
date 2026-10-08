---
description: Builds a report that calculates a custom weighted engagement score for each account from user activity and click data. The weighting is arbitrary and not a native product score.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# Account engagement score trend

Slash command: /account-engagement-score-trend

## Step 1: Score account engagement weekly

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
