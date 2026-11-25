---
frontmatter_id: pqa-account-engagement-to-ae-task
slash_command: /pqa-account-engagement-to-ae-task
description: When several people from one company start using the product in the same fortnight, it scores the account and
  emails an AE a brief asking them to open a deal.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: When several people from one company start using the product in the same fortnight, the account is scored and AEs
    get an emailed brief to open a deal, plus a weekly digest.
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
  - name: alert_recipients
    type: string
    label: Email addresses of the AEs and AE managers who get the briefs
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
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
  steps:
  - id: s1
    builds: attribute
    uses:
    - user_activity_event
    - activity_window
    - min_active_users
    instruction: 'Build a computed attribute on accounts named "pqa_score", a number from 0 to 100, refreshed daily: 40 points
      scaled by the number of distinct users of the account who did {user_activity_event} in the last {activity_window} (full
      points at {min_active_users} or more); 30 points scaled by the account''s total {user_activity_event} events in that
      window; 30 points scaled by the number of distinct {user_activity_event.feature_name} values used.'
  - id: s2
    builds: segment
    uses:
    - s1
    - open_deal_status
    - ae_engagement_status
    - paid_customer_status
    - icp_fit_attribute
    - pqa_threshold
    - ae_engagement_lookback
    dependsOn:
    - s1
    instruction: 'Build a new segment of accounts named "Product Qualified Accounts". An account is in it when all of these
      are true: its pqa_score from "Score the whole account" is {pqa_threshold} or more; its {open_deal_status} is not open;
      its {ae_engagement_status} is empty or older than {ae_engagement_lookback}; its {paid_customer_status} is not paid;
      its {icp_fit_attribute} is true.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - user_activity_event
    - user_signup_event
    - activity_window
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation triggered when an account enters the segment from "Find product qualified accounts".
      An analysis step writes: the account''s pqa_score from "Score the whole account"; how many of its users did {user_activity_event}
      in the last {activity_window}; the top features each used; users who look like decision-makers by job title; new users
      from its domain by {user_signup_event.email_domain} in that window. Then it emails {alert_recipients} the account name
      and this brief, asking an AE to open a deal and start outreach.'
  - id: s4
    builds: automation
    uses:
    - s2
    - open_deal_status
    - digest_recipients
    dependsOn:
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the segment from
      "Find product qualified accounts" and writes these figures: accounts that entered it in the last 7 days and in each
      of the 4 weeks before; of the accounts that entered it in the last 90 days, the share whose {open_deal_status} is now
      open. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is
      sent.'
---

# Account level signal to AE task

Slash command: /pqa-account-engagement-to-ae-task

## Step 1: Score the whole account

Build a computed attribute on accounts named "pqa_score", a number from 0 to 100, refreshed daily: 40 points scaled by the number of distinct users of the account who did user activity event in the last 14 d (full points at 3 or more); 30 points scaled by the account's total user activity event events in that window; 30 points scaled by the number of distinct feature name values used.

## Step 2: Find product qualified accounts

Build a new segment of accounts named "Product Qualified Accounts". An account is in it when all of these are true: its pqa_score from "Score the whole account" is 70 or more; its open deal status is not open; its ae engagement status is empty or older than 60 d; its paid customer status is not paid; its icp fit attribute is true.

## Step 3: Brief an AE to open a deal

Build an automation triggered when an account enters the segment from "Find product qualified accounts". An analysis step writes: the account's pqa_score from "Score the whole account"; how many of its users did user activity event in the last 14 d; the top features each used; users who look like decision-makers by job title; new users from its domain by email domain in that window. Then it emails the email addresses of the AEs and AE managers who get the briefs the account name and this brief, asking an AE to open a deal and start outreach.

## Step 4: Email the weekly PQA digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the segment from "Find product qualified accounts" and writes these figures: accounts that entered it in the last 7 days and in each of the 4 weeks before; of the accounts that entered it in the last 90 days, the share whose open deal status is now open. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
