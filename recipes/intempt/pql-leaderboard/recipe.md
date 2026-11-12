---
frontmatter_id: pql-leaderboard
slash_command: /pql-leaderboard
description: Scores free users with a custom formula and includes contact details, so sales can prioritize outreach.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Ranks free or trial users who show strong buying intent into a sales leaderboard, with contact details, scores,
    and account-level grouping so sales can prioritize outreach.
  parameters:
  - name: window
    type: duration
    label: PQL rolling window
    default: 14 d
    required: false
  - name: min_sessions
    type: number
    label: Minimum distinct session days
    default: 3
    required: false
  - name: min_goal_completions
    type: number
    label: Minimum activation journey goal completions
    default: 1
    required: false
  - name: min_core_clicks
    type: number
    label: Minimum clicks on core feature targets
    default: 10
    required: false
  - name: core_target_pattern
    type: text
    label: Core feature target id pattern
    default: core-feature*
    required: false
  - name: high_fit_utm_sources
    type: text
    label: High-fit UTM sources (ICP filter, comma separated)
    required: false
  - name: account_pqa_threshold
    type: number
    label: PQL count at one account that marks a PQA
    default: 3
    required: false
  - name: stale_days_threshold
    type: number
    label: Days over threshold without sales contact before flagging
    default: 7
    required: false
  - name: benchmark_low
    type: number
    label: Low PQL-to-paid conversion benchmark (%)
    default: 10
    required: false
  - name: benchmark_healthy_low
    type: number
    label: Healthy PQL-to-paid conversion lower bound (%)
    default: 15
    required: false
  - name: benchmark_healthy_high
    type: number
    label: Healthy PQL-to-paid conversion upper bound (%)
    default: 30
    required: false
  - name: benchmark_high
    type: number
    label: High PQL-to-paid conversion benchmark (%)
    default: 35
    required: false
  - name: trend_weeks
    type: number
    label: Trend history in weeks
    default: 12
    required: false
  requirements:
  - slot: session_event
    kind: event
    meaning: A user started a session in the product
    properties:
    - name: session_day
      type: date
      meaning: Calendar day of the session start
      optional: false
  - slot: journey_goal_event
    kind: event
    meaning: A user completed a goal in the activation journey
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey the goal belongs to
      optional: false
    - name: goal_id
      type: string
      meaning: Identifier of the completed goal
      optional: true
  - slot: click_event
    kind: event
    meaning: A user clicked an element in the product
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element
      optional: false
  - slot: subscription_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: trial_end
      type: date
      meaning: Trial end date, if the subscription started with a trial
      optional: true
    - name: plan_type
      type: string
      meaning: Whether the subscription is paid or trial
      optional: true
  - slot: user_profile
    kind: attribute
    meaning: Users with name, email, account they belong to, UTM source, first seen and last seen dates
  - slot: user_account
    kind: attribute
    meaning: The account (company) a user belongs to, used to group users into accounts
  - slot: pql_segment
    kind: segment
    meaning: Users currently in the product qualified lead state
    creatable: true
    definition: users with no active subscription or with a trial subscription, who have {session_event} on at least {min_sessions}
      different days, at least {min_goal_completions} {journey_goal_event} within {window}, and at least {min_core_clicks}
      {click_event} on targets matching {core_target_pattern} within {window}
  steps:
  - id: s1
    builds: report
    uses:
    - pql_segment
    - user_profile
    - user_account
    - session_event
    - journey_goal_event
    - click_event
    - subscription_event
    - window
    - min_sessions
    - min_goal_completions
    - min_core_clicks
    - core_target_pattern
    - high_fit_utm_sources
    - account_pqa_threshold
    - stale_days_threshold
    - benchmark_low
    - benchmark_healthy_low
    - benchmark_healthy_high
    - benchmark_high
    - trend_weeks
    instruction: 'Create an Insights report named "PQL Leaderboard" that ranks users in {pql_segment} as a sortable table,
      one row per PQL, showing user name, email, and the account they belong to from {user_account}, taken from {user_profile}.
      Compute a PQL score from 0 to 100 as the weighted blend: distinct session days from {session_event} times 5, plus {journey_goal_event}
      completions times 15, plus clicks on {click_event} matching {core_target_pattern} times 1, plus a recency multiplier
      based on days since {user_profile} first seen, capped at the threshold. Also show days as PQL, the most recent {user_profile}
      last seen timestamp, and the behavior that most recently crossed the user over the threshold. If {high_fit_utm_sources}
      is set, limit rows to users whose {user_profile} UTM source matches one of those values. Add a secondary weekly trend
      chart over the last {trend_weeks} weeks with two series: Series A, count of users in {pql_segment}, labeled "Active
      PQLs"; Series B, trailing 7-day conversion rate from PQL to a paid, non-trial {subscription_event} (plan_type not trial),
      labeled "PQL Conversion Rate". Break down the table by account. Highlight any account with at least {account_pqa_threshold}
      users in {pql_segment} as a PQA for priority sales outreach. Flag any PQL over the threshold for {stale_days_threshold}
      or more days without sales contact. Annotate the conversion rate series with benchmarks: {benchmark_healthy_low} to
      {benchmark_healthy_high} percent is healthy, below {benchmark_low} percent suggests the threshold is too lenient, and
      above {benchmark_high} percent suggests the bar may be too high. Show the most common qualifying behavior among current
      PQLs to inform the opening message for sales.'
