---
frontmatter_id: paid-users-low-engagement
slash_command: /paid-users-low-engagement
description: Paying customers with lower numeric engagement scores, useful for early retention outreach.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Paid users losing interest

Slash command: /paid-users-low-engagement

## Step 1: Build the low-engagement list

Build a segment of users named "Paid Users: Low Engagement".
A user is in the segment only when all of these are true:
- their Plan attribute is neither "free" nor "trial"
- their Days since last activity attribute is between 7 and 21
- their Engagement score attribute is "Low"
