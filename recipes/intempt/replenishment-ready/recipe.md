---
description: Customers whose last order was one to two months ago and who are about due for another, the moment a running-low reminder lands best.
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

# Customers due to re-order

Slash command: /replenishment-ready

## Step 1: Build the replenishment list

Build a segment of users named "Replenishment-Ready".
A user is in the segment only when all of these are true:
- they did the order_created event at least once between 30 and 60 days ago
- they did not do the order_created event in the last 30 days
