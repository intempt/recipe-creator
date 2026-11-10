---
frontmatter_id: cinematic-studio
slash_command: /cinematic-studio
description: Visitors who browsed lightly a few weeks ago and are browsing a lot more now, tagged and surfaced to growth as an escalating-interest signal draft worth a closer look.
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

# Warming Up Visitors

Slash command: /cinematic-studio

## Step 1: Build the warming-up visitor list

Build a segment of users named "Warming Up Visitors". A user is in the segment only when all of these are true: triggered "View page" at least once between 14 and 30 days ago; triggered "View page" at least 3 times in the last 7 days.

## Step 2: Tag the matched visitors

Create an attribute named "warming_up" on users in "Warming Up Visitors", set to true. Use the result of "Build the warming-up visitor list".

## Step 3: Draft a growth alert

Generate a Slack message to the growth team channel. Say how many users are in "Warming Up Visitors" right now, so the team has a ready-made shortlist of visitors trending toward higher engagement. Use the result of "Build the warming-up visitor list". This drafts the Slack message only; a person on the team still posts it.
