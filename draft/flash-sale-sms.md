---
description: "Builds the list of recently active shoppers, writes a time-limited offer text naming the discount and deadline, and lets marketing ops see the reach before it sends."
frontmatter_id: flash-sale-sms
author:
  name: V
  last_name: Ranadheer
  org_name: intempt
  email: rana@intempt.com
---
# Flash sale text message

## Step 1: Build the flash-sale audience

Build a segment of users named "Flash Sale Audience". A user is in the segment only when all of these are true: they did the View page event at least once in the last 14 days.

## Step 2: Write the flash sale SMS

Generate an SMS for the users in "Flash Sale Audience" announcing a time-limited discount. State the discount percentage and the exact end date for the offer in the message. Include a short.link preview card for the offer's landing page. One or two sentences, direct and urgent tone. Use the result of "Build the flash-sale audience".

## Step 3: Alert marketing ops

Generate a Slack message to the marketing ops channel noting the size of "Flash Sale Audience" so the team can track reach before the sale goes out. Use the result of "Build the flash-sale audience".
