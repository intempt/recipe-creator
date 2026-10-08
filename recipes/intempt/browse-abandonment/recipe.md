---
description: Reminds people who looked at products but never added anything to the cart, showing the items they viewed and a few they might prefer.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce
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
