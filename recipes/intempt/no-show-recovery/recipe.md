---
frontmatter_id: no-show-recovery
slash_command: /no-show-recovery
description: Assumes a diary clash rather than disinterest and offers an easy reschedule in three emails over five days, stopping
  as soon as the prospect rebooks or replies.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends prospects who missed a meeting three friendly reschedule emails over five days and stops when they rebook,
    reply or opt out.
  parameters:
  - name: no_show_window
    type: duration
    label: How far back a missed meeting counts
    default: 7 d
    required: false
  - name: touch1_delay
    type: duration
    label: Wait before email 1
    default: 1 h
    required: false
  - name: touch2_delay
    type: duration
    label: Wait after email 1 before email 2
    default: 47 h
    required: false
  - name: touch3_delay
    type: duration
    label: Wait after email 2 before email 3
    default: 3 d
    required: false
  - name: min_attended_minutes
    type: number
    label: Minutes attended below which a meeting counts as missed
    default: 2
    required: false
  - name: reschedule_link
    type: string
    label: Booking link people use to reschedule
    required: true
  requirements:
  - slot: meeting_completed
    kind: event
    meaning: A prospect's scheduled meeting time passed, with whether they attended
    properties:
    - name: attendance
      type: boolean
      meaning: Whether the prospect attended
      optional: false
    - name: attended_minutes
      type: number
      meaning: Minutes the prospect was in the meeting
      optional: true
  - slot: meeting_rescheduled
    kind: event
    meaning: A prospect booked a new meeting
  - slot: email_replied
    kind: event
    meaning: A prospect replied to an outreach email
  - slot: opted_out
    kind: attribute
    meaning: True when the prospect opted out of marketing or sales email
  - slot: case_study_asset
    kind: knowledge
    meaning: A case study or playbook relevant to prospects
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - meeting_completed
    - meeting_rescheduled
    - opted_out
    - no_show_window
    - min_attended_minutes
    instruction: Build a new segment of users named "Recent no-shows". A user is in it when they did {meeting_completed} in
      the last {no_show_window} with {meeting_completed.attendance} false or {meeting_completed.attended_minutes} below {min_attended_minutes},
      they did not do {meeting_rescheduled} since that meeting, and their {opted_out} attribute is not true.
  - id: s2
    builds: email
    uses:
    - s1
    - reschedule_link
    dependsOn:
    - s1
    instruction: 'Write a short email for users in the segment from "Find who missed a meeting", from the meeting host. Assume
      a scheduling clash, not lack of interest, with no guilt: "Looks like the time didn''t work out". One button to pick
      a new time, linking to {reschedule_link}.'
  - id: s3
    builds: email
    uses:
    - s1
    - reschedule_link
    dependsOn:
    - s1
    instruction: Write a two-sentence reminder email for users in the segment from "Find who missed a meeting" who have not
      rebooked, from the meeting host. Mention the meeting they missed and that the booking link is still open. One button
      linking to {reschedule_link}.
  - id: s4
    builds: email
    uses:
    - s1
    - reschedule_link
    - case_study_asset
    dependsOn:
    - s1
    instruction: Write a final, friendly email for users in the segment from "Find who missed a meeting" who have not rebooked,
      from the meeting host. Share one useful takeaway from {case_study_asset} and leave the door open with one button linking
      to {reschedule_link}. No pressure, no further follow-up promised.
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - touch1_delay
    - touch2_delay
    - touch3_delay
    - meeting_rescheduled
    - email_replied
    - opted_out
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: Build an automation that starts when a user enters the segment from "Find who missed a meeting". It waits
      {touch1_delay} and sends the email from "Write reschedule email 1", waits {touch2_delay} and sends the email from "Write
      reschedule email 2", waits {touch3_delay} and sends the email from "Write reschedule email 3". Before each send it stops
      if the user did {meeting_rescheduled} or {email_replied} since entering, or their {opted_out} attribute is true.
---

# Meeting no show recovery

Slash command: /no-show-recovery

## Step 1: Find who missed a meeting

Build a new segment of users named "Recent no-shows". A user is in it when they did meeting completed in the last 7 d with attendance false or attended minutes below 2, they did not do meeting rescheduled since that meeting, and their opted out attribute is not true.

## Step 2: Write reschedule email 1

Write a short email for users in the segment from "Find who missed a meeting", from the meeting host. Assume a scheduling clash, not lack of interest, with no guilt: "Looks like the time didn't work out". One button to pick a new time, linking to the booking link people use to reschedule.

## Step 3: Write reschedule email 2

Write a two-sentence reminder email for users in the segment from "Find who missed a meeting" who have not rebooked, from the meeting host. Mention the meeting they missed and that the booking link is still open. One button linking to the booking link people use to reschedule.

## Step 4: Write reschedule email 3

Write a final, friendly email for users in the segment from "Find who missed a meeting" who have not rebooked, from the meeting host. Share one useful takeaway from case study asset and leave the door open with one button linking to the booking link people use to reschedule. No pressure, no further follow-up promised.

## Step 5: Send at 1 hour, 2 days, 5 days

Build an automation that starts when a user enters the segment from "Find who missed a meeting". It waits 1 h and sends the email from "Write reschedule email 1", waits 47 h and sends the email from "Write reschedule email 2", waits 3 d and sends the email from "Write reschedule email 3". Before each send it stops if the user did meeting rescheduled or email replied since entering, or their opted out attribute is true.
