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
    meaning: A customer submitted a form
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the product
  - slot: quiet_after_submit_segment
    kind: segment
    meaning: Users who submitted a form but have not started a session recently
    creatable: true
    definition: users who did {form_submit_event} in the last {submit_window} and did not do {session_start_event} in the
      last {quiet_window}
  steps:
  - id: s1
    builds: segment
    uses:
    - form_submit_event
    - session_start_event
    - submit_window
    - quiet_window
    instruction: Build a segment named "Submitted Then Quiet". Include users who did {form_submit_event} at least once in
      the last {submit_window} and did not do {session_start_event} in the last {quiet_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - email_tone
    instruction: Generate a designed marketing email for the users in the segment from "Build the quiet-after-submit list"
      with a warm follow-up nudge. Use three sentences, a {email_tone} tone, no discount language, and one button linking
      back to the product. This drafts the email only; a person still sends it.
---

# Submitted Then Quiet

Slash command: /submitted-then-quiet

## Step 1: Build the quiet-after-submit list

Build a segment of users named "Submitted Then Quiet". A user is in the segment only when all of these are true: triggered "Submit on" at least once in the last 14 days; did not trigger "Session start" in the last 7 days.

## Step 2: Draft the follow-up email

Generate a designed marketing email for the users in "Submitted Then Quiet" with a warm follow-up nudge. Three sentences, encouraging tone, no discount language, one button linking back to the product. Use the result of "Build the quiet-after-submit list". This drafts the email only; a person still sends it.
