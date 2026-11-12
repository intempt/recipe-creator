---
frontmatter_id: engaged-non-buyer-conversion
slash_command: /engaged-non-buyer-conversion
description: Identifies highly engaged free users who have not converted, sending targeted email check-ins and routing replies using sentiment analysis.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Finds highly engaged free users who have not upgraded, sends blocker-matched email check-ins, runs a diagnostic
    agent chat, and hands qualified signals to a human rep.
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
  - name: segmentWindow
    type: duration
    label: Segment membership window
    default: 60 d
    required: false
  - name: sessionWindow
    type: duration
    label: Session activity window
    default: 30 d
    required: false
  - name: touch2Delay
    type: duration
    label: Delay before in-app chat invitation
    default: 3 d
    required: false
  - name: touch3Delay
    type: duration
    label: Delay before AE outreach task
    default: 7 d
    required: false
  - name: retentionDiscountPercent
    type: number
    label: Retention discount percent for price blocker
    default: 30
    required: false
  - name: retentionDiscountMonths
    type: number
    label: Retention discount duration (months)
    default: 3
    required: false
  - name: sendFromAddress
    type: enum
    label: Send-from address
    default: success
    required: false
    options:
    - success
    - matched_ae
  - name: conversionWindowDays
    type: number
    label: Expected conversion window (days)
    default: 14
    required: false
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
  - slot: email_channel
    kind: destination
    meaning: Email channel to send check-in emails from success or the matched account executive
    channel: email
  - slot: in_app_chat
    kind: destination
    meaning: In-app chat surface where the diagnostic agent can talk to users
    optional: true
    channel: email
  - slot: crm_task_destination
    kind: integration
    meaning: CRM where AE outreach tasks are created with the user's profile
    optional: true
    channel: hubspot
  - slot: diagnostic_knowledge
    kind: knowledge
    meaning: Product pricing, retention discount terms and feature roadmap information for the diagnostic agent
    optional: true
  - slot: engagement_paradox_score
    kind: attribute
    meaning: A 0-100 score of the gap between a user's engagement and their conversion behavior, with an inferred blocker
  - slot: engaged_non_buyers
    kind: segment
    meaning: Engaged free or trialing users with a high engagement paradox score who have not converted
    creatable: true
    definition: users where account age is at least {minAccountAgeDays} days AND subscription_status is free or trialing AND
      engagement_paradox_score is at least {paradoxScoreThreshold}, excluding users in an active sales conversation and users
      who declined an upgrade within {declineLookbackDays}
  steps:
  - id: s1
    builds: attribute
    uses:
    - user_profile
    - engagement_paradox_score
    - sessionWindow
    - paradoxScoreThreshold
    instruction: 'Create an AI-derived attribute {engagement_paradox_score} on the user object. Calculate the gap between
      engagement intensity and conversion behavior using sessions in the last {sessionWindow}, feature breadth and depth,
      marketing email engagement (opens and clicks), and in-product activity compared with typical-converter benchmarks. High
      score means the user behaves like a converter should but has not converted. Output a numeric value from 0 to 100. A
      score of {paradoxScoreThreshold} or higher marks high engagement paradox (engaged but stuck). Include a diagnostic field
      naming the likely blocker as one of: price-sensitivity, feature-gap, authority-issue, decision-paralysis, or no-urgency,
      inferred from behavior patterns.'
  - id: s2
    builds: segment
    uses:
    - engaged_non_buyers
    - account_age_attribute
    - subscription_status
    - engagement_paradox_score
    - sales_conversation_status
    - upgrade_decline_event
    - minAccountAgeDays
    - paradoxScoreThreshold
    - declineLookbackDays
    - s1
    instruction: 'Build the segment {engaged_non_buyers} with these rules: account age is at least {minAccountAgeDays} days
      AND subscription status is free or trialing AND {engagement_paradox_score} is at least {paradoxScoreThreshold}. Exclude
      users currently in an active sales conversation ({sales_conversation_status}) and users who declined an upgrade within
      {declineLookbackDays} ({upgrade_decline_event}). Use the result of "Measure the gap".'
  - id: s3
    builds: email
    uses:
    - engagement_paradox_score
    - engaged_non_buyers
    - email_channel
    - sendFromAddress
    - retentionDiscountPercent
    - retentionDiscountMonths
    - s1
    - s2
    instruction: 'Write one diagnostic email per inferred blocker, using the {engagement_paradox_score} blocker field. Send
      from {sendFromAddress}. Price-sensitivity: tell the user they are using the product like a paid customer and offer a
      {retentionDiscountPercent}% retention discount for the first {retentionDiscountMonths} months. Feature-gap: say they
      tried a feature but did not continue, share what most users do next, and offer 1:1 help if they want it. Authority-issue:
      offer a business-case template and a team usage summary to share with their manager. Decision-paralysis: say they have
      evaluated the product thoroughly and invite them to a 15-minute decision-clarity call. No-urgency: say there is no rush,
      and if a deadline is approaching, offer a limited-time price-lock offer.'
  - id: s4
    builds: agent
    uses:
    - in_app_chat
    - diagnostic_knowledge
    - engagement_paradox_score
    - engaged_non_buyers
    - sessionWindow
    - retentionDiscountPercent
    - retentionDiscountMonths
    - s1
    - s2
    instruction: 'Configure an AI agent named Engaged non-buyer diagnostic that reaches high-paradox users through {in_app_chat}
      or by email reply. Warmly mention the user''s product usage over the past {sessionWindow}, then ask: What is keeping
      you from upgrading: cost, features, internal approval, timing, or something else? Branch on the answer: price routes
      to the retention discount offer at {retentionDiscountPercent}% for {retentionDiscountMonths} months; feature-gap routes
      to the product feedback queue with a feature-roadmap signal; authority routes to business-case generation; timing routes
      to deferred follow-up; anything else routes to human handoff. Produce a qualified diagnostic summary for the account
      executive or customer success manager, not raw chat. Use {diagnostic_knowledge} for pricing and roadmap facts.'
  - id: s5
    builds: automation
    uses:
    - engaged_non_buyers
    - crm_task_destination
    - in_app_chat
    - engagement_paradox_score
    - touch2Delay
    - touch3Delay
    - s3
    - s4
    instruction: 'Build a three-touch diagnostic journey for the {engaged_non_buyers} segment. Touch 1 on day 0 of entry:
      send the diagnostic email matched to the inferred blocker from "Write one email per blocker". Touch 2 after {touch2Delay}
      with no engagement: invite the user to chat with the diagnostic agent from "Configure an AI agent scenario" on their
      next session. Touch 3 after {touch3Delay} with no conversion: create a personalized AE outreach task in {crm_task_destination}
      containing the full engagement-paradox profile, the inferred blocker, and a suggested approach. Exit the journey when
      the subscription starts (celebrate the win), when the user explicitly declines or opts out, or when the agent diagnostic
      completes and hands off to sales, support, or product.'
  - id: s6
    builds: dashboard
    uses:
    - engaged_non_buyers
    - engagement_paradox_score
    - conversionWindowDays
    - s1
    - s2
    - s3
    - s4
    - s5
    instruction: 'Build an engaged non-buyer dashboard with these views: paradox cohort size over time from {engaged_non_buyers}
      (growing or shrinking signals product fit); conversion lift versus a holdout that stays on the generic free-tier nurture;
      conversion by inferred blocker from {engagement_paradox_score} (shows which diagnostic angle converts); agent diagnostic
      completion rate; and time-to-conversion distribution, checking how many conversions happen within {conversionWindowDays}
      days of journey entry. Fewer conversions within that window suggests a structural blocker.'
