---
frontmatter_id: recently-won-accounts
slash_command: /recently-won-accounts
description: Accounts that became customers in the last quarter, so onboarding and implementation start from one current list.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Recently won accounts

Slash command: /recently-won-accounts

## Step 1: Build the recently-won list

Build a segment of accounts named "Recently-Won Accounts".
An account is in the segment only when all of these are true:
- its Lifecycle changed date attribute is within the last 90 days
- its Lifecycle stage attribute is "customer"
- its Has an open deal attribute is false
