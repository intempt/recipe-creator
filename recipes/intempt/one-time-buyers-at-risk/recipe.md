---
description: Customers who bought once, have not been back in two months, and are not trending well, so you can give them a reason to return.
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

# One-time buyers going cold

Slash command: /one-time-buyers-at-risk

## Step 1: Build the one-time-buyer list

Build a segment of users named "One-Time Buyers At Risk".
A user is in the segment only when all of these are true:
- they did the order_created event exactly 1 time, at any time
- their days_since_last_activity attribute is 60 or more
- their lifecycle_score attribute is neither "Regulars" nor "Promising"
