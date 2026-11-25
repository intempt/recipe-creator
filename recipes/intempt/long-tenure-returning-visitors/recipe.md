---
frontmatter_id: long-tenure-returning-visitors
slash_command: /long-tenure-returning-visitors
description: Visitors active again this week who first showed up months ago, with a ready-to-send welcome-back email drafted and a heads-up drafted for the lifecycle team.
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
  summary: Finds visitors active again this week who first appeared months ago, then drafts a welcome-back email and a Slack
    heads-up for the lifecycle team; a person still sends both.
  parameters:
  - name: recent_window
    type: duration
    label: Recent activity window
    default: 7 d
    required: false
  - name: tenure_min_days
    type: number
    label: Earliest days ago of the older session
    default: 60
    required: false
  - name: tenure_max_days
    type: number
    label: Latest days ago of the older session
    default: 90
    required: false
  - name: email_sentences
    type: number
    label: Number of sentences in welcome-back email
    default: 3
    required: false
  - name: email_tone
    type: string
    label: Email tone
    default: warm
    required: false
  requirements:
  - slot: session_start
    kind: event
    meaning: A visitor started a session on the product
  - slot: lifecycle_team_channel
    kind: integration
    meaning: Slack workspace with a channel the lifecycle team reads
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start
    - recent_window
    - tenure_min_days
    - tenure_max_days
    instruction: Build a new segment named "Long-Tenure Returning Visitors" with users who triggered {session_start} at least
      once in the last {recent_window} and triggered {session_start} at least once between {tenure_max_days} and {tenure_min_days}
      days ago.
  - id: s2
    builds: email
    uses:
    - s1
    - email_sentences
    - email_tone
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the users in the "Long-Tenure Returning Visitors" segment that welcomes
      them back and points to what is new in the product since they last visited regularly. Use exactly {email_sentences}
      sentences in a {email_tone} tone. Do not use discount language. Include one button linking to the product. This drafts
      the email only; a person still sends it. If the brand kit has no logo, use the brand name as a plain text header; the
      button links to the URL chosen for this run.
  - id: s3
    builds: slack
    uses:
    - s1
    - lifecycle_team_channel
    instruction: Draft a Slack message to {lifecycle_team_channel} stating how many users are currently in the "Long-Tenure
      Returning Visitors" segment, so the team knows a batch of long-time users is active again. This drafts the message only;
      a person on the team still posts it. Use the segment's current member count from the step that built it; never write
      a placeholder in square brackets. If no count is available, name the segment and say it can be opened in Segments.
---

# Long-Tenure Returning Visitors

Slash command: /long-tenure-returning-visitors

## Step 1: Build the long-tenure returning visitor list

Build a new segment named "Long-Tenure Returning Visitors" with users who triggered session start at least once in the last 7 d and triggered session start at least once between 90 and 60 days ago.

## Step 2: Draft a welcome-back email

Generate a designed marketing email for the users in the "Long-Tenure Returning Visitors" segment that welcomes them back and points to what is new in the product since they last visited regularly. Use exactly 3 sentences in a warm tone. Do not use discount language. Include one button linking to the product. This drafts the email only; a person still sends it. If the brand kit has no logo, use the brand name as a plain text header; the button links to the URL chosen for this run.

## Step 3: Draft a note for the lifecycle team

Draft a Slack message to lifecycle team channel stating how many users are currently in the "Long-Tenure Returning Visitors" segment, so the team knows a batch of long-time users is active again. This drafts the message only; a person on the team still posts it. Use the segment's current member count from the step that built it; never write a placeholder in square brackets. If no count is available, name the segment and say it can be opened in Segments.