---

# Product qualified lead leaderboard

Slash command: /pql-leaderboard

## Step 1: Rank free users by buying signal

Create an Insights report called "PQL Leaderboard".
This recipe surfaces the highest-intent free users for sales follow-up: the Product Qualified Lead (PQL) leaderboard.
PQL definition (configurable; default thresholds):
A user qualifies as a PQL if ALL of the following are true within a 14-day rolling window:
 1. User is currently on a free or trial plan (Subscription started with trial_end populated, OR no active Subscription started)
 2. User has emitted ≥3 distinct sessions (≥3 Session start events on different days)
 3. User has emitted ≥1 Completed a journey goal for the activation journey
 4. User has emitted ≥10 Click on events on core feature targets (configurable target_id pattern)
Optional ICP filter: user's Users.UTM source matches a high-fit channel (configurable)
For each PQL, surface:
- User identity (name, email, the account the user belongs to from Users object)
- PQL score = a 0-100 number computed from a weighted blend of: session count × 5 + goal completions × 15 + core-feature clicks × 1 + days_since_first_seen as a recency multiplier (capped at the threshold)
- Days as PQL (how long they've been over the threshold: long-tenured PQLs need urgent sales attention)
- Most recent activity timestamp (Users.Last seen)
- The specific behavior that crossed them over the threshold (which condition flipped most recently)
Series A: Count of users in PQL state, weekly, label: "Active PQLs"
Series B: Trailing-7-day PQL to Subscription started (paid, non-trial) conversion rate, label: "PQL Conversion Rate"
Time range: Current snapshot + last 12 weeks for the trend
Breakdown: By Users.the account the user belongs to (account-level aggregation (for B2B-leaning SaaS, multiple PQLs at the same account is the strongest signal; this is a "PQA") Product Qualified Account)
Chart type: Sortable table (the leaderboard) plus a secondary trend chart showing weekly PQL volume
Annotations:
- Add benchmarks: PQL-to-paid conversion rates of 15-30% are healthy; below 10% suggests threshold is too lenient (qualifying too early). Above 35% means the bar may be too high: you might be missing users who'd convert with sales touch.
- Flag PQLs who have been over-threshold for 7+ days without sales contact (lost-opportunity signal: every hour of delay reduces conversion).
- Highlight accounts (the account the user belongs to) with 3+ users currently in PQL state: these are PQAs and warrant priority sales outreach.
- Surface the dominant "qualifying behavior" pattern (which threshold was hit most recently): this informs the right opening message for sales.
Use case: the single most-cited PLG report across the entire research base (Custify, Correlated, OpenView, ProductLed, Klipfolio, Userpilot all describe it as foundational). Routes high-intent free users to sales when the intent is hottest.
Taxonomy notes:
- All thresholds use canonical events: Session start, Click on, Completed a journey goal, Subscription started.
- Users.the account the user belongs to enables account-level PQA aggregation.
- Users.UTM source enables ICP filtering.
- PQL scoring is computed by Lovable from these inputs: the recipe defines the formula.
