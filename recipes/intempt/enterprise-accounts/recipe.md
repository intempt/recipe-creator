---
frontmatter_id: enterprise-accounts
slash_command: /enterprise-accounts
description: Companies with 1,000 or more employees, alerted to enterprise sales and welcomed with a dedicated-manager email, so outreach starts the moment they qualify.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
---

# Enterprise accounts

Slash command: /enterprise-accounts

## Step 1: Build the enterprise list

Build a segment of accounts named "Enterprise Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is 1000 or more

## Step 2: Alert enterprise sales

Generate a Slack message to the channel chosen for this run listing the accounts in "Enterprise Accounts" so reps can prioritize outreach to the newest ones first. Use the result of "Build the enterprise list".

## Step 3: Welcome the account

Generate a designed marketing email for the accounts in "Enterprise Accounts" welcoming them to the enterprise tier and introducing their dedicated account manager. Three sentences, professional tone, no pricing or discount language, one button linking to the onboarding scheduling page. Use the result of "Build the enterprise list".
