---
frontmatter_id: paid-users-low-engagement
slash_command: /paid-users-low-engagement
description: Paying customers with lower numeric engagement scores, useful for early retention outreach.
author:
  name: Harish Kumar
  first_name: Harish
  last_name: Kumar
  company: Intempt
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# Paid users losing interest

Slash command: /paid-users-low-engagement

## Step 1: Build the low-engagement list

Build a segment of users named "Paid Users: Low Engagement".
A user is in the segment only when all of these are true:
- their Plan attribute is neither "free" nor "trial"
- their Days since last activity attribute is between 7 and 21
- their Engagement score attribute is "Low"
