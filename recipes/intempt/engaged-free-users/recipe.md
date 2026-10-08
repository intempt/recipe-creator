---
description: Identify free-plan users using their computed engagement_score to help prioritize upgrade outreach. The score is a number, not a High-tier match.
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

# Engaged free users

Slash command: /engaged-free-users

## Step 1: Build the engaged free list

Build a segment of users named "Engaged Free Users".
A user is in the segment only when all of these are true:
- their plan_name attribute is "free"
- their engagement_score attribute is "High"
- their days_since_last_activity attribute is 7 or less
- they did the session_start event 5 or more times in the last 14 days
