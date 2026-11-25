---
frontmatter_id: booking-confirmation-flow
slash_command: /booking-confirmation-flow
description: Reminds the other side before a booked meeting at 48 hours and 24 hours by email and 2 hours by SMS, and emails
  a weekly show-rate digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends meeting reminders by email at 48 and 24 hours and by SMS at 2 hours before a booked call, plus a weekly show-rate
    digest.
  parameters:
  - name: reminder_48h_offset
    type: duration
    label: First email reminder before the start
    default: 48 h
    required: false
  - name: reminder_24h_offset
    type: duration
    label: Second email reminder before the start
    default: 24 h
    required: false
  - name: sms_reminder_offset
    type: duration
    label: SMS reminder before the start
    default: 2 h
    required: false
  - name: tone
    type: string
    label: Reminder tone
    default: professional, confirming
    required: false
  - name: reschedule_link
    type: string
    label: Link people use to reschedule
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: meeting_scheduled_event
    kind: event
    meaning: A customer booked a meeting with a sales rep
    properties:
    - name: meeting_start_time
      type: date
      meaning: When the meeting starts
      optional: false
    - name: meeting_type
      type: string
      meaning: Kind of meeting
      optional: true
    - name: host
      type: string
      meaning: Rep hosting the meeting
      optional: false
  - slot: meeting_completed_event
    kind: event
    meaning: A booked meeting was held
  - slot: meeting_cancelled_event
    kind: event
    meaning: A booked meeting was cancelled
  - slot: sms_opt_in
    kind: attribute
    meaning: True when the customer opted in to SMS messages
  - slot: reminder_sms_sender
    kind: destination
    channel: sms
    meaning: An SMS sending channel used to deliver reminder texts
  steps:
  - id: s1
    builds: email
    uses:
    - meeting_scheduled_event
    - tone
    - reschedule_link
    instruction: Write a designed HTML reminder email for people who booked a meeting, sent from the meeting host ({meeting_scheduled_event.host})
      in a {tone} tone. Confirm the meeting time ({meeting_scheduled_event.meeting_start_time}), say in two lines what the
      meeting will cover, and include a button to reschedule linking to {reschedule_link}.
  - id: s2
    builds: email
    uses:
    - meeting_scheduled_event
    - tone
    - reschedule_link
    instruction: 'Write a short reminder email for people with a meeting tomorrow, sent from the meeting host ({meeting_scheduled_event.host})
      in a {tone} tone: the meeting time ({meeting_scheduled_event.meeting_start_time}) and one low-friction button to reschedule
      linking to {reschedule_link}.'
  - id: s3
    builds: sms
    uses:
    - meeting_scheduled_event
    - reschedule_link
    instruction: 'Write an SMS reminder under 160 characters for people whose meeting with {meeting_scheduled_event.host}
      starts in 2 hours: the start time ({meeting_scheduled_event.meeting_start_time}) and the reschedule link {reschedule_link}.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - meeting_scheduled_event
    - meeting_completed_event
    - meeting_cancelled_event
    - sms_opt_in
    - reminder_sms_sender
    - reminder_48h_offset
    - reminder_24h_offset
    - sms_reminder_offset
    dependsOn:
    - s1
    - s2
    - s3
    instruction: Build an automation that starts when a user does {meeting_scheduled_event}. It waits until {reminder_48h_offset}
      before {meeting_scheduled_event.meeting_start_time} and sends the email from "Write the 48-hour reminder" (skipped when
      the meeting was booked less than {reminder_48h_offset} ahead); waits until {reminder_24h_offset} before the start and
      sends the email from "Write the 24-hour reminder"; waits until {sms_reminder_offset} before the start and, only if the
      user's {sms_opt_in} is true, sends the SMS from "Write the two hour text" through {reminder_sms_sender}. It stops when
      the user does {meeting_cancelled_event} or {meeting_completed_event}.
  - id: s5
    builds: automation
    uses:
    - meeting_scheduled_event
    - meeting_completed_event
    - meeting_cancelled_event
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes meetings whose {meeting_scheduled_event.meeting_start_time}
      was in the last 7 days and writes these figures: meetings booked; meetings held ({meeting_completed_event}); meetings
      cancelled ({meeting_cancelled_event}); the show rate, held divided by booked minus cancelled, with the same rate for
      the 7 days before; and the show rate by {meeting_scheduled_event.host}. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Meeting reminders before a call

Slash command: /booking-confirmation-flow

## Step 1: Write the 48-hour reminder

Write a designed HTML reminder email for people who booked a meeting, sent from the meeting host (host) in a professional, confirming tone. Confirm the meeting time (meeting start time), say in two lines what the meeting will cover, and include a button to reschedule linking to the link people use to reschedule.

## Step 2: Write the 24-hour reminder

Write a short reminder email for people with a meeting tomorrow, sent from the meeting host (host) in a professional, confirming tone: the meeting time (meeting start time) and one low-friction button to reschedule linking to the link people use to reschedule.

## Step 3: Write the two hour text

Write an SMS reminder under 160 characters for people whose meeting with host starts in 2 hours: the start time (meeting start time) and the reschedule link the link people use to reschedule.

## Step 4: Remind at 48, 24 and 2 hours

Build an automation that starts when a user does meeting scheduled event. It waits until 48 h before meeting start time and sends the email from "Write the 48-hour reminder" (skipped when the meeting was booked less than 48 h ahead); waits until 24 h before the start and sends the email from "Write the 24-hour reminder"; waits until 2 h before the start and, only if the user's sms opt in is true, sends the SMS from "Write the two hour text" through reminder sms sender. It stops when the user does meeting cancelled event or meeting completed event.

## Step 5: See what reminders are worth

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes meetings whose meeting start time was in the last 7 days and writes these figures: meetings booked; meetings held (meeting completed event); meetings cancelled (meeting cancelled event); the show rate, held divided by booked minus cancelled, with the same rate for the 7 days before; and the show rate by host. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
