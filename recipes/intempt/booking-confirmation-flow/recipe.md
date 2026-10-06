---
id: booking-confirmation-flow
title: Meeting reminders before a call
slash_command: /booking-confirmation-flow
group: Workflows
owner: intempt
curator: trishik
summary: Reminds the other side before a booked meeting at 48 hours, 24 hours and 2 hours, and shows what
  that does to your show rate.
description: >-
  When a B2B meeting books, fire a reminder ladder (48hr email, 24hr email, 2hr SMS) to maximize show-rate,
  plus host notification on book and a coverage dashboard. Distinct from scheduling-setup (which configures
  the booking link itself).
version: 2.0.0
classification:
  product:
    - sales
  agent: scheduling-assistant
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
  vertical: []
  complexity: standard
  executionMode: live
  tags:
    - meeting-reminders
    - show-rate
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: meeting_scheduled
      severity: blocking
touches:
  reads:
    - The meeting_scheduled event in your project
    - Your Slack connection
  writes:
    - A new designed email, from step 1 "Write the two reminder emails"
    - A new SMS message, from step 2 "Write the two hour text"
    - A new journey, from step 3 "Remind at 48, 24 and 2 hours"
    - A new workflow, from step 4 "Tell the host, link the deal"
    - A new dashboard, from step 5 "See what reminders are worth"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Write the two reminder emails
    summary: >-
      At 48 hours: the agenda, who is coming, add to calendar links, the joining details and a reschedule
      link. At 24 hours: just the time, the link and an easy reschedule. Both from the host.
    builds: email_html
    description: >-
      Generate 2 reminder email touches for upcoming B2B meetings. 48hr-before reminder: full agenda recap,
      attendee list, add-to-calendar links (iCal + Google + Outlook), location/conferencing details, and
      a reschedule link. 24hr-before reminder: lighter: just the meeting time, conferencing link, and
      a low-friction reschedule button. Send-from: the meeting host. Tone: professional, confirming.
  - id: s2
    title: Write the two hour text
    summary: >-
      Under 160 characters with the time, a shortened joining link and a reply RESCHEDULE option. Only
      sent to people who opted into SMS.
    builds: sms
    description: >-
      Generate a 2-hour-before SMS reminder. Format: under 160 chars. Include meeting time, conferencing
      link (shortened), and a reply-RESCHEDULE option. Example: 'Reminder: your call with [Host Name]
      starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.' Only fires if user has SMS opt-in.
      Use the result of "Write the two reminder emails".
    dependsOn:
      - s1
  - id: s3
    title: Remind at 48, 24 and 2 hours
    summary: >-
      All three are timed off the meeting start. The 48 hour email is skipped if the booking came in later
      than that, and the text only goes to people who opted in. It ends on the meeting happening, on a
      cancellation or on an opt out, and every time is recalculated if the meeting moves.
    builds: journey
    description: >-
      Build a 3-touch journey triggered by meeting_scheduled, with all touches timed relative to meeting_start_time.
      Touch 1: 48hr email reminder (skip if meeting is sooner than 48hr at scheduling time). Touch 2:
      24hr email reminder. Touch 3: 2hr SMS reminder (only if user has SMS opt-in). Exit conditions: meeting_completed,
      meeting_cancelled, or user opted out. If meeting is rescheduled, recompute all touch times from
      the new meeting_start_time. Use the result of "Write the two reminder emails", "Write the two hour
      text".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Tell the host, link the deal
    summary: >-
      On booking: a Slack note to the host with the details and a link to the record, the meeting linked
      to any open deal at that account, and the reminders started. On a cancellation the host is told
      and the reminders stop.
    builds: workflow
    description: >-
      Create a workflow firing on meeting_scheduled. Step sequence: (1) post host notification to Slack
      with meeting details and a link to the user record; (2) link the meeting to the open deal if one
      exists for the user's account; (3) trigger the reminder journey. On meeting_cancelled, send the
      host a notification and exit the journey for that user. Use the result of "Write the two reminder
      emails", "Remind at 48, 24 and 2 hours".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: See what reminders are worth
    summary: >-
      Show rate against how many of the three reminders actually went out, email opens and clicks, replies
      to the text, and the reschedule rate, broken out by meeting type and rep, with meetings that got
      the full ladder set against those that did not.
    builds: dashboard
    description: >-
      Compose a dashboard tracking meeting show-rate: overall show-rate by reminder cadence completeness
      (how many of the 3 reminders were delivered before the meeting), email reminder open/click rates,
      SMS reminder reply rate, and reschedule rate. Break down by meeting type and rep. Compare show-rate
      for meetings with vs. without the full reminder ladder (this is the proof-of-value chart). Use the
      result of "Write the two reminder emails", "Write the two hour text", "Remind at 48, 24 and 2 hours",
      "Tell the host, link the deal".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: asset
    producedByStep: s1
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
  - key: workflow
    producedByStep: s4
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Meeting reminders before a call

Reminds the other side before a booked meeting at 48 hours, 24 hours and 2 hours, and shows what that does to your show rate.

## Steps

1. **Write the two reminder emails** (builds email_html)

   At 48 hours: the agenda, who is coming, add to calendar links, the joining details and a reschedule link. At 24 hours: just the time, the link and an easy reschedule. Both from the host.

2. **Write the two hour text** (builds sms)

   Under 160 characters with the time, a shortened joining link and a reply RESCHEDULE option. Only sent to people who opted into SMS.

3. **Remind at 48, 24 and 2 hours** (builds journey)

   All three are timed off the meeting start. The 48 hour email is skipped if the booking came in later than that, and the text only goes to people who opted in. It ends on the meeting happening, on a cancellation or on an opt out, and every time is recalculated if the meeting moves.

4. **Tell the host, link the deal** (builds workflow)

   On booking: a Slack note to the host with the details and a link to the record, the meeting linked to any open deal at that account, and the reminders started. On a cancellation the host is told and the reminders stop.

5. **See what reminders are worth** (builds dashboard)

   Show rate against how many of the three reminders actually went out, email opens and clicks, replies to the text, and the reschedule rate, broken out by meeting type and rep, with meetings that got the full ladder set against those that did not.

## What you end up with

- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The meeting_scheduled event in your project
- Your Slack connection

Writes:

- A new designed email, from step 1 "Write the two reminder emails"
- A new SMS message, from step 2 "Write the two hour text"
- A new journey, from step 3 "Remind at 48, 24 and 2 hours"
- A new workflow, from step 4 "Tell the host, link the deal"
- A new dashboard, from step 5 "See what reminders are worth"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, workflow.
