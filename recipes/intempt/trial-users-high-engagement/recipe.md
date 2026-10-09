---
description: Trial users with high numeric engagement scores and two weeks remaining in their trial period.
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
  - media
---

# Trials most likely to convert

Slash command: /trial-users-high-engagement

## Step 1: Build the strong-trial list

Build a segment of users named "Trial Users: High Engagement".
A user is in the segment only when all of these are true:
- their plan_name attribute is "trial"
- their end_date attribute is within the next 14 days
- their engagement_score attribute is "High"
- they did the goal_completed_in_journey event 3 or more times in the last 14 days
