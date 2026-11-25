---
frontmatter_id: post-purchase
slash_command: /post-purchase
description: Thanks the buyer and shows them how to use what they bought, asks for a review a week later, and suggests products
  that go with it two weeks after the order.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Sends every buyer a thank-you with care tips, a review request and a cross-sell email from your catalog over the
    two weeks after their order.
  parameters:
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
  requirements:
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
    properties:
    - name: purchased_items
      type: string
      meaning: Names of the items in the order
      optional: false
  - slot: product_catalog
    kind: product_feed
    meaning: The store's product catalog with items that can be recommended together
  steps:
  - id: s1
    builds: email
    uses:
    - order_placed
    instruction: Write a thank-you email for customers who just did {order_placed}. It thanks them, names the items in {order_placed.purchased_items},
      and gives three short tips on using and caring for them, with one button to their order. No discount, no other products.
  - id: s2
    builds: email
    uses:
    - order_placed
    instruction: Write a short email asking customers who did {order_placed} a week ago to review the items in {order_placed.purchased_items}.
      One question on how they are finding it, one button to leave a review, and a line saying replies go to a real person.
  - id: s3
    builds: email
    uses:
    - order_placed
    - product_catalog
    instruction: Write a cross-sell email for customers who did {order_placed} two weeks ago. It shows three products from
      {product_catalog} that go with the items in {order_placed.purchased_items}, never an item already in the order, each
      with its image, name and one line on why it pairs, and a button to each.
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - order_placed
    - review_delay
    - cross_sell_delay
    dependsOn:
    - s1
    - s2
    - s3
    instruction: Build an automation triggered when a user does {order_placed}. It sends the email from "Write the thank-you
      and care email" right away, waits {review_delay} and sends the email from "Write the review request", then waits until
      {cross_sell_delay} after the order and sends the email from "Write the goes-with-it email". A user already in this automation
      from an earlier order does not start it again.
---

# Post purchase follow up

Slash command: /post-purchase

## Step 1: Write the thank-you and care email

Write a thank-you email for customers who just did order placed. It thanks them, names the items in purchased items, and gives three short tips on using and caring for them, with one button to their order. No discount, no other products.

## Step 2: Write the review request

Write a short email asking customers who did order placed a week ago to review the items in purchased items. One question on how they are finding it, one button to leave a review, and a line saying replies go to a real person.

## Step 3: Write the goes-with-it email

Write a cross-sell email for customers who did order placed two weeks ago. It shows three products from product catalog that go with the items in purchased items, never an item already in the order, each with its image, name and one line on why it pairs, and a button to each.

## Step 4: Follow up over two weeks after the purchase

Build an automation triggered when a user does order placed. It sends the email from "Write the thank-you and care email" right away, waits 7 d and sends the email from "Write the review request", then waits until 14 d after the order and sends the email from "Write the goes-with-it email". A user already in this automation from an earlier order does not start it again.
