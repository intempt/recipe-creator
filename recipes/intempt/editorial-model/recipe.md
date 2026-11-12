---
frontmatter_id: editorial-model
slash_command: /editorial-model
description: Visitors who submitted a form today and kept browsing right afterward, the hottest possible same-day lead signal, surfaced to sales with a follow-up email drafted and ready to review.
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
  summary: Surfaces visitors who submitted a form today and kept browsing afterward to sales, with a follow-up email drafted
    for review.
  parameters:
  - name: submit_window
    type: duration
    label: Lookback window for form submission and browsing
    default: 1 d
    required: false
  - name: min_page_views
    type: number
    label: Minimum page views after submitting
    default: 3
    required: false
  - name: email_sentence_count
    type: number
    label: Number of sentences in the follow-up email
    default: 3
    required: false
  - name: email_tone
    type: enum
    label: Tone of the follow-up email
    default: confident
    required: false
    options:
    - confident
    - friendly
    - formal
  requirements:
  - slot: submit_event
    kind: event
    meaning: A customer submitted a form on the site
  - slot: page_view_event
    kind: event
    meaning: A customer viewed a page on the site
  - slot: sales_slack
    kind: integration
    meaning: A Slack connection that can post to the sales team channel
    channel: slack
  - slot: still_engaged_submitters
    kind: segment
    meaning: Users who submitted a form and kept browsing right afterward
    creatable: true
    definition: users who did {submit_event} at least once in the last {submit_window} and did {page_view_event} at least
      {min_page_views} times in the last {submit_window}
  steps:
  - id: s1
    builds: segment
    uses:
    - submit_event
    - page_view_event
    - submit_window
    - min_page_views
    instruction: Build a segment named "Submitted And Still Engaged" containing users who did {submit_event} at least once
      in the last {submit_window} and did {page_view_event} at least {min_page_views} times in the last {submit_window}.
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_slack
    instruction: Draft a Slack message to the sales team channel stating how many users are currently in the segment built
      in "Build the still-engaged submitter list", so reps can follow up while these users are still active on the site today.
      Draft only; a team member posts it.
  - id: s3
    builds: email
    uses:
    - s1
    - email_sentence_count
    - email_tone
    instruction: Draft a designed marketing email for users in the segment built in "Build the still-engaged submitter list"
      confirming their form submission and naming the one next step worth taking right now. Write {email_sentence_count} sentences
      in a {email_tone} and helpful tone, with no discount language, and include one button linking to that next step. Draft
      only; a person sends it.
---

# Submitted And Still Engaged

Slash command: /editorial-model

## Step 1: Build the still-engaged submitter list

Build a segment of users named "Submitted And Still Engaged". A user is in the segment only when all of these are true: triggered "Submit on" at least once in the last 1 day; triggered "View page" at least 3 times in the last 1 day.

## Step 2: Draft a sales alert

Generate a Slack message to the sales team channel. Say how many users are in "Submitted And Still Engaged" right now, so reps can follow up while the user is still active on the site today. Use the result of "Build the still-engaged submitter list". This drafts the Slack message only; a person on the team still posts it.

## Step 3: Draft a next-step email

Generate a designed marketing email for the users in "Submitted And Still Engaged" confirming their submission and naming the one next step worth taking right now. Three sentences, confident and helpful tone, no discount language, one button linking to that next step. Use the result of "Build the still-engaged submitter list". This drafts the email only; a person still sends it.
