---
frontmatter_id: account-engagement-score-trend
slash_command: /account-engagement-score-trend
description: Builds a report that calculates a custom weighted engagement score for each account from user activity and click data. The weighting is arbitrary and not a native product score.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a weekly report scoring each account's engagement from distinct active users and click volume, with flags
    for drops, growth, and single-threaded accounts.
  parameters:
  - name: score_user_weight
    type: number
    label: Weight per distinct active user
    default: 5
  - name: score_activity_weight
    type: number
    label: Weight per click-on event
    default: 0.1
  - name: report_window
    type: duration
    label: Report time range
    default: 12 w
  - name: comparison_window
    type: duration
    label: Recent window for trend flags
    default: 4 w
  - name: baseline_window
    type: duration
    label: Trailing baseline window
    default: 8 w
  - name: drop_threshold
    type: number
    label: Acute drop threshold (percent)
    default: 30
  - name: growth_threshold
    type: number
    label: Expansion growth threshold (percent)
    default: 50
  - name: top_account_count
    type: number
    label: Number of accounts to break down
    default: 30
  - name: highlight_count
    type: number
    label: Top accounts to highlight per list
    default: 5
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
    properties:
    - name: user
      type: text
      meaning: The user who started the session
      optional: false
  - slot: click_event
    kind: event
    meaning: A user clicked on an element in the product
    properties:
    - name: user
      type: text
      meaning: The user who clicked
      optional: false
  - slot: user_account_relation
    kind: attribute
    meaning: The account that a user belongs to
  - slot: account_record
    kind: attribute
    meaning: An account record that groups users into a company
  steps:
  - id: s1
    builds: report
    uses:
    - session_start_event
    - click_event
    - user_account_relation
    - account_record
    - score_user_weight
    - score_activity_weight
    - report_window
    - comparison_window
    - baseline_window
    - drop_threshold
    - growth_threshold
    - top_account_count
    - highlight_count
    instruction: 'Create an Insights report named "Account Engagement Score Trend". Series A: count unique users of {session_start_event}
      rolled up by the account each user belongs to via {user_account_relation}. Series B: count of {click_event} rolled up
      by the account each user belongs to via {user_account_relation}. Series C: computed engagement score per account = (Series
      A x {score_user_weight}) + (Series B x {score_activity_weight}). Use weekly time granularity over the last {report_window},
      with the previous period as comparison. Break down by {account_record} for the top {top_account_count} accounts by current
      engagement score. Chart as a multi-line chart with one line per account, plus a heatmap small-multiple showing week-over-week
      change in score. Annotations: flag accounts whose score dropped more than {drop_threshold} percent over the last {comparison_window}
      versus the trailing {baseline_window} baseline as acute disengagement (churn risk). Flag accounts whose score grew more
      than {growth_threshold} percent over the last {comparison_window} as expansion candidates for sales outreach. Flag accounts
      where Series A is shrinking while Series B is stable as consolidating to a smaller power-user group (single-threaded
      risk). Highlight the top {highlight_count} accounts by absolute score and the top {highlight_count} accounts by week-over-week
      growth rate as two separate lists.'
---

# Account engagement score trend

Slash command: /account-engagement-score-trend

## Step 1: Score account engagement weekly

Create an Insights report called "Account Engagement Score Trend".
Series A: Event "Session start", aggregation: Count Unique Users: rolled up by Users.the account the user belongs to (so each account's score = number of distinct users from that account who emitted a Session start in the period)
Series B: Event "Click on", aggregation: Count, rolled up by Users.the account the user belongs to (raw activity volume per account)
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
- Users.the account the user belongs to is the canonical relation linking users to accounts.
- The Accounts object has 58 attributes including engagement-score relation possibilities.
- Session start and Click on are canonical engagement signals.
