---
description: Customers who have never bought anything without a discount code, so you can keep them out of full-price campaigns and protect your margin.
author:
  first_name: Harish
  last_name: Kumar
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
---

# Discount-only buyers

Slash command: /discount-only-buyers

## Step 1: Build the discount-only list

Build a segment of users named "Discount-Only Buyers".
A user is in the segment only when all of these are true:
- they did the order_created event with a discount_codes value that is not empty 2 or more times, at any time
- they never did the order_created event with an empty discount_codes value
