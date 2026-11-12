---
frontmatter_id: email-click-retargeting
slash_command: /email-click-retargeting
description: Treats a click on pricing, a feature page or a case study as interest and sends more on that exact topic, at most once a week.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: When a contact clicks a pricing, feature or case-study link in a marketing email, they get one topic-matched follow-up,
    then a soft nudge, at most once a week.
  parameters:
  - name: lookback_window
    type: duration
    label: Click lookback window
    default: 14 d
    required: false
  - name: journey_timeout
    type: duration
    label: Journey timeout
    default: 10 d
    required: false
  - name: first_touch_delay
    type: duration
    label: Delay before first follow-up
    default: 1 d
    required: false
  - name: nudge_delay
    type: duration
    label: Delay before soft call-to-action nudge
    default: 5 d
    required: false
  - name: throttle_window
    type: duration
    label: Maximum one journey entry per user within
    default: 7 d
    required: false
  - name: sender_address
    type: enum
    label: Sender address for follow-ups
    default: marketing
    options:
    - marketing
    - original_sender
  requirements:
  - slot: email_clicked_event
    kind: event
    meaning: A contact clicked a link in a marketing email
    properties:
    - name: link_topic
      type: enum
      meaning: 'Topic of the clicked link: pricing, feature, case_study, blog, integration, or generic'
      optional: false
    - name: link_url
      type: string
      meaning: URL of the clicked link
      optional: true
  - slot: click_topics_attribute
    kind: attribute
    meaning: A contact's recent email click topics ranked by click count
  - slot: pricing_page_visited_event
    kind: event
    meaning: A contact visited the pricing page on the website
    optional: true
  - slot: trial_started_event
    kind: event
    meaning: A contact started a free trial
    optional: true
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a contact
  - slot: deal_created_event
    kind: event
    meaning: A deal was created for a contact
  - slot: email_channel
    kind: destination
    meaning: Email channel used to send marketing follow-ups
    channel: email
  steps:
  - id: s1
    builds: attribute
    uses:
    - email_clicked_event
    - lookback_window
    - click_topics_attribute
    instruction: Create an AI-derived attribute named 'recent_click_topics' on the contact record. Using {email_clicked_event}
      events from the last {lookback_window}, classify each clicked link by topic (pricing, feature, case study, blog, integration).
      Output a ranked list of topics by click count, highest first. Treat each click as a signal of interest and log it for
      use in later steps.
  - id: s2
    builds: segment
    uses:
    - s1
    - email_clicked_event
    - pricing_page_visited_event
    - trial_started_event
    - lookback_window
    instruction: Build a segment named 'Recent email clickers' containing contacts with {email_clicked_event} in the last
      {lookback_window} where link_topic is pricing, feature, or case_study. Exclude generic links such as view-in-browser
      or footer links. Partition the segment by the topic from 'Log what they clicked'. Exclude contacts who already visited
      {pricing_page_visited_event} or started {trial_started_event}, since they receive other journeys.
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - sender_address
    instruction: 'Write one follow-up email per topic for the segment in ''Find the meaningful clicks''. Pricing click: ''You
      looked at pricing: want to talk it through? Or here''s a pricing FAQ.'' Feature click: a deeper dive on the clicked
      feature with a customer story that uses it. Case-study click: a related case study from a similar company or industry.
      Each email is low-pressure and educational, and reads as a continuation of the conversation rather than as surveillance.
      Send from {sender_address}.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - email_clicked_event
    - meeting_scheduled_event
    - deal_created_event
    - first_touch_delay
    - nudge_delay
    - journey_timeout
    - throttle_window
    - email_channel
    instruction: 'Build a two-touch journey that starts when {email_clicked_event} fires on a pricing, feature, or case_study
      link. Touch 1 after {first_touch_delay}: send the topic-matched email from ''Write one follow-up email per topic''.
      Touch 2 after {nudge_delay}: if the contact has not engaged further, send a soft call to action (book a chat, try free,
      or talk to an account executive depending on company size). If the contact clicks a link during the journey, restart
      with a fresh topic-matched sequence. Exit when {meeting_scheduled_event} or {deal_created_event} fires, or after {journey_timeout}.
      Enforce a throttle so a contact enters this journey at most once per {throttle_window}.'
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - meeting_scheduled_event
    - deal_created_event
    instruction: Create a dashboard named 'Click retargeting performance'. Show retargeting trigger volume by click topic,
      follow-up engagement rate compared with the original email engagement rate, click-to-meeting conversion rate, and click-to-deal
      conversion rate. Include a chart comparing conversion rate of retargeted contacts against a control group of contacts
      who clicked but received no retargeting.
---

# Email click follow up

Slash command: /email-click-retargeting

## Step 1: Log what they clicked

Create an AI-derived attribute 'recent_click_topics' on the User object. Capture: links clicked in marketing emails in the last 14 days, classified by topic (pricing / feature-X / case-study / blog / integration). Output: ranked list of top topics by click count. The clicker is showing you what they care about: log it and act on it.

## Step 2: Find the meaningful clicks

Build a segment 'Recent email clickers - last 14 days' capturing users with Email clicked event in the last 14 days where the click was on a high-signal link (pricing, feature page, case study, not generic 'view in browser' or footer). Partitioned by click_topic. Excludes users who already engaged downstream (e.g. visited pricing page, started trial, those are getting other journeys). Use the result of "Log what they clicked".

## Step 3: Write a reply per topic

Generate retargeting email content per click topic. Pricing-page click: 'You looked at pricing: want to talk it through? Or here's a pricing FAQ.' Feature-X click: deeper dive on feature X with a customer story using it. Case-study click: related case study from a similar company/industry. Each: low-pressure, educational, treats the click as continued conversation not aggressive 'we saw you!' creepiness. Send-from: marketing@ or the original email's sender. Use the result of "Log what they clicked", "Find the meaningful clicks".

## Step 4: Follow up once, nudge once

Build a 2-touch journey triggered when Email clicked fires on a high-signal link. Touch 1 (Day 1): topic-matched follow-up. Touch 2 (Day 5): if no further engagement, offer a soft CTA (book a chat / try free / talk to AE based on company size). If user clicks something during this journey, reset to a fresh topic-matched cadence. Exit on: Meeting scheduled, Deal created, or 10-day timeout. Throttle hard: never trigger this journey more than once per week per user: clicks happen constantly, don't bombard. Use the result of "Log what they clicked", "Find the meaningful clicks", "Write a reply per topic".

## Step 5: Compare against no follow up

Compose a click-retargeting dashboard: retargeting trigger volume by click topic, follow-up engagement rate (do retargeting emails get higher engagement than the original: they should: matched intent), click-to-meeting conversion rate, click-to-deal conversion rate. The killer chart: compare conversion rate of click-retargeted users vs. control (users who clicked but received no retargeting): typically retargeting drives 2-3x higher conversion. Surfaces evidence of behavioral-nurture value. Use the result of "Log what they clicked", "Find the meaningful clicks", "Write a reply per topic", "Follow up once, nudge once".
