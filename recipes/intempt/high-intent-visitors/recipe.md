---
description: Free and unregistered users who read both your pricing and your docs in the last two weeks, the clearest sign somebody is close to buying.
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

# High-intent visitors

Slash command: /high-intent-visitors

## Step 1: Build the high-intent list

Build a segment of users named "High-Intent Visitors".
A user is in the segment only when all of these are true:
- they did the page_viewed event with a page_url that contains "/pricing" at least once in the last 14 days
- they did the page_viewed event with a page_url that contains "/docs" at least once in the last 14 days
- their plan_name attribute is empty or is "free"
