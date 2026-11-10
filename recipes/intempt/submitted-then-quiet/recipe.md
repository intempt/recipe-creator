---
frontmatter_id: submitted-then-quiet
slash_command: /submitted-then-quiet
description: Users who submitted a form but have gone quiet since, nudged with a warm follow-up before the lead goes cold.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Submitted Then Quiet

Slash command: /submitted-then-quiet

## Step 1: Build the quiet-after-submit list

Build a segment of users named "Submitted Then Quiet". A user is in the segment only when all of these are true: triggered "Submit on" at least once in the last 14 days; did not trigger "Session start" in the last 7 days.

## Step 2: Send the follow-up email

Generate a designed marketing email for the users in "Submitted Then Quiet" with a warm follow-up nudge. Three sentences, encouraging tone, no discount language, one button linking back to the product. Use the result of "Build the quiet-after-submit list".
