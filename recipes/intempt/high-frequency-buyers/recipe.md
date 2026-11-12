---
frontmatter_id: high-frequency-buyers
slash_command: /high-frequency-buyers
description: Visitors who both browse repeatedly and click around the site, surfaced to marketing as a draft alert, a stronger engagement signal than page views alone.
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
  summary: Builds a segment of repeat visitors who browse and click, then drafts a Slack alert for marketing with the segment's
    current size for a person to post.
  parameters:
  - name: page_view_min_count
    type: number
    label: Minimum page view events in window
    default: 3
    required: false
  - name: lookback_window
    type: duration
    label: Lookback window
    default: 7 d
    required: false
  - name: marketing_channel_name
    type: string
    label: Marketing team Slack channel
    default: marketing
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A user viewed a page on the website
  - slot: click_event
    kind: event
    meaning: A user clicked an element on the website
  - slot: engaged_repeat_visitors
    kind: segment
    meaning: Users who viewed pages repeatedly and clicked on the website recently
    creatable: true
    definition: users who triggered {page_view_event} at least {page_view_min_count} times in the last {lookback_window} and
      triggered {click_event} at least once in the last {lookback_window}
  - slot: slack_integration
    kind: integration
    meaning: A connected Slack workspace for posting alerts to the marketing team
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - page_view_event
    - click_event
    - page_view_min_count
    - lookback_window
    - engaged_repeat_visitors
    instruction: Build a segment named "Engaged Repeat Visitors" containing users who triggered {page_view_event} at least
      {page_view_min_count} times in the last {lookback_window} and triggered {click_event} at least once in the last {lookback_window}.
  - id: s2
    builds: slack
    uses:
    - s1
    - engaged_repeat_visitors
    - slack_integration
    - marketing_channel_name
    instruction: Draft a Slack message to the {marketing_channel_name} channel in {slack_integration} stating how many users
      are currently in "Build a segment named" segment {engaged_repeat_visitors}, so the team knows who is browsing and clicking
      rather than just passing through. This drafts the message only; a team member still posts it.
---

# Engaged Repeat Visitors

Slash command: /high-frequency-buyers

## Step 1: Build the engaged repeat visitor list

Build a segment of users named "Engaged Repeat Visitors". A user is in the segment only when all of these are true: triggered "View page" at least 3 times in the last 7 days; triggered "Click on" at least once in the last 7 days.

## Step 2: Draft a marketing alert

Generate a Slack message to the marketing team channel. Say how many users are in "Engaged Repeat Visitors" right now, so the team knows who is browsing and clicking, not just passing through. Use the result of "Build the engaged repeat visitor list". This drafts the Slack message only; a person on the team still posts it.
