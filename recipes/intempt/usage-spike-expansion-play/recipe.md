---
frontmatter_id: usage-spike-expansion-play
slash_command: /usage-spike-expansion-play
description: When an existing paying account crosses usage thresholds, enroll the contact in an expansion journey and send upgrade-focused messages to that same profile. Report journey activity in dashboards.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: When a paying account crosses usage thresholds, it gets an expansion journey with upgrade-focused emails to the
    champion and budget holder, in-app plan comparisons, an AE task if needed, and dashboard reporting.
  parameters:
  - name: expansion_score_threshold
    type: number
    label: Expansion signal score threshold (0-100)
    default: 70
    required: false
  - name: signal_window
    type: duration
    label: Lookback window for expansion signal
    default: 14 d
    required: false
  - name: exit_score_floor
    type: number
    label: Score below which the account exits the journey
    default: 50
    required: false
  - name: exit_quiet_period
    type: duration
    label: Duration the score must stay below the floor before exit
    default: 30 d
    required: false
  - name: journey_duration
    type: duration
    label: How long the recommendation surface stays active
    default: 60 d
    required: false
  - name: ae_task_delay
    type: duration
    label: Wait before creating AE task if no meeting booked
    default: 14 d
    required: false
  - name: usage_growth_window
    type: duration
    label: Window for active-user growth measurement
    default: 30 d
    required: false
  - name: growth_baseline_window
    type: duration
    label: Baseline window for active-user growth
    default: 90 d
    required: false
  - name: champion_tone
    type: enum
    label: Tone for champion emails
    default: peer-to-peer enablement
    required: false
    options:
    - peer-to-peer enablement
    - neutral
    - formal
  - name: buyer_tone
    type: enum
    label: Tone for budget holder emails
    default: business-formal, value-substantive
    required: false
    options:
    - business-formal, value-substantive
    - neutral
    - friendly
  - name: feature_depth_percentile
    type: number
    label: Feature-depth percentile cited in champion email
    default: 85
    required: false
  - name: top_depth_percentile
    type: number
    label: Top-depth percentile cited in budget holder email
    default: 15
    required: false
  requirements:
  - slot: paying_account
    kind: segment
    meaning: Existing paying accounts with users and a subscription
  - slot: account_usage_event
    kind: event
    meaning: A customer account's product usage was recorded
    properties:
    - name: feature
      type: text
      meaning: Feature used
      optional: false
    - name: user_id
      type: text
      meaning: Active user identifier
      optional: false
  - slot: expansion_deal
    kind: event
    meaning: An expansion or upgrade deal was opened for an account
    properties:
    - name: deal_status
      type: text
      meaning: Current status of the deal
      optional: false
  - slot: expansion_signal_score
    kind: attribute
    meaning: Composite 0-100 expansion signal score on the account
  - slot: champion_user
    kind: attribute
    meaning: The most active user at the account, used as champion
  - slot: budget_holder_contact
    kind: attribute
    meaning: Economic buyer contact at the account (admin, manager, or finance owner)
  - slot: expansion_segment
    kind: segment
    meaning: Accounts currently expansion-ready
    creatable: true
    definition: accounts in {paying_account} where {expansion_signal_score} is at least {expansion_score_threshold} within
      the last {signal_window} and no open {expansion_deal} exists
  - slot: crm_ae_owner
    kind: integration
    meaning: CRM integration that can create tasks and deals for the assigned account executive
    channel: hubspot
  - slot: email_channel
    kind: destination
    meaning: Email sending destination for champion and buyer messages
    channel: email
  - slot: product_knowledge
    kind: knowledge
    meaning: Product tier and feature catalog describing higher-tier plan features
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_usage_event
    - paying_account
    - growth_baseline_window
    - usage_growth_window
    instruction: 'Create an AI-derived account attribute named expansion_signal_score on {paying_account}. Inputs: (a) active-user
      growth rate, new users added from the account''s domain in the last {usage_growth_window} versus the trailing {growth_baseline_window}
      baseline; (b) feature-depth expansion, the count of distinct features used per active user from {account_usage_event.feature}
      trending up; (c) multi-team adoption, users from different functions or departments based on email domain or profile
      data; (d) usage-cap proximity across seats, API calls, events and storage; (e) integration-attach, new integrations
      connected, which signals deeper commitment. Output a 0-100 score plus a composite reasoning string that states which
      signals are firing.'
  - id: s2
    builds: segment
    uses:
    - s1
    - expansion_segment
    - expansion_score_threshold
    - signal_window
    - expansion_deal
    instruction: 'Build the segment named Expansion-ready customer accounts: existing paying accounts where {expansion_signal_score}
      is at least {expansion_score_threshold} within the last {signal_window} and no open {expansion_deal} exists, so the
      team does not double-orchestrate against AE work. Partition the segment by dominant signal type (user-growth, feature-depth,
      or usage-cap) so the journey can branch on it. Use the result of "Score the expansion signals".'
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - champion_user
    - champion_tone
    - feature_depth_percentile
    - email_channel
    instruction: 'Write a champion email to {champion_user}, the most active user at the account. Tone: {champion_tone}. The
      champion should feel proud, not pitched. Variant user-growth: subject ''Your team is growing on the product'', body
      explaining how power-using teams stay organized at this scale. Variant feature-depth: subject ''You are using the product
      deeper than {feature_depth_percentile}% of similar accounts'', body with what is next. Variant usage-cap: subject ''Your
      team is approaching the resource limit. Here are options.'' Use the result of "Score the expansion signals" and "Find
      accounts outgrowing the plan".'
  - id: s4
    builds: email
    uses:
    - s1
    - s2
    - s3
    - budget_holder_contact
    - buyer_tone
    - top_depth_percentile
    - crm_ae_owner
    - email_channel
    instruction: 'Write a budget-holder email to {budget_holder_contact}, who is often not using the product day to day. Tone:
      {buyer_tone}. Variant user-growth: subject ''Your team''s usage grew this quarter, here is a business-case summary of
      value delivered'', with the growth percentage and value summary. Variant feature-depth: subject ''Your team is in the
      top {top_depth_percentile}% of users by depth; let''s discuss expansion options''. Variant usage-cap: subject ''Cost
      comparison: upgrade versus current overage costs'', including an ROI snapshot. Set reply-to as the assigned account
      executive from {crm_ae_owner}. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan"
      and "Write to the champion".'
  - id: s5
    builds: recommendation
    uses:
    - s1
    - s2
    - product_knowledge
    - journey_duration
    instruction: 'Configure a recommendation surface named Expansion features that activates when an account is in {expansion_segment}.
      Render it in-app on the admin dashboard and in the email touches. Show features available on higher-tier plans that
      the account would benefit from, based on current usage patterns, phrased as ''Teams using [current features] often graduate
      to [advanced features]: here is what they unlock''. Include an upgrade-comparison surface for plan decision-makers.
      Keep the surface active for {journey_duration}. Use the result of "Score the expansion signals" and "Find accounts outgrowing
      the plan".'
  - id: s6
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - expansion_segment
    - ae_task_delay
    - exit_score_floor
    - exit_quiet_period
    - expansion_signal_score
    - crm_ae_owner
    - email_channel
    instruction: 'Build a multi-stakeholder journey that starts when an account enters {expansion_segment}. Day 0: send the
      champion email from "Write to the champion" with the variant matching the dominant signal. Day 3: activate the upgrade-comparison
      surface from "Show the plan above theirs" for admin users at the account on their next session. Day 7: send the budget-holder
      email from "Write to the budget holder" with an AE meeting call to action. Day 14: if no meeting is booked, create an
      AE task in {crm_ae_owner} after {ae_task_delay} with the full account context attached (signals, decision-makers, recommended
      package). Keep the recommendation surface active for {journey_duration}. Exit when a meeting is scheduled (hand off
      to AE), when upgrade_completed fires (celebrate), when an expansion deal is created (AE owns from there), or when {expansion_signal_score}
      stays below {exit_score_floor} for {exit_quiet_period} (exit gracefully). Use the results of the earlier steps.'
  - id: s7
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - s6
    instruction: 'Build an expansion performance dashboard showing: expansion-signal volume per week by signal type; expansion-signal-to-meeting
      conversion; expansion-signal-to-deal-created conversion; ARR uplift from journey-attributed expansion, cohort-attributed
      versus control; signal-type effectiveness comparing user-growth, feature-depth and usage-cap conversion; and NRR contribution
      from this play. Use the results of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the
      champion", "Write to the budget holder", "Show the plan above theirs" and "Work the account over two weeks".'
