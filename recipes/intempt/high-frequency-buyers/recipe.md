---
frontmatter_id: high-frequency-buyers
slash_command: /high-frequency-buyers
description: Visitors who both browse repeatedly and click around the site, surfaced to marketing as a draft alert, a stronger engagement signal than page views alone.
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

# Engaged Repeat Visitors

Slash command: /high-frequency-buyers

## Step 1: Build the engaged repeat visitor list

Build a segment of users named "Engaged Repeat Visitors". A user is in the segment only when all of these are true: triggered "View page" at least 3 times in the last 7 days; triggered "Click on" at least once in the last 7 days.

## Step 2: Draft a marketing alert

Generate a Slack message to the marketing team channel. Say how many users are in "Engaged Repeat Visitors" right now, so the team knows who is browsing and clicking, not just passing through. Use the result of "Build the engaged repeat visitor list". This drafts the Slack message only; a person on the team still posts it.
