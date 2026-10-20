---
frontmatter_id: onboarding-stalled-users
slash_command: /onboarding-stalled-users
description: People who signed up a few weeks ago and still drop in now and then, but have never finished setup, so you can help them over the line.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Users stuck in onboarding

Slash command: /onboarding-stalled-users

## Step 1: Build the stalled-onboarding list

Build a segment of users named "Onboarding-Stalled Users".
A user is in the segment only when all of these are true:
- their First seen attribute is between 7 and 30 days ago
- they have not done the Completed a journey goal event since their First seen date
- their Days since last activity attribute is 14 or less
