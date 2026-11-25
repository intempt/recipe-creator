---
frontmatter_id: multi-page-account-researchers
slash_command: /multi-page-account-researchers
description: Accounts where several people together are reading a lot of pages, tagged and surfaced to sales as a broad research-intensity signal draft worth account-based outreach.
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
  summary: Flags accounts where several people together view many pages in a week, tags them as research-intensive, and drafts
    a Slack alert for sales to review before outreach.
  parameters:
  - name: page_view_threshold
    type: number
    label: Minimum combined page views across the account
    default: 15
    required: false
  - name: lookback_window
    type: duration
    label: Lookback window
    default: 7 d
    required: false
  - name: sales_channel
    type: string
    label: Sales Slack channel name
    default: sales
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A person viewed a web page
  - slot: research_flag_attribute
    kind: attribute
    meaning: An account-level true/false flag that marks research-intensive accounts
    optional: true
  - slot: sales_slack
    kind: integration
    meaning: A connected Slack workspace where the sales team channel can receive messages
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - page_view_event
    - page_view_threshold
    - lookback_window
    instruction: Build a new segment named "Multi-Page Account Researchers" of accounts where the users in the account together
      did {page_view_event} {page_view_threshold} or more times in the last {lookback_window}. Include only accounts that
      meet this condition.
  - id: s2
    builds: attribute
    uses:
    - s1
    - research_flag_attribute
    dependsOn:
    - s1
    instruction: Create an account attribute named "research_intensive" set to true for every account in the segment built
      in "Build the research-intensive account list".
  - id: s3
    builds: slack
    uses:
    - s1
    - sales_slack
    - sales_channel
    instruction: Draft a Slack message to the {sales_channel} channel that names each account in the segment built in "Build
      the research-intensive account list", so reps can prioritize outreach while research activity is high. Draft only; a
      team member posts it manually. Take the names or addresses from the member list of the step that built the segment (at
      most 20, then how many more); never write a placeholder or ask the reader to paste anything in. If no member list is
      available, name the segment and say it can be opened in Segments.
---

# Multi-Page Account Researchers

Slash command: /multi-page-account-researchers

## Step 1: Build the research-intensive account list

Build a new segment named "Multi-Page Account Researchers" of accounts where the users in the account together did page view event 15 or more times in the last 7 d. Include only accounts that meet this condition.

## Step 2: Tag the matched accounts

Create an account attribute named "research_intensive" set to true for every account in the segment built in "Build the research-intensive account list".

## Step 3: Draft a sales alert

Draft a Slack message to the sales channel that names each account in the segment built in "Build the research-intensive account list", so reps can prioritize outreach while research activity is high. Draft only; a team member posts it manually. Take the names or addresses from the member list of the step that built the segment (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. If no member list is available, name the segment and say it can be opened in Segments.
