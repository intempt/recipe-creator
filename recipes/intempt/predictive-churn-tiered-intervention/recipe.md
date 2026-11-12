---
frontmatter_id: predictive-churn-tiered-intervention
slash_command: /predictive-churn-tiered-intervention
description: 'Scores churn risk daily and routes each band to email, SMS, push, or Slack: nurture content at low risk, personalized messages at medium, and CSM or founder outreach at high and critical.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores churn risk daily and routes paying users by risk band to nurture, personalized, or founder/CSM outreach
    across email, SMS, push, and Slack.
  parameters:
  - name: risk_threshold
    type: number
    label: Minimum churn risk score to enter intervention
    default: 30
    required: false
  - name: new_user_grace_period
    type: duration
    label: Grace period for newly signed-up users
    default: 14 d
    required: false
  - name: recovery_window
    type: duration
    label: Days below threshold before a user counts as recovered
    default: 14 d
    required: false
  - name: low_followup_delay
    type: duration
    label: Delay before low-tier nurture email
    default: 7 d
    required: false
  - name: medium_followup_delay
    type: duration
    label: Delay before medium-tier follow-up email
    default: 7 d
    required: false
  - name: critical_response_window
    type: duration
    label: Maximum time to start founder/CSM outreach for critical tier
    default: 4 h
    required: false
  - name: medium_tone
    type: enum
    label: Tone for medium-tier emails
    default: helpful
    required: false
    options:
    - helpful
    - neutral
    - encouraging
  - name: walkthrough_length
    type: duration
    label: Length of offered walkthrough call
    default: 15 min
    required: false
  requirements:
  - slot: churn_risk_attribute
    kind: attribute
    meaning: A user's computed churn risk score (0-100) with tier label low, medium, high, or critical
  - slot: paying_user_status
    kind: attribute
    meaning: A user's subscription status showing whether they are a paying customer and whether their subscription is active
      or canceled
  - slot: signup_date
    kind: attribute
    meaning: The date a user first signed up
  - slot: save_flow_status
    kind: attribute
    meaning: Whether a user is currently enrolled in an active save or retention flow
  - slot: session_event
    kind: event
    meaning: A customer logged a session in the product
    properties:
    - name: session_start
      type: date
      meaning: When the session started
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled their subscription
  - slot: unsubscribe_event
    kind: event
    meaning: A customer unsubscribed from marketing email
  - slot: feature_usage_event
    kind: event
    meaning: A customer used a product feature
    properties:
    - name: feature_name
      type: string
      meaning: Name of the feature used
      optional: false
  - slot: retention_cohort_features
    kind: knowledge
    meaning: Knowledge of which features are most correlated with retention within each customer cohort
  - slot: email_channel
    kind: integration
    meaning: An email sending integration for outbound messages
    channel: email
  - slot: sms_channel
    kind: integration
    meaning: An SMS sending integration for outbound messages
    optional: true
    channel: sms
  - slot: push_channel
    kind: integration
    meaning: A mobile push notification integration
    optional: true
    channel: push
  - slot: slack_channel
    kind: integration
    meaning: A Slack integration for sending internal alerts to the CSM team
    channel: slack
  - slot: csm_team
    kind: brand
    meaning: The customer success team and named CSMs who send outreach
  - slot: founder_sender
    kind: brand
    meaning: The founder or CEO identity who sends personal critical-tier letters
  - slot: product_feed
    kind: product_feed
    meaning: Catalog of product features with their deep-link URLs
  steps:
  - id: s1
    builds: attribute
    uses:
    - churn_risk_attribute
    - session_event
    - feature_usage_event
    - subscription_canceled_event
    instruction: 'Create an AI-derived attribute on the user object named {churn_risk_attribute}, refreshed daily and on every
      significant behavioral event. Inputs: engagement velocity from session trend over 30, 14 and 7 days, feature usage decay,
      support sentiment trajectory, billing-status signals, peer-cohort churn patterns, and account-level usage for B2B accounts.
      Output a numeric score from 0 to 100 with tier labels: low 0-29, medium 30-59, high 60-79, critical 80-100. Keep it
      tiered, not binary at-risk or not.'
  - id: s2
    builds: segment
    uses:
    - s1
    - churn_risk_attribute
    - paying_user_status
    - signup_date
    - save_flow_status
    - risk_threshold
    - new_user_grace_period
    instruction: Build a segment of paying users with a churn risk score at or above {risk_threshold}, excluding users who
      signed up within {new_user_grace_period} and users already enrolled in an active save flow. The tier partition comes
      from the attribute itself.
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - churn_risk_attribute
    - csm_team
    - founder_sender
    - email_channel
    - product_feed
    - retention_cohort_features
    - medium_tone
    - walkthrough_length
    instruction: 'Write one email per tier. Medium tier: a {medium_tone} educational email on underutilized features that
      drive retention in the user''s cohort, plus a personal ''pick up where you left off'' deep link, sent from the success
      address. High tier: urgent value reinforcement, a signal that a CSM is available, and a specific offer of help such
      as a {walkthrough_length} walkthrough on a named feature, sent from the assigned named CSM. Critical tier: a personal
      letter from the founder or CEO saying the account has not been used much and asking what would help, with a direct calendar
      link and concrete asks.'
  - id: s4
    builds: page
    uses:
    - s1
    - s2
    - s3
    - churn_risk_attribute
    - csm_team
    - founder_sender
    - retention_cohort_features
    - session_event
    instruction: 'Build in-app messages shown when high-tier users log in: a contextual banner pointing to the feature most
      successful users in their segment use, offered as a 60-second walkthrough. For critical-tier users on rare logins, show
      a full-screen modal from the CSM or founder offering a 1:1 call. Show these only when the risk signal is strong, never
      to all users.'
  - id: s5
    builds: recommendation
    uses:
    - s1
    - s2
    - churn_risk_attribute
    - retention_cohort_features
    - product_feed
    - feature_usage_event
    instruction: Configure a recommendation surface for high and critical tier users that lists features the user's cohort
      uses successfully but this user has not adopted, ranked by retention correlation in the user's segment. Render it on
      the dashboard, in email content blocks, and in personalization slots on visits.
  - id: s6
    builds: automation
    uses:
    - s2
    - s3
    - s4
    - s5
    - churn_risk_attribute
    - email_channel
    - push_channel
    - slack_channel
    - csm_team
    - founder_sender
    - subscription_canceled_event
    - unsubscribe_event
    - risk_threshold
    - recovery_window
    - low_followup_delay
    - medium_followup_delay
    - critical_response_window
    instruction: 'Build a tiered journey on the churn-risk segment, branching on tier at entry and re-evaluated weekly. Low
      tier: a light nurture email after {low_followup_delay} with no urgency. Medium tier: email on day 0 with a helpful tip,
      in-app deep link at next login, then the "Write an email per band" medium follow-up email after {medium_followup_delay}
      with the cohort-success recommendations. High tier: CSM email on day 0 with an offer of help, urgent in-app banner at
      next session, and a same-day CSM task. Critical tier: within {critical_response_window} send the founder email, hand
      off to an agent offering a 1:1 call, and create an urgent CSM task and an executive-sponsor task. Weekly, de-escalated
      users exit gracefully and escalated users get the next tier-appropriate touch. Exit when the score stays below {risk_threshold}
      for {recovery_window} (log a retention win), when the subscription is canceled (hand off to the post-cancel winback),
      or when the user unsubscribes.'
  - id: s7
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - s6
    - churn_risk_attribute
    - critical_response_window
    instruction: 'Build a tiered churn intervention dashboard showing: weekly user counts per tier (low, medium, high, critical);
      save rate per tier (share of users who exit risk versus churn); critical-tier CSM response time against a target under
      {critical_response_window}; ARR-weighted save value per tier; and tier migration (high to medium counted as success,
      medium to high as early warning). Also compare predicted churn against actual churn at 30, 60 and 90 days.'
