---
frontmatter_id: pql-multi-user-account
slash_command: /pql-multi-user-account
description: Free accounts showing real product usage, surfaced to sales as a product-qualified-lead draft with a ready-to-send upgrade email drafted.
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

# Free accounts showing real usage

Slash command: /pql-multi-user-account

## Step 1: Build the active-free-account list

Build a segment of accounts named "PQL: Active Free Accounts". An account is in the segment only when all of these are true: the users in the account together did the Session start event 3 or more times in the last 14 days.

## Step 2: Draft a sales alert

Generate a Slack message to the sales channel. For each account in "PQL: Active Free Accounts", name the account, so reps can reach out to this product-qualified lead while usage is fresh. Use the result of "Build the active-free-account list". This drafts the Slack message only; a person on the team still posts it.

## Step 3: Draft an upgrade email

Generate a designed marketing email for the accounts in "PQL: Active Free Accounts" showing what the team unlocks on a paid plan. Three sentences, confident and helpful tone, no discount language, one button linking to the pricing page. Use the result of "Build the active-free-account list". This drafts the email only; a person still sends it.
