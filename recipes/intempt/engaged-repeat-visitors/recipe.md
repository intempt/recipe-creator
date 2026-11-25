---
frontmatter_id: engaged-repeat-visitors
slash_command: /engaged-repeat-visitors
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
    meaning: A user clicked an element on the site or app (the project's click event)
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
    instruction: Build a new segment named "Engaged Repeat Visitors" containing users who triggered {page_view_event} at least
      {page_view_min_count} times in the last {lookback_window} and triggered {click_event} at least once in the last {lookback_window}.
  - id: s2
    builds: slack
    uses:
    - s1
    - slack_integration
    - marketing_channel_name
    dependsOn:
    - s1
    instruction: Draft a Slack message to the {marketing_channel_name} channel in {slack_integration} stating how many users
      are in the segment from "Build the engaged repeat visitor list" right now, so the team knows who is browsing and clicking
      rather than just passing through. This drafts the message only; a team member still posts it. Use the segment's current
      member count from the step that built it; never write a placeholder in square brackets. If no count is available, name
      the segment and say it can be opened in Segments.
---

# Engaged Repeat Visitors

Slash command: /engaged-repeat-visitors

## Step 1: Build the engaged repeat visitor list

Build a new segment named "Engaged Repeat Visitors" containing users who triggered page view event at least 3 times in the last 7 d and triggered click event at least once in the last 7 d.

## Step 2: Draft a marketing alert

Draft a Slack message to the marketing channel in slack integration stating how many users are in the segment from "Build the engaged repeat visitor list" right now, so the team knows who is browsing and clicking rather than just passing through. This drafts the message only; a team member still posts it. Use the segment's current member count from the step that built it; never write a placeholder in square brackets. If no count is available, name the segment and say it can be opened in Segments.
