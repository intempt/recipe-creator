---
frontmatter_id: submitted-then-quiet
slash_command: /submitted-then-quiet
description: Users who submitted a form but have gone quiet since, with a warm follow-up email drafted before the lead goes cold.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds users who submitted a form recently but have gone quiet since, and drafts a warm three-sentence follow-up
    email for a person to review and send.
  parameters:
  - name: submit_window
    type: duration
    label: Lookback window for form submission
    default: 14 d
    required: false
  - name: quiet_window
    type: duration
    label: Inactivity window with no session
    default: 7 d
    required: false
  - name: email_tone
    type: string
    label: Tone of the follow-up email
    default: encouraging
    required: false
  requirements:
  - slot: form_submit_event
    kind: event
    meaning: A user submitted a form on the site (the project's form-submit event, never a survey or NPS answer)
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the product
  steps:
  - id: s1
    builds: segment
    uses:
    - form_submit_event
    - session_start_event
    - submit_window
    - quiet_window
    instruction: Build a new segment named "Submitted Then Quiet". Include users who did {form_submit_event} at least once
      in the last {submit_window} and did not do {session_start_event} in the last {quiet_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - email_tone
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in the segment from "Build the quiet-after-submit list"
      with a warm follow-up nudge. Use three sentences, a {email_tone} tone, no discount language, and one button linking
      back to the product. This drafts the email only; a person still sends it. If the brand kit has no logo, use the brand
      name as a plain text header; the button links to the URL chosen for this run.
---

# Submitted Then Quiet

Slash command: /submitted-then-quiet

## Step 1: Build the quiet-after-submit list

Build a new segment named "Submitted Then Quiet". Include users who did form submit event at least once in the last 14 d and did not do session start event in the last 7 d.

## Step 2: Draft the follow-up email

Generate a designed marketing email for the users in the segment from "Build the quiet-after-submit list" with a warm follow-up nudge. Use three sentences, a encouraging tone, no discount language, and one button linking back to the product. This drafts the email only; a person still sends it. If the brand kit has no logo, use the brand name as a plain text header; the button links to the URL chosen for this run.
