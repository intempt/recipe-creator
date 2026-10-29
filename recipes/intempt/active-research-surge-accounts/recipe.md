---
frontmatter_id: active-research-surge-accounts
slash_command: /active-research-surge-accounts
description: Accounts whose users are browsing your site heavily right now, flagged to sales while interest is at its peak and sent a relevant resource to keep them moving.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Accounts showing a research surge

Slash command: /active-research-surge-accounts

## Step 1: Build the research-surge list

Build a segment of accounts named "Active Research Surge Accounts".
An account is in the segment only when all of these are true:
- the users in the account together did the View page event 3 or more times in the last 7 days

## Step 2: Alert sales

Generate a Slack message to the sales channel listing the accounts in "Active Research Surge Accounts" so reps can reach out while interest is at its peak. Use the result of "Build the research-surge list".

## Step 3: Send a relevant resource

Generate a designed marketing email for the accounts in "Active Research Surge Accounts" offering a resource that answers the questions a researching buyer usually has at this stage. Three sentences, helpful and low-pressure tone, no discount language, one button linking to a call-booking page. Use the result of "Build the research-surge list".
