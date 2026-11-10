---
frontmatter_id: form-abandoners
slash_command: /form-abandoners
description: Users who started filling out a form and never finished, tagged while their intent is still fresh for a quick nudge or retargeting.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Form Abandoners

Slash command: /form-abandoners

## Step 1: Build the form abandoner list

Build a segment of users named "Form Abandoners". A user is in the segment only when all of these are true: triggered "Change on" at least once in the last 3 days; did not trigger "Submit on" in the last 3 days.

## Step 2: Tag the matched users

Create an attribute named "form_abandoner" on users in "Form Abandoners", set to true. Use the result of "Build the form abandoner list".
