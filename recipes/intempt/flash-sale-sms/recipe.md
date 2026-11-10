---
frontmatter_id: flash-sale-sms
slash_command: /flash-sale-sms
description: Builds the list of recently active shoppers, writes a time-limited offer text without inventing a discount or deadline it does not have, and lets marketing ops see the reach before it sends.
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

# Flash sale text message

Slash command: /flash-sale-sms

## Step 1: Build the flash-sale audience

Build a segment of users named "Flash Sale Audience". A user is in the segment only when all of these are true: triggered "View page" at least 3 times in the last 7 days.

## Step 2: Write the flash sale SMS

Generate an SMS for the users in "Flash Sale Audience" announcing a limited-time discount on their next purchase. Use the discount percentage and the offer's end date chosen for this run; do not invent either if neither is supplied. Include a short.link preview card for the offer's landing page. One or two sentences, direct and urgent tone. Use the result of "Build the flash-sale audience".

## Step 3: Alert marketing ops

Generate a Slack message to the marketing ops channel noting the size of "Flash Sale Audience" so the team can track reach before the sale goes out. Use the result of "Build the flash-sale audience".
