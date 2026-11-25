---
frontmatter_id: discovery-call-summary-recipe
slash_command: /discovery-call-summary-recipe
description: After every Discovery call, analyzes the transcript into seven qualification fields and emails them to the team,
  plus a weekly digest of field capture by rep.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails the seven qualification fields (champion, pain, current solution, decision criteria, timeline, budget, next
    step) after each Discovery call, and a weekly quality digest by rep.
  parameters:
  - name: target_capture_rate
    type: number
    label: Target share of discovery calls with all 7 fields captured (%)
    default: 70
    required: false
  - name: discovery_meeting_type
    type: string
    label: Meeting type name for Discovery calls
    default: Discovery
    required: false
  - name: unknown_value_label
    type: string
    label: Value written when a field was not discussed
    default: not_discussed
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses that get each call's fields
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: meeting_recording
    kind: event
    meaning: A customer meeting was recorded and transcribed
    properties:
    - name: meeting_type
      type: string
      meaning: The meeting type name, such as Discovery
      optional: false
    - name: rep_name
      type: string
      meaning: The rep who ran the meeting
      optional: false
    - name: transcript
      type: string
      meaning: Transcript text of the meeting
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - meeting_recording
    - discovery_meeting_type
    - unknown_value_label
    - alert_recipients
    instruction: 'Build an automation triggered by {meeting_recording} with {meeting_recording.meeting_type} equal to {discovery_meeting_type}.
      It analyzes {meeting_recording.transcript} and writes seven fields: champion (name, title, buy-in high, medium, low
      or none, a quote); pain (in the prospect''s words, severity must-solve, should-solve or nice-to-have, business impact);
      current solution (what they use, what works, what does not); decision criteria (each criterion and its priority); timeline
      (target go-live, urgency drivers); budget (number, range or signal); next step (what was agreed, owner, due date). A
      field not discussed is written as {unknown_value_label}. Then it emails the prospect''s name, {meeting_recording.rep_name}
      and these fields to {alert_recipients}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - meeting_recording
    - discovery_meeting_type
    - target_capture_rate
    - unknown_value_label
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the fields written
      by "Capture the discovery fields" for {meeting_recording} with {meeting_recording.meeting_type} equal to {discovery_meeting_type}
      in the last 7 days and writes these figures by {meeting_recording.rep_name}: the number of calls; the share with all
      seven fields captured, against {target_capture_rate}%; the fields most often {unknown_value_label}; the calls with no
      budget signal; the split of champion buy-in and of pain severity. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Discovery call qualification fields

Slash command: /discovery-call-summary-recipe

## Step 1: Capture the discovery fields

Build an automation triggered by meeting recording with meeting type equal to Discovery. It analyzes transcript and writes seven fields: champion (name, title, buy-in high, medium, low or none, a quote); pain (in the prospect's words, severity must-solve, should-solve or nice-to-have, business impact); current solution (what they use, what works, what does not); decision criteria (each criterion and its priority); timeline (target go-live, urgency drivers); budget (number, range or signal); next step (what was agreed, owner, due date). A field not discussed is written as not_discussed. Then it emails the prospect's name, rep name and these fields to the email addresses that get each call's fields.

## Step 2: Email the weekly discovery quality digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the fields written by "Capture the discovery fields" for meeting recording with meeting type equal to Discovery in the last 7 days and writes these figures by rep name: the number of calls; the share with all seven fields captured, against 70%; the fields most often not_discussed; the calls with no budget signal; the split of champion buy-in and of pain severity. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
