---
frontmatter_id: feature-discovery-for-paid-users
slash_command: /feature-discovery-for-paid-users
description: Finds the features each paying customer has never opened, picks the next one for the way they use the product,
  and emails a deep-link nudge up to three times, two weeks apart.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows paying customers the features they have never opened, one at a time, with a deep-link email nudge up to three
    times, and emails a weekly adoption digest.
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
    label: Cooldown after a feature-discovery series
    default: 30 d
    required: false
  - name: touch_interval
    type: duration
    label: Days between nudges
    default: 14 d
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
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: plan
    kind: attribute
    meaning: The user's plan; a value that is not free or trial means a paying customer
  - slot: subscription_start
    kind: attribute
    meaning: Date the user's paid subscription started
  - slot: feature_usage_event
    kind: event
    meaning: A customer used a product feature
    properties:
    - name: feature_name
      type: string
      meaning: Name of the feature used
      optional: false
  - slot: session_event
    kind: event
    meaning: A customer started an app session
  - slot: cancel_flow_event
    kind: event
    meaning: A customer opened the cancellation flow
  - slot: feature_catalog
    kind: product_feed
    meaning: Catalog of product features with the plans that include them, a benefit line and a deep link
  steps:
  - id: s1
    builds: attribute
    uses:
    - plan
    - feature_usage_event
    - feature_catalog
    - untouched_lookback
    instruction: Build a computed attribute on users named "untouched_features", recomputed weekly, for users whose {plan}
      has a value that is not free or trial. It lists up to 3 features from {feature_catalog} included in the user's {plan}
      that the user did not use as {feature_usage_event.feature_name} in the last {untouched_lookback}, ordered by how often
      users on the same {plan} who kept paying use them, highest first.
  - id: s2
    builds: segment
    uses:
    - s1
    - plan
    - subscription_start
    - session_event
    - cancel_flow_event
    - min_subscription_age
    - min_sessions
    - session_window
    dependsOn:
    - s1
    instruction: Build a new segment of users named "Feature discovery audience". A user is in it when their {plan} has a
      value that is not free or trial, their {subscription_start} is more than {min_subscription_age} ago, the attribute from
      "Find features they never use" has at least one feature, they did {session_event} {min_sessions} or more times in the
      last {session_window}, and they did not do {cancel_flow_event} in the last 30 days.
  - id: s3
    builds: email
    uses:
    - s1
    - feature_catalog
    - nudge_tone
    dependsOn:
    - s1
    instruction: Write an email for paying users that introduces the first feature in their attribute from "Find features
      they never use". The subject and first line name that feature and its benefit from {feature_catalog}; the body gives
      one short example of the feature at work and one button with the feature's deep link from {feature_catalog}. In a {nudge_tone}
      tone, as a helpful tip, never implying they are not getting value.
  - id: s4
    builds: automation
    uses:
    - s2
    - s3
    - cancel_flow_event
    - touch_interval
    - nudge_cooldown
    dependsOn:
    - s2
    - s3
    instruction: Build an automation triggered when a user enters the segment from "Pick who is worth nudging", at most once
      per {nudge_cooldown}. It sends the email from "Write the nudge", waits {touch_interval}, sends it again, waits {touch_interval},
      and sends it a third time; each send shows the user's first untouched feature at that moment. It stops when the user
      leaves the segment or does {cancel_flow_event}.
  - id: s5
    builds: automation
    uses:
    - s1
    - s4
    - feature_usage_event
    - digest_recipients
    dependsOn:
    - s1
    - s4
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users sent the email
      by "One feature every two weeks" and writes these figures: nudges sent in the last 7 days by feature; the share who
      did {feature_usage_event} with that {feature_usage_event.feature_name} within 14 days of the nudge, by feature; how
      often each feature appears in the attribute from "Find features they never use". Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Feature discovery for paid users

Slash command: /feature-discovery-for-paid-users

## Step 1: Find features they never use

Build a computed attribute on users named "untouched_features", recomputed weekly, for users whose plan has a value that is not free or trial. It lists up to 3 features from feature catalog included in the user's plan that the user did not use as feature name in the last 90 d, ordered by how often users on the same plan who kept paying use them, highest first.

## Step 2: Pick who is worth nudging

Build a new segment of users named "Feature discovery audience". A user is in it when their plan has a value that is not free or trial, their subscription start is more than 30 d ago, the attribute from "Find features they never use" has at least one feature, they did session event 2 or more times in the last 14 d, and they did not do cancel flow event in the last 30 days.

## Step 3: Write the nudge

Write an email for paying users that introduces the first feature in their attribute from "Find features they never use". The subject and first line name that feature and its benefit from feature catalog; the body gives one short example of the feature at work and one button with the feature's deep link from feature catalog. In a helpful tone, as a helpful tip, never implying they are not getting value.

## Step 4: One feature every two weeks

Build an automation triggered when a user enters the segment from "Pick who is worth nudging", at most once per 30 d. It sends the email from "Write the nudge", waits 14 d, sends it again, waits 14 d, and sends it a third time; each send shows the user's first untouched feature at that moment. It stops when the user leaves the segment or does cancel flow event.

## Step 5: Email the weekly adoption digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users sent the email by "One feature every two weeks" and writes these figures: nudges sent in the last 7 days by feature; the share who did feature usage event with that feature name within 14 days of the nudge, by feature; how often each feature appears in the attribute from "Find features they never use". Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
