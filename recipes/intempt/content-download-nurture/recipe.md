---
frontmatter_id: content-download-nurture
slash_command: /content-download-nurture
description: Follows a gated download with two more pieces on the same topic and a soft invite, and fast tracks anyone who reads all three.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Sends a three-touch nurture series over two weeks to people who download a gated content piece, and fast-tracks
    those who engage strongly to sales.
  parameters:
  - name: lookback_window
    type: duration
    label: Lookback window for recent downloaders
    default: 30 d
    required: false
  - name: touch_1_delay
    type: duration
    label: Delay before touch 1
    default: 1 d
    required: false
  - name: touch_2_delay
    type: duration
    label: Delay before touch 2
    default: 7 d
    required: false
  - name: touch_3_delay
    type: duration
    label: Delay before touch 3
    default: 14 d
    required: false
  - name: journey_timeout
    type: duration
    label: Journey timeout
    default: 21 d
    required: false
  - name: strong_open_count
    type: number
    label: Emails opened to count as strong engagement
    default: 3
    required: false
  - name: strong_click_count
    type: number
    label: CTA clicks to count as strong engagement
    default: 2
    required: false
  - name: multi_download_threshold
    type: number
    label: Downloads that flag a multi-download user
    default: 3
    required: false
  - name: marketing_sender
    type: string
    label: Sender for touches 1 and 2 (marketing)
    default: marketing@
    required: false
  - name: sales_sender
    type: string
    label: Sender for touch 3 (sales)
    default: sales@
    required: false
  requirements:
  - slot: content_download_event
    kind: event
    meaning: A customer submitted the gated content download form
    properties:
    - name: form_type
      type: string
      meaning: Type of form submitted, here content_download
      optional: false
    - name: content_topic
      type: string
      meaning: Topic of the downloaded content
      optional: false
    - name: content_title
      type: string
      meaning: Title of the downloaded content piece
      optional: true
  - slot: paying_customer_segment
    kind: segment
    meaning: Users who are already paying customers
  - slot: open_deal_segment
    kind: segment
    meaning: Users who have an open deal
  - slot: meeting_scheduled_event
    kind: event
    meaning: A customer scheduled a meeting
  - slot: deal_created_event
    kind: event
    meaning: A deal was created for a customer
  - slot: email_channel
    kind: destination
    meaning: Email sending channel for nurture emails
    channel: email
  - slot: sdr_task_destination
    kind: destination
    meaning: Task queue for sales development reps to follow up on high-intent leads
    channel: hubspot
  steps:
  - id: s1
    builds: segment
    uses:
    - content_download_event
    - paying_customer_segment
    - open_deal_segment
    - lookback_window
    instruction: Build the segment 'Recent content downloaders - last {lookback_window}' of users who submitted {content_download_event}
      where {content_download_event.form_type} is content_download within the last {lookback_window}, partitioned by {content_download_event.content_topic}
      so each topic gets its own nurture cadence. Exclude users in {paying_customer_segment} and users in {open_deal_segment}.
  - id: s2
    builds: email
    uses:
    - content_download_event
    - touch_1_delay
    - touch_2_delay
    - touch_3_delay
    - marketing_sender
    - sales_sender
    - s1
    instruction: 'For each content topic in the ''Recent content downloaders'' segment, write a three-touch nurture email
      series that is educational first and sales second. Touch 1 (sent {touch_1_delay} after download) thanks the reader for
      downloading {content_download_event.content_title} and offers a related piece of content on the same topic. Touch 2
      (sent {touch_2_delay} after download) shares a customer case study from a similar company or industry where the same
      topic problem was solved with our product. Touch 3 (sent {touch_3_delay} after download) makes a warm call to action:
      invite the reader to see how it works in their context by booking a 30-minute demo or trying it free for 14 days. Send
      touches 1 and 2 from {marketing_sender} and touch 3 from {sales_sender}.'
  - id: s3
    builds: automation
    uses:
    - content_download_event
    - touch_1_delay
    - touch_2_delay
    - touch_3_delay
    - strong_open_count
    - strong_click_count
    - sdr_task_destination
    - meeting_scheduled_event
    - deal_created_event
    - journey_timeout
    - s2
    instruction: 'Build a three-touch journey triggered when {content_download_event} fires. Send the ''Write three emails
      per topic'' touches at {touch_1_delay}, {touch_2_delay} and {touch_3_delay} after the download. Engagement branch: if
      the user opens at least {strong_open_count} of the three emails and clicks at least {strong_click_count} call-to-action
      links, create a follow-up task in {sdr_task_destination} as a high-intent signal and exit the journey. Restart rule:
      if the user downloads another piece of content during the journey, reset the journey to day 1 using the new topic. Exit
      conditions: {meeting_scheduled_event} occurs, {deal_created_event} occurs, or {journey_timeout} elapses.'
  - id: s4
    builds: dashboard
    uses:
    - content_download_event
    - multi_download_threshold
    - meeting_scheduled_event
    - deal_created_event
    - s1
    - s2
    - s3
    instruction: 'Build a content-nurture funnel dashboard showing: content-download volume by {content_download_event.content_topic};
      download-to-meeting conversion rate by topic; email engagement for each touch of the ''Write three emails per topic''
      series; count of users with {multi_download_threshold} or more downloads flagged for SDR fast-tracking; and pipeline
      value from content-sourced deals closed over the longer cycle.'
---

# Content download nurture

Slash command: /content-download-nurture

## Step 1: Find recent downloaders

Build a segment 'Recent content downloaders - last 30 days' capturing users with Form submitted where form_type = content_download in the last 30 days, partitioned by the content_topic (so each topic gets its own nurture cadence). Excludes users who are already paying customers (different motion) and users with an open deal already (don't double-nurture).

## Step 2: Write three emails per topic

Generate 3-touch nurture email content per content topic. Touch 1 (Day 1): 'Thanks for downloading [content title] (here's a related piece you might like') second piece of related content. Touch 2 (Day 7): customer case study from a similar company/industry where the topic problem was solved using your product. Touch 3 (Day 14): warm CTA: 'Want to see how this works in your context? Book a 30-min demo' or 'Try it free for 14 days'. Each email educational-first, sales-second. Send-from: marketing@ for touch 1-2, sales@ or AE for touch 3. Use the result of "Find recent downloaders".

## Step 3: Send on days 1, 7 and 14

Build a 3-touch journey triggered when content_download event fires. Touch 1: Day 1. Touch 2: Day 7. Touch 3: Day 14. Add an engagement branch: if the user engages strongly (opens all 3 emails + clicks 2+ CTAs), fast-track to an SDR task (high-intent signal) and exit journey. If user downloads ANOTHER piece of content during the journey, reset the journey to Day 1 with the new topic (signals deeper exploration, restart the nurture in the new context). Exit conditions: Meeting scheduled, Deal created, or 21-day timeout. Use the result of "Find recent downloaders", "Write three emails per topic".

## Step 4: See which topics make pipeline

Compose a content-nurture funnel dashboard: content-download volume by topic (which topics attract the most downloads: informs content strategy), download-to-meeting conversion rate by topic (which topics actually correlate with sales pipeline: informs which content to produce more of), email engagement per touch, multi-download user count (users downloading 3+ pieces are high-intent signals: flag for SDR fast-tracking), and content-to-deal-closed pipeline value (the longer-cycle proof-of-value). Use the result of "Find recent downloaders", "Write three emails per topic", "Send on days 1, 7 and 14".
