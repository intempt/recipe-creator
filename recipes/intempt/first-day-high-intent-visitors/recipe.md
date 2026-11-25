---
frontmatter_id: first-day-high-intent-visitors
slash_command: /first-day-high-intent-visitors
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
    meaning: A user clicked an element on the site or app (the project's click event)
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
    instruction: 'Build a new segment named "First-Day High-Intent Visitors" with the rule: users who triggered {session_start_event}
      at least once in the last {lookback_window}; did not trigger {session_start_event} more than {lookback_window} ago;
      and triggered {click_event} at least {min_clicks} times in the last {lookback_window}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_team_slack
    dependsOn:
    - s1
    instruction: Draft a Slack message for the sales team channel on {sales_team_slack} stating how many users are currently
      in the segment from "Build the first-day high-intent list", noting that these are brand-new visitors already showing
      strong interest today. Use the result of "Build the first-day high-intent list". This drafts the message only; a person
      on the team posts it. Use the segment's current member count from the step that built it; never write a placeholder
      in square brackets. If no count is available, name the segment and say it can be opened in Segments.
  - id: s3
    builds: push
    uses:
    - s1
    - push_tone
    - push_title_max_chars
    - push_body_lines
    dependsOn:
    - s1
    instruction: Draft a push notification for users in the segment from "Build the first-day high-intent list" inviting them
      back to pick up where they left off. Title must be under {push_title_max_chars} characters; body must be {push_body_lines}
      short line(s); tone {push_tone}. Use the result of "Build the first-day high-intent list". This drafts the push only;
      a person still sends it. Write no link, URL, template tag or placeholder in the title or body; the push opens the site
      or app.
---

# First-Day High-Intent Visitors

Slash command: /first-day-high-intent-visitors

## Step 1: Build the first-day high-intent list

Build a new segment named "First-Day High-Intent Visitors" with the rule: users who triggered session start event at least once in the last 1 d; did not trigger session start event more than 1 d ago; and triggered click event at least 5 times in the last 1 d.

## Step 2: Draft a sales alert

Draft a Slack message for the sales team channel on sales team slack stating how many users are currently in the segment from "Build the first-day high-intent list", noting that these are brand-new visitors already showing strong interest today. Use the result of "Build the first-day high-intent list". This drafts the message only; a person on the team posts it. Use the segment's current member count from the step that built it; never write a placeholder in square brackets. If no count is available, name the segment and say it can be opened in Segments.

## Step 3: Draft a nudge push

Draft a push notification for users in the segment from "Build the first-day high-intent list" inviting them back to pick up where they left off. Title must be under 40 characters; body must be 1 short line(s); tone friendly and curious. Use the result of "Build the first-day high-intent list". This drafts the push only; a person still sends it. Write no link, URL, template tag or placeholder in the title or body; the push opens the site or app.
