---
description: Paying users who hit their activation milestone in the last week, while they are warm enough to say yes to more.
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

# Newly activated users

Slash command: /newly-activated-users

## Step 1: Build the newly-activated list

Build a segment of users named "Newly Activated Users".
A user is in the segment only when all of these are true:
- they did the goal_completed_in_journey event at least once in the last 7 days, with a journey_id equal to the activation journey chosen for this run
- their plan_name attribute is not "free"
