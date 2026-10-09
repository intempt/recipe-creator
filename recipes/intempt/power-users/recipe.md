---
description: Segment your most active users based on frequent sessions and high activity thresholds over the last 30 days.
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
  - finance
  - media
---

# Power users

Slash command: /power-users

## Step 1: Build the power-user list

Build a segment of users named "Power Users".
A user is in the segment only when all of these are true:
- they did the Session start event 10 or more times in the last 30 days
- they did the Click on event 20 or more times in the last 30 days
- their Engagement score attribute is "High"
- their Last seen attribute is within the last 7 days
