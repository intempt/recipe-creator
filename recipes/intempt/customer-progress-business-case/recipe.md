---
frontmatter_id: customer-progress-business-case
slash_command: /customer-progress-business-case
description: Sends each account a quarterly account of what they got out of the product, in the app and as a PDF they can hand to their own boss.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends each paying account a quarterly summary of the value they got from the product, in the app and as an exportable
    PDF they can share internally.
  parameters:
  - name: quarter_lookback_days
    type: duration
    label: Account age required before receiving the report
    default: 90 d
    required: false
  - name: churn_risk_threshold
    type: number
    label: Maximum churn risk score allowed to receive the report
    default: 60
    required: false
  - name: journey_start_delay
    type: duration
    label: Delay after quarter end before the email is sent
    default: 3 d
    required: false
  - name: followup_delay
    type: duration
    label: Delay before the follow-up touch
    default: 14 d
    required: false
  - name: in_app_window
    type: duration
    label: How long the in-app snapshot stays visible after quarter close
    default: 30 d
    required: false
  - name: journey_exit_window
    type: duration
    label: Maximum time a quarterly journey instance runs
    default: 60 d
    required: false
  - name: open_rate_target
    type: number
    label: Target email open rate for the progress program
    default: 60
    required: false
  - name: sender_name
    type: string
    label: Named CSM or success lead who sends the email
    required: true
  - name: product_name
    type: string
    label: Product name used in the subject line
    required: true
  requirements:
  - slot: paying_account
    kind: segment
    meaning: Accounts that are currently paying customers
  - slot: account_age_days
    kind: attribute
    meaning: Number of days since the account was created
  - slot: churn_risk_score
    kind: attribute
    meaning: Account churn risk score from 0 to 100
  - slot: account_admin_contact
    kind: attribute
    meaning: The admin or champion contact for each account, who receives account-level emails
  - slot: product_usage_event
    kind: event
    meaning: A customer used the product (any tracked usage action)
    properties:
    - name: event_timestamp
      type: date
      meaning: When the usage happened
      optional: false
    - name: user_id
      type: string
      meaning: The user who performed the action
      optional: false
    - name: feature_name
      type: string
      meaning: The product feature used
      optional: true
  - slot: email_channel
    kind: integration
    meaning: An email sending integration used to deliver account emails
    channel: email
  - slot: in_app_channel
    kind: destination
    meaning: An in-app messaging surface on the admin or owner dashboard
    channel: email
  - slot: product_outcomes_data
    kind: knowledge
    meaning: Customer-reported milestones, KPI values, and ROI inputs such as time saved or error rates, where available
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - paying_account
    - product_usage_event
    - product_outcomes_data
    - account_age_days
    instruction: 'Create an AI-derived account attribute ''quarterly_progress_snapshot'' on {paying_account}, computed at
      the end of each quarter. Include: (a) usage trajectory: total {product_usage_event}, active users, and feature breadth,
      compared with the prior quarter and with similar-cohort accounts; (b) outcomes attributed to the product: milestones
      reached and KPI changes where trackable from {product_outcomes_data}; (c) ROI where data permits (time saved, error
      rate reduced, throughput increased); (d) team impact: new users added and departments adopting; (e) noteworthy events,
      such as first use of a feature or exceeding a benchmark. Output a structured, story-ready snapshot that the email and
      in-app surface render from.'
  - id: s2
    builds: segment
    uses:
    - paying_account
    - account_age_days
    - product_usage_event
    - churn_risk_score
    - s1
    - quarter_lookback_days
    - churn_risk_threshold
    instruction: Build segment 'Quarterly progress recipients' of {paying_account} where account age is at least {quarter_lookback_days},
      usage in the past quarter is above the noise floor (not barely active), and {churn_risk_score} is below {churn_risk_threshold}.
      Use the snapshot from "Total up the quarter". Refresh the audience once per quarter at quarter close.
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - sender_name
    - product_name
    - email_channel
    instruction: 'Generate the quarterly progress email. Subject: ''Your [Quarter] with {product_name}: [headline metric]'',
      for example ''Your Q2 with Acme: 247 hours saved''. Body: hero number (top KPI from the snapshot), 3 to 4 supporting
      metrics with quarter-over-quarter trend arrows, callouts to noteworthy events (for example ''You hit your 1000th unit
      this quarter''), a team-impact summary, and a soft prompt: ''Want this as a PDF to share with your team or manager?''
      Send from {sender_name}. Tone: celebratory but factual, no marketing language, all figures from the account''s own data.
      Use the snapshot from "Total up the quarter" and the recipients from "Pick who should get it".'
  - id: s4
    builds: personalization
    uses:
    - s1
    - s2
    - in_app_channel
    - in_app_window
    instruction: Configure an in-app personalization 'Your Quarter snapshot' on the admin or owner dashboard for users in
      "Pick who should get it". Render the same snapshot content as the email (hero metric, supporting metrics, trend arrows,
      callouts) and keep it visible for {in_app_window} after quarter close. Include an 'Export to PDF' action so the customer
      can share the summary internally.
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - journey_start_delay
    - followup_delay
    - journey_exit_window
    - account_admin_contact
    - email_channel
    instruction: 'Build a journey triggered at quarter close for all users in "Pick who should get it", with one journey instance
      per quarter. Touch 1: wait {journey_start_delay} after quarter end, then send the email from "Write the quarter in numbers"
      to the account admin or champion. Touch 2: on the same day as touch 1, activate the in-app snapshot from "Show it in
      the app too" for {in_app_window}. Touch 3: after {followup_delay}, only if the contact opened the email or interacted
      with the in-app snapshot, send a light follow-up. If account metrics are strong, make it an advocacy ask and hand off
      to a milestone-driven advocacy ask flow. Otherwise offer a CSM-led deeper review for renewal preparation. Exit each
      instance after {journey_exit_window}.'
  - id: s6
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - open_rate_target
    instruction: 'Build a progress-program dashboard with: send volume per quarter; email open rate against a target of {open_rate_target}%
      (these are factual personal emails, not marketing); PDF export rate from the in-app snapshot in "Show it in the app
      too", since exports indicate internal sharing and are a leading indicator of renewal; correlation between opens in "Write
      the quarter in numbers" and renewal rate at the next renewal, the proof-of-value view; and a count of account-team-reported
      cases where the snapshot was referenced in renewal conversations.'
