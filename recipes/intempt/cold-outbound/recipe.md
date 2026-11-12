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
portable:
  summary: Builds a target prospect list from ideal-customer criteria, runs a multi-touch cold email sequence with a booking
    link, and reports the pipeline it produces.
  parameters:
  - name: touch_count
    type: number
    label: Number of outbound touches
    default: 5
    required: false
  - name: cadence_gap
    type: duration
    label: Gap between touches
    default: 3 d
    required: false
  - name: meeting_duration
    type: duration
    label: Meeting length offered via booking link
    default: 30 min
    required: false
  - name: brand_voice
    type: text
    label: Brand voice for email copy
    default: brand voice
    required: false
  requirements:
  - slot: icp_criteria
    kind: segment
    meaning: Prospect accounts matching the ideal customer profile, using firmographic and intent signals
    creatable: true
    definition: accounts matching ideal customer profile firmographic criteria and showing intent signals
  - slot: booking_calendar
    kind: integration
    meaning: A meeting booking calendar that reps can link in outreach emails
    channel: google_sheets
  - slot: outreach_sender
    kind: destination
    meaning: An email sending channel used to deliver outbound sequence messages
    channel: email
  - slot: outbound_reply
    kind: event
    meaning: A prospect replied to an outbound email
    properties:
    - name: prospect_id
      type: string
      meaning: Identifier of the replying prospect
      optional: false
  - slot: meeting_booked
    kind: event
    meaning: A prospect booked a meeting through the booking link
    properties:
    - name: prospect_id
      type: string
      meaning: Identifier of the prospect who booked
      optional: false
  steps:
  - id: s1
    builds: segment
    uses:
    - icp_criteria
    instruction: Build a target prospect list from {icp_criteria} using firmographic criteria and intent signals.
  - id: s2
    builds: email
    uses:
    - s1
    - brand_voice
    instruction: Write personalized cold outbound email templates in {brand_voice} using prospect-specific personalization
      fields, based on the "Build the target list" segment.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - outreach_sender
    - touch_count
    - cadence_gap
    instruction: Build a multi-touch outbound journey of {touch_count} touches spaced {cadence_gap} apart over the "Build
      the target list" segment, using the "Write the outbound emails" templates, sent through {outreach_sender}, with break-up
      logic that stops the sequence after the final touch or on reply.
  - id: s4
    builds: automation
    uses:
    - s2
    - s3
    - booking_calendar
    - meeting_duration
    instruction: Configure the booking link reps include in outreach, offering {meeting_duration} meetings, with availability
      drawn from {booking_calendar}, and insert it into the "Write the outbound emails" templates.
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - outbound_reply
    - meeting_booked
    instruction: Compose a dashboard tracking outreach volume, reply rate from {outbound_reply}, meeting-booked rate from
      {meeting_booked}, and pipeline contribution across the "Build the target list" segment and the "Run the touches, then
      break off" journey.
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
