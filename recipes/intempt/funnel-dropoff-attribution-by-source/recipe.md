---
frontmatter_id: funnel-dropoff-attribution-by-source
slash_command: /funnel-dropoff-attribution-by-source
description: Emails a weekly digest of the acquisition to retention funnel for each traffic source, so you can see which channels
  bring people who activate, convert and stay.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of the signup-to-retention funnel per traffic source, with revenue per source and flags
    for weak channels.
  parameters:
  - name: journey_id
    type: string
    label: Journey whose goal marks the Activated step
    required: true
  - name: conversion_window
    type: duration
    label: Conversion window
    default: 60 d
  - name: retention_window
    type: duration
    label: Retention check after conversion
    default: 30 d
  - name: top_sources
    type: number
    label: Number of top traffic sources to break down
    default: 8
  - name: comparison_period
    type: duration
    label: Comparison period (prior period)
    default: 60 d
  - name: business_model
    type: enum
    label: Business model for the Converted step
    default: saas
    options:
    - saas
    - ecommerce
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: user_created_event
    kind: event
    meaning: A new user account was created
  - slot: journey_goal_event
    kind: event
    meaning: A customer completed a journey goal
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey goal completed
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: amount
      type: number
      meaning: Subscription amount paid
      optional: false
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total price of the order
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: utm_source_attribute
    kind: attribute
    meaning: First-touch UTM source of the user
  steps:
  - id: s1
    builds: automation
    uses:
    - user_created_event
    - journey_goal_event
    - subscription_started_event
    - placed_order_event
    - session_start_event
    - utm_source_attribute
    - journey_id
    - conversion_window
    - retention_window
    - top_sources
    - comparison_period
    - business_model
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {user_created_event}
      in the last {comparison_period} against the {comparison_period} before, grouped by {utm_source_attribute} (the top {top_sources}
      sources by signups), through four steps within {conversion_window}: acquired ({user_created_event}); activated ({journey_goal_event}
      with {journey_goal_event.journey_id} equal to {journey_id}); converted ({subscription_started_event} when {business_model}
      is saas, {placed_order_event} when it is ecommerce); retained ({session_start_event} at least {retention_window} after
      converting). It writes per source: users at each step, end-to-end conversion %, revenue (sum of {subscription_started_event.amount}
      or {placed_order_event.total_price}); the best source by end-to-end conversion; sources whose acquired-to-activated
      rate is under half the average; sources whose converted-to-retained rate is below average; the largest gap between sources
      at one step. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing
      else is sent.'
---

# Funnel drop off by source

Slash command: /funnel-dropoff-attribution-by-source

## Step 1: Email the weekly funnel by source digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did user created event in the last 60 d against the 60 d before, grouped by utm source attribute (the top 8 sources by signups), through four steps within 60 d: acquired (user created event); activated (journey goal event with journey id equal to the journey whose goal marks the Activated step); converted (subscription started event when saas is saas, placed order event when it is ecommerce); retained (session start event at least 30 d after converting). It writes per source: users at each step, end-to-end conversion %, revenue (sum of amount or total price); the best source by end-to-end conversion; sources whose acquired-to-activated rate is under half the average; sources whose converted-to-retained rate is below average; the largest gap between sources at one step. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
