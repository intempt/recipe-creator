---
frontmatter_id: next-best-action-orchestration
slash_command: /next-best-action-orchestration
description: Scores each active user's next best action from their recent behaviour, sends the email that matches it every
  week, and holds out a control group to measure the uplift.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Picks a next best action for each active user (educate, nurture, offer, feature tip or wait), sends the matching
    email weekly and measures uplift against a holdout.
  parameters:
  - name: holdout_percent
    type: number
    label: Share of users held out as a control (%)
    default: 10
    required: false
  - name: no_engagement_gates
    type: number
    label: Unopened emails in a row before a user is left alone
    default: 3
    required: false
  - name: offer_discount_percent
    type: number
    label: Discount in the offer email (%)
    default: 10
    required: false
  requirements:
  - slot: app_session_event
    kind: event
    meaning: A customer started a session in the product app
  - slot: pricing_visit_event
    kind: event
    meaning: A customer visited the pricing page
  - slot: feature_first_click_event
    kind: event
    meaning: A customer first clicked a product feature
    properties:
    - name: feature_name
      type: string
      meaning: The feature clicked
      optional: false
  - slot: support_touch_event
    kind: event
    meaning: A customer contacted support
  - slot: conversion_event
    kind: event
    meaning: A customer completed a conversion such as a subscription started or an upgrade
  - slot: email_channel
    kind: destination
    meaning: Email sending destination for the action emails
    channel: email
  steps:
  - id: s1
    builds: attribute
    uses:
    - app_session_event
    - pricing_visit_event
    - feature_first_click_event
    - support_touch_event
    instruction: 'Create a computed user attribute named "next_best_action", refreshed daily, for users who did {app_session_event}
      in the last 60 days. The first rule that matches sets the value: "wait" when they did {support_touch_event} in the last
      7 days; "offer" when they did {pricing_visit_event} 2 or more times in the last 14 days; "surface_feature" when they
      did {app_session_event} 3 or more times in the last 14 days and {feature_first_click_event} for fewer than 3 different
      {feature_first_click_event.feature_name} values in the last 30 days; "educate" when they did {app_session_event} 1 or
      2 times in the last 14 days; "nurture" otherwise.'
  - id: s2
    builds: segment
    uses:
    - s1
    - app_session_event
    - conversion_event
    dependsOn:
    - s1
    instruction: Build a new segment of users named "Next Best Action Audience". A user is in it when they did {app_session_event}
      in the last 30 days, their next_best_action attribute from "Decide the next step per user" has a value other than "wait",
      and they did not do {conversion_event} in the last 30 days.
  - id: s3
    builds: email
    uses:
    - s2
    - offer_discount_percent
    dependsOn:
    - s2
    instruction: 'Write four emails for users in the segment from "Only route active users", one per next_best_action value.
      educate: one practical tip that helps a new user get value in five minutes. nurture: a short customer story of a team
      like theirs and what they achieved. offer: {offer_discount_percent}% off the first paid period, with one button to the
      pricing page. surface_feature: a spotlight on one feature they have not tried, with one button that opens it in the
      product. Each is short, with one call to action. If the brand kit has no logo, use the brand name as a plain text header.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - email_channel
    - conversion_event
    - no_engagement_gates
    dependsOn:
    - s1
    - s2
    - s3
    instruction: Build an automation that runs every Monday at 10:00 on a schedule for users in the segment from "Only route
      active users". For each user it reads their next_best_action attribute from "Decide the next step per user" and sends
      the matching email from "Write an email per action" through {email_channel}. It skips users who got one of these emails
      in the last 6 days and users who did {conversion_event} in the last 30 days. It stops sending to a user after {no_engagement_gates}
      of these emails in a row were not opened.
  - id: s5
    builds: experiment
    uses:
    - s2
    - s4
    - conversion_event
    - holdout_percent
    dependsOn:
    - s2
    - s4
    instruction: 'Create an experiment on the automation from "Re-read the signal at each gate" for users in the segment from
      "Only route active users". Hold out {holdout_percent}% of users at random as a control that gets no email from it; the
      rest get the emails as built. Primary metric: share of users who do {conversion_event} within 30 days of entering the
      segment. Secondary metric: share who did {conversion_event} by next_best_action value. Run for 60 days.'
---

# Next best action orchestration

Slash command: /next-best-action-orchestration

## Step 1: Decide the next step per user

Create a computed user attribute named "next_best_action", refreshed daily, for users who did app session event in the last 60 days. The first rule that matches sets the value: "wait" when they did support touch event in the last 7 days; "offer" when they did pricing visit event 2 or more times in the last 14 days; "surface_feature" when they did app session event 3 or more times in the last 14 days and feature first click event for fewer than 3 different feature name values in the last 30 days; "educate" when they did app session event 1 or 2 times in the last 14 days; "nurture" otherwise.

## Step 2: Only route active users

Build a new segment of users named "Next Best Action Audience". A user is in it when they did app session event in the last 30 days, their next_best_action attribute from "Decide the next step per user" has a value other than "wait", and they did not do conversion event in the last 30 days.

## Step 3: Write an email per action

Write four emails for users in the segment from "Only route active users", one per next_best_action value. educate: one practical tip that helps a new user get value in five minutes. nurture: a short customer story of a team like theirs and what they achieved. offer: 10% off the first paid period, with one button to the pricing page. surface_feature: a spotlight on one feature they have not tried, with one button that opens it in the product. Each is short, with one call to action. If the brand kit has no logo, use the brand name as a plain text header.

## Step 4: Re-read the signal at each gate

Build an automation that runs every Monday at 10:00 on a schedule for users in the segment from "Only route active users". For each user it reads their next_best_action attribute from "Decide the next step per user" and sends the matching email from "Write an email per action" through email channel. It skips users who got one of these emails in the last 6 days and users who did conversion event in the last 30 days. It stops sending to a user after 3 of these emails in a row were not opened.

## Step 5: Check the model against a control

Create an experiment on the automation from "Re-read the signal at each gate" for users in the segment from "Only route active users". Hold out 10% of users at random as a control that gets no email from it; the rest get the emails as built. Primary metric: share of users who do conversion event within 30 days of entering the segment. Secondary metric: share who did conversion event by next_best_action value. Run for 60 days.
