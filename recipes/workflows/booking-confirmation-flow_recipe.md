---
name: booking-confirmation-flow
description: Use when a user mentions "booking confirmation flow", "B2B meeting reminders", "pre-meeting reminder ladder", or asks for related help. When a B2B meeting books, fire a reminder ladder — 48hr email, 24hr email, 2hr SMS — to maximize show-rate, plus host notification on book and a coverage dashboard. Distinct from scheduling-setup (which configures the booking link itself).
arguments: []
intempt:
  id: booking-confirmation-flow
  version: 1.0.0
  slashCommand: /booking-confirmation-flow
  group: Workflows
  shortDescription: 'When a B2B meeting books, fire a reminder ladder (48hr email, 24hr email, 2hr SMS) to maximize show-rate, plus host notification on book and a coverage dashboard. Distinct from scheduling-setup (which configures the booking link itself).'
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
      title: Build Reminder Email Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      description: 'Generate 2 reminder email touches for upcoming B2B meetings. 48hr-before reminder: full agenda recap, attendee list, add-to-calendar links (iCal + Google + Outlook), location/conferencing details, and a reschedule link. 24hr-before reminder: lighter — just the meeting time, conferencing link, and a low-friction reschedule button. Send-from: the meeting host. Tone: professional, confirming.'
      prompt: 'Generate 2 reminder email touches for upcoming B2B meetings. 48hr-before reminder: full agenda recap, attendee list, add-to-calendar links (iCal + Google + Outlook), location/conferencing details, and a reschedule link. 24hr-before reminder: lighter — just the meeting time, conferencing link, and a low-friction reschedule button. Send-from: the meeting host. Tone: professional, confirming.'
    - step: 2
      title: Build SMS Reminder Content
      command: create_sms_content
      produces: asset
      bindsAs: sms_asset
      dependsOn: [asset]
      description: 'Generate a 2-hour-before SMS reminder. Format: under 160 chars. Include meeting time, conferencing link (shortened), and a reply-RESCHEDULE option. Example: ''Reminder: your call with [Host Name] starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.'' Only fires if user has SMS opt-in.'
      prompt: 'Generate a 2-hour-before SMS reminder. Format: under 160 chars. Include meeting time, conferencing link (shortened), and a reply-RESCHEDULE option. Example: ''Reminder: your call with [Host Name] starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.'' Only fires if user has SMS opt-in.'
    - step: 3
      title: Build Reminder Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [asset, sms_asset]
      description: 'Build a 3-touch journey triggered by meeting_scheduled, with all touches timed relative to meeting_start_time. Touch 1: 48hr email reminder (skip if meeting is sooner than 48hr at scheduling time). Touch 2: 24hr email reminder. Touch 3: 2hr SMS reminder (only if user has SMS opt-in). Exit conditions: meeting_completed, meeting_cancelled, or user opted out. If meeting is rescheduled, recompute all touch times from the new meeting_start_time.'
      prompt: 'Build a 3-touch journey triggered by meeting_scheduled, with all touches timed relative to meeting_start_time. Touch 1: 48hr email reminder (skip if meeting is sooner than 48hr at scheduling time). Touch 2: 24hr email reminder. Touch 3: 2hr SMS reminder (only if user has SMS opt-in). Exit conditions: meeting_completed, meeting_cancelled, or user opted out. If meeting is rescheduled, recompute all touch times from the new meeting_start_time.'
    - step: 4
      title: Build Booking Confirmation Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [asset, journey]
      description: 'Create a workflow firing on meeting_scheduled. Step sequence: (1) post host notification to Slack with meeting details and a link to the user record; (2) link the meeting to the open deal if one exists for the user''s account; (3) trigger the reminder journey. On meeting_cancelled, send the host a notification and exit the journey for that user.'
      prompt: 'Create a workflow firing on meeting_scheduled. Step sequence: (1) post host notification to Slack with meeting details and a link to the user record; (2) link the meeting to the open deal if one exists for the user''s account; (3) trigger the reminder journey. On meeting_cancelled, send the host a notification and exit the journey for that user.'
    - step: 5
      title: Build Show-Rate Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [asset, sms_asset, journey, workflow]
      description: 'Compose a dashboard tracking meeting show-rate: overall show-rate by reminder cadence completeness (how many of the 3 reminders were delivered before the meeting), email reminder open/click rates, SMS reminder reply rate, and reschedule rate. Break down by meeting type and rep. Compare show-rate for meetings with vs. without the full reminder ladder (this is the proof-of-value chart).'
      prompt: 'Compose a dashboard tracking meeting show-rate: overall show-rate by reminder cadence completeness (how many of the 3 reminders were delivered before the meeting), email reminder open/click rates, SMS reminder reply rate, and reschedule rate. Break down by meeting type and rep. Compare show-rate for meetings with vs. without the full reminder ladder (this is the proof-of-value chart).'
  outputs:
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Booking Confirmation Flow

## Procedure

1. **Build Reminder Email Content** [`create_email_content`] — Generate 2 reminder email touches for upcoming B2B meetings. 48hr-before reminder: full agenda recap, attendee list, add-to-calendar links (iCal + Google + Outlook), location/conferencing details, and a reschedule link. 24hr-before reminder: lighter — just the meeting time, conferencing link, and a low-friction reschedule button. Send-from: the meeting host. Tone: professional, confirming. → produces: asset
2. **Build SMS Reminder Content** [`create_sms_content`] — Generate a 2-hour-before SMS reminder. Format: under 160 chars. Include meeting time, conferencing link (shortened), and a reply-RESCHEDULE option. Example: 'Reminder: your call with [Host Name] starts in 2 hours. Join: [link]. Reply RESCHEDULE to move it.' Only fires if user has SMS opt-in. → produces: asset
3. **Build Reminder Journey** [`create_journey`] — Build a 3-touch journey triggered by meeting_scheduled, with all touches timed relative to meeting_start_time. Touch 1: 48hr email reminder (skip if meeting is sooner than 48hr at scheduling time). Touch 2: 24hr email reminder. Touch 3: 2hr SMS reminder (only if user has SMS opt-in). Exit conditions: meeting_completed, meeting_cancelled, or user opted out. If meeting is rescheduled, recompute all touch times from the new meeting_start_time. → produces: journey
4. **Build Booking Confirmation Workflow** [`create_workflow`] — Create a workflow firing on meeting_scheduled. Step sequence: (1) post host notification to Slack with meeting details and a link to the user record; (2) link the meeting to the open deal if one exists for the user's account; (3) trigger the reminder journey. On meeting_cancelled, send the host a notification and exit the journey for that user. → produces: workflow
5. **Build Show-Rate Dashboard** [`create_dashboard`] — Compose a dashboard tracking meeting show-rate: overall show-rate by reminder cadence completeness (how many of the 3 reminders were delivered before the meeting), email reminder open/click rates, SMS reminder reply rate, and reschedule rate. Break down by meeting type and rep. Compare show-rate for meetings with vs. without the full reminder ladder (this is the proof-of-value chart). → produces: dashboard
