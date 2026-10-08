---
description: Your biggest spenders who have gone quiet for about six weeks, so you can reach out personally before they drift away for good.
author:
  first_name: Harish
  last_name: Kumar
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce
---

# At-risk VIP customers

Slash command: /at-risk-vips

## Step 1: Build the at-risk VIP list

Build a segment of users named "At-Risk VIPs".
A user is in the segment only when all of these are true:
- their lifetime_value attribute is 1000 or more
- their days_since_last_activity attribute is between 45 and 90
- they did the order_created event 2 or more times, at any time
- they did not do the order_created event in the last 45 days
