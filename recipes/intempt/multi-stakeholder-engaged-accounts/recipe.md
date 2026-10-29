---
frontmatter_id: multi-stakeholder-engaged-accounts
slash_command: /multi-stakeholder-engaged-accounts
description: Accounts where several people are actively using the product at once, the clearest sign a real buying committee has formed, flagged to sales and sent a resource built for teams.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Accounts with a buying group active

Slash command: /multi-stakeholder-engaged-accounts

## Step 1: Build the multi-stakeholder list

Build a segment of accounts named "Multi-Stakeholder Engaged Accounts".
An account is in the segment only when all of these are true:
- the users in the account together did the Session start event 5 or more times in the last 14 days
- the users in the account together did the View page event 10 or more times in the last 14 days

## Step 2: Alert sales

Generate a Slack message to the channel chosen for this run listing the accounts in "Multi-Stakeholder Engaged Accounts" so reps know a buying committee may have formed and can act while interest is high. Use the result of "Build the multi-stakeholder list".

## Step 3: Send a team resource

Generate a designed marketing email for the accounts in "Multi-Stakeholder Engaged Accounts" offering a resource built for teams evaluating the product together. Three sentences, consultative tone, no discount language, one button linking to a call-booking page. Use the result of "Build the multi-stakeholder list".
