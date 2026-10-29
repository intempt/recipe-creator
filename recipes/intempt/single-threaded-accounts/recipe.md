---
frontmatter_id: single-threaded-accounts
slash_command: /single-threaded-accounts
description: Enterprise accounts where nobody has logged in for a month, the highest-stakes version of a churn signal, checked in on personally and flagged to the key accounts team.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
---

# Enterprise accounts going quiet

Slash command: /single-threaded-accounts

## Step 1: Build the quiet-enterprise list

Build a segment of accounts named "Enterprise Accounts Going Quiet".
An account is in the segment only when all of these are true:
- its employees attribute is 1000 or more
- the users in the account together did not do the Session start event in the last 30 days

## Step 2: Draft a personal check-in

Generate a plain-text email for the accounts in "Enterprise Accounts Going Quiet" written as a personal note from their account manager, asking how things are going and offering a quick call. Three sentences, warm and personal tone, no product pitch, no discount language. Use the result of "Build the quiet-enterprise list".

## Step 3: Alert the key accounts team

Generate a Slack message to the channel chosen for this run listing the accounts in "Enterprise Accounts Going Quiet" so the team can prioritize outreach before it becomes a renewal problem. Use the result of "Build the quiet-enterprise list".
