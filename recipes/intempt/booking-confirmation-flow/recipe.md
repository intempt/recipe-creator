---
description: Reminds the other side before a booked meeting at 48 hours, 24 hours and 2 hours, and shows what that does to your show rate.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Meeting reminders before a call

Slash command: /booking-confirmation-flow

## Step 1: Write the two reminder emails

Generate 2 reminder email touches for upcoming B2B meetings. 48hr-before reminder: full agenda recap, attendee list, add-to-calendar links (iCal + Google + Outlook), location/conferencing details, and a reschedule link. 24hr-before reminder: lighter: just the meeting time, conferencing link, and a low-friction reschedule button. Send-from: the meeting host. Tone: professional, confirming.

## Step 2: Write the two hour text

Generate a 2-hour-before SMS reminder. Format: under 160 chars. Include meeting time, conferencing link (shortened), and a reply-RESCHEDULE option. Example: 'Reminder: your call with [Host Name] starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.' Only fires if user has SMS opt-in. Use the result of "Write the two reminder emails".

## Step 3: Remind at 48, 24 and 2 hours

Build a 3-touch journey triggered by meeting_scheduled, with all touches timed relative to meeting_start_time. Touch 1: 48hr email reminder (skip if meeting is sooner than 48hr at scheduling time). Touch 2: 24hr email reminder. Touch 3: 2hr SMS reminder (only if user has SMS opt-in). Exit conditions: meeting_completed, meeting_cancelled, or user opted out. If meeting is rescheduled, recompute all touch times from the new meeting_start_time. Use the result of "Write the two reminder emails", "Write the two hour text".

## Step 4: Tell the host, link the deal

Create a workflow firing on meeting_scheduled. Step sequence: (1) post host notification to Slack with meeting details and a link to the user record; (2) link the meeting to the open deal if one exists for the user's account; (3) trigger the reminder journey. On meeting_cancelled, send the host a notification and exit the journey for that user. Use the result of "Write the two reminder emails", "Remind at 48, 24 and 2 hours".

## Step 5: See what reminders are worth

Compose a dashboard tracking meeting show-rate: overall show-rate by reminder cadence completeness (how many of the 3 reminders were delivered before the meeting), email reminder open/click rates, SMS reminder reply rate, and reschedule rate. Break down by meeting type and rep. Compare show-rate for meetings with vs. without the full reminder ladder (this is the proof-of-value chart). Use the result of "Write the two reminder emails", "Write the two hour text", "Remind at 48, 24 and 2 hours", "Tell the host, link the deal".
