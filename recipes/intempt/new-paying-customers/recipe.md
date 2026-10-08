---
description: Customers who started paying in the last month, the window where onboarding decides whether they stay.
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

# New paying customers

Slash command: /new-paying-customers

## Step 1: Build the new-customer list

Build a segment of users named "New Paying Customers".
A user is in the segment only when all of these are true:
- they did the subscription_created event at least once in the last 30 days
- their plan_name attribute is not "free"
- their plan_name attribute is not "trial"