---

# Quarterly customer progress report

Slash command: /customer-progress-business-case

## Step 1: Total up the quarter

Create an AI-derived attribute 'quarterly_progress_snapshot' on the Account object, computed at end of each quarter for all paying accounts. Aggregates: (a) usage trajectory (total events, active users, feature breadth: compared to prior quarter and to similar-cohort accounts); (b) outcomes attributed to the product (milestones reached, KPI changes if trackable); (c) ROI computed where data permits (time saved, error rate reduced, throughput increased); (d) team-impact (new users added, departments adopting); (e) noteworthy events (first time using feature X, exceeded benchmark Y). Output: structured story-ready snapshot the email and in-app surface render from.

## Step 2: Pick who should get it

Build a segment 'Quarterly progress recipients' capturing paying accounts where: (a) account is 90+ days old (needs a full quarter of data), (b) usage in the past quarter was meaningful (above noise floor: don't send 'your impact' to barely-active accounts, it backfires), (c) churn_risk_score is below 60 (don't send celebratory content to at-risk accounts: that's tone-deaf; they get the tiered-churn journey instead). Audience refreshes once per quarter at quarter-close. Use the result of "Total up the quarter".

## Step 3: Write the quarter in numbers

Generate quarterly progress email content. Subject: 'Your [Quarter] with [Product]: [headline metric]' (e.g. 'Your Q2 with Acme: 247 hours saved'). Body: hero number (top KPI from snapshot), 3-4 supporting metrics with quarter-over-quarter trend arrows, callouts to noteworthy events ('You hit your 1000th [unit] this quarter'), team-impact summary, and a soft prompt: 'Want this as a PDF to share with your team or manager?' Send-from: named CSM or success lead. Tone: celebratory but factual: no marketing-speak, all real numbers from their account. Use the result of "Total up the quarter", "Pick who should get it".

## Step 4: Show it in the app too

Configure an in-app personalization 'Your Quarter snapshot' on the admin/owner dashboard for users in the quarterly-review segment. Renders the same snapshot content as the email (hero metric, supporting metrics, trend arrows, callouts) visible for the 30 days after quarter-close. Includes an export-to-PDF action so the customer can easily share internally (the killer feature of this play, customers SHARE this content with their bosses, which is its own marketing channel). Use the result of "Total up the quarter", "Pick who should get it".

## Step 5: Send three days after close

Build a journey triggered quarterly at quarter-close for all users in the segment. Touch 1 (Day 3 after quarter end: gives time for last-day data to settle): quarterly progress email goes to the account's admin/champion. Touch 2 (Day 0 of touch 1): in-app personalization activates for 30 days. Touch 3 (Day 14, if user opened the email or interacted with in-app): light follow-up offering a CSM-led deeper review for renewal-prep, OR an advocacy ask if the metrics are strong (handoff to milestone-driven-advocacy-asks). Exit on: 60-day completion (each quarter is its own journey instance). Use the result of "Total up the quarter", "Pick who should get it", "Write the quarter in numbers", "Show it in the app too".

## Step 6: See if the report earns renewals

Compose a progress-program dashboard: send volume per quarter, email engagement rate (target: 60%+ open (these are factual personal emails, not marketing), PDF-export rate (the killer metric) exports mean the customer is sharing internally, which is a renewal leading indicator), correlation between progress-email opens and renewal rate at next renewal (the proof-of-value chart: opens typically correlate with 5-10 percentage point higher renewal rates), and AE/CSM-reported instances of the snapshot being referenced in renewal conversations. Use the result of "Total up the quarter", "Pick who should get it", "Write the quarter in numbers", "Show it in the app too", "Send three days after close".
