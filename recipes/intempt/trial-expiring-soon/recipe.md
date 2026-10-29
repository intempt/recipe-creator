---
frontmatter_id: trial-expiring-soon
slash_command: /trial-expiring-soon
description: Trial users who started their trial 3 to 4 weeks ago and still have not paid, nudged by email and flagged to sales while there is still time to close them.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
---

# Trials nearing the end

Slash command: /trial-expiring-soon

## Step 1: Build the expiring-trial list

Build a segment of users named "Trial Expiring Soon".
A user is in the segment only when all of these are true:
- their Plan attribute is "trial"
- they did the Subscription started event at least once between 23 and 30 days ago

## Step 2: Send a final nudge

Generate a designed marketing email for the users in "Trial Expiring Soon" letting them know their trial is nearing its end and highlighting the one feature most worth trying before it does. Three sentences, warm and helpful tone, no discount language, one button linking to the upgrade page. Use the result of "Build the expiring-trial list".

## Step 3: Alert sales

Generate a Slack message to the channel chosen for this run listing the users in "Trial Expiring Soon" so reps can reach out personally before the window closes. Use the result of "Build the expiring-trial list".