---

# Engaged users who never buy

Slash command: /engaged-non-buyer-conversion

## Step 1: Measure the gap

Create an AI-derived attribute 'engagement_paradox_score' on the User object. Calculates the gap between engagement intensity and conversion behavior. Inputs: sessions in last 30 days, feature breadth/depth, marketing email engagement (opens / clicks), in-product activity vs. typical-converter benchmarks. High score = the user behaves like a converter SHOULD behave, but hasn't converted. Output: numeric 0-100. Score >= 70 = high engagement paradox (engaged but stuck: the most interesting cohort). Includes a diagnostic field naming the likely blocker (price-sensitivity / feature-gap / authority-issue / decision-paralysis / no-urgency) inferred from behavior patterns.

## Step 2: Find engaged free users

Build a segment 'Engaged non-buyers - last 60 days' capturing users where (a) account age is 30+ days AND (b) subscription_status is free or trialing AND (c) engagement_paradox_score >= 70. Excludes users in active sales conversations (don't double-orchestrate) and users who explicitly declined an upgrade in the last 90 days (respect the no). Use the result of "Measure the gap".

## Step 3: Write one email per blocker

Generate diagnostic email variants per inferred blocker. Price-sensitivity blocker: 'You're using [Product] like a paid customer: here's a 30% retention discount for the first 3 months.' Feature-gap blocker: 'We noticed you tried [feature X] but didn't continue. Here's what most users do next: and 1:1 help if you'd like.' Authority-issue blocker: 'Need help making the case internally? Here's a business-case template + your team's usage summary to share with your manager.' Decision-paralysis blocker: 'You've evaluated [Product] thoroughly. Want a 15-min decision-clarity call?' No-urgency blocker: 'No rush: but if a deadline is approaching, here's a limited-time price-lock offer.' Send-from: success@ or matched AE. Use the result of "Measure the gap", "Find engaged free users".

## Step 4: Ask what is stopping them

Configure an AI agent scenario 'Engaged non-buyer diagnostic' that engages high-engagement-paradox users via in-app chat or email reply. Scenario: surface user's product usage warmly ('I see you've been using [Product] for 45 days: that's great!'), then ask the diagnostic question ('What's keeping you from upgrading? Cost, features, internal approval, timing, or something else?'). Branch on response: route price to retention-discount offer, feature-gap to PM-feedback queue + feature-roadmap signal, authority to business-case generation, timing to deferred-followup, other to human handoff. The agent generates qualified diagnostic signal for the AE/CSM, not raw chat. Use the result of "Measure the gap", "Find engaged free users".

