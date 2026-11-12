---
frontmatter_id: pqa-account-engagement-to-ae-task
slash_command: /pqa-account-engagement-to-ae-task
description: When several people from one company start using the product in the same fortnight, it briefs an AE and asks them to open a deal.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: When several people from one company start using the product in the same fortnight, the account is scored, and
    an AE gets a high-priority task and Slack brief to open a deal.
  parameters:
  - name: activity_window
    type: duration
    label: Activity window for counting active users
    default: 14 d
    required: false
  - name: min_active_users
    type: number
    label: Minimum active users for a strong signal
    default: 3
    required: false
  - name: pqa_threshold
    type: number
    label: Account score threshold that flags a PQA
    default: 70
    required: false
  - name: ae_engagement_lookback
    type: duration
    label: Lookback for recent AE engagement
    default: 60 d
    required: false
  - name: dashboard_comparison_note
    type: text
    label: Comparison focus for PQA vs cold outbound
    default: win-rate and cycle time
    required: false
  requirements:
  - slot: account_object
    kind: attribute
    meaning: Account record that holds company-level data for scoring
  - slot: user_activity_event
    kind: event
    meaning: A user of a customer's company used a product feature
    properties:
    - name: account_id
      type: string
      meaning: Account the user belongs to
      optional: false
    - name: feature_name
      type: string
      meaning: Feature that was used
      optional: true
  - slot: user_signup_event
    kind: event
    meaning: A new user signed up using a company email domain
    properties:
    - name: email_domain
      type: string
      meaning: Domain of the signing-up user's email
      optional: false
  - slot: pqa_score_attribute
    kind: attribute
    meaning: Account-level product qualified account score from 0 to 100
  - slot: open_deal_status
    kind: attribute
    meaning: Whether an account has an open deal
  - slot: ae_engagement_status
    kind: attribute
    meaning: Last time an AE actively engaged with an account
  - slot: paid_customer_status
    kind: attribute
    meaning: Whether the account is an existing paid customer
  - slot: icp_fit_attribute
    kind: attribute
    meaning: Whether the account matches the ideal customer profile
  - slot: enrichment_provider
    kind: integration
    meaning: Firmographic and contact enrichment service connected to the project
    optional: true
    channel: email
  - slot: ae_team_channel
    kind: integration
    meaning: Slack workspace used to notify AEs and AE managers
    channel: slack
  - slot: ae_task_destination
    kind: destination
    meaning: CRM where AE tasks and deal records are created
    channel: hubspot
  - slot: pqa_account_segment
    kind: segment
    meaning: Accounts that crossed the PQA score threshold and have no open deal or recent AE engagement
    creatable: true
    definition: accounts where {pqa_score_attribute} crossed {pqa_threshold} in the last {activity_window} AND no open deal
      exists for the account AND no AE was engaged in the last {ae_engagement_lookback} AND the account is not a paid customer
  - slot: pqa_dashboard_destination
    kind: destination
    meaning: Reporting destination for PQA metrics
    optional: true
    channel: email
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_object
    - user_activity_event
    - user_signup_event
    - pqa_score_attribute
    - activity_window
    - min_active_users
    - pqa_threshold
    instruction: 'Create an AI-derived account attribute named pqa_score scored 0-100 by combining: (a) count of distinct
      users from the account active in the last {activity_window} ({min_active_users}+ users is a strong signal); (b) total
      feature events across the account; (c) seniority of users, flagging any decision-makers by title or email pattern; (d)
      usage depth across the account team. A score at or above {pqa_threshold} marks the account as a PQA. Refresh daily and
      whenever a new user signs up from the account''s domain.'
  - id: s2
    builds: segment
    uses:
    - s1
    - pqa_account_segment
    - pqa_score_attribute
    - open_deal_status
    - ae_engagement_status
    - paid_customer_status
    - pqa_threshold
    - activity_window
    - ae_engagement_lookback
    instruction: 'Build the segment "PQA: accounts score >= 70" as accounts whose {pqa_score_attribute} crossed {pqa_threshold}
      in the last {activity_window}, with no open deal, no AE engagement in the last {ae_engagement_lookback}, and excluding
      existing paid customers (those are handled by the seat-expansion motion). Use the scores from "Score the whole account".'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - pqa_score_attribute
    - pqa_threshold
    - icp_fit_attribute
    - enrichment_provider
    - ae_task_destination
    - ae_team_channel
    - user_activity_event
    instruction: 'Create a workflow that fires when {pqa_score_attribute} crosses {pqa_threshold}, for ICP-matched accounts
      only ({icp_fit_attribute}). Steps in order: (1) refresh account enrichment for firmographics, technographics and decision-maker
      contacts using {enrichment_provider} if connected; (2) compute an account context summary with active user count, key
      features used per user, decision-makers identified, employee count and ICP fit; (3) create a high-priority AE task in
      {ae_task_destination} to create a deal record and start outreach, with the full account context attached; (4) send a
      Slack message to the AE manager and assigned AE in {ae_team_channel} with a one-paragraph summary and a link to the
      account record. Use the scores from "Score the whole account" and the accounts from "Find accounts crossing 70".'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - pqa_threshold
    - dashboard_comparison_note
    - pqa_dashboard_destination
    instruction: 'Build a PQA dashboard tracking: PQA detection volume (accounts crossing {pqa_threshold} per month); median
      time from PQA flag to deal created for AE response time; PQA-to-deal conversion rate; PQA-to-meeting rate; and ARR-weighted
      PQA value compared with non-PQA outbound deals. Compare PQA-sourced and cold-outbound-sourced deals on {dashboard_comparison_note}.
      Use the results of "Score the whole account", "Find accounts crossing 70" and "Brief an AE to open a deal".'
