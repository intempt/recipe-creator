---
frontmatter_id: next-best-action-orchestration
slash_command: /next-best-action-orchestration
description: A rules-based journey that routes each person to a next step from a candidate set using attributes and segment membership at branch points.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Routes each active user to a next best action (email, in-app, recommendations, agent handoff, or wait) at set journey
    gates, learning from each outcome, with a holdout to measure uplift.
  parameters:
  - name: confidence_threshold
    type: number
    label: Minimum NBA confidence to route (0-100)
    default: 50
    required: false
  - name: gate_schedule
    type: text
    label: Journey gates after signup
    default: 7 d, 14 d, 30 d, 60 d, then weekly
    required: false
  - name: holdout_percent
    type: number
    label: Control holdout percentage
    default: 10
    required: false
  - name: no_engagement_gates
    type: number
    label: Consecutive wait gates before suppression
    default: 3
    required: false
  - name: offer_discount_percent
    type: number
    label: Offer discount percent for the offer variant
    default: 10
    required: false
  - name: recs_refresh_interval
    type: duration
    label: Recommendation refresh interval
    default: 7 d
    required: false
  requirements:
  - slot: user_profile
    kind: attribute
    meaning: User profile attributes such as lifecycle stage, plan, tenure, and engagement signals
  - slot: app_session_event
    kind: event
    meaning: A customer started or was active in the product app session
    properties:
    - name: session_trend
      type: number
      meaning: Trend in session count over recent period
      optional: false
  - slot: pricing_visit_event
    kind: event
    meaning: A customer visited the pricing page
    optional: true
  - slot: feature_first_click_event
    kind: event
    meaning: A customer first clicked a product feature
    properties:
    - name: feature_name
      type: text
      meaning: Name of the feature clicked
      optional: false
    optional: true
  - slot: support_touch_event
    kind: event
    meaning: A customer contacted support
    optional: true
  - slot: high_priority_journey_membership
    kind: segment
    meaning: Users currently enrolled in another high-priority journey
  - slot: active_users_segment
    kind: segment
    meaning: Users who are active in the product
  - slot: nba_attribute
    kind: attribute
    meaning: An AI-derived next best action attribute on the user with recommended action, channel, content theme, and confidence
  - slot: email_channel
    kind: destination
    meaning: Email sending destination for journey messages
    channel: email
  - slot: in_app_channel
    kind: destination
    meaning: In-app messaging surface shown only during active sessions
    optional: true
    channel: push
  - slot: agent_handoff
    kind: integration
    meaning: Integration that opens an agent conversation handoff for a user
    optional: true
    channel: slack
  - slot: product_catalog
    kind: product_feed
    meaning: Product catalog and usage affinity data used for recommendations
    optional: true
  - slot: nba_orchestrated_segment
    kind: segment
    meaning: Active users with NBA confidence above threshold and not in another high-priority journey
    creatable: true
    definition: users who are active and whose next_best_action.confidence >= {confidence_threshold} and who are not in {high_priority_journey_membership}
  - slot: conversion_event
    kind: event
    meaning: A customer completed a conversion such as a deal created, subscription started, or activation milestone
  - slot: sms_connection
    kind: integration
    channel: sms
    meaning: The SMS sender the text goes out from
  steps:
  - id: s1
    builds: attribute
    uses:
    - user_profile
    - app_session_event
    - pricing_visit_event
    - feature_first_click_event
    - support_touch_event
    - nba_attribute
    - confidence_threshold
    instruction: 'Create an AI-derived attribute {nba_attribute} on the user record, refreshed daily and on every significant
      behavioral event. Inputs: lifecycle stage from {user_profile}, session trend from {app_session_event.session_trend},
      feature usage breadth, recent intent signals ({pricing_visit_event}, {feature_first_click_event.feature_name}, {support_touch_event}),
      and prior message engagement. Output a structured object with recommended_action (one of educate, nurture, offer, surface-feature,
      surface-recommendations, handoff-to-agent, wait), recommended_channel (one of email, sms, in_app, push, slack-internal),
      recommended_content_theme, confidence (0-100), and expected_uplift_signal. Routing at each gate reads this attribute.'
  - id: s2
    builds: segment
    uses:
    - s1
    - nba_orchestrated_segment
    - active_users_segment
    - high_priority_journey_membership
    - confidence_threshold
    instruction: Build {nba_orchestrated_segment} from {active_users_segment} where the {nba_attribute} confidence is at least
      {confidence_threshold} and the user is not in {high_priority_journey_membership}. Refresh continuously so users move
      between action sub-cohorts as their recommended action changes.
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - email_channel
    - offer_discount_percent
    instruction: 'Write one email variant per recommended action for {nba_orchestrated_segment}. Educate: short value tip
      matched to the user''s lifecycle stage. Nurture: case study or customer story relevant to the user''s segment. Offer:
      personalized incentive of {offer_discount_percent} percent matched to plan and tenure. Surface-feature: feature spotlight
      with a deep link to the in-app destination. Each variant pulls dynamic content blocks based on the full user profile,
      not only first name. Send through {email_channel}.'
  - id: s4
    builds: page
    uses:
    - s1
    - s2
    - s3
    - in_app_channel
    instruction: 'Create in-app message variants for the surface-feature and surface-recommendations actions. Surface-feature:
      contextual tooltip anchored to the feature with a one-line value proposition and a ''try it'' call to action, shown
      in the relevant in-app location. Surface-recommendations: personalized recommendation card drawn from the user''s product
      affinity. Show in-app messages only during active sessions, never outside the app. Deliver through {in_app_channel}.'
  - id: s5
    builds: recommendation
    uses:
    - s1
    - s2
    - product_catalog
    - recs_refresh_interval
    instruction: 'Configure a recommendation surface ''NBA-driven product and content recs'' that activates when the recommended
      action is surface-recommendations. Sources: the user''s prior interaction history, purchase and usage patterns of similar
      users, and currently trending items in the user''s segment. Render in the in-app sidebar, as an email content block,
      and in a page personalization slot. Refresh every {recs_refresh_interval}.'
  - id: s6
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - email_channel
    - in_app_channel
    - agent_handoff
    - conversion_event
    - gate_schedule
    - no_engagement_gates
    instruction: 'Build an adaptive journey on {nba_orchestrated_segment}. At each gate ({gate_schedule} after signup), read
      {nba_attribute} and route to the matching branch: educate to the ''Write an email per action'' educate variant; nurture
      to the nurture variant; offer to the offer variant with the discount; surface-feature to the in-app tooltip from ''Write
      the in app versions'' plus the surface-feature email; surface-recommendations to activate the ''Build the recommendation
      set'' surface plus an email digest with recommendations; handoff-to-agent to trigger an agent conversation through {agent_handoff};
      wait to skip the touch and recompute at the next gate. Feed each branch outcome (clicked, engaged, converted, ignored)
      back into the next recommendation computation. Exit on {conversion_event}, unsubscribe, or {no_engagement_gates} consecutive
      wait results in a row, which suppresses the user.'
  - id: s7
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - s6
    - holdout_percent
    instruction: 'Compose an NBA orchestration dashboard with four views: distribution of recommended action across users
      to check model balance; engagement rate per branch to show which actions convert; confidence versus conversion correlation
      to test model quality; and uplift versus a {holdout_percent} percent control holdout on fixed cadence, plus per-segment
      NBA quality to set retraining priorities.'
