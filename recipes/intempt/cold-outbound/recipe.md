---
frontmatter_id: cold-outbound
slash_command: /cold-outbound
description: Builds a target list from your ICP, runs a multi touch sequence with a booking link in it, and shows what pipeline came out.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Cold outbound sequence

Slash command: /cold-outbound

## Step 1: Build the target list

This step builds a segment.
Build target prospect list from ICP criteria (firmographic + intent signals).

## Step 2: Write the outbound emails

Generate personalized cold-outbound email templates with brand voice and prospect-specific personalization tokens. Use the result of "Build the target list".

## Step 3: Run the touches, then break off

Build a multi-touch outbound journey with appropriate cadence and break-up logic. Use the result of "Build the target list", "Write the outbound emails".

## Step 4: Set up the booking link

Configure the booking link reps include in outreach, with availability and meeting-type config. Use the result of "Build the target list", "Write the outbound emails", "Run the touches, then break off".

## Step 5: Track replies and meetings

Compose a dashboard tracking outreach volume, reply rate, meeting-booked rate, and pipeline contribution. Use the result of "Build the target list", "Write the outbound emails", "Run the touches, then break off", "Set up the booking link".
