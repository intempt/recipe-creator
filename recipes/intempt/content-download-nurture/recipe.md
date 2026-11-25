---
frontmatter_id: content-download-nurture
slash_command: /content-download-nurture
description: Follows a gated content download with a related piece, a customer story and a soft demo invite over two weeks,
  and alerts sales when someone downloads several pieces.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Sends people who download gated content a three-email nurture over two weeks and alerts sales about repeat downloaders.
  parameters:
  - name: lookback_window
    type: duration
    label: Lookback window for recent downloaders
    default: 30 d
    required: false
  - name: touch_1_delay
    type: duration
    label: Wait after entering before email 1
    default: 1 d
    required: false
  - name: touch_2_delay
    type: duration
    label: Wait after email 1 before email 2
    default: 6 d
    required: false
  - name: touch_3_delay
    type: duration
    label: Wait after email 2 before email 3
    default: 7 d
    required: false
  - name: multi_download_threshold
    type: number
    label: Downloads that make someone a repeat downloader
    default: 3
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the sales team alerted about repeat downloaders
    required: true
  requirements:
  - slot: content_download_event
    kind: event
    meaning: A person submitted a gated content download form
    properties:
    - name: content_topic
      type: string
      meaning: Topic of the downloaded content
      optional: false
    - name: content_title
      type: string
      meaning: Title of the downloaded content piece
      optional: true
  - slot: plan
    kind: attribute
    meaning: The user's current plan, empty or free/trial when they are not paying
  - slot: meeting_scheduled_event
    kind: event
    meaning: A person scheduled a meeting with sales
  - slot: deal_created_event
    kind: event
    meaning: A deal was created for a person
  steps:
  - id: s1
    builds: segment
    uses:
    - content_download_event
    - plan
    - deal_created_event
    - lookback_window
    instruction: Build a new segment of users named "Recent content downloaders". A user is in it when they did {content_download_event}
      at least once in the last {lookback_window}, they did not do {deal_created_event} at any time, and their {plan} attribute
      is empty, free or trial.
  - id: s2
    builds: email
    uses:
    - s1
    - content_download_event
    dependsOn:
    - s1
    instruction: Write a designed HTML email for users in the segment from "Find recent downloaders". Thank them for downloading
      {content_download_event.content_title} and suggest one more read on the same topic, {content_download_event.content_topic},
      with one button to the resources page. Educational, no sales ask.
  - id: s3
    builds: email
    uses:
    - s1
    - content_download_event
    dependsOn:
    - s1
    instruction: Write a designed HTML email for users in the segment from "Find recent downloaders". Share one short customer
      story about a company that solved a problem on the topic {content_download_event.content_topic} with our product, with
      the result in one line and one button to read the full story. Helpful, light on selling.
  - id: s4
    builds: email
    uses:
    - s1
    - content_download_event
    dependsOn:
    - s1
    instruction: Write a designed HTML email for users in the segment from "Find recent downloaders". Invite them to see how
      the ideas on {content_download_event.content_topic} would work for their team in a 30-minute demo, with one button to
      book it. Warm, low pressure, no pricing.
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - touch_1_delay
    - touch_2_delay
    - touch_3_delay
    - meeting_scheduled_event
    - deal_created_event
    - content_download_event
    - multi_download_threshold
    - lookback_window
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: 'Build an automation that starts when a user enters the segment from "Find recent downloaders". It waits
      {touch_1_delay} and sends the email from "Write email 1: a related piece", waits {touch_2_delay} and sends the email
      from "Write email 2: a customer story", waits {touch_3_delay} and sends the email from "Write email 3: a soft demo invite".
      Before each send it stops if the user did {meeting_scheduled_event} or {deal_created_event} since entering. When the
      user has done {content_download_event} {multi_download_threshold} or more times in the last {lookback_window}, it emails
      {alert_recipients} once with their name, email and the topics they downloaded.'
---

# Content download nurture

Slash command: /content-download-nurture

## Step 1: Find recent downloaders

Build a new segment of users named "Recent content downloaders". A user is in it when they did content download event at least once in the last 30 d, they did not do deal created event at any time, and their plan attribute is empty, free or trial.

## Step 2: Write email 1: a related piece

Write a designed HTML email for users in the segment from "Find recent downloaders". Thank them for downloading content title and suggest one more read on the same topic, content topic, with one button to the resources page. Educational, no sales ask.

## Step 3: Write email 2: a customer story

Write a designed HTML email for users in the segment from "Find recent downloaders". Share one short customer story about a company that solved a problem on the topic content topic with our product, with the result in one line and one button to read the full story. Helpful, light on selling.

## Step 4: Write email 3: a soft demo invite

Write a designed HTML email for users in the segment from "Find recent downloaders". Invite them to see how the ideas on content topic would work for their team in a 30-minute demo, with one button to book it. Warm, low pressure, no pricing.

## Step 5: Send on days 1, 7 and 14

Build an automation that starts when a user enters the segment from "Find recent downloaders". It waits 1 d and sends the email from "Write email 1: a related piece", waits 6 d and sends the email from "Write email 2: a customer story", waits 7 d and sends the email from "Write email 3: a soft demo invite". Before each send it stops if the user did meeting scheduled event or deal created event since entering. When the user has done content download event 3 or more times in the last 30 d, it emails the email addresses of the sales team alerted about repeat downloaders once with their name, email and the topics they downloaded.
