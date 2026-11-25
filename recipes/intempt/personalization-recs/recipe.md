---
frontmatter_id: personalization-recs
slash_command: /personalization-recs
description: Builds catalog-aware product recommendations, shows them on the product page, cart and post-purchase page, and
  emails product picks to high-intent browsers who have not bought.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows shoppers catalog-aware product recommendations on the product page, cart and post-purchase page, and emails
    picks to high-intent browsers who have not bought.
  parameters:
  - name: high_intent_window
    type: duration
    label: Browsing window for high-intent shoppers
    default: 7 d
    required: false
  - name: high_intent_views
    type: number
    label: Product views that make a shopper high intent
    default: 3
    required: false
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
      meaning: The product viewed
      optional: false
  - slot: order_completed
    kind: event
    meaning: A customer completed an order
    properties:
    - name: product_id
      type: string
      meaning: A product in the order
      optional: false
  - slot: email_channel
    kind: integration
    meaning: An email sending integration for recommendation emails
    channel: email
  steps:
  - id: s1
    builds: recommendation
    uses:
    - product_catalog
    - product_viewed
    - order_completed
    instruction: Create a product recommendation named "Recommended for you" from {product_catalog}. For each user it ranks
      products by what users with similar {product_viewed} and {order_completed} history bought (by {product_viewed.product_id}
      and {order_completed.product_id}) and by similarity to the products the user viewed in the last 30 days. It leaves out
      products the user ordered in the last 30 days and products that are out of stock. Users with no history get the best
      sellers of the last 30 days.
  - id: s2
    builds: personalization
    uses:
    - s1
    dependsOn:
    - s1
    instruction: 'Create a website personalization that shows 4 products from the recommendation from "Build the recommendation
      model" in a "Recommended for you" row on three pages: below the product details on product pages, below the line items
      on the cart page, and on the order confirmation page. Audience: all visitors; devices: any; display frequency: always;
      schedule: continuous.'
  - id: s3
    builds: segment
    uses:
    - product_viewed
    - order_completed
    - high_intent_window
    - high_intent_views
    instruction: Build a new segment of users named "High-Intent Browsers". A user is in it when they did {product_viewed}
      {high_intent_views} or more times in the last {high_intent_window} and did not do {order_completed} in the last {high_intent_window}.
  - id: s4
    builds: email
    uses:
    - s3
    - product_catalog
    - product_viewed
    dependsOn:
    - s3
    instruction: Write an email for users in the segment from "Find high-intent browsers". It shows the last product they
      viewed ({product_viewed.product_id}) and four similar products from {product_catalog}, each with its image, name and
      a link to its product page. Subject line about the product they looked at. Helpful tone, no discount. If the brand kit
      has no logo, use the brand name as a plain text header.
  - id: s5
    builds: automation
    uses:
    - s3
    - s4
    - order_completed
    - email_channel
    dependsOn:
    - s3
    - s4
    instruction: Build an automation triggered when a user enters the segment from "Find high-intent browsers". After 24 hours,
      if the user has not done {order_completed} since entering, it sends the email from "Write the product picks email" through
      {email_channel}. Each user gets it at most once in 30 days.
---

# Product recommendations across channels

Slash command: /personalization-recs

## Step 1: Build the recommendation model

Create a product recommendation named "Recommended for you" from product catalog. For each user it ranks products by what users with similar product viewed and order completed history bought (by product id and product id) and by similarity to the products the user viewed in the last 30 days. It leaves out products the user ordered in the last 30 days and products that are out of stock. Users with no history get the best sellers of the last 30 days.

## Step 2: Place them on each surface

Create a website personalization that shows 4 products from the recommendation from "Build the recommendation model" in a "Recommended for you" row on three pages: below the product details on product pages, below the line items on the cart page, and on the order confirmation page. Audience: all visitors; devices: any; display frequency: always; schedule: continuous.

## Step 3: Find high-intent browsers

Build a new segment of users named "High-Intent Browsers". A user is in it when they did product viewed 3 or more times in the last 7 d and did not do order completed in the last 7 d.

## Step 4: Write the product picks email

Write an email for users in the segment from "Find high-intent browsers". It shows the last product they viewed (product id) and four similar products from product catalog, each with its image, name and a link to its product page. Subject line about the product they looked at. Helpful tone, no discount. If the brand kit has no logo, use the brand name as a plain text header.

## Step 5: Follow up with high-intent browsers

Build an automation triggered when a user enters the segment from "Find high-intent browsers". After 24 hours, if the user has not done order completed since entering, it sends the email from "Write the product picks email" through email channel. Each user gets it at most once in 30 days.
