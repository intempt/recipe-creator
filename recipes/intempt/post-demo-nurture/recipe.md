---
frontmatter_id: post-demo-nurture
slash_command: /post-demo-nurture
description: Keeps a demo warm for 90 days with a playbook, a case study and an account executive check-in, and emails the
  AE early if the prospect clicks.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Keeps recent demo attendees warm for 90 days with three timed emails (playbook, case study, AE check-in) and emails
    the AE an alert on early buying signals.
  parameters:
  - name: demo_window
    type: duration
    label: Lookback window for recent demo attendees
    default: 90 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the account executives who get buying-signal alerts
    required: true
  requirements:
  - slot: demo_meeting_event
    kind: event
    meaning: A customer completed a meeting, with meeting type and attendance recorded
    properties:
    - name: meeting_type
      type: string
      meaning: Type of meeting, equal to demo for demos
      optional: false
    - name: attendance
      type: boolean
      meaning: True when the prospect attended
      optional: false
  - slot: deal_won_status
    kind: attribute
    meaning: True when the customer has a won deal
  - slot: in_active_cadence
    kind: attribute
    meaning: True when an account executive is already working the prospect in an active deal cadence
    optional: true
  - slot: email_clicked
    kind: event
    meaning: A prospect clicked a link in an email
  - slot: meeting_scheduled
    kind: event
    meaning: A meeting was scheduled with the prospect
  - slot: unsubscribed
    kind: event
    meaning: A prospect unsubscribed from email
  - slot: case_study_library
    kind: knowledge
    meaning: Playbooks and case studies to reference in the emails
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - demo_meeting_event
    - deal_won_status
    - in_active_cadence
    - demo_window
    instruction: Build a new segment of users named "Post-demo nurture". A user is in it when they did {demo_meeting_event}
      with {demo_meeting_event.meeting_type} equal to demo and {demo_meeting_event.attendance} true in the last {demo_window},
      their {deal_won_status} is not true, and their {in_active_cadence} is not true.
  - id: s2
    builds: email
    uses:
    - case_study_library
    instruction: Write a follow-up email for prospects who saw a product demo a week ago. It shares one practical playbook
      from {case_study_library} on getting the most from the product in their first month, in three short points, with one
      button to read it. Helpful, no sales push.
  - id: s3
    builds: email
    uses:
    - case_study_library
    instruction: 'Write a follow-up email for prospects who saw a product demo about a month ago. It tells one customer story
      from {case_study_library}: the problem, what they did and the outcome after six months, in three short paragraphs, with
      one button to read the full case study.'
  - id: s4
    builds: email
    instruction: Write a short plain email from the account executive to prospects who saw a demo about 90 days ago. It asks
      three direct, low-pressure questions, on timing, budget and who else is involved in the decision, and offers a 15-minute
      call with one button. No images.
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - demo_meeting_event
    - email_clicked
    - meeting_scheduled
    - unsubscribed
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: Build an automation triggered when a user enters the segment from "Find recent demo attendees". Counted from
      their {demo_meeting_event}, it sends the email from "Write the playbook email" at day 7, the email from "Write the case
      study email" at day 30 and the email from "Write the AE check-in" at day 90. When the user does {email_clicked} on one
      of the first two emails, it emails an alert to {alert_recipients} with the prospect's name, email and the email clicked,
      and stops. It stops when they do {meeting_scheduled} or {unsubscribed}.
---

# Post demo nurture

Slash command: /post-demo-nurture

## Step 1: Find recent demo attendees

Build a new segment of users named "Post-demo nurture". A user is in it when they did demo meeting event with meeting type equal to demo and attendance true in the last 90 d, their deal won status is not true, and their in active cadence is not true.

## Step 2: Write the playbook email

Write a follow-up email for prospects who saw a product demo a week ago. It shares one practical playbook from case study library on getting the most from the product in their first month, in three short points, with one button to read it. Helpful, no sales push.

## Step 3: Write the case study email

Write a follow-up email for prospects who saw a product demo about a month ago. It tells one customer story from case study library: the problem, what they did and the outcome after six months, in three short paragraphs, with one button to read the full case study.

## Step 4: Write the AE check-in

Write a short plain email from the account executive to prospects who saw a demo about 90 days ago. It asks three direct, low-pressure questions, on timing, budget and who else is involved in the decision, and offers a 15-minute call with one button. No images.

## Step 5: Send over 90 days

Build an automation triggered when a user enters the segment from "Find recent demo attendees". Counted from their demo meeting event, it sends the email from "Write the playbook email" at day 7, the email from "Write the case study email" at day 30 and the email from "Write the AE check-in" at day 90. When the user does email clicked on one of the first two emails, it emails an alert to the email addresses of the account executives who get buying-signal alerts with the prospect's name, email and the email clicked, and stops. It stops when they do meeting scheduled or unsubscribed.
