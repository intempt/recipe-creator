---
frontmatter_id: renewal-window-90-day
slash_command: /renewal-window-90-day
description: Paying subscriptions that started roughly a year ago and are likely due for renewal, flagged to the renewals team and sent a value recap, so the conversation starts early instead of the week before.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Accounts in the renewal window

Slash command: /renewal-window-90-day

## Step 1: Build the renewal list

Build a segment of users named "Renewal Window 90 Days".
A user is in the segment only when all of these are true:
- their Plan attribute is not "free"
- they did the Subscription started event at least once between 275 and 365 days ago

## Step 2: Notify the renewals team

Generate a plain-text email to the renewals team distribution list listing the users in "Renewal Window 90 Days" so conversations start months early instead of the week before. Use the result of "Build the renewal list".

## Step 3: Send a value recap

Generate a designed marketing email for the users in "Renewal Window 90 Days" recapping one meaningful result they have gotten from the product this year. Three sentences, warm and appreciative tone, no pricing or discount language, one button linking to a call-booking page with their account manager. Use the result of "Build the renewal list".
