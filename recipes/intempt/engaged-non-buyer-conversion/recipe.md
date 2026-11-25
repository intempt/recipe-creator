---
frontmatter_id: engaged-non-buyer-conversion
slash_command: /engaged-non-buyer-conversion
description: Scores free users who are highly engaged but have not converted, sends them a check-in email that asks what is
  stopping them, and emails a rep the stuck users who still have not upgraded.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Scores highly engaged free users who have not upgraded, sends them a check-in email asking what is in the way,
    and alerts a rep with their likely blocker if they still do not upgrade.
  parameters:
  - name: minAccountAgeDays
    type: number
    label: Minimum account age (days)
    default: 30
    required: false
  - name: paradoxScoreThreshold
    type: number
    label: Engagement paradox score threshold (0-100)
    default: 70
    required: false
  - name: declineLookbackDays
    type: duration
    label: Lookback window for declined upgrade
    default: 90 d
    required: false
  - name: sessionWindow
    type: duration
    label: Session activity window
    default: 30 d
    required: false
  - name: touch3Delay
    type: duration
    label: Delay before AE outreach task
    default: 7 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the reps who get the stuck-user alerts
    required: true
  requirements:
  - slot: user_profile
    kind: event
    meaning: A user was active in the product (sessions, feature use, email engagement)
    properties:
    - name: session_count_30d
      type: number
      meaning: Sessions in the last 30 days
      optional: false
    - name: feature_breadth
      type: number
      meaning: Number of distinct features used
      optional: false
    - name: email_engagement
      type: number
      meaning: Marketing email opens and clicks
      optional: false
  - slot: account_age_attribute
    kind: attribute
    meaning: The number of days since the user account was created
  - slot: subscription_status
    kind: attribute
    meaning: The user's current subscription status (free, trialing, paid)
  - slot: sales_conversation_status
    kind: attribute
    meaning: Whether the user is currently in an active sales conversation
  - slot: upgrade_decline_event
    kind: event
    meaning: A user explicitly declined an upgrade offer
    properties:
    - name: declined_at
      type: date
      meaning: When the upgrade was declined
      optional: false
  steps:
  - id: s1
    builds: attribute
    uses:
    - user_profile
    - sessionWindow
    instruction: 'Build a computed attribute on users named "engagement_paradox_score", a number from 0 to 100, refreshed
      daily: how far the user''s engagement exceeds their conversion, from {user_profile.session_count_30d}, {user_profile.feature_breadth}
      and {user_profile.email_engagement} in the last {sessionWindow}, compared with the same figures of users who became
      paying. 100 means the user is as engaged as a typical paying user or more but has not paid.'
  - id: s2
    builds: attribute
    uses:
    - user_profile
    - upgrade_decline_event
    - sessionWindow
    instruction: 'Build a computed attribute on users named "conversion_blocker", refreshed daily, with exactly one of these
      values: price-sensitivity, feature-gap, authority-issue, decision-paralysis, no-urgency. Infer it from the user''s activity
      in the last {sessionWindow}: visits to pricing or plan pages and {upgrade_decline_event} point to price-sensitivity;
      a feature tried once and not again to feature-gap; many invited teammates but no admin activity to authority-issue;
      repeated plan comparisons to decision-paralysis; otherwise no-urgency.'
  - id: s3
    builds: segment
    uses:
    - s1
    - account_age_attribute
    - subscription_status
    - sales_conversation_status
    - upgrade_decline_event
    - minAccountAgeDays
    - paradoxScoreThreshold
    - declineLookbackDays
    dependsOn:
    - s1
    instruction: 'Build a new segment of users named "Engaged Non-Buyers". A user is in it when all of these are true: their
      {account_age_attribute} is {minAccountAgeDays} or more; their {subscription_status} is free or trialing; their engagement_paradox_score
      from "Measure the gap" is {paradoxScoreThreshold} or more; their {sales_conversation_status} is not active; they did
      not do {upgrade_decline_event} in the last {declineLookbackDays}.'
  - id: s4
    builds: email
    instruction: 'Write a short plain check-in email to a free user who uses the product a lot but has not upgraded. It says
      they use it like a paying customer, then asks one question: what is keeping them from upgrading, cost, a missing feature,
      approval from someone else, timing, or something else, and asks them to reply in one line. It offers a 15-minute call
      with the team. No discount and no prices.'
  - id: s5
    builds: automation
    uses:
    - s2
    - s3
    - s4
    - subscription_status
    - touch3Delay
    - alert_recipients
    dependsOn:
    - s2
    - s3
    - s4
    instruction: Build an automation triggered when a user enters the segment from "Find engaged free users". It sends the
      email from "Write the check-in email" to that user. Then it waits {touch3Delay}; if the user's {subscription_status}
      is still free or trialing, it sends one email via Blu's mailer to {alert_recipients} with the user's name and email,
      their engagement_paradox_score from "Measure the gap", their conversion_blocker from "Name the likely blocker", and
      a one-line suggested approach for that blocker. The automation ends when the user's {subscription_status} becomes paid.
---

# Engaged users who never buy

Slash command: /engaged-non-buyer-conversion

## Step 1: Measure the gap

Build a computed attribute on users named "engagement_paradox_score", a number from 0 to 100, refreshed daily: how far the user's engagement exceeds their conversion, from session count 30d, feature breadth and email engagement in the last 30 d, compared with the same figures of users who became paying. 100 means the user is as engaged as a typical paying user or more but has not paid.

## Step 2: Name the likely blocker

Build a computed attribute on users named "conversion_blocker", refreshed daily, with exactly one of these values: price-sensitivity, feature-gap, authority-issue, decision-paralysis, no-urgency. Infer it from the user's activity in the last 30 d: visits to pricing or plan pages and upgrade decline event point to price-sensitivity; a feature tried once and not again to feature-gap; many invited teammates but no admin activity to authority-issue; repeated plan comparisons to decision-paralysis; otherwise no-urgency.

## Step 3: Find engaged free users

Build a new segment of users named "Engaged Non-Buyers". A user is in it when all of these are true: their account age attribute is 30 or more; their subscription status is free or trialing; their engagement_paradox_score from "Measure the gap" is 70 or more; their sales conversation status is not active; they did not do upgrade decline event in the last 90 d.

## Step 4: Write the check-in email

Write a short plain check-in email to a free user who uses the product a lot but has not upgraded. It says they use it like a paying customer, then asks one question: what is keeping them from upgrading, cost, a missing feature, approval from someone else, timing, or something else, and asks them to reply in one line. It offers a 15-minute call with the team. No discount and no prices.

## Step 5: Check in, then bring a rep in

Build an automation triggered when a user enters the segment from "Find engaged free users". It sends the email from "Write the check-in email" to that user. Then it waits 7 d; if the user's subscription status is still free or trialing, it sends one email via Blu's mailer to the email addresses of the reps who get the stuck-user alerts with the user's name and email, their engagement_paradox_score from "Measure the gap", their conversion_blocker from "Name the likely blocker", and a one-line suggested approach for that blocker. The automation ends when the user's subscription status becomes paid.
