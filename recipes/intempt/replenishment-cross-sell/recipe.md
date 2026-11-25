---
frontmatter_id: replenishment-cross-sell
slash_command: /replenishment-cross-sell
description: Works out how often each customer reorders a consumable product, reminds them by email before they run out, and
  suggests products from the catalog that pair with it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Reminds customers by email to reorder consumable products before they run out, paced to how fast they use them,
    with complementary products that pair with them.
  parameters:
  - name: reorder_window
    type: duration
    label: Reorder interval assumed for one-time buyers
    default: 30 d
    required: false
  - name: reminder_lead_days
    type: number
    label: Days before the expected run-out the reminder goes
    default: 5
    required: false
  requirements:
  - slot: consumable_purchase
    kind: event
    meaning: A customer purchased a consumable product
    properties:
    - name: product
      type: string
      meaning: The product bought
      optional: false
    - name: quantity
      type: number
      meaning: Units bought
      optional: false
  - slot: email_channel
    kind: destination
    meaning: Email channel for sending customer messages
    channel: email
  - slot: product_catalog
    kind: product_feed
    meaning: Product catalog with product pages, images and categories
  steps:
  - id: s1
    builds: attribute
    uses:
    - consumable_purchase
    - reorder_window
    instruction: Create a computed user attribute named "days_until_reorder". For each user who did {consumable_purchase}
      at least once in the last 365 days, take the median number of days between their {consumable_purchase} events (use {reorder_window}
      when they bought only once), and subtract the days since their latest {consumable_purchase}. The value is that number
      of days; it is empty for users with no {consumable_purchase} in the last 365 days.
  - id: s2
    builds: segment
    uses:
    - s1
    - consumable_purchase
    - reminder_lead_days
    dependsOn:
    - s1
    instruction: Build a new segment of users named "Due to Reorder". A user is in it when their days_until_reorder attribute
      from "Work out when they run out" is between 0 and {reminder_lead_days}, and they did not do {consumable_purchase} in
      the last 7 days.
  - id: s3
    builds: email
    uses:
    - s2
    - consumable_purchase
    - product_catalog
    dependsOn:
    - s2
    instruction: Write a reorder reminder email for users in the segment from "Find who is due to reorder". It names the product
      from their latest {consumable_purchase} ({consumable_purchase.product}) and the quantity ({consumable_purchase.quantity}),
      says they are likely to run out within a few days, and has one button linking to that product's page in {product_catalog}
      to reorder. Below it, as a cross sell, show two products from {product_catalog} in the same category that pair with
      it, each with image, name and link. If the brand kit has no logo, use the brand name as a plain text header.
  - id: s4
    builds: automation
    uses:
    - s2
    - s3
    - consumable_purchase
    - email_channel
    dependsOn:
    - s2
    - s3
    instruction: Build an automation triggered when a user enters the segment from "Find who is due to reorder". It sends
      the email from "Write the reorder reminder" through {email_channel} at once. After 3 days, if the user has not done
      {consumable_purchase} since, it sends the same email once more. Each user gets at most two reminders per reorder cycle.
---

# Replenishment and cross sell

Slash command: /replenishment-cross-sell

## Step 1: Work out when they run out

Create a computed user attribute named "days_until_reorder". For each user who did consumable purchase at least once in the last 365 days, take the median number of days between their consumable purchase events (use 30 d when they bought only once), and subtract the days since their latest consumable purchase. The value is that number of days; it is empty for users with no consumable purchase in the last 365 days.

## Step 2: Find who is due to reorder

Build a new segment of users named "Due to Reorder". A user is in it when their days_until_reorder attribute from "Work out when they run out" is between 0 and 5, and they did not do consumable purchase in the last 7 days.

## Step 3: Write the reorder reminder

Write a reorder reminder email for users in the segment from "Find who is due to reorder". It names the product from their latest consumable purchase (product) and the quantity (quantity), says they are likely to run out within a few days, and has one button linking to that product's page in product catalog to reorder. Below it, as a cross sell, show two products from product catalog in the same category that pair with it, each with image, name and link. If the brand kit has no logo, use the brand name as a plain text header.

## Step 4: Remind before they run dry

Build an automation triggered when a user enters the segment from "Find who is due to reorder". It sends the email from "Write the reorder reminder" through email channel at once. After 3 days, if the user has not done consumable purchase since, it sends the same email once more. Each user gets at most two reminders per reorder cycle.
