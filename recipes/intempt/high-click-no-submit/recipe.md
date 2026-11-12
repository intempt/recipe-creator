---
frontmatter_id: high-click-no-submit
slash_command: /high-click-no-submit
description: Visitors clicking around heavily without ever submitting a form, surfaced to growth as a friction-signal draft worth a closer look.
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
  summary: Builds a list of visitors who click heavily but never submit a form, and drafts a Slack alert so growth can review
    them as friction signals.
  parameters:
  - name: click_threshold
    type: number
    label: Minimum click events
    default: 8
    required: false
  - name: click_window
    type: duration
    label: Click lookback window
    default: 7 d
    required: false
  - name: submit_window
    type: duration
    label: Submit lookback window
    default: 7 d
    required: false
  - name: segment_name
    type: string
    label: Segment name
    default: High-Click Non-Converters
    required: false
  requirements:
  - slot: click_event
    kind: event
    meaning: A visitor clicked on a page element
  - slot: submit_event
    kind: event
    meaning: A visitor submitted a form
  - slot: high_click_non_converters
    kind: segment
    meaning: Users who clicked heavily without submitting a form
    creatable: true
    definition: users who triggered {click_event} at least {click_threshold} times in the last {click_window} and did not
      trigger {submit_event} in the last {submit_window}
  - slot: growth_team_channel
    kind: integration
    meaning: A Slack channel used by the growth team
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - click_event
    - submit_event
    - click_threshold
    - click_window
    - submit_window
    - segment_name
    instruction: 'Build a segment named {segment_name}. A user is in the segment only when all of these are true: triggered
      {click_event} at least {click_threshold} times in the last {click_window}; did not trigger {submit_event} in the last
      {submit_window}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - growth_team_channel
    - segment_name
    instruction: Draft a Slack message to {growth_team_channel}. State how many users are in "Build a segment named {segment_name}"
      right now, so the team has a ready-made shortlist of high-friction visitors worth a closer look. This drafts the Slack
      message only; a person on the team still posts it.
---

# High-Click Non-Converters

Slash command: /high-click-no-submit

## Step 1: Build the high-click non-converter list

Build a segment of users named "High-Click Non-Converters". A user is in the segment only when all of these are true: triggered "Click on" at least 8 times in the last 7 days; did not trigger "Submit on" in the last 7 days.

## Step 2: Draft a growth alert

Generate a Slack message to the growth team channel. Say how many users are in "High-Click Non-Converters" right now, so the team has a ready-made shortlist of high-friction visitors worth a closer look. Use the result of "Build the high-click non-converter list". This drafts the Slack message only; a person on the team still posts it.