---

# Expansion play on a usage spike

Slash command: /usage-spike-expansion-play

## Step 1: Score the expansion signals

Create an AI-derived attribute 'expansion_signal_score' on the Account object. Inputs: (a) active-user growth rate (new users added from domain in last 30 days vs. trailing 90-day baseline); (b) feature-depth expansion (count of distinct features used per active user trending up); (c) multi-team adoption (users from different functions / departments based on email domain or profile data); (d) usage-cap proximity (seats / API calls / events / storage); (e) integration-attach (new integrations connected: signals deeper commitment). Output: 0-100 score with composite reasoning string explaining which signals are firing.

## Step 2: Find accounts outgrowing the plan

Build a segment 'Expansion-ready customer accounts' capturing existing paying accounts where expansion_signal_score >= 70 in the last 14 days AND no active expansion deal already in flight (don't double-orchestrate against AE work). Partitioned by primary signal type so the journey can branch on the dominant signal (user-growth-driven vs. feature-depth-driven vs. usage-cap-driven). Use the result of "Score the expansion signals".

## Step 3: Write to the champion

Generate email content for the user-champion at the account (the most-active user, usually). Variants by signal type: user-growth ('Your team is growing on [Product]) here's how power-using teams stay organized at this scale.' Feature-depth ('You're using [Product] deeper than 85% of similar accounts) here's what's next.' Usage-cap: 'Your team is approaching the [resource] limit. Here are options.' Tone: peer-to-peer enablement, not sales pitch. The champion should feel proud, not pitched. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan".

## Step 4: Write to the budget holder

Generate email content for the economic buyer at the account (often someone NOT actively using the product day-to-day (admin / manager / finance owner). Variants by signal type: user-growth) 'Your team's usage of [Product] grew [N%] this quarter (here's a business-case summary of value delivered.' Feature-depth) 'Your team is in the top 15% of [Product] users by depth (let's discuss expansion options.' Usage-cap) 'Cost-comparison: upgrade vs. current overage costs.' Includes ROI snapshot. Tone: business-formal, value-substantive. Reply-to: assigned AE. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion".

## Step 5: Show the plan above theirs

Configure a recommendation surface 'Expansion features' that activates when the account is in the expansion segment. Renders in-app on the admin dashboard and in the email touches. Pulls: features available on higher-tier plans that the account would benefit from based on current usage patterns (e.g., 'Teams using [current features] often graduate to [advanced features]: here's what they unlock'). Includes upgrade-comparison surface for plan-decision-makers. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan".

## Step 6: Work the account over two weeks

Build a multi-stakeholder journey triggered when an account enters expansion-ready segment. Touch 1 (Day 0): champion email: 'you're growing fast / using deeply / hitting limits' content. Touch 2 (Day 3): in-app upgrade-comparison surface activates for admin users at the account on next session. Touch 3 (Day 7): economic-buyer email with ROI summary and AE meeting CTA. Touch 4 (Day 14): if no AE meeting booked, create AE task with the full account context attached (signals, decision-makers, recommended package). Recommendation surface stays active for 60 days. Exit on: Meeting scheduled (handoff to AE), upgrade_completed (success (celebrate), Deal created (AE-owned from here), or expansion_signal drops below 50 for 30 days (false signal) exit gracefully). Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion", "Write to the budget holder", "Show the plan above theirs".

## Step 7: Measure the expansion it makes

Compose an expansion performance dashboard: expansion-signal volume per week by signal type (which signals fire most: informs which expansion levers the product naturally creates), expansion-signal-to-meeting conversion, expansion-signal-to-deal-created conversion, ARR uplift from journey-attributed expansion (cohort-attributed vs. control), and signal-type effectiveness (does user-growth signal convert better than feature-depth: informs product/marketing focus). NRR contribution from this play. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion", "Write to the budget holder", "Show the plan above theirs", "Work the account over two weeks".
