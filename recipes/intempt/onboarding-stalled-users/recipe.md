---
description: People who signed up a few weeks ago and still drop in now and then, but have never finished setup, so you can help them over the line.
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

# Users stuck in onboarding

Slash command: /onboarding-stalled-users

## Step 1: Build the stalled-onboarding list

Build a segment of users named "Onboarding-Stalled Users".
A user is in the segment only when all of these are true:
- their first_seen_at attribute is between 7 and 30 days ago
- they have not done the goal_completed_in_journey event since their first_seen_at date
- their days_since_last_activity attribute is 14 or less
