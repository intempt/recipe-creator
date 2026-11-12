---
frontmatter_id: trial-activation
slash_command: /trial-activation
description: Scores how well each trial is going and sends different onboarding to the ones racing ahead, the ones drifting, and the ones at risk.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Scores each trial's health, splits trials into three tiers, and sends each tier tailored onboarding that leads
    toward paid conversion, tracked in a funnel report.
  parameters:
  - name: login_window
    type: duration
    label: Engagement lookback window
    default: 30 d
    required: false
  - name: tier_high_min_score
    type: number
    label: Minimum trial health score for high-engagement tier
    default: 70
    required: false
  - name: tier_at_risk_max_score
    type: number
    label: Maximum trial health score for at-risk tier
    default: 40
    required: false
  - name: tone
    type: enum
    label: Tone of onboarding emails
    default: encouraging
    required: false
    options:
    - encouraging
    - neutral
    - direct
  requirements:
  - slot: trial_user
    kind: segment
    meaning: Users currently on a free trial
  - slot: trial_login_event
    kind: event
    meaning: A customer logged into the product
    properties:
    - name: timestamp
      type: date
      meaning: When the login happened
      optional: false
  - slot: key_feature_event
    kind: event
    meaning: A customer used a key product feature
    properties:
    - name: feature_name
      type: string
      meaning: Which key feature was used
      optional: false
  - slot: team_invite_event
    kind: event
    meaning: A customer invited a teammate to the product
    properties:
    - name: invitee_count
      type: number
      meaning: How many teammates were invited
      optional: true
  - slot: data_upload_event
    kind: event
    meaning: A customer uploaded data into the product
    properties:
    - name: row_count
      type: number
      meaning: How many rows or records were uploaded
      optional: true
  - slot: key_event_1
    kind: event
    meaning: A trial customer reached the first key activation milestone
  - slot: key_event_2
    kind: event
    meaning: A trial customer reached the second key activation milestone
  - slot: trial_signup_event
    kind: event
    meaning: A customer signed up for a trial
  - slot: paid_conversion_event
    kind: event
    meaning: A trial customer converted to a paid subscription
  - slot: trial_health_score
    kind: attribute
    meaning: A computed score of how well each trial is going, based on engagement signals
  - slot: trial_tier
    kind: segment
    meaning: Trial users grouped into high-engagement, moderate, and at-risk tiers by health score
  - slot: onboarding_email_channel
    kind: destination
    meaning: Channel used to send onboarding emails to trial users
    channel: email
  steps:
  - id: s1
    builds: attribute
    instruction: Define an AI-derived {trial_health_score} attribute computed from {trial_login_event} within {login_window},
      {key_feature_event}, {team_invite_event}, and {data_upload_event} signals.
  - id: s2
    builds: segment
    uses:
    - trial_user
    - s1
    - tier_high_min_score
    - tier_at_risk_max_score
    instruction: 'Segment {trial_user} into three risk tiers using the result of "Score how the trial is going": high-engagement
      where {trial_health_score} is at least {tier_high_min_score}, at-risk where it is at most {tier_at_risk_max_score},
      and moderate for everyone in between.'
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - tone
    instruction: Write tier-specific onboarding email content in a {tone} tone for each tier in {trial_tier}, using the result
      of "Score how the trial is going" and "Split trials into three tiers" to emphasize the aha-moment features relevant
      to each tier.
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - trial_user
    - onboarding_email_channel
    - key_event_1
    - key_event_2
    - paid_conversion_event
    instruction: Build a tiered onboarding journey for {trial_tier} that routes each tier through appropriate education and
      conversion touches over {onboarding_email_channel}, using the result of "Score how the trial is going", "Split trials
      into three tiers", and "Write onboarding per tier".
  - id: s5
    builds: report
    uses:
    - s1
    - s2
    - s3
    - s4
    - trial_signup_event
    - key_event_1
    - key_event_2
    - paid_conversion_event
    instruction: Compose a funnel report tracking {trial_signup_event} to {key_event_1} to {key_event_2} to {paid_conversion_event}
      with a retention overlay, using the result of "Score how the trial is going", "Split trials into three tiers", "Write
      onboarding per tier", and "Route each tier differently".
---

# Trial to paid activation

Slash command: /trial-activation

## Step 1: Score how the trial is going

Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded).

## Step 2: Split trials into three tiers

Segment trial users into risk tiers (high-engagement, moderate, at-risk) based on trial_health_score. Use the result of "Score how the trial is going".

## Step 3: Write onboarding per tier

Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. Use the result of "Score how the trial is going", "Split trials into three tiers".

## Step 4: Route each tier differently

Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. Use the result of "Score how the trial is going", "Split trials into three tiers", "Write onboarding per tier".

## Step 5: Track trial to paid

Compose a funnel report tracking trial-signup to key-event-1 to key-event-2 to paid-conversion with retention overlay. Use the result of "Score how the trial is going", "Split trials into three tiers", "Write onboarding per tier", "Route each tier differently".
