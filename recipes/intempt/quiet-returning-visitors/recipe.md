---
frontmatter_id: quiet-returning-visitors
slash_command: /quiet-returning-visitors
description: Visitors who keep coming back without ever clicking anything, with a push nudge drafted and a note drafted for the content team about a possible low-interaction signal.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Finds visitors who return often but never click anything, drafts a friendly push nudge for them, and drafts a Slack
    note to the content team about the group size.
  parameters:
  - name: session_threshold
    type: number
    label: Minimum session starts in the window
    default: 2
    required: false
  - name: lookback_window
    type: duration
    label: Lookback window
    default: 14 d
    required: false
  - name: push_tone
    type: enum
    label: Push tone
    default: friendly
    required: false
    options:
    - friendly
    - playful
    - formal
  - name: push_title_max_chars
    type: number
    label: Push title maximum characters
    default: 40
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session on the site or app
  - slot: click_event
    kind: event
    meaning: A user clicked an element on the site or app (the project's click event)
  - slot: content_team_channel
    kind: integration
    meaning: A Slack channel used by the content team
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - click_event
    - session_threshold
    - lookback_window
    instruction: Build a new segment named "Quiet Returning Visitors" for users who did {session_start_event} at least {session_threshold}
      times in the last {lookback_window} and did not do {click_event} in the last {lookback_window}.
  - id: s2
    builds: push
    uses:
    - s1
    - push_tone
    - push_title_max_chars
    dependsOn:
    - s1
    instruction: Draft a push notification for the users in the segment from "Build the quiet returning visitor list" that
      highlights one thing worth clicking on, chosen for this run. Title must be under {push_title_max_chars} characters,
      followed by one short body line, in a {push_tone} and inviting tone. Use the result of "Build the quiet returning visitor
      list". This drafts the push only; a person still sends it. Write no link, URL, template tag or placeholder in the title
      or body; the push opens the site or app.
  - id: s3
    builds: slack
    uses:
    - s1
    - content_team_channel
    dependsOn:
    - s1
    instruction: Draft a Slack message for {content_team_channel} stating how many users are in the segment from "Build the
      quiet returning visitor list" right now, so the team knows a group of returning visitors is not finding anything worth
      clicking on. Use the result of "Build the quiet returning visitor list". This drafts the Slack message only; a person
      on the team still posts it. Use the segment's current member count from the step that built it; never write a placeholder
      in square brackets. If no count is available, name the segment and say it can be opened in Segments.
---

# Quiet Returning Visitors

Slash command: /quiet-returning-visitors

## Step 1: Build the quiet returning visitor list

Build a new segment named "Quiet Returning Visitors" for users who did session start event at least 2 times in the last 14 d and did not do click event in the last 14 d.

## Step 2: Draft a nudge push

Draft a push notification for the users in the segment from "Build the quiet returning visitor list" that highlights one thing worth clicking on, chosen for this run. Title must be under 40 characters, followed by one short body line, in a friendly and inviting tone. Use the result of "Build the quiet returning visitor list". This drafts the push only; a person still sends it. Write no link, URL, template tag or placeholder in the title or body; the push opens the site or app.

## Step 3: Draft a note for the content team

Draft a Slack message for content team channel stating how many users are in the segment from "Build the quiet returning visitor list" right now, so the team knows a group of returning visitors is not finding anything worth clicking on. Use the result of "Build the quiet returning visitor list". This drafts the Slack message only; a person on the team still posts it. Use the segment's current member count from the step that built it; never write a placeholder in square brackets. If no count is available, name the segment and say it can be opened in Segments.
