---
frontmatter_id: funnel-dropoff-attribution-by-source
slash_command: /funnel-dropoff-attribution-by-source
description: Runs the same acquisition to retention funnel separately for each traffic source, so you can see which channels bring people who actually stick.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows an acquisition-to-retention funnel for each traffic source, so you can see which channels bring in customers
    who stay, with flags and per-source revenue.
  parameters:
  - name: journey_id
    type: string
    label: Journey goal ID used for the Activated step
    required: false
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
    builds: report
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
    instruction: 'Create a funnel report called "Funnel Drop-off by Acquisition Source" with these steps: Step 1 "Acquired"
      uses {user_created_event}; Step 2 "Activated" uses {journey_goal_event} filtered to journey_id {journey_id}; Step 3
      "Converted" uses {subscription_started_event} when {business_model} is saas, or {placed_order_event} when it is ecommerce;
      Step 4 "Retained {retention_window}" uses {session_start_event} occurring at least {retention_window} after the Step
      3 conversion. Set the conversion window to {conversion_window}. Break down by {utm_source_attribute}, keeping the top
      {top_sources} sources by Step 1 volume. Compare against the previous {comparison_period}. Render as small multiples,
      one funnel per source, sorted by end-to-end conversion rate descending. Add a summary table with columns: Source, Volume
      at Step 1, End-to-end conversion %, Volume at final step, and per-source revenue (sum of {subscription_started_event.amount}
      or {placed_order_event.total_price} for users who reached Step 3 or later). Add annotations: flag the source with the
      highest end-to-end conversion whose Step 1 volume is above the 33rd percentile; flag any source whose Step 1 to Step
      2 conversion is below 50% of the average across sources; flag any source whose Step 3 to Step 4 conversion is below
      average; highlight the largest gap between sources at any single step. Surface revenue-weighted ROI per source using
      per-source revenue.'
---

# Funnel drop off by source

Slash command: /funnel-dropoff-attribution-by-source

## Step 1: Run one funnel per source

Create a Funnel report called "Funnel Drop-off by Acquisition Source".
This is a configurable funnel: the user specifies which canonical events make up the funnel. Defaults if unspecified:
1. Event "User created": "Acquired"
2. Event "Completed a journey goal" (configurable journey_id): "Activated"
3. Event "Subscription started" (saas) OR "Placed order" (ecommerce): "Converted"
4. Event "Session start" with date 30+ days after the conversion event: "Retained 30 days"
Conversion window: 60 days
Breakdown: By Users.UTM source (top 8 sources by Step 1 volume)
Compare: Previous period (prior 60 days)
Render as small-multiples: one funnel per source, sorted by end-to-end conversion rate descending.
Also include a summary table:
- Source · Volume at Step 1 · End-to-end conversion % · Volume at final step · Per-source revenue (sum of Subscription started.amount or Placed order.total_price for users who reached Step 3+)
Annotations:
- Flag the source with highest end-to-end conversion AND volume above the 33rd percentile.
- Flag any source where Step 1 to 2 conversion is below 50% of the average across sources (lead-quality issue).
- Flag any source where Step 3 to 4 conversion is below average (conversion fine but customers don't retain).
- Highlight the largest gap between sources at any single step.
Surface the actual revenue-weighted ROI per source.
Taxonomy notes:
- All steps reference canonical events. Users.UTM source is a real first-touch attribution attribute.
- Note: this recipe does NOT compute CAC because ad-spend is not in the canonical taxonomy. Per-source revenue is the closest proxy.
