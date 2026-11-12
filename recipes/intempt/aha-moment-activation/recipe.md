---
frontmatter_id: aha-moment-activation
slash_command: /aha-moment-activation
description: Follows up right after someone hits the action that predicts retention, so the first win turns into a habit instead of a one off.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends a three-touch email sequence after users reach their aha moment, turning a first win into a lasting habit,
    with a dashboard tracking activation and retention.
  parameters:
  - name: aha_lookback
    type: duration
    label: Aha-moment lookback window
    default: 14 d
    required: false
  - name: touch_1_delay
    type: duration
    label: Delay before touch 1
    default: 1 d
    required: false
  - name: touch_2_delay
    type: duration
    label: Delay before touch 2
    default: 5 d
    required: false
  - name: touch_3_delay
    type: duration
    label: Delay before touch 3
    default: 10 d
    required: false
  - name: journey_timeout
    type: duration
    label: Journey timeout
    default: 14 d
    required: false
  - name: email_tone
    type: enum
    label: Email tone
    default: warm_motivating
    required: false
    options:
    - warm_motivating
    - neutral
    - formal
  - name: retention_target_window
    type: duration
    label: Retention comparison window
    default: 30 d
    required: false
  requirements:
  - slot: aha_moment_event
    kind: event
    meaning: A user completed the product's aha-moment action that predicts retention (e.g. first message sent, first project
      published, first deal created)
    properties:
    - name: feature
      type: string
      meaning: Name of the feature or action that was first used
      optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A user started a paid subscription
  - slot: unsubscribed_event
    kind: event
    meaning: A user unsubscribed from marketing emails
  - slot: next_step_feature_event
    kind: event
    meaning: A user used the complementary feature that naturally follows the aha action
    optional: true
  - slot: new_signup_attribute
    kind: attribute
    meaning: A user's signup date, used to measure time from signup to aha moment
  - slot: activation_reinforcement_flag
    kind: attribute
    meaning: Whether a user has already received the activation reinforcement sequence
  - slot: aha_achievers_segment
    kind: segment
    meaning: Users who completed the aha-moment action in the recent window and have not yet received the reinforcement sequence
    creatable: true
    definition: users who completed {aha_moment_event} in the last {aha_lookback} AND whose {activation_reinforcement_flag}
      is not set
  - slot: email_sender
    kind: destination
    meaning: An email channel that can deliver the reinforcement emails
    channel: email
  - slot: product_deep_link_base
    kind: knowledge
    meaning: Product knowledge describing the next-step feature, its how-to, and in-app deep link, plus success stories
  steps:
  - id: s1
    builds: segment
    uses:
    - aha_moment_event
    - activation_reinforcement_flag
    - aha_lookback
    - aha_achievers_segment
    instruction: Build the segment 'Recent aha-moment achievers' with users who completed {aha_moment_event} in the last {aha_lookback}
      and whose {activation_reinforcement_flag} is not set. The aha-moment event is product-specific and should be set by
      the Product team from retention curve analysis; change it in the segment definition.
  - id: s2
    builds: email
    uses:
    - aha_achievers_segment
    - product_deep_link_base
    - email_tone
    - touch_1_delay
    - touch_2_delay
    - touch_3_delay
    instruction: 'Write three reinforcement emails for the aha-achievers segment in a {email_tone} tone. Touch 1 (sent {touch_1_delay}
      after the aha moment): celebrate the milestone, frame it as a meaningful first step, and share one or two success stories
      of users who reached a similar moment. Touch 2 (sent {touch_2_delay} after the aha moment): point to the natural next
      feature that complements the aha action (cross-sell within the product, not an upsell to a plan), with a brief how-to
      and an in-app deep link, using {product_deep_link_base}. Touch 3 (sent {touch_3_delay} after the aha moment): introduce
      a power-user behavior using the line ''now that you''ve done this, here''s how power users go further'', with the aim
      of moving the user from trying the feature to relying on it.'
  - id: s3
    builds: automation
    uses:
    - aha_achievers_segment
    - aha_moment_event
    - next_step_feature_event
    - subscription_started_event
    - unsubscribed_event
    - touch_1_delay
    - touch_2_delay
    - touch_3_delay
    - journey_timeout
    - s2
    instruction: 'Build a three-touch journey for {aha_achievers_segment}, triggered when {aha_moment_event} fires. Send ''Touch
      1'' from step s2 after {touch_1_delay}, ''Touch 2'' from step s2 after {touch_2_delay}, and ''Touch 3'' from step s2
      after {touch_3_delay}. Add a branch: if the user has already used {next_step_feature_event} by the time touch 2 is due,
      skip touch 2 and send touch 3 immediately. Exit the journey when {subscription_started_event} fires (move the user to
      the free-to-paid CSM kickoff handoff), when {unsubscribed_event} fires, or after {journey_timeout} has passed.'
  - id: s4
    builds: report
    uses:
    - new_signup_attribute
    - aha_moment_event
    - retention_target_window
    - s2
    - s3
    instruction: 'Build an activation dashboard with four views: the aha-moment achievement rate among new signups, using
      {new_signup_attribute} as the cohort start (trend matters more than the absolute rate); the distribution of time from
      signup to aha moment; the post-aha retention curve comparing users who achieved the aha moment with those who did not;
      and journey engagement by touch from step s2. Compare 30-day retention of aha-achievers who went through the journey
      with aha-achievers who did not, over {retention_target_window}.'
---

# Aha moment reinforcement

Slash command: /aha-moment-activation

## Step 1: Find people who just got value

Build a segment 'Recent aha-moment achievers' capturing users who completed the aha-moment event (defined per product, e.g. 'first message sent', 'first project published', 'first deal created'; configurable in the segment definition) in the last 14 days AND who haven't received the activation reinforcement yet. The aha-moment event is product-specific and should be set by Product team based on retention curve analysis.

## Step 2: Write three follow up emails

Generate 3-touch reinforcement email content. Touch 1 (24 hours after aha): celebrate the milestone, frame it as a meaningful first step, share 1-2 success stories of users who achieved similar moments. Tone: warm, motivating. Touch 2 (Day 5): point to the natural next feature that complements the aha action (cross-sell within the product, not upsell to plan). Include a brief how-to and an in-app deep link. Touch 3 (Day 10): introduce a power-user behavior: 'now that you've [done aha], here's how power users go further.' Aim: shift user from 'tried it' to 'depends on it'. Use the result of "Find people who just got value".

## Step 3: Send on days 1, 5 and 10

Build a 3-touch journey triggered when feature_first_used = aha-moment fires. Touch 1: Day 1. Touch 2: Day 5. Touch 3: Day 10. Add a branch: if the user has already done the next-step feature naturally by Day 5 (great sign), skip touch 2 and go straight to touch 3 power-user content. Exit on: Subscription started (paid conversion: celebrate and handoff to free-to-paid-csm-kickoff), unsubscribe, or 14-day timeout. Use the result of "Find people who just got value", "Write three follow up emails".

## Step 4: Track activation and retention

Compose an activation funnel dashboard: aha-moment achievement rate among new signups (the activation rate: target depends on product, but trend matters more than absolute), time-from-signup-to-aha distribution, post-aha retention curve (do aha-achievers stick around better than non-achievers?: this is the proof-of-value of focusing activation efforts), and journey engagement by touch. Compare 30-day retention of aha-achievers who went through this journey vs. aha-achievers who didn't (typical lift: 10-20% retention improvement). Use the result of "Find people who just got value", "Write three follow up emails", "Send on days 1, 5 and 10".
