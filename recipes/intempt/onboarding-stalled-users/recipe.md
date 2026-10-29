---
frontmatter_id: onboarding-stalled-users
slash_command: /onboarding-stalled-users
description: Trial users logging in often enough to be ready to buy, offered a personal demo by email while sales still has the window to close them.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Engaged trial users

Slash command: /onboarding-stalled-users

## Step 1: Build the engaged-trial list

Build a segment of users named "Engaged Trial Users".
A user is in the segment only when all of these are true:
- their Plan attribute is "trial"
- they did the Session start event 5 or more times in the last 14 days

## Step 2: Offer a personal demo

Generate a designed marketing email for the users in "Engaged Trial Users" offering a personal walkthrough of a feature they have not tried yet. Three sentences, warm and helpful tone, no discount language, one button linking to the demo booking page. Use the result of "Build the engaged-trial list".

## Step 3: Alert sales

Generate a Slack message to the channel chosen for this run listing the users in "Engaged Trial Users" so reps can reach out while the trial window is still open. Use the result of "Build the engaged-trial list".
