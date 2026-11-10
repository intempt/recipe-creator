---
frontmatter_id: hands-in-use
slash_command: /hands-in-use
description: Accounts where several people together are reading a lot of pages, tagged and surfaced to sales as a broad research-intensity signal draft worth account-based outreach.
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

# Multi-Page Account Researchers

Slash command: /hands-in-use

## Step 1: Build the research-intensive account list

Build a segment of accounts named "Multi-Page Account Researchers". An account is in the segment only when all of these are true: the users in the account together did the View page event 15 or more times in the last 7 days.

## Step 2: Tag the matched accounts

Create an attribute named "research_intensive" on accounts in "Multi-Page Account Researchers", set to true. Use the result of "Build the research-intensive account list".

## Step 3: Draft a sales alert

Generate a Slack message to the sales channel. For each account in "Multi-Page Account Researchers", name the account, so reps can prioritize outreach while research activity is high. Use the result of "Build the research-intensive account list". This drafts the Slack message only; a person on the team still posts it.
