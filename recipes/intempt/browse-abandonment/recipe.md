---
frontmatter_id: browse-abandonment
slash_command: /browse-abandonment
description: Reminds people who looked at products but never added anything to the cart, showing the items they viewed and a few they might prefer.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Reminds shoppers who viewed products but never added to cart, showing the items they viewed and suggested alternatives
    over a two-touch email sequence.
  parameters:
  - name: browse_window
    type: duration
    label: Browse lookback window
    default: 7 d
    required: false
  - name: first_reminder_delay
    type: duration
    label: Delay before first reminder
    default: 24 h
    required: false
  - name: second_reminder_delay
    type: duration
    label: Delay before second reminder
    default: 72 h
    required: false
  requirements:
  - slot: product_viewed
    kind: event
    meaning: A customer viewed a product page
    properties:
    - name: product
      type: string
      meaning: The product that was viewed
      optional: false
  - slot: cart_added
    kind: event
    meaning: A customer added a product to their cart
  - slot: browsers_segment
    kind: segment
    meaning: Customers who viewed products in the last 7 days but never added to cart
    creatable: true
    definition: users who did {product_viewed} in the last {browse_window} and did not do {cart_added}
  - slot: email_channel
    kind: destination
    meaning: An email channel to send reminder emails
    channel: email
  - slot: product_feed
    kind: product_feed
    meaning: A catalog of products with similar-item and best-seller data
  - slot: purchase_completed
    kind: event
    meaning: A customer completed a purchase
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - product_viewed
    - cart_added
    - browse_window
    - browsers_segment
    instruction: Identify users who did {product_viewed} in the last {browse_window} and did not do {cart_added}. Save as
      {browsers_segment}.
  - id: s2
    builds: email
    uses:
    - s1
    - browsers_segment
    - product_viewed
    - product_feed
    instruction: Write browse-recovery email content for the people in {browsers_segment}, highlighting the products they
      viewed ({product_viewed.product}) and similar items from {product_feed}.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - browsers_segment
    - email_channel
    - first_reminder_delay
    - second_reminder_delay
    instruction: Build a two-touch journey for {browsers_segment} that sends the browse reminder email from "Write the browse
      reminder" through {email_channel} at {first_reminder_delay} and again at {second_reminder_delay} after the browse.
  - id: s4
    builds: recommendation
    uses:
    - s1
    - s2
    - s3
    - browsers_segment
    - product_viewed
    - purchase_completed
    - product_feed
    instruction: For each shopper in {browsers_segment}, generate product recommendations from their viewed items ({product_viewed.product})
      and purchase history ({purchase_completed}) using {product_feed}.
  - id: s5
    builds: experiment
    uses:
    - s1
    - s2
    - s3
    - s4
    - browsers_segment
    - product_feed
    instruction: Add A/B variants for the journey in "Send at 24 and 72 hours" comparing personalized recommendations from
      "Pick items for each shopper" against trending best-seller products from {product_feed}.
  - id: s6
    builds: report
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - browsers_segment
    - cart_added
    - purchase_completed
    instruction: Compose a funnel report for {browsers_segment} tracking browse, email open, email click, cart add, and purchase,
      using results from "Send at 24 and 72 hours", "Pick items for each shopper", and "Test picks against best sellers".
---

# Browse abandonment follow up

Slash command: /browse-abandonment

## Step 1: Find people who only browsed

This step builds a segment.
Identify users with product_viewed events in last 7 days who did NOT trigger cart_added.

## Step 2: Write the browse reminder

Generate browse-recovery email content highlighting the viewed products and similar items. Use the result of "Find people who only browsed".

## Step 3: Send at 24 and 72 hours

Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse. Use the result of "Find people who only browsed", "Write the browse reminder".

## Step 4: Pick items for each shopper

Generate product recommendations for each browser based on their viewed items and purchase history. Use the result of "Find people who only browsed", "Write the browse reminder", "Send at 24 and 72 hours".

## Step 5: Test picks against best sellers

Add A/B variants comparing personalized recommendations vs trending products. Use the result of "Find people who only browsed", "Write the browse reminder", "Send at 24 and 72 hours", "Pick items for each shopper".

## Step 6: Follow browse through to sale

Compose a funnel report tracking browse to email-open to email-click to cart-add to purchase. Use the result of "Find people who only browsed", "Write the browse reminder", "Send at 24 and 72 hours", "Pick items for each shopper", "Test picks against best sellers".