## Step 5: Diagnose, then bring a human in

Build a 3-touch diagnostic journey wired to engaged-non-buyer segment. Touch 1 (Day 0 of entry): diagnostic email matched to inferred blocker. Touch 2 (Day 3, if no engagement): in-app chat invitation to the diagnostic agent on next session. Touch 3 (Day 7, if still no conversion): personalized AE outreach task with the full engagement-paradox profile + inferred blocker + suggested approach attached. Exit on: Subscription started (won (celebrate), explicit decline / opt-out, or successful agent diagnostic (handoff to appropriate downstream) sales, support, or PM). Use the result of "Measure the gap", "Find engaged free users", "Write one email per blocker", "Ask what is stopping them".

## Step 6: See which angle converts

Compose an engaged-non-buyer dashboard: paradox-cohort size over time (is this cohort growing or shrinking: product fit signal), conversion lift vs. control (cohort getting this journey vs. holdout staying on generic free-tier nurture), conversion by inferred blocker (which diagnostic angle actually converts: informs pricing/product/sales-collateral decisions), agent-diagnostic completion rate, and time-to-conversion distribution (most paradox conversions happen within 14 days of journey entry: if not, the blocker is structural). Use the result of "Measure the gap", "Find engaged free users", "Write one email per blocker", "Ask what is stopping them", "Diagnose, then bring a human in".
