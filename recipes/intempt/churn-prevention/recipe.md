---
frontmatter_id: churn-prevention
slash_command: /churn-prevention
description: Flags customers who are drifting away, reaches them automatically while it is still cheap to fix, and pulls in a CSM when it is not.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Flags customers drifting away, automatically re-engages medium-risk users early, and alerts a CSM in Slack for
    high-risk users, with reporting on churn by tier.
  parameters:
  - name: high_risk_threshold
    type: number
    label: High-risk score threshold
    default: 0.8
    required: false
  - name: medium_risk_threshold
    type: number
    label: Medium-risk score threshold
    default: 0.5
    required: false
  - name: scoring_window
    type: duration
    label: Engagement decline lookback window
    default: 30 d
    required: false
  - name: win_back_tone
    type: enum
    label: Tone of win-back emails
    default: friendly
    required: false
    options:
    - friendly
    - professional
    - casual
  requirements:
  - slot: customer_profile
    kind: attribute
    meaning: A customer's engagement, support and feature-usage history used to derive churn risk
  - slot: churn_risk_score
    kind: attribute
    meaning: A customer's churn risk score
  - slot: churn_risk_tier
    kind: segment
    meaning: Customers grouped into low, medium and high churn-risk buckets
    creatable: true
    definition: users whose {churn_risk_score} is at or above {medium_risk_threshold} and below {high_risk_threshold} (medium),
      above {high_risk_threshold} (high), or below {medium_risk_threshold} (low)
  - slot: csm_slack
    kind: integration
    meaning: Slack workspace used to alert customer success managers
    channel: slack
  steps:
  - id: s1
    builds: attribute
    uses:
    - customer_profile
    - scoring_window
    instruction: Define an AI-derived {churn_risk_score} attribute using engagement decline over {scoring_window}, support
      ticket sentiment, and feature-usage signals.
  - id: s2
    builds: segment
    uses:
    - s1
    - churn_risk_tier
    - medium_risk_threshold
    - high_risk_threshold
    instruction: Segment users into low, medium and high churn-risk buckets using {churn_risk_tier}, based on the result of
      "Score churn risk" with medium at or above {medium_risk_threshold} and high above {high_risk_threshold}.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - csm_slack
    - high_risk_threshold
    instruction: Create a workflow that alerts CSMs in {csm_slack} when high-risk users from "Split into low, medium and high"
      cross the {high_risk_threshold} threshold, including a context payload with the user's churn score.
  - id: s4
    builds: email
    uses:
    - s1
    - s2
    - s3
    - win_back_tone
    instruction: 'Generate re-engagement content in a {win_back_tone} tone: win-back-feature emails, success-story emails,
      and value-reminder emails for users in the risk buckets from "Split into low, medium and high" and the alert from "Tell
      the CSM about high risk".'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    instruction: Build a journey for medium-risk users from "Split into low, medium and high" with automated engagement using
      the emails from "Write the win back emails" before CSM intervention is needed.
  - id: s6
    builds: report
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    instruction: Compose a retention report tracking churn rate by risk tier and intervention type across "Split into low,
      medium and high", "Tell the CSM about high risk", "Write the win back emails" and "Reach medium risk first".
  - id: s7
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - s6
    instruction: Compose a dashboard showing risk distribution, intervention success rate, and net retention impact drawn
      from "Compare churn by risk tier" and the prior steps.
---

# Churn prevention

Slash command: /churn-prevention

## Step 1: Score churn risk

Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals.

## Step 2: Split into low, medium and high

Segment users into low/medium/high churn-risk buckets. Use the result of "Score churn risk".

## Step 3: Tell the CSM about high risk

Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. Use the result of "Score churn risk", "Split into low, medium and high".

## Step 4: Write the win back emails

Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk".

## Step 5: Reach medium risk first

Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk", "Write the win back emails".

## Step 6: Compare churn by risk tier

Compose a retention report tracking churn rate by risk tier and intervention type. Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk", "Write the win back emails", "Reach medium risk first".

## Step 7: See if the saves are working

Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk", "Write the win back emails", "Reach medium risk first", "Compare churn by risk tier".
