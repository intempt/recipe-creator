---
frontmatter_id: cinematic-studio
slash_command: /cinematic-studio
description: Visitors who browsed lightly a few weeks ago and are browsing a lot more now, tagged and surfaced to growth as an escalating-interest signal draft worth a closer look.
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
  summary: Finds visitors who browsed lightly two to four weeks ago and now browse much more, tags them, and drafts a Slack
    alert for the growth team to review.
  parameters:
  - name: lightBrowseMinDays
    type: duration
    label: Earliest window for light browsing (days ago)
    default: 30 d
    required: false
  - name: lightBrowseMaxDays
    type: duration
    label: Latest window for light browsing (days ago)
    default: 14 d
    required: false
  - name: recentWindow
    type: duration
    label: Recent browsing window
    default: 7 d
    required: false
  - name: recentViewThreshold
    type: number
    label: Minimum page views in the recent window
    default: 3
    required: false
  - name: growthChannel
    type: string
    label: Growth team Slack channel
    default: growth team channel
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A user viewed a page on the website
  - slot: slack_workspace
    kind: integration
    meaning: A connected Slack workspace for sending growth alerts
    channel: slack
  - slot: growth_team_channel
    kind: destination
    meaning: The Slack channel the growth team reads for alerts
    channel: slack
  - slot: warming_up_segment
    kind: segment
    meaning: Users who browsed lightly two to four weeks ago and are browsing much more in the last week
    creatable: true
    definition: users who did {page_view_event} at least once between {lightBrowseMaxDays} and {lightBrowseMinDays} ago and
      did {page_view_event} at least {recentViewThreshold} times in the last {recentWindow}
  steps:
  - id: s1
    builds: segment
    uses:
    - page_view_event
    - lightBrowseMinDays
    - lightBrowseMaxDays
    - recentViewThreshold
    - recentWindow
    instruction: Build a segment named "Warming Up Visitors" of users who did {page_view_event} at least once between {lightBrowseMaxDays}
      and {lightBrowseMinDays} ago and did {page_view_event} at least {recentViewThreshold} times in the last {recentWindow}.
  - id: s2
    builds: attribute
    uses:
    - s1
    - warming_up_segment
    instruction: Create an attribute named "warming_up" on users in the segment built in "Build the warming-up visitor list",
      set to true.
  - id: s3
    builds: slack
    uses:
    - s1
    - growth_team_channel
    - slack_workspace
    instruction: Draft a Slack message to {growth_team_channel} stating how many users are in the segment built in "Build
      the warming-up visitor list" right now, as a ready-made shortlist of visitors trending toward higher engagement. Draft
      only; a person on the team posts it.
---

# Warming Up Visitors

Slash command: /cinematic-studio

## Step 1: Build the warming-up visitor list

Build a segment of users named "Warming Up Visitors". A user is in the segment only when all of these are true: triggered "View page" at least once between 14 and 30 days ago; triggered "View page" at least 3 times in the last 7 days.

## Step 2: Tag the matched visitors

Create an attribute named "warming_up" on users in "Warming Up Visitors", set to true. Use the result of "Build the warming-up visitor list".

## Step 3: Draft a growth alert

Generate a Slack message to the growth team channel. Say how many users are in "Warming Up Visitors" right now, so the team has a ready-made shortlist of visitors trending toward higher engagement. Use the result of "Build the warming-up visitor list". This drafts the Slack message only; a person on the team still posts it.
