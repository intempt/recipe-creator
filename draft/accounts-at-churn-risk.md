---
description: Paying accounts the health score has flagged as at risk, with no renewal deal in flight, so your CSMs can step in before they leave.
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

# Accounts at churn risk

Slash command: /accounts-at-churn-risk

## Step 1: Build the at-risk account list

Build a segment of accounts named "Accounts At Churn Risk".
An account is in the segment only when all of these are true:
- its Account health attribute is "at_risk"
- its Has a renewal deal attribute is false
- its Account lifetime value attribute is more than 0
- its User count attribute is 1 or more
