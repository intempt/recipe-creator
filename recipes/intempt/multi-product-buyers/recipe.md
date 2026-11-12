---
frontmatter_id: multi-product-buyers
slash_command: /multi-product-buyers
description: Visitors who return across several sessions and view many pages, tagged with a reusable attribute and surfaced to growth as a draft alert, the strongest organic engagement signal available without any custom tracking.
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
  summary: Builds a segment of visitors who return across several sessions and view many pages, tags them with a reusable
    attribute, and drafts a Slack alert for the growth team to review.
  parameters:
  - name: session_threshold
    type: number
    label: Minimum session starts in the window
    default: 3
    required: false
  - name: page_view_threshold
    type: number
    label: Minimum page views in the window
    default: 5
    required: false
  - name: window
    type: duration
    label: Lookback window
    default: 30 d
    required: false
  - name: growth_channel
    type: string
    label: Growth team Slack channel
    default: growth
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A visitor started a session on the site or app
  - slot: page_view_event
    kind: event
    meaning: A visitor viewed a page
  - slot: highly_active_segment
    kind: segment
    meaning: Users who did session start at least a set number of times and did view page at least a set number of times in
      the last window
    creatable: true
    definition: users who triggered {session_start_event} at least {session_threshold} times in the last {window} and triggered
      {page_view_event} at least {page_view_threshold} times in the last {window}
  - slot: power_browser_attribute
    kind: attribute
    meaning: A user-level true/false flag marking highly engaged multi-session visitors
  - slot: growth_slack
    kind: destination
    meaning: Slack workspace channel used by the growth team
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - page_view_event
    - session_threshold
    - page_view_threshold
    - window
    - highly_active_segment
    instruction: 'Build the segment {highly_active_segment} named "Highly Active Multi-Session Visitors". A user is in the
      segment only when all of these are true: triggered {session_start_event} at least {session_threshold} times in the last
      {window}; triggered {page_view_event} at least {page_view_threshold} times in the last {window}.'
  - id: s2
    builds: attribute
    uses:
    - highly_active_segment
    - power_browser_attribute
    - s1
    instruction: Create the attribute {power_browser_attribute} on users in {highly_active_segment}, set to true. Use the
      result of "Build the highly active visitor list".
  - id: s3
    builds: slack
    uses:
    - highly_active_segment
    - growth_slack
    - growth_channel
    - s1
    instruction: Draft a Slack message to the {growth_channel} channel on {growth_slack}. State how many users are in {highly_active_segment}
      right now, so the team has a ready-made shortlist worth a closer look. Use the result of "Build the highly active visitor
      list". This drafts the Slack message only; a person on the team still posts it.
---

# Highly Active Multi-Session Visitors

Slash command: /multi-product-buyers

## Step 1: Build the highly active visitor list

Build a segment of users named "Highly Active Multi-Session Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least 3 times in the last 30 days; triggered "View page" at least 5 times in the last 30 days.

## Step 2: Tag the matched visitors

Create an attribute named "power_browser" on users in "Highly Active Multi-Session Visitors", set to true. Use the result of "Build the highly active visitor list".

## Step 3: Draft a growth alert

Generate a Slack message to the growth team channel. Say how many users are in "Highly Active Multi-Session Visitors" right now, so the team has a ready-made shortlist worth a closer look. Use the result of "Build the highly active visitor list". This drafts the Slack message only; a person on the team still posts it.