---

# Next best action orchestration

Slash command: /next-best-action-orchestration

## Step 1: Decide the next step per user

Create an AI-derived attribute 'next_best_action' on the User object, refreshed daily and on every significant behavioral event. Inputs: current lifecycle stage, engagement velocity (sessions trend), feature usage breadth, recent intent signals (pricing visit, feature first-click, support touch), and prior message engagement. Outputs: a structured object with (a) recommended_action one of [educate / nurture / offer / surface-feature / surface-recommendations / handoff-to-agent / wait]; (b) recommended_channel [email / sms / in_app / push / slack-internal]; (c) recommended_content_theme; (d) confidence (0-100); (e) expected_uplift_signal. The attribute is the decisioning brain: the journey routes from it at each gate.

## Step 2: Only route confident calls

Build a segment 'NBA-orchestrated users' capturing active users where next_best_action.confidence >= 50 AND user is not currently in another high-priority journey (no double-orchestration). Refreshed continuously, as users' NBA changes, they move between sub-cohorts of this parent segment. Use the result of "Decide the next step per user".

## Step 3: Write an email per action

Generate email content variants per recommended_action: (a) educate variant (short value tip matched to the user's stage; (b) nurture variant) case study/customer story relevant to user's segment; (c) offer variant (personalized incentive (discount / trial extension / credit) matched to plan and tenure; (d) surface-feature variant) feature spotlight with deep-link to the in-app destination. Each variant pulls dynamic content blocks based on the user's full profile, not just first name. Use the result of "Decide the next step per user", "Only route confident calls".

## Step 4: Write the in app versions

This step builds a page.
Generate in-app message variants for the surface-feature and surface-recommendations branches. Surface-feature: contextual tooltip pointing to the feature, with a 1-line value prop and 'try it' CTA, rendered in the relevant in-app location. Surface-recommendations: a personalized recommendation card pulling from the user's product affinity. In-app fires only during active sessions, never outside the app (avoids interruption fatigue). Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action".

## Step 5: Build the recommendation set

Configure a recommendation surface 'NBA-driven product/content recs' that activates when next_best_action.recommended_action = surface-recommendations. Sources: the user's prior interaction history + similar-user purchase/usage patterns + currently-trending items in their segment. Render in: in-app sidebar + email content block + page personalization slot. Refresh weekly. Use the result of "Decide the next step per user", "Only route confident calls".

## Step 6: Re-read the signal at each gate

Build an adaptive journey wired to the NBA segment. At each gate (signup+7d, +14d, +30d, +60d, ongoing weekly), the journey reads next_best_action attribute and routes the user down the matching branch: educate to email variant a; nurture to email variant b; offer to email variant c with discount; surface-feature to in-app tooltip + email variant d; surface-recommendations to activate recommendation surface + email digest with recs; handoff-to-agent to trigger agent conversation; wait to skip touch, recompute next gate. Each branch's outcome (clicked / engaged / converted / ignored) feeds back into the next NBA computation so the decisioning learns. Exit on: conversion event (Deal created / Subscription started / activation_milestone: depending on lifecycle), unsubscribe, or sustained no-engagement (NBA returns wait 3 gates in a row to suppress). Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action", "Write the in app versions", "Build the recommendation set".

## Step 7: Check the model against a control

Compose an NBA orchestration dashboard: distribution of recommended_action across users (which actions does the model favor: sanity check on model balance), per-branch engagement rates (which actions actually convert), confidence-vs-conversion correlation (does higher-confidence routing actually predict higher conversion (model-quality signal), uplift vs control (a 5-10% holdout that gets fixed cadence) the proof-of-value chart), and per-segment NBA quality (model may serve some segments better than others: informs retraining priorities). Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action", "Write the in app versions", "Build the recommendation set", "Re-read the signal at each gate".
