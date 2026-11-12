---
frontmatter_id: booking-confirmation-flow
slash_command: /booking-confirmation-flow
description: Reminds the other side before a booked meeting at 48 hours, 24 hours and 2 hours, and shows what that does to your show rate.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends a booked meeting's other side reminders at 48 hours, 24 hours and 2 hours before the call, and dashboards
    how much those reminders lift show rate.
  parameters:
  - name: reminder_48h_offset
    type: duration
    label: Email reminder lead time before meeting
    default: 48 h
    required: false
  - name: reminder_24h_offset
    type: duration
    label: Second email reminder lead time before meeting
    default: 24 h
    required: false
  - name: sms_reminder_offset
    type: duration
    label: SMS reminder lead time before meeting
    default: 2 h
    required: false
  - name: sender_role
    type: string
    label: Sender of reminder emails
    default: meeting host
    required: false
  - name: tone
    type: string
    label: Tone of reminder emails
    default: professional, confirming
    required: false
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
      meaning: Type of meeting
      optional: true
    - name: host
      type: string
      meaning: Rep hosting the meeting
      optional: false
  - slot: meeting_completed_event
    kind: event
    meaning: A booked meeting was completed
  - slot: meeting_cancelled_event
    kind: event
    meaning: A booked meeting was cancelled
  - slot: meeting_rescheduled_event
    kind: event
    meaning: A booked meeting was moved to a new time
    properties:
    - name: meeting_start_time
      type: date
      meaning: New meeting start time
      optional: false
  - slot: sms_opt_in
    kind: attribute
    meaning: Whether the customer has opted in to SMS messages
  - slot: open_deal
    kind: attribute
    meaning: An open deal linked to the customer's account
    optional: true
  - slot: host_slack_channel
    kind: integration
    meaning: A Slack workspace connection for posting host notifications
    channel: slack
  - slot: reminder_email_sender
    kind: destination
    meaning: An email sending channel used to deliver reminder emails
    channel: email
  - slot: reminder_sms_sender
    kind: destination
    meaning: An SMS sending channel used to deliver reminder texts
    channel: sms
  - slot: reminder_opt_out_segment
    kind: segment
    meaning: Customers who have opted out of meeting reminders
    optional: true
  steps:
  - id: s1
    builds: email
    uses:
    - reminder_48h_offset
    - reminder_24h_offset
    - sender_role
    - tone
    instruction: 'Write two reminder emails for upcoming B2B meetings, sent from the {sender_role}, in a {tone} tone. The
      48-hour reminder ({reminder_48h_offset} before start) recaps the full agenda, lists attendees, provides add-to-calendar
      links (iCal, Google and Outlook), location or conferencing details, and a reschedule link. The 24-hour reminder ({reminder_24h_offset}
      before start) is lighter: meeting time, conferencing link, and a low-friction reschedule button.'
  - id: s2
    builds: sms
    uses:
    - s1
    - sms_reminder_offset
    - reminder_sms_sender
    instruction: 'Write a reminder text sent {sms_reminder_offset} before the meeting starts. Keep it under 160 characters.
      Include the meeting time, a shortened conferencing link, and a reply RESCHEDULE option. Example: ''Reminder: your call
      with [Host Name] starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.'' Send only to customers with SMS opt-in.
      Reuse the wording approach from "Write the two reminder emails".'
  - id: s3
    builds: automation
    uses:
    - meeting_scheduled_event
    - meeting_completed_event
    - meeting_cancelled_event
    - meeting_rescheduled_event
    - sms_opt_in
    - reminder_opt_out_segment
    - reminder_email_sender
    - reminder_sms_sender
    - s1
    - s2
    - reminder_48h_offset
    - reminder_24h_offset
    - sms_reminder_offset
    instruction: 'Build a three-touch journey triggered by {meeting_scheduled_event}, with every touch timed relative to {meeting_scheduled_event.meeting_start_time}.
      Touch 1: send the 48-hour email from "Write the two reminder emails" at {reminder_48h_offset} before start, skipping
      it if the meeting is sooner than {reminder_48h_offset} away at scheduling time. Touch 2: send the 24-hour email from
      "Write the two reminder emails" at {reminder_24h_offset} before start. Touch 3: send the SMS from "Write the two hour
      text" at {sms_reminder_offset} before start, only if {sms_opt_in} is true. Exit the journey on {meeting_completed_event},
      {meeting_cancelled_event}, or when the customer is in {reminder_opt_out_segment}. On {meeting_rescheduled_event}, recompute
      all touch times from the new {meeting_rescheduled_event.meeting_start_time}.'
  - id: s4
    builds: automation
    uses:
    - meeting_scheduled_event
    - meeting_cancelled_event
    - host_slack_channel
    - open_deal
    - s1
    - s3
    instruction: 'Create a workflow triggered by {meeting_scheduled_event}. Step 1: post a Slack notification to {host_slack_channel}
      with the meeting details and a link to the customer record. Step 2: link the meeting to {open_deal} if one exists for
      the customer''s account. Step 3: start the reminder journey from "Remind at 48, 24 and 2 hours". On {meeting_cancelled_event},
      notify the host and exit the journey for that customer.'
  - id: s5
    builds: dashboard
    uses:
    - meeting_scheduled_event
    - meeting_completed_event
    - meeting_cancelled_event
    - meeting_rescheduled_event
    - sms_opt_in
    - s1
    - s2
    - s3
    - s4
    instruction: 'Build a dashboard tracking meeting show rate. Show: overall show rate by reminder cadence completeness (how
      many of the three reminders were delivered before the meeting); email reminder open and click rates; SMS reminder reply
      rate; and reschedule rate from {meeting_rescheduled_event}. Break down by meeting type and rep ({meeting_scheduled_event.host}).
      Include a comparison chart of show rate for meetings with the full reminder ladder versus meetings without it.'
