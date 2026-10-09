---
description: Thanks the buyer, shows them how to use what they bought, asks for a review, and suggests what goes with it.
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
  - social
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
