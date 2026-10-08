---
description: People who walked away from an expensive cart in the last week and have not bought since, so you chase the baskets worth chasing.
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
  - finance
---

# High-value cart abandoners

Slash command: /high-cart-value-abandoners

## Step 1: Build the big-cart list

Build a segment of users named "High-Cart-Value Abandoners".
A user is in the segment only when all of these are true:
- they did the cart_abandoned event with a total_amount of 200 or more at least once in the last 7 days
- they did not do the order_created event in the last 7 days
