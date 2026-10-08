---
description: People who use your site a lot but have never placed an order, so you can aim a first-purchase offer at them.
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

# Engaged visitors who never bought

Slash command: /engaged-non-buyers

## Step 1: Build the non-buyer list

Build a segment of users named "Engaged Non-Buyers".
A user is in the segment only when all of these are true:
- their total_events attribute is 10 or more
- they have never done the order_created event
- their days_since_last_activity attribute is 7 or less
- their email attribute is not empty