---

# Tiered churn intervention

Slash command: /predictive-churn-tiered-intervention

## Step 1: Score churn risk daily

Create an AI-derived attribute 'churn_risk_score' on the User object, refreshed daily. Inputs: engagement velocity (sessions trend over 30/14/7 days), feature usage decay, support sentiment trajectory, billing-status signals, peer-cohort churn patterns, account-level usage (for B2B). Output: numeric 0-100 with tier label (low (0-29) / medium (30-59) / high (60-79) / critical (80-100). NOT binary at-risk-or-not) the nuance is the point: medium and high get different treatments. Refresh on every significant behavioral event so a sudden engagement drop is caught fast.

## Step 2: Take everyone above 30

Build a parent segment 'Churn risk - paying users' capturing all paying users with churn_risk_score >= 30. Implicitly partitioned by tier through the attribute. Excludes users in the first 14 days (early signals aren't reliable yet) and users already in active save flows (no double-intervention). Use the result of "Score churn risk daily".

## Step 3: Write an email per band

Generate per-tier email content. Medium tier: educational content matched to underutilized features that drive retention in their cohort + personalized 'pick up where you left off' deep-link. Tone: helpful, not alarmed. High tier: urgent value reinforcement, CSM availability signal, specific use-case help offer ('Want a 15-min walkthrough on [feature]?'). Critical tier: founder/CEO personal letter ('I noticed your account hasn't been used much: anything we can do?'), with direct calendar link and concrete asks. Send-from: success@ for medium, named CSM for high, founder/CEO for critical. Use the result of "Score churn risk daily", "Take everyone above 30".

## Step 4: Catch them when they log in

This step builds a page.
Generate in-app messages for high-tier users when they DO log in (rare and precious moments). Format: contextual banner referencing their most-likely-success-path ('Most users in your segment succeed by trying [feature] (want a 60-second walkthrough?'). For critical-tier users on rare logins: a personal-touch interrupt) full-screen modal from the CSM or founder offering a 1:1 call. Never blanket: only when AI signal is strong. Use the result of "Score churn risk daily", "Take everyone above 30", "Write an email per band".

## Step 5: Recommend what keeps people

Configure a recommendation surface specifically for high+critical tier users: surfaces underutilized features that THIS user's cohort uses successfully but THIS user has not adopted (the 'features-that-stick-users' pattern). Renders in-app on dashboard, in email content blocks, and on personalization slots when the user does visit. The recommendation logic prioritizes features with high retention-correlation in this user's segment. Use the result of "Score churn risk daily", "Take everyone above 30".

## Step 6: Treat each band differently

Build a tiered journey wired to the churn-risk segment. Branch on churn_risk tier at entry AND re-evaluate weekly: LOW tier (light-touch nurture email at Day 7 (no urgency, just value content). MEDIUM tier) Touch 1 email Day 0 (helpful tip), Touch 2 in-app at next login (deep-link to retention feature), Touch 3 email Day 7 with recommendation surface highlighting cohort-success features. HIGH tier: Touch 1 email Day 0 from CSM with offer of help, in-app urgent banner on next session, CSM task created same-day. CRITICAL tier: within 4 hours: founder/CEO personal email + agent handoff offering 1:1 call + urgent CSM task + executive-sponsor task. Tier RECOMPUTED weekly: users de-escalate (engagement returned) exit gracefully; users escalate get tier-appropriate next-touch. Exit on: churn_risk drops below 30 for 14+ days (recovered: log retention_win), Subscription canceled (handoff to post-cancel-winback), or unsubscribe. Use the result of "Score churn risk daily", "Take everyone above 30", "Write an email per band", "Catch them when they log in", "Recommend what keeps people".

## Step 7: See if the bands hold up

Compose a tiered churn intervention dashboard: distribution of users across tiers (low/medium/high/critical) per week (leading indicator of book-of-business health, tier-level save rate (% of users in each tier who exit risk vs. churn) proves tiered strategy works), critical-tier CSM response SLA (target: <4hr for human-touch start), ARR-weighted save value by tier, and tier-migration tracking (high to medium = success, medium to high = early warning). Compare model accuracy: predicted churn vs. actual churn at 30/60/90 days. Use the result of "Score churn risk daily", "Take everyone above 30", "Write an email per band", "Catch them when they log in", "Recommend what keeps people", "Treat each band differently".
