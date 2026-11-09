---
frontmatter_id: failed-payment-accounts
slash_command: /failed-payment-accounts
description: Visitors currently filling out a form, flagged to the team in real time so they can be reached while they are still on the page.
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

# Active Form Starters

Slash command: /failed-payment-accounts

## Step 1: Build the active form starter list

Build a segment of users named "Active Form Starters". A user is in the segment only when all of these are true: triggered "Change on" at least once in the last 1 day.

## Step 2: Alert the team

Generate a Slack message to the support team channel. Say how many users are in "Active Form Starters" right now, so the team knows someone is actively filling out a form today. Use the result of "Build the active form starter list".
