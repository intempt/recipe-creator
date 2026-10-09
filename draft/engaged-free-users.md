---
description: Identify free-plan users using their computed Engagement score to help prioritize upgrade outreach. The score is a number, not a High-tier match.
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
- their Plan attribute is "free"
- their Engagement score attribute is "High"
- their Days since last activity attribute is 7 or less
- they did the Session start event 5 or more times in the last 14 days
