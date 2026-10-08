---
description: Customers who cancelled in the last month, while the reason is fresh and a win-back still has a chance.
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
  - finance
  - media
---

# Recently cancelled customers

Slash command: /recently-churned-users

## Step 1: Build the recent-cancel list

Build a segment of users named "Recently Churned Users".
A user is in the segment only when all of these are true:
- they did the subscription_cancelled event at least once in the last 30 days
- their lifetime_value attribute is more than 0
