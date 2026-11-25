---
frontmatter_id: free-to-paid-csm-kickoff
slash_command: /free-to-paid-csm-kickoff
description: Every upgrade from free to paid emails the CSM team a kickoff brief with the customer's whole free period history,
  due inside five working days, plus a weekly hand-off digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Each free-to-paid upgrade emails the CSM team a kickoff brief with the customer's free-period history, due within
    five business days, plus a weekly hand-off digest.
  parameters:
  - name: conversion_window
    type: duration
    label: Window for recent upgrades
    default: 7 d
    required: false
  - name: min_mrr
    type: number
    label: Minimum MRR for CSM motion (USD)
    default: 50
    required: false
  - name: kickoff_due_days
    type: number
    label: Business days to complete kickoff task
    default: 5
    required: false
  - name: completion_target
    type: number
    label: Target kickoff completion rate (%)
    default: 95
    required: false
  - name: retention_window
    type: duration
    label: Retention measurement window
    default: 90 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the CSMs who get the kickoff briefs
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: mrr
      type: number
      meaning: Monthly recurring revenue of the subscription
      optional: false
    - name: plan_tier
      type: string
      meaning: Plan tier of the subscription (enterprise, SMB, etc.)
      optional: false
  - slot: subscription_status_attribute
    kind: attribute
    meaning: The user's subscription status (free, trialing, paid)
  - slot: signup_event
    kind: event
    meaning: A user signed up for the product
  - slot: feature_used_event
    kind: event
    meaning: A user used a product feature
    properties:
    - name: feature_name
      type: string
      meaning: Name of the feature used
      optional: false
  - slot: kickoff_completed
    kind: event
    meaning: A CSM completed the kickoff call with a new paying customer
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - subscription_started_event
    - subscription_status_attribute
    - signup_event
    - conversion_window
    - min_mrr
    instruction: 'Build a new segment of users named "Free-to-Paid Converters". A user is in it when all of these are true:
      they did {subscription_started_event} in the last {conversion_window} with {subscription_started_event.mrr} of {min_mrr}
      or more; they did {signup_event} at least 1 day before their first {subscription_started_event}; their {subscription_status_attribute}
      is paid.'
  - id: s2
    builds: automation
    uses:
    - s1
    - subscription_started_event
    - signup_event
    - feature_used_event
    - kickoff_due_days
    - alert_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation triggered when a user enters the segment from "Find genuine upgrades". An analysis step
      writes the pre-call brief: days from {signup_event} to {subscription_started_event}; the 5 {feature_used_event.feature_name}
      values they used most while free; key features they never used; how many users from the same account are on free and
      on paid; their {subscription_started_event.plan_tier} and {subscription_started_event.mrr}. Then it emails {alert_recipients}
      the user''s name, email and this brief, asking for a kickoff call within {kickoff_due_days} business days, with a named
      CSM for an enterprise plan tier and the pooled CSM team otherwise.'
  - id: s3
    builds: automation
    uses:
    - s1
    - subscription_started_event
    - signup_event
    - subscription_status_attribute
    - kickoff_completed
    - kickoff_due_days
    - completion_target
    - retention_window
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the segment from
      "Find genuine upgrades" and writes these figures: users who entered it in the last 7 days and the 7 days before; the
      median days from {signup_event} to {subscription_started_event} for them; the share who did {kickoff_completed} within
      {kickoff_due_days} business days, against {completion_target}%; of users who entered {retention_window} ago or earlier,
      the share still paid by {subscription_status_attribute}, split by whether they did {kickoff_completed} in time. Then
      it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Free to paid CSM kickoff

Slash command: /free-to-paid-csm-kickoff

## Step 1: Find genuine upgrades

Build a new segment of users named "Free-to-Paid Converters". A user is in it when all of these are true: they did subscription started event in the last 7 d with mrr of 50 or more; they did signup event at least 1 day before their first subscription started event; their subscription status attribute is paid.

## Step 2: Brief the CSM for kickoff

Build an automation triggered when a user enters the segment from "Find genuine upgrades". An analysis step writes the pre-call brief: days from signup event to subscription started event; the 5 feature name values they used most while free; key features they never used; how many users from the same account are on free and on paid; their plan tier and mrr. Then it emails the email addresses of the CSMs who get the kickoff briefs the user's name, email and this brief, asking for a kickoff call within 5 business days, with a named CSM for an enterprise plan tier and the pooled CSM team otherwise.

## Step 3: Email the weekly hand-off digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the segment from "Find genuine upgrades" and writes these figures: users who entered it in the last 7 days and the 7 days before; the median days from signup event to subscription started event for them; the share who did kickoff completed within 5 business days, against 95%; of users who entered 90 d ago or earlier, the share still paid by subscription status attribute, split by whether they did kickoff completed in time. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
