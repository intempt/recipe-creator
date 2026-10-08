---
description: People who cancelled in the last two months but used the product heavily before they left, the best odds for a win-back.
author:
  first_name: Harish
  last_name: Kumar
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - media
---

# Winnable churned users

Slash command: /winnable-churned-users

## Step 1: Build the win-back list

Build a segment of users named "Winnable Churned Users".
A user is in the segment only when all of these are true:
- they did the subscription_cancelled event at least once in the last 60 days
- their lifetime_value attribute is more than 0
- their total_events attribute is 50 or more