---

# Account level signal to AE task

Slash command: /pqa-account-engagement-to-ae-task

## Step 1: Score the whole account

Create an AI-derived attribute 'pqa_score' on the Account object. Composite: (a) count of distinct users from the account active in last 14 days (3+ users = strong PQA signal); (b) total feature events across the account; (c) seniority of users (any decision-makers based on title/email pattern); (d) usage depth across the account team. Output: numeric score 0-100. Score >= 70 = PQA. Updated daily and on new user signups from the domain.

## Step 2: Find accounts crossing 70

Build a segment 'PQA: accounts score >= 70' capturing accounts where pqa_score crossed 70 in the last 14 days AND no open deal currently exists for the account AND no AE has been actively engaged in the last 60 days. Excludes existing paid customers (different motion: see seat-expansion workflow). Use the result of "Score the whole account".

## Step 3: Brief an AE to open a deal

Create a workflow firing when pqa_score crosses 70. Step sequence: (1) refresh account enrichment (firmographics, technographics, decision-maker contacts via Apollo/ZoomInfo if connected); (2) compute account context summary: active user count, key features used per user, decision-makers identified, employee count, ICP fit; (3) create a high-priority AE task to create a deal record and start outreach, with the full account context pre-attached; (4) notify AE manager and assigned AE via Slack with a one-paragraph summary and link to the account record. Only fire for ICP-matched accounts. Use the result of "Score the whole account", "Find accounts crossing 70".

## Step 4: Compare against cold outbound

Compose a PQA dashboard tracking: PQA detection volume (accounts crossing threshold per month), AE response time (median time from PQA-flag to Deal created), PQA-to-deal conversion rate, PQA-to-meeting rate, ARR-weighted PQA value (deals from PQAs vs. non-PQA outbound). Compare PQA-sourced deals vs. cold-outbound-sourced deals on win-rate and cycle time: usually PQAs win 2-3x more reliably. Use the result of "Score the whole account", "Find accounts crossing 70", "Brief an AE to open a deal".
