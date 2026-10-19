---
frontmatter_id: multi-stakeholder-engaged-accounts
slash_command: /multi-stakeholder-engaged-accounts
description: Individual users who logged 5 or more Session start and 10 or more View page events in the last 14 days, a high-engagement segment per user.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Accounts with a buying group active

Slash command: /multi-stakeholder-engaged-accounts

## Step 1: Build the multi-stakeholder list

Build a segment of accounts named "Multi-Stakeholder Engaged Accounts".
An account is in the segment only when all of these are true:
- its User count attribute is 3 or more
- the users in the account together did the Session start event 5 or more times in the last 14 days
- the users in the account together did the View page event 10 or more times in the last 14 days
