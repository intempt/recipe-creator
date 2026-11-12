---
frontmatter_id: feature-discovery-for-paid-users
slash_command: /feature-discovery-for-paid-users
description: Shows paying customers the features they have never opened, one at a time, picked for the way they actually use the product.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows paying customers the features they have never opened, one at a time, chosen by how they use the product,
    with a deep-link nudge sent up to three times over 28 days.
  parameters:
  - name: untouched_lookback
    type: duration
    label: Feature usage lookback window
    default: 90 d
    required: false
  - name: min_subscription_age
    type: duration
    label: Minimum subscription age
    default: 30 d
    required: false
  - name: min_sessions
    type: number
    label: Minimum sessions in recent window
    default: 2
    required: false
  - name: session_window
    type: duration
    label: Recent session window
    default: 14 d
    required: false
  - name: nudge_cooldown
    type: duration
    label: Cooldown after a feature-discovery nudge
    default: 30 d
    required: false
  - name: touch_interval
    type: duration
    label: Days between journey touches
    default: 14 d
    required: false
  - name: journey_max_length
    type: duration
    label: Maximum journey length
    default: 60 d
    required: false
  - name: nudge_tone
    type: enum
    label: Email tone
    default: helpful
    required: false
    options:
    - helpful
    - friendly
    - direct
  requirements:
  - slot: paid_user_profile
    kind: attribute
    meaning: A user's paid subscription status and subscription start date
  - slot: feature_usage_event
    kind: event
    meaning: A customer used a product feature
    properties:
    - name: feature_name
      type: string
      meaning: Name of the feature used
      optional: false
    - name: plan
      type: string
      meaning: Plan the customer was on when using the feature
      optional: true
  - slot: session_event
    kind: event
    meaning: A customer started an app session
  - slot: feature_catalog
    kind: product_feed
    meaning: Catalog of product features with their plan inclusion and benefit metrics
  - slot: email_channel
    kind: destination
    meaning: Email sending integration used to deliver nudges
    channel: email
  - slot: cancel_flow_event
    kind: event
    meaning: A customer opened the cancellation flow
  - slot: feature_adoption_event
    kind: event
    meaning: A customer used a specific feature after receiving a nudge
    properties:
    - name: feature_name
      type: string
      meaning: Name of the feature adopted
      optional: false
  - slot: feature_discovery_audience
    kind: segment
    meaning: Paid users eligible for feature-discovery nudges
    creatable: true
    definition: users who are on a paid plan with subscription age of at least {min_subscription_age}, have a non-empty untouched
      features list, had at least {min_sessions} sessions in the last {session_window}, are not in initial onboarding, and
      have not received a feature-discovery nudge in the last {nudge_cooldown}
  steps:
  - id: s1
    builds: attribute
    uses:
    - paid_user_profile
    - feature_usage_event
    - feature_catalog
    - untouched_lookback
    instruction: Create an AI-derived user attribute named 'untouched_features' on the User object, recomputed weekly. For
      each user, compare features touched in the last {untouched_lookback} against the features in {feature_catalog} available
      on the user's plan, excluding any feature the user's plan does not include. Rank the untouched features by (a) historical
      correlation with retention among similar users and (b) fit with the user's use case inferred from segment, industry,
      or role. Store the top 3 as an ordered list with the recommended order.
  - id: s2
    builds: segment
    uses:
    - s1
    - paid_user_profile
    - session_event
    - min_subscription_age
    - min_sessions
    - session_window
    - nudge_cooldown
    instruction: Build a segment named 'Feature discovery audience' of paid users where subscription age is at least {min_subscription_age},
      the 'untouched_features' list from "Find features they never use" is non-empty, and the user had at least {min_sessions}
      sessions in the last {session_window}. Exclude users still in initial onboarding and users who received a feature-discovery
      nudge in the last {nudge_cooldown}.
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - email_channel
    - nudge_tone
    instruction: 'Create one email template that pulls each recipient''s top untouched feature from "Find features they never
      use" for users in "Pick who is worth nudging". Subject: ''[First name], you haven''t tried feature yet'', naming the
      specific feature and its specific benefit. Body: a short value statement for the feature with an average time or effort
      saving metric, a brief use-case description matched to the recipient''s segment, a screenshot or short GIF of the feature
      in use, and a deep-link call to action that opens the feature in the app. Use a {nudge_tone} tone, as a helpful nudge
      rather than an accusatory message about not getting value from the subscription.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - touch_interval
    - journey_max_length
    - cancel_flow_event
    - feature_adoption_event
    instruction: Build a journey that enters users weekly from "Pick who is worth nudging". Touch 1 sends the top feature
      from "Write the nudge" on Day 0. Touch 2 sends the second untouched feature on Day {touch_interval}. Touch 3 sends the
      third untouched feature on Day {touch_interval} after touch 2. Each touch must feature a different untouched feature
      from the user's list. Skip a touch if the user has started using that feature since the previous touch. Exit the user
      when they adopt all 3 features, when they open the cancellation flow (hand off to the pre-cancellation save journey),
      or when {journey_max_length} has elapsed.
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - feature_adoption_event
    - feature_discovery_audience
    instruction: 'Build a feature adoption dashboard with four panels. (1) Feature-discovery email volume broken down by feature,
      to show which features need the most nudging, which may signal weak in-app discoverability. (2) Feature adoption rate
      after nudge: the percentage of recipients from "Pick who is worth nudging" who used the feature within 14 days of the
      nudge, with a typical range of 8-15%. (3) Retention lift from adoption: 90-day retention of users who adopted a feature
      after a nudge compared with a control group. (4) Untouched-feature distribution: how often each feature appears as never-touched,
      to show product teams where discoverability gaps are. Source the data from "Find features they never use", "Pick who
      is worth nudging", "Write the nudge", and "One feature every two weeks".'
