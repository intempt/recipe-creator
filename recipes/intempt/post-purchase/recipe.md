---
frontmatter_id: post-purchase
slash_command: /post-purchase
description: Thanks the buyer, shows them how to use what they bought, asks for a review, and suggests what goes with it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Thanks new buyers, shows them how to use their purchase, asks for a review, and suggests complementary products
    over the first month.
  parameters:
  - name: lookback_window
    type: duration
    label: Look-back window for recent orders
    default: 14 d
    required: false
  - name: care_delay
    type: duration
    label: Delay before product-care email
    default: 3 d
    required: false
  - name: review_delay
    type: duration
    label: Delay before review request
    default: 7 d
    required: false
  - name: cross_sell_delay
    type: duration
    label: Delay before cross-sell email
    default: 14 d
    required: false
  - name: loyalty_delay
    type: duration
    label: Delay before loyalty introduction
    default: 30 d
    required: false
  requirements:
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
    properties:
    - name: purchased_items
      type: text
      meaning: Items included in the order
      optional: false
  - slot: buyer_type
    kind: attribute
    meaning: Whether a customer is a first-time or repeat buyer
  - slot: new_buyer_segment
    kind: segment
    meaning: Customers who placed their first order within the look-back window
    optional: true
  - slot: email_channel
    kind: destination
    meaning: An email sending destination for customer messages
    channel: email
  - slot: product_catalog
    kind: product_feed
    meaning: The store's product catalog with items that can be recommended together
  steps:
  - id: s1
    builds: segment
    uses:
    - order_placed
    - buyer_type
    - lookback_window
    instruction: Identify customers who placed an {order_placed} within the last {lookback_window}, and split them into first-time
      buyers and repeat buyers using {buyer_type}.
  - id: s2
    builds: content
    uses:
    - s1
    instruction: 'Write five emails for the recipients from "Split first time from repeat": a thank-you email, a product-care
      email using {order_placed.purchased_items}, a review request, cross-sell suggestions drawn from {product_catalog}, and
      a loyalty introduction.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - email_channel
    - care_delay
    - review_delay
    - cross_sell_delay
    - loyalty_delay
    instruction: 'Build a five-touch journey on {email_channel} for the audience from "Split first time from repeat": send
      the confirmation email from "Write the five emails" immediately (0 hours), the product-care email at {care_delay}, the
      review request at {review_delay}, the cross-sell email at {cross_sell_delay}, and the loyalty introduction at {loyalty_delay}.'
  - id: s4
    builds: recommendation
    uses:
    - s1
    - s2
    - s3
    - product_catalog
    instruction: Generate cross-sell recommendations from {product_catalog} based on {order_placed.purchased_items} and each
      customer's profile, for the audience from "Split first time from repeat", and place them in the cross-sell email from
      "Send over the first month".
  - id: s5
    builds: experiment
    uses:
    - s1
    - s2
    - s3
    - s4
    - review_delay
    instruction: Add an A/B test on the review-request timing in the journey from "Send over the first month", comparing variants
      at 3 days, 7 days, and 14 days after purchase, starting from the base of {review_delay}.
  - id: s6
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - order_placed
    instruction: Create a dashboard tracking the review-collection rate, the second-purchase rate for the audience from "Split
      first time from repeat", and the average order value uplift from cross-sell recommendations in "Pick what goes with
      it", using {order_placed} as the purchase source.
---

# Post purchase follow up

Slash command: /post-purchase

## Step 1: Split first time from repeat

Identify users with order_placed event in last 14 days, segmented by first-time vs repeat buyer.

## Step 2: Write the five emails

Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions. Use the result of "Split first time from repeat".

## Step 3: Send over the first month

Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro). Use the result of "Split first time from repeat", "Write the five emails".

## Step 4: Pick what goes with it

Generate cross-sell recommendations based on the purchased items and the customer's profile. Use the result of "Split first time from repeat", "Write the five emails", "Send over the first month".

## Step 5: Test when to ask for a review

Add A/B variants on review-request timing (3day vs 7day vs 14day). Use the result of "Split first time from repeat", "Write the five emails", "Send over the first month", "Pick what goes with it".

## Step 6: Track reviews and repeat orders

Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell. Use the result of "Split first time from repeat", "Write the five emails", "Send over the first month", "Pick what goes with it", "Test when to ask for a review".
