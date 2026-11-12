---
frontmatter_id: replenishment-cross-sell
slash_command: /replenishment-cross-sell
description: Reminds people to reorder before they run out, at the pace they actually get through it, and suggests what pairs with it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Reminds customers to reorder consumable products before they run out, paced to how fast they use them, and suggests
    complementary products that pair with them.
  parameters:
  - name: reorder_window
    type: duration
    label: Typical reorder window before run-out
    default: 30 d
    required: false
  - name: cross_sell_test_split
    type: number
    label: Share of users in cross-sell timing test (%)
    default: 50
    required: false
  requirements:
  - slot: consumable_purchase
    kind: event
    meaning: A customer purchased a consumable product
    properties:
    - name: product
      type: string
      meaning: Product purchased
      optional: false
    - name: quantity
      type: number
      meaning: Quantity purchased
      optional: true
    - name: purchased_at
      type: date
      meaning: Date of purchase
      optional: false
  - slot: reorder_candidates
    kind: segment
    meaning: Customers approaching their typical reorder window for a consumable product
    creatable: true
    definition: users whose time since last consumable purchase is nearing their typical reorder interval based on purchase
      history, within {reorder_window}
  - slot: email_channel
    kind: destination
    meaning: Email channel for sending customer messages
    channel: email
  - slot: product_catalog
    kind: product_feed
    meaning: Product catalog with complementary product relationships
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - consumable_purchase
    - reorder_window
    instruction: Identify {reorder_candidates} as users approaching their typical reorder window for consumable products,
      based on {consumable_purchase} history and the {reorder_window} window.
  - id: s2
    builds: email
    uses:
    - s1
    - reorder_candidates
    - email_channel
    instruction: Generate reorder reminder emails for {reorder_candidates} timed to each user's consumption pattern, each
      including a one-click reorder link. Send via {email_channel}.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - reorder_candidates
    instruction: Build a journey that sends the reorder reminders from "Write the reorder reminder" to {reorder_candidates}
      at intervals before depletion, based on the timing from "Work out when they run out".
  - id: s4
    builds: recommendation
    uses:
    - s1
    - s2
    - s3
    - product_catalog
    - consumable_purchase
    instruction: Generate cross-sell recommendations for complementary products from {product_catalog}, based on each customer's
      {consumable_purchase} history, for users in {reorder_candidates}.
  - id: s5
    builds: experiment
    uses:
    - s1
    - s2
    - s3
    - s4
    - cross_sell_test_split
    instruction: Add an A/B test on cross-sell timing, comparing cross-sell sent with the reorder reminder against a separate
      later touch, with {cross_sell_test_split}% of users in the test group.
  - id: s6
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - consumable_purchase
    instruction: Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value for
      {reorder_candidates}, using {consumable_purchase} events.
---

# Replenishment and cross sell

Slash command: /replenishment-cross-sell

## Step 1: Work out when they run out

This step builds a segment.
Identify users approaching their typical reorder window for consumable products based on purchase history.

## Step 2: Write the reorder reminder

Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder link. Use the result of "Work out when they run out".

## Step 3: Remind before they run dry

Build a journey sending reorder reminders at appropriate intervals before depletion. Use the result of "Work out when they run out", "Write the reorder reminder".

## Step 4: Pick what pairs with it

Generate cross-sell recommendations for complementary products based on the customer's purchase history. Use the result of "Work out when they run out", "Write the reorder reminder", "Remind before they run dry".

## Step 5: Test when to cross sell

Add A/B variants on cross-sell timing (with-reorder vs separate-touch). Use the result of "Work out when they run out", "Write the reorder reminder", "Remind before they run dry", "Pick what pairs with it".

## Step 6: Track reorders and attach rate

Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value. Use the result of "Work out when they run out", "Write the reorder reminder", "Remind before they run dry", "Pick what pairs with it", "Test when to cross sell".
