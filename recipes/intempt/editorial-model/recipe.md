---
frontmatter_id: editorial-model
slash_command: /editorial-model
description: Visitors who submitted a form today and kept browsing right afterward, the hottest possible same-day lead signal, surfaced to sales with a follow-up email drafted and ready to review.
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

# Submitted And Still Engaged

Slash command: /editorial-model

## Step 1: Build the still-engaged submitter list

Build a segment of users named "Submitted And Still Engaged". A user is in the segment only when all of these are true: triggered "Submit on" at least once in the last 1 day; triggered "View page" at least 3 times in the last 1 day.

## Step 2: Draft a sales alert

Generate a Slack message to the sales team channel. Say how many users are in "Submitted And Still Engaged" right now, so reps can follow up while the user is still active on the site today. Use the result of "Build the still-engaged submitter list". This drafts the Slack message only; a person on the team still posts it.

## Step 3: Draft a next-step email

Generate a designed marketing email for the users in "Submitted And Still Engaged" confirming their submission and naming the one next step worth taking right now. Three sentences, confident and helpful tone, no discount language, one button linking to that next step. Use the result of "Build the still-engaged submitter list". This drafts the email only; a person still sends it.
