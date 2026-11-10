---
frontmatter_id: image-remix
slash_command: /image-remix
description: Visitors who clicked around actively in one visit and then disappeared for days, tagged and nudged back with a push notification.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Clicked But Didn't Return

Slash command: /image-remix

## Step 1: Build the clicked-but-gone list

Build a segment of users named "Clicked But Didn't Return". A user is in the segment only when all of these are true: triggered "Click on" at least 3 times in the last 1 day; did not trigger "Session start" in the last 3 days.

## Step 2: Tag the matched visitors

Create an attribute named "clicked_then_gone" on users in "Clicked But Didn't Return", set to true. Use the result of "Build the clicked-but-gone list".

## Step 3: Send a nudge push

Generate a push notification for the users in "Clicked But Didn't Return" inviting them back to pick up where they left off. Title under 40 characters, one short body line, friendly tone. Use the result of "Build the clicked-but-gone list".
