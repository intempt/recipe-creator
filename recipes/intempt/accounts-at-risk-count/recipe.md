---
frontmatter_id: accounts-at-risk-count
slash_command: /accounts-at-risk-count
description: Counts accounts in predefined engagement-decline segments and tracks the weekly total. Uses fixed segments as an approximate at-risk signal.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tracks weekly counts of accounts showing engagement decline or high-priority ticket signals, plus the subscription
    revenue tied to at-risk accounts.
  parameters:
  - name: trailingWindow
    type: duration
    label: Trailing comparison window
    default: 4 w
    required: false
  - name: baselineWindow
    type: duration
    label: Baseline window
    default: 8 w
    required: false
  - name: distinctUserDropThreshold
    type: number
    label: Distinct active user drop threshold (%)
    default: 30
    required: false
  - name: earlyWarningDropThreshold
    type: number
    label: Early-warning drop threshold (%)
    default: 10
    required: false
  - name: championInactivityWindow
    type: duration
    label: Champion inactivity window
    default: 14 d
    required: false
  - name: ticketLookback
    type: duration
    label: High-priority ticket lookback
    default: 30 d
    required: false
  - name: reportTimeRange
    type: duration
    label: Report time range
    default: 12 w
    required: false
  - name: spikeThreshold
    type: number
    label: Weekly spike alert threshold (%)
    default: 20
    required: false
  - name: broadHealthThreshold
    type: number
    label: Broad-base health alert threshold (% of active accounts)
    default: 15
    required: false
  - name: topAccountCount
    type: number
    label: Number of top at-risk accounts to surface
    default: 5
    required: false
  requirements:
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  - slot: ticket_created
    kind: event
    meaning: A customer created a support ticket
    properties:
    - name: priority
      type: string
      meaning: Priority level of the ticket (e.g. P1-P4 or High/Medium/Low)
      optional: false
  - slot: subscription_started
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: amount
      type: number
      meaning: Subscription amount in dollars
      optional: false
  - slot: account_of_user
    kind: attribute
    meaning: The account a user belongs to
  - slot: account_primary_user
    kind: attribute
    meaning: The primary user ID of an account
  - slot: account_tier
    kind: attribute
    meaning: Account tier such as Enterprise, Mid-Market or SMB, if present on accounts
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - session_start
    - ticket_created
    - subscription_started
    - account_of_user
    - account_primary_user
    - account_tier
    - trailingWindow
    - baselineWindow
    - distinctUserDropThreshold
    - earlyWarningDropThreshold
    - championInactivityWindow
    - ticketLookback
    - reportTimeRange
    - spikeThreshold
    - broadHealthThreshold
    - topAccountCount
    instruction: 'Create an Insights report named "Accounts at Risk". Define an account as at-risk when, comparing the trailing
      {trailingWindow} against the prior {baselineWindow} baseline, any one of these holds: (a) distinct users from the account
      who fired {session_start} dropped by at least {distinctUserDropThreshold}%; (b) the champion user, defined as the account
      user with the most {session_start} events in the trailing 30 days, has fired zero {session_start} events in the last
      {championInactivityWindow}; (c) the account''s {account_primary_user} fired {ticket_created} with {ticket_created.priority}
      equal to the high-priority level (P1 or High) in the last {ticketLookback}. Series A: count unique accounts (via {account_of_user})
      that are at-risk, weekly snapshot, labeled "Accounts at Risk". Series B: count unique accounts not at-risk whose distinct
      active user count dropped by at least {earlyWarningDropThreshold}% but less than {distinctUserDropThreshold}%, labeled
      "Accounts to Watch". Series C: sum of the most recent active {subscription_started.amount} for each at-risk account''s
      primary user (summed across users on the account where multiple subscriptions exist), in dollars, labeled "Revenue at
      Risk". Time range: last {reportTimeRange}. Compare against the previous period of equal length. Breakdown by {account_tier}
      if available; otherwise by trailing-30-day engagement-volume bucket. Chart: stacked area for Series A and B over time,
      with Series C as a secondary line on a right axis. Annotations: flag any week where Series A grew by at least {spikeThreshold}%
      versus the trailing 4-week average; list the top {topAccountCount} accounts in Series A ranked by subscription amount;
      flag when Series A exceeds {broadHealthThreshold}% of total active accounts; report which of the three at-risk triggers
      (a, b, c) fires most often and name the dominant one.'
---

# Accounts at risk

Slash command: /accounts-at-risk-count

## Step 1: Count accounts going quiet

Create an Insights report called "Accounts at Risk".
Definition of "at risk":
An account (Users.the account the user belongs to) qualifies as at-risk if ALL of the following hold for the trailing 4 weeks vs. the prior 8-week baseline:
 - Distinct active users in the account dropped by ≥30% (count of unique users from the account who emitted a Session start)
 - OR the dominant user (most-active user on the account) has emitted zero Session start events in the last 14 days (champion-departure proxy)
 - OR the account's primary_user_id has emitted ≥1 Ticket created with priority = high or P1 in the last 30 days
Series A: Count Unique values of the account the user belongs to satisfying the at-risk criteria, time granularity: Weekly snapshot, label: "Accounts at Risk"
Series B: Count Unique values of the account the user belongs to NOT satisfying the criteria but whose engagement dropped 10: 30% (early-warning band), label: "Accounts to Watch"
Series C: Sum of subscription amount (most-recent active Subscription started.amount) across at-risk accounts: the dollar revenue at risk, unit: $, label: "Revenue at Risk"
Time range: Last 12 weeks
Breakdown: By the account the user belongs to segment if the project has account-tier metadata (Enterprise / Mid-Market / SMB) on the Accounts object; otherwise by trailing-30d engagement-volume bucket
Compare: Previous period (prior 12 weeks)
Chart type: Stacked area chart for Series A and B over time, with Series C ($) as a secondary line on a right axis
Annotations:
- Flag any week where Series A grew by ≥20% vs. the trailing 4-week average (acute risk spike: investigate what happened that week).
- Surface the top 5 accounts currently in Series A by subscription amount (highest-value at-risk accounts get priority CSM action).
- Flag if Series A as % of total active accounts exceeds 15% (broad-base health issue, not isolated account problems).
- Highlight the dominant trigger: which of the three at-risk criteria fires most often? If "distinct users dropped" dominates, the issue is account-level disengagement; if "champion departure" dominates, the issue is single-threading; if "high-priority tickets" dominates, the issue is product quality.
Use case: the canonical CS headline metric. Most CS teams maintain this list manually in a spreadsheet; this recipe automates it. Distinct from account-engagement-score-trend (which is the per-account engagement timeline): this is the count headline.
Taxonomy notes:
- Session start, Ticket created are canonical events. Users.the account the user belongs to is the canonical account-level relation.
- "Champion" identification = the user with the highest count of Session start events on the account in the trailing 30 days. "Departure" = zero Session start events from that user in the last 14 days.
- Ticket created.priority is a real property; the "high-priority" classification depends on the project's priority enum (typically P1, P2, P3, P4 or High/Medium/Low).
- Subscription amount lookup: the account's primary_user_id's most-recent active Subscription started.amount, summed across users on the account if the workspace has multi-subscription accounts.
