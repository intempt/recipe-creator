---
frontmatter_id: beauty-close-up
slash_command: /beauty-close-up
description: Brand-new visitors already clicking around heavily on their first day, flagged to sales as a hot lead and nudged back with a push notification.
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

# First-Day High-Intent Visitors

Slash command: /beauty-close-up

## Step 1: Build the first-day high-intent list

Build a segment of users named "First-Day High-Intent Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least once in the last 1 day; did not trigger "Session start" more than 1 day ago; triggered "Click on" at least 5 times in the last 1 day.

## Step 2: Alert sales

Generate a Slack message to the sales team channel. Say how many users are in "First-Day High-Intent Visitors" right now, so reps know a brand-new visitor is already showing strong interest today. Use the result of "Build the first-day high-intent list".

## Step 3: Send a nudge push

Generate a push notification for the users in "First-Day High-Intent Visitors" inviting them back to pick up where they left off. Title under 40 characters, one short body line, friendly and curious tone. Use the result of "Build the first-day high-intent list".
