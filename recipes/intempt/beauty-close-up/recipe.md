---
frontmatter_id: beauty-close-up
slash_command: /beauty-close-up
description: Brand-new visitors already clicking around heavily on their first day, surfaced to sales as a hot-lead draft with a ready-to-send push nudge back to the site.
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
  summary: Finds brand-new visitors who are clicking heavily on their first day, drafts a sales alert for Slack, and drafts
    a friendly push nudge inviting them back to the site for a person to review and send.
  parameters:
  - name: lookback_window
    type: duration
    label: Window for recent session and click activity
    default: 1 d
    required: false
  - name: min_clicks
    type: number
    label: Minimum click events in the window
    default: 5
    required: false
  - name: push_tone
    type: enum
    label: Tone of the push nudge
    default: friendly and curious
    required: false
    options:
    - friendly and curious
    - friendly and direct
    - playful
  - name: push_title_max_chars
    type: number
    label: Maximum characters for push title
    default: 40
    required: false
  - name: push_body_lines
    type: number
    label: Number of short body lines in push
    default: 1
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session on the site or app
  - slot: click_event
    kind: event
    meaning: A user clicked an element on the site or app
  - slot: first_day_high_intent_segment
    kind: segment
    meaning: Users who started a session in the last day, had no session start more than one day ago, and clicked at least
      a set number of times in the last day
    creatable: true
    definition: users who triggered {session_start_event} at least once in the last {lookback_window}, did not trigger {session_start_event}
      more than {lookback_window} ago, and triggered {click_event} at least {min_clicks} times in the last {lookback_window}
  - slot: sales_team_slack
    kind: integration
    meaning: A Slack workspace connected to post alerts to the sales team channel
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - click_event
    - lookback_window
    - min_clicks
    - first_day_high_intent_segment
    instruction: 'Build the segment {first_day_high_intent_segment} with the rule: users who triggered {session_start_event}
      at least once in the last {lookback_window}; did not trigger {session_start_event} more than {lookback_window} ago;
      and triggered {click_event} at least {min_clicks} times in the last {lookback_window}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - first_day_high_intent_segment
    - sales_team_slack
    instruction: Draft a Slack message for the sales team channel on {sales_team_slack} stating how many users are currently
      in {first_day_high_intent_segment}, noting that these are brand-new visitors already showing strong interest today.
      Use the result of "Build the first-day high-intent list". This drafts the message only; a person on the team posts it.
  - id: s3
    builds: push
    uses:
    - s1
    - first_day_high_intent_segment
    - push_tone
    - push_title_max_chars
    - push_body_lines
    instruction: Draft a push notification for users in {first_day_high_intent_segment} inviting them back to pick up where
      they left off. Title must be under {push_title_max_chars} characters; body must be {push_body_lines} short line(s);
      tone {push_tone}. Use the result of "Build the first-day high-intent list". This drafts the push only; a person still
      sends it.
---

# First-Day High-Intent Visitors

Slash command: /beauty-close-up

## Step 1: Build the first-day high-intent list

Build a segment of users named "First-Day High-Intent Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least once in the last 1 day; did not trigger "Session start" more than 1 day ago; triggered "Click on" at least 5 times in the last 1 day.

## Step 2: Draft a sales alert

Generate a Slack message to the sales team channel. Say how many users are in "First-Day High-Intent Visitors" right now, so reps know a brand-new visitor is already showing strong interest today. Use the result of "Build the first-day high-intent list". This drafts the Slack message only; a person on the team still posts it.

## Step 3: Draft a nudge push

Generate a push notification for the users in "First-Day High-Intent Visitors" inviting them back to pick up where they left off. Title under 40 characters, one short body line, friendly and curious tone. Use the result of "Build the first-day high-intent list". This drafts the push only; a person still sends it.
