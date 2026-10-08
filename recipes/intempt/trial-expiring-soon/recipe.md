---
description: Trial users whose trial runs out within a week and who have not paid yet, your last chance to convert them.
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
---

# Trials expiring this week

Slash command: /trial-expiring-soon

## Step 1: Build the expiring-trial list

Build a segment of users named "Trial Expiring Soon".
A user is in the segment only when all of these are true:
- their plan_name attribute is "trial"
- their end_date attribute is within the next 7 days
- they did not do the subscription_created event in the last 14 days
