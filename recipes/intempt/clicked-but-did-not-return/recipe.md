---
frontmatter_id: clicked-but-did-not-return
slash_command: /clicked-but-did-not-return
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
    default: 7 d
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
    meaning: A user clicked an element on the site or app (the project's click event)
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the app or site
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
    instruction: Build a new segment named "Clicked But Did Not Return" of users who triggered {click_event} at least {min_clicks}
      times in the last {click_window} and did not trigger {session_start_event} in the last {absence_window}.
  - id: s2
    builds: attribute
    uses:
    - s1
    - clicked_then_gone_flag
    dependsOn:
    - s1
    instruction: Create a user attribute named "clicked_then_gone" set to true for all users in the segment built in "Build
      the clicked-but-gone list".
  - id: s3
    builds: push
    uses:
    - s1
    - push_channel
    - push_tone
    - title_max_length
    dependsOn:
    - s1
    instruction: Generate a push notification for users in the segment built in "Build the clicked-but-gone list" inviting
      them to pick up where they left off. Title must be under {title_max_length} characters, body one short line, {push_tone}
      tone. This only drafts the push; a person still sends it. Write no link, URL, template tag or placeholder in the title
      or body; the push opens the site or app.
---

# Clicked But Did Not Return

Slash command: /clicked-but-did-not-return

## Step 1: Build the clicked-but-gone list

Build a new segment named "Clicked But Did Not Return" of users who triggered click event at least 3 times in the last 7 d and did not trigger session start event in the last 3 d.

## Step 2: Tag the matched visitors

Create a user attribute named "clicked_then_gone" set to true for all users in the segment built in "Build the clicked-but-gone list".

## Step 3: Draft a nudge push

Generate a push notification for users in the segment built in "Build the clicked-but-gone list" inviting them to pick up where they left off. Title must be under 40 characters, body one short line, friendly tone. This only drafts the push; a person still sends it. Write no link, URL, template tag or placeholder in the title or body; the push opens the site or app.
