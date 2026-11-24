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
  - slot: quiet_returning_visitors
    kind: segment
    meaning: Users who started at least a set number of sessions in the lookback window and did not click in that window
    creatable: true
    definition: users who did {session_start_event} at least {session_threshold} times in the last {lookback_window} and did
      not do {click_event} in the last {lookback_window}
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
    - quiet_returning_visitors
    instruction: Build the segment {quiet_returning_visitors} for users who did {session_start_event} at least {session_threshold}
      times in the last {lookback_window} and did not do {click_event} in the last {lookback_window}.
  - id: s2
    builds: push
    uses:
    - quiet_returning_visitors
    - s1
    - push_tone
    - push_title_max_chars
    instruction: Draft a push notification for the users in {quiet_returning_visitors} that highlights one thing worth clicking
      on, chosen for this run. Title must be under {push_title_max_chars} characters, followed by one short body line, in
      a {push_tone} and inviting tone. Use the result of "Build the quiet returning visitor list". This drafts the push only;
      a person still sends it. Write no link, URL, template tag or placeholder in the title or body; the push opens the site
      or app.
  - id: s3
    builds: slack
    uses:
    - quiet_returning_visitors
    - s1
    - content_team_channel
    instruction: Draft a Slack message for {content_team_channel} stating how many users are in {quiet_returning_visitors}
      right now, so the team knows a group of returning visitors is not finding anything worth clicking on. Use the result
      of "Build the quiet returning visitor list". This drafts the Slack message only; a person on the team still posts it.
      Use the segment's current member count from the step that built it; never write a placeholder in square brackets. If
      no count is available, name the segment and say it can be opened in Segments.
---

# Quiet Returning Visitors

Slash command: /quiet-returning-visitors

## Step 1: Build the quiet returning visitor list

Build a segment of users named "Quiet Returning Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least 2 times in the last 14 days; did not trigger the click event (a tracked click on a page element) in the last 14 days.

## Step 2: Draft a nudge push

Generate a push notification for the users in "Quiet Returning Visitors" highlighting one thing worth clicking on, chosen for this run. Title under 40 characters, one short body line, friendly and inviting tone. Use the result of "Build the quiet returning visitor list". Write no link, URL, template tag or placeholder in the title or body; the push opens the site or app. This drafts the push only; a person still sends it.

## Step 3: Draft a note for the content team

Generate a Slack message to the content team channel. State how many users are in "Quiet Returning Visitors" right now, using the member count in the result of "Build the quiet returning visitor list". If that result carries no count, write no number and no placeholder in square brackets; say instead that the list is saved as the segment "Quiet Returning Visitors" and can be opened in Segments. Say a group of returning visitors is not finding anything worth clicking on. This drafts the Slack message only; a person on the team still posts it.
