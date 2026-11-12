---
frontmatter_id: personalization-recs
slash_command: /personalization-recs
description: Generates catalog-aware product recommendations tailored to user cohorts and evaluates their performance with A/B experiments.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows shoppers catalog-aware product recommendations tailored to their cohort on site, cart, post-purchase and
    email, and measures their performance through A/B tests.
  parameters:
  - name: high_intent_window
    type: duration
    label: Look-back window for high-intent browsing
    default: 7 d
    required: false
  - name: control_variant
    type: enum
    label: Baseline variant compared against personalized recs
    default: trending
    required: false
    options:
    - trending
    - editors_pick
  requirements:
  - slot: product_catalog
    kind: product_feed
    meaning: A product catalog feed with product details used to source recommendations
  - slot: product_viewed
    kind: event
    meaning: A customer viewed a product page
    properties:
    - name: product_id
      type: string
      meaning: Identifier of the product viewed
      optional: false
  - slot: order_completed
    kind: event
    meaning: A customer completed an order
    properties:
    - name: product_id
      type: string
      meaning: Identifier of the product purchased
      optional: true
  - slot: recommendation_cohort_segments
    kind: segment
    meaning: Shopper cohorts such as new visitor, browsing, returning and lapsed
    optional: true
  - slot: high_intent_browsers
    kind: segment
    meaning: Shoppers who browsed products repeatedly without buying
    optional: true
  - slot: email_channel
    kind: integration
    meaning: An email sending integration for campaign and journey emails
    channel: email
  steps:
  - id: s1
    builds: recommendation
    uses:
    - product_catalog
    instruction: Configure a recommendation engine sourcing from {product_catalog} using collaborative-filtering and item-similarity
      models.
  - id: s2
    builds: personalization
    uses:
    - s1
    instruction: Configure personalization rules serving recommendations from "Build the recommendation model" on the product
      detail page, cart, post-purchase, and email surfaces.
  - id: s3
    builds: segment
    uses:
    - s1
    - s2
    - product_viewed
    - order_completed
    instruction: Segment users into recommendation cohorts (new visitor, browsing, returning, lapsed) for tuned strategies,
      using {product_viewed} and {order_completed}, applied to the surfaces in "Place them on each surface".
  - id: s4
    builds: experiment
    uses:
    - s1
    - s2
    - s3
    - control_variant
    instruction: Add A/B variants comparing personalized recommendations against trending products and editor's-pick, per
      cohort from "Split shoppers into cohorts", using the baseline {control_variant}.
  - id: s5
    builds: email
    uses:
    - s1
    - s2
    - s3
    - s4
    - email_channel
    instruction: Generate email modules that surface recommendations from "Build the recommendation model" within campaign
      and journey emails, assigned to cohorts from "Split shoppers into cohorts" and variants from "Test against the alternatives".
  - id: s6
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - high_intent_browsers
    - high_intent_window
    - email_channel
    instruction: Build a journey that sends personalized product picks from "Build the email modules" to {high_intent_browsers}
      who viewed products within {high_intent_window}, using the recommendations from "Build the recommendation model".
  - id: s7
    builds: dashboard
    uses:
    - s2
    - s4
    - s5
    - s6
    instruction: Compose a dashboard tracking recommendation click-through rate, attributed revenue, and per-surface performance
      across "Place them on each surface", "Test against the alternatives", "Build the email modules", and "Follow up with
      high-intent browsers".
---

# Product recommendations across channels

Slash command: /personalization-recs

## Step 1: Build the recommendation model

Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity models.

## Step 2: Place them on each surface

Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces. Use the result of "Build the recommendation model".

## Step 3: Split shoppers into cohorts

Segment users into recommendation cohorts (new visitor, browsing, returning, lapsed) for tuned strategies. Use the result of "Build the recommendation model", "Place them on each surface".

## Step 4: Test against the alternatives

Add A/B variants comparing personalized recs vs trending products vs editor's-pick. Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts".

## Step 5: Build the email modules

Generate email modules that surface recommendations within campaign and journey emails. Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts", "Test against the alternatives".

## Step 6: Follow up with high-intent browsers

Build a journey delivering personalized product picks to high-intent browsers. Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts", "Test against the alternatives", "Build the email modules".

## Step 7: Track what recommendations earn

Compose a dashboard tracking recommendation CTR, attributed revenue, and per-surface performance. Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts", "Test against the alternatives", "Build the email modules", "Follow up with high-intent browsers".
