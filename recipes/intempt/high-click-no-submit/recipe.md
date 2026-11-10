---
frontmatter_id: high-click-no-submit
slash_command: /high-click-no-submit
description: Visitors clicking around heavily without ever submitting a form, surfaced to growth as a friction-signal draft worth a closer look.
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

# High-Click Non-Converters

Slash command: /high-click-no-submit

## Step 1: Build the high-click non-converter list

Build a segment of users named "High-Click Non-Converters". A user is in the segment only when all of these are true: triggered "Click on" at least 8 times in the last 7 days; did not trigger "Submit on" in the last 7 days.

## Step 2: Draft a growth alert

Generate a Slack message to the growth team channel. Say how many users are in "High-Click Non-Converters" right now, so the team has a ready-made shortlist of high-friction visitors worth a closer look. Use the result of "Build the high-click non-converter list". This drafts the Slack message only; a person on the team still posts it.
