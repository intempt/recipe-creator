---
frontmatter_id: image-remix
slash_command: /image-remix
description: Visitors who clicked around actively in one visit and then disappeared for days, tagged with a ready-to-send push nudge drafted to bring them back.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds visitors who clicked actively in one visit then vanished for days, tags them, and drafts a friendly push
    nudge to bring them back for a person to send.
  parameters:
  - name: click_window
    type: duration
    label: Window for click activity
    default: 1 d
    required: false
  - name: min_clicks
    type: number
    label: Minimum click events in window
    default: 3
    required: false
  - name: absence_window
    type: duration
    label: Period with no session start
    default: 3 d
    required: false
  - name: push_tone
    type: enum
    label: Tone of the push draft
    default: friendly
    required: false
    options:
    - friendly
    - playful
    - formal
    - urgent
  - name: title_max_length
    type: number
    label: Maximum push title length (characters)
    default: 40
    required: false
  requirements:
  - slot: click_event
    kind: event
    meaning: A customer clicked on something in the app or site
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the app or site
  - slot: clicked_then_gone_segment
    kind: segment
    meaning: Users who clicked actively in one visit and have not started a session for several days
    creatable: true
    definition: users who triggered {click_event} at least {min_clicks} times in the last {click_window} and did not trigger
      {session_start_event} in the last {absence_window}
  - slot: clicked_then_gone_flag
    kind: attribute
    meaning: A user attribute that marks whether the user clicked then went quiet
  - slot: push_channel
    kind: integration
    meaning: A push notification channel connected to the project
    channel: push
  steps:
  - id: s1
    builds: segment
    uses:
    - click_event
    - session_start_event
    - click_window
    - min_clicks
    - absence_window
    instruction: Build a segment named "Clicked But Didn't Return" of users who triggered {click_event} at least {min_clicks}
      times in the last {click_window} and did not trigger {session_start_event} in the last {absence_window}.
  - id: s2
    builds: attribute
    uses:
    - s1
    - clicked_then_gone_flag
    instruction: Create a user attribute named "clicked_then_gone" set to true for all users in the segment built in "Build
      the clicked-but-gone list".
  - id: s3
    builds: push
    uses:
    - s1
    - push_channel
    - push_tone
    - title_max_length
    instruction: Generate a push notification for users in the segment built in "Build the clicked-but-gone list" inviting
      them to pick up where they left off. Title must be under {title_max_length} characters, body one short line, {push_tone}
      tone. This only drafts the push; a person still sends it.
---

# Clicked But Didn't Return

Slash command: /image-remix

## Step 1: Build the clicked-but-gone list

Build a segment of users named "Clicked But Didn't Return". A user is in the segment only when all of these are true: triggered "Click on" at least 3 times in the last 1 day; did not trigger "Session start" in the last 3 days.

## Step 2: Tag the matched visitors

Create an attribute named "clicked_then_gone" on users in "Clicked But Didn't Return", set to true. Use the result of "Build the clicked-but-gone list".

## Step 3: Draft a nudge push

Generate a push notification for the users in "Clicked But Didn't Return" inviting them back to pick up where they left off. Title under 40 characters, one short body line, friendly tone. Use the result of "Build the clicked-but-gone list". This drafts the push only; a person still sends it.
