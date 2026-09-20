---
name: booking-confirmation-flow
description: Use when a user mentions "booking confirmation flow", "B2B meeting reminders", "pre-meeting reminder ladder", or asks for related help. When a B2B meeting books, fire a reminder ladder (48hr email, 24hr email, 2hr SMS) to maximize show-rate, plus host notification on book and a coverage dashboard. Distinct from scheduling-setup (which configures the booking link itself).
arguments: []
intempt:
  id: booking-confirmation-flow
  title: "Meeting reminders before a call"
  version: 1.0.0
  slashCommand: /booking-confirmation-flow
  group: Workflows
  shortDescription: "Reminds the other side before a booked meeting at 48 hours, 24 hours and 2 hours, and shows what that does to your show rate."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: scheduling-assistant
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [meeting-reminders, show-rate]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: meeting_scheduled, severity: blocking }
  invokesCommands:
    - create_email_content
    - create_sms_content
    - create_journey
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Write the two reminder emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      description: "At 48 hours: the agenda, who is coming, add to calendar links, the joining details and a reschedule link. At 24 hours: just the time, the link and an easy reschedule. Both from the host."
      prompt: 'Generate 2 reminder email touches for upcoming B2B meetings. 48hr-before reminder: full agenda recap, attendee list, add-to-calendar links (iCal + Google + Outlook), location/conferencing details, and a reschedule link. 24hr-before reminder: lighter: just the meeting time, conferencing link, and a low-friction reschedule button. Send-from: the meeting host. Tone: professional, confirming.'
    - step: 2
      title: "Write the two hour text"
      command: create_sms_content
      produces: asset
      bindsAs: sms_asset
      dependsOn: [asset]
      description: "Under 160 characters with the time, a shortened joining link and a reply RESCHEDULE option. Only sent to people who opted into SMS."
      prompt: 'Generate a 2-hour-before SMS reminder. Format: under 160 chars. Include meeting time, conferencing link (shortened), and a reply-RESCHEDULE option. Example: ''Reminder: your call with [Host Name] starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.'' Only fires if user has SMS opt-in.'
    - step: 3
      title: "Remind at 48, 24 and 2 hours"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [asset, sms_asset]
      description: "All three are timed off the meeting start. The 48 hour email is skipped if the booking came in later than that, and the text only goes to people who opted in. It ends on the meeting happening, on a cancellation or on an opt out, and every time is recalculated if the meeting moves."
      prompt: 'Build a 3-touch journey triggered by meeting_scheduled, with all touches timed relative to meeting_start_time. Touch 1: 48hr email reminder (skip if meeting is sooner than 48hr at scheduling time). Touch 2: 24hr email reminder. Touch 3: 2hr SMS reminder (only if user has SMS opt-in). Exit conditions: meeting_completed, meeting_cancelled, or user opted out. If meeting is rescheduled, recompute all touch times from the new meeting_start_time.'
    - step: 4
      title: "Tell the host, link the deal"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [asset, journey]
      description: "On booking: a Slack note to the host with the details and a link to the record, the meeting linked to any open deal at that account, and the reminders started. On a cancellation the host is told and the reminders stop."
      prompt: 'Create a workflow firing on meeting_scheduled. Step sequence: (1) post host notification to Slack with meeting details and a link to the user record; (2) link the meeting to the open deal if one exists for the user''s account; (3) trigger the reminder journey. On meeting_cancelled, send the host a notification and exit the journey for that user.'
    - step: 5
      title: "See what reminders are worth"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [asset, sms_asset, journey, workflow]
      description: "Show rate against how many of the three reminders actually went out, email opens and clicks, replies to the text, and the reschedule rate, broken out by meeting type and rep, with meetings that got the full ladder set against those that did not."
      prompt: 'Compose a dashboard tracking meeting show-rate: overall show-rate by reminder cadence completeness (how many of the 3 reminders were delivered before the meeting), email reminder open/click rates, SMS reminder reply rate, and reschedule rate. Break down by meeting type and rep. Compare show-rate for meetings with vs. without the full reminder ladder (this is the proof-of-value chart).'
  outputs:
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Meeting reminders before a call

Reminds the other side before a booked meeting at 48 hours, 24 hours and 2 hours, and shows what that does to your show rate.

## Before you run it

- Connect slack
- Send the `meeting_scheduled` event

## What it does

1. **Write the two reminder emails** (`create_email_content`)

   At 48 hours: the agenda, who is coming, add to calendar links, the joining details and a reschedule link. At 24 hours: just the time, the link and an easy reschedule. Both from the host.

2. **Write the two hour text** (`create_sms_content`)

   Under 160 characters with the time, a shortened joining link and a reply RESCHEDULE option. Only sent to people who opted into SMS.

3. **Remind at 48, 24 and 2 hours** (`create_journey`)

   All three are timed off the meeting start. The 48 hour email is skipped if the booking came in later than that, and the text only goes to people who opted in. It ends on the meeting happening, on a cancellation or on an opt out, and every time is recalculated if the meeting moves.

4. **Tell the host, link the deal** (`create_workflow`)

   On booking: a Slack note to the host with the details and a link to the record, the meeting linked to any open deal at that account, and the reminders started. On a cancellation the host is told and the reminders stop.

5. **See what reminders are worth** (`create_dashboard`)

   Show rate against how many of the three reminders actually went out, email opens and clicks, replies to the text, and the reschedule rate, broken out by meeting type and rep, with meetings that got the full ladder set against those that did not.

## What you end up with

- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