---

# Feature discovery for paid users

Slash command: /feature-discovery-for-paid-users

## Step 1: Find features they never use

Create an AI-derived attribute 'untouched_features' on the User object. Computed weekly. For each user, compare features-touched in last 90 days against the catalog of features available on their plan, and surface the top 3 high-value features they haven't used. Prioritize features by: (a) historical correlation with retention among similar users, (b) features the user's use case (inferred from segment / industry / role) suggests they should benefit from. Excludes features that the user's plan doesn't include. Output: ranked list of 3 untouched features with the recommended order.

## Step 2: Pick who is worth nudging

Build a segment 'Feature discovery audience' capturing paid users where subscription is at least 30 days old AND untouched_features list is non-empty AND the user has had at least 2 sessions in the last 14 days (active enough to benefit from a feature nudge). Excludes users in initial onboarding (different motion) and users who already received a feature-discovery nudge in the last 30 days. Use the result of "Find features they never use".

## Step 3: Write the nudge

Generate per-feature discovery email templates (one template that pulls the top untouched feature per recipient). Subject: '[First name], you haven't tried [feature] yet': specific feature, specific benefit. Body: brief value statement of the feature ('Users who use [feature] save an average of [time/effort metric]'), a short use-case description that matches the user's segment, a screenshot or short GIF showing the feature in action, and a deep-link CTA into the app at the right place. Tone: helpful nudge, not 'we noticed you're not getting your money's worth' (which feels accusatory). Use the result of "Find features they never use", "Pick who is worth nudging".

## Step 4: One feature every two weeks

Build a 3-touch journey triggered weekly for users in the feature-discovery segment. Each touch surfaces a DIFFERENT untouched feature from the user's list (not the same feature 3 times). Touch 1: top feature, Day 0. Touch 2: second feature, Day 14. Touch 3: third feature, Day 28. Skip a touch if the user actually started using that feature between touches (they got the message: don't pester). Exit on: user adopts all 3 features (success), user opens cancel-flow (handoff to pre-cancellation-save), or 60-day completion. Use the result of "Find features they never use", "Pick who is worth nudging", "Write the nudge".

## Step 5: See what the nudges actually change

Compose a feature adoption dashboard: feature-discovery email volume by feature (which features need the most nudge: could signal weak in-app discoverability), feature-adoption rate after nudge (% of recipients who use the feature within 14 days of receiving the nudge: typical: 8-15%), retention lift from adoption (compare 90-day retention of users who adopted post-nudge vs. control), and untouched-feature distribution (which features are most-commonly never-touched: informs product team where the discoverability gaps are). Use the result of "Find features they never use", "Pick who is worth nudging", "Write the nudge", "One feature every two weeks".
