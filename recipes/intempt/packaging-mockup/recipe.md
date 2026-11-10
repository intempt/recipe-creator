---
frontmatter_id: packaging-mockup
slash_command: /packaging-mockup
description: Visitors who keep coming back without ever clicking anything, with a push nudge drafted and a note drafted for the content team about a possible low-interaction signal.
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

# Quiet Returning Visitors

Slash command: /packaging-mockup

## Step 1: Build the quiet returning visitor list

Build a segment of users named "Quiet Returning Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least 2 times in the last 14 days; did not trigger "Click on" in the last 14 days.

## Step 2: Draft a nudge push

Generate a push notification for the users in "Quiet Returning Visitors" highlighting one thing worth clicking on, chosen for this run. Title under 40 characters, one short body line, friendly and inviting tone. Use the result of "Build the quiet returning visitor list". This drafts the push only; a person still sends it.

## Step 3: Draft a note for the content team

Generate a Slack message to the content team channel. Say how many users are in "Quiet Returning Visitors" right now, so the team knows a group of returning visitors is not finding anything worth clicking on. Use the result of "Build the quiet returning visitor list". This drafts the Slack message only; a person on the team still posts it.