---

# Meeting reminders before a call

Slash command: /booking-confirmation-flow

## Step 1: Write the two reminder emails

Generate 2 reminder email touches for upcoming B2B meetings. 48hr-before reminder: full agenda recap, attendee list, add-to-calendar links (iCal + Google + Outlook), location/conferencing details, and a reschedule link. 24hr-before reminder: lighter: just the meeting time, conferencing link, and a low-friction reschedule button. Send-from: the meeting host. Tone: professional, confirming.

## Step 2: Write the two hour text

Generate a 2-hour-before SMS reminder. Format: under 160 chars. Include meeting time, conferencing link (shortened), and a reply-RESCHEDULE option. Example: 'Reminder: your call with [Host Name] starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.' Only fires if user has SMS opt-in. Use the result of "Write the two reminder emails".

## Step 3: Remind at 48, 24 and 2 hours

Build a 3-touch journey triggered by Meeting scheduled, with all touches timed relative to meeting_start_time. Touch 1: 48hr email reminder (skip if meeting is sooner than 48hr at scheduling time). Touch 2: 24hr email reminder. Touch 3: 2hr SMS reminder (only if user has SMS opt-in). Exit conditions: meeting_completed, meeting_cancelled, or user opted out. If meeting is rescheduled, recompute all touch times from the new meeting_start_time. Use the result of "Write the two reminder emails", "Write the two hour text".

## Step 4: Tell the host, link the deal

Create a workflow firing on Meeting scheduled. Step sequence: (1) post host notification to Slack with meeting details and a link to the user record; (2) link the meeting to the open deal if one exists for the user's account; (3) trigger the reminder journey. On meeting_cancelled, send the host a notification and exit the journey for that user. Use the result of "Write the two reminder emails", "Remind at 48, 24 and 2 hours".

## Step 5: See what reminders are worth

Compose a dashboard tracking meeting show-rate: overall show-rate by reminder cadence completeness (how many of the 3 reminders were delivered before the meeting), email reminder open/click rates, SMS reminder reply rate, and reschedule rate. Break down by meeting type and rep. Compare show-rate for meetings with vs. without the full reminder ladder (this is the proof-of-value chart). Use the result of "Write the two reminder emails", "Write the two hour text", "Remind at 48, 24 and 2 hours", "Tell the host, link the deal".
