---
frontmatter_id: email-click-retargeting
slash_command: /email-click-retargeting
description: Treats a click on pricing, a feature page or a case study in a marketing email as interest and sends one follow-up
  on that exact topic, then a soft nudge, at most once a week.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: When a contact clicks a pricing, feature or case-study link in a marketing email, they get one topic-matched follow-up
    email, then a soft nudge, at most once a week.
  parameters:
  - name: first_touch_delay
    type: duration
    label: Delay before first follow-up
    default: 1 d
    required: false
  - name: nudge_delay
    type: duration
    label: Delay before soft nudge
    default: 5 d
    required: false
  - name: throttle_window
    type: duration
    label: At most one follow-up series per user within
    default: 7 d
    required: false
  requirements:
  - slot: email_clicked_event
    kind: event
    meaning: A contact clicked a link in a marketing email
    properties:
    - name: link_topic
      type: string
      meaning: 'Topic of the clicked link: pricing, feature, case_study or other'
      optional: false
    - name: link_url
      type: string
      meaning: URL of the clicked link
      optional: false
  - slot: pricing_page_visited_event
    kind: event
    meaning: A contact visited the pricing page on the website
  - slot: trial_started_event
    kind: event
    meaning: A contact started a free trial
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a contact
  steps:
  - id: s1
    builds: email
    instruction: 'Write a short, low-pressure email for contacts who clicked a pricing link in a marketing email. It reads
      as a continuation: ''You looked at pricing, want to talk it through?'', answers three common pricing questions in one
      line each, and has one button to book a short call. It never says we tracked their click.'
  - id: s2
    builds: email
    instruction: Write a short, educational email for contacts who clicked a feature link in a marketing email. It goes one
      level deeper on what the product's key features do, with a short customer story of a team using them, and one button
      to try it. It never says we tracked their click.
  - id: s3
    builds: email
    instruction: Write a short email for contacts who clicked a case-study link in a marketing email. It offers one more customer
      story with the problem, what they did and the result in three short paragraphs, and one button to read it. It never
      says we tracked their click.
  - id: s4
    builds: email
    instruction: 'Write a two-sentence email for contacts who got a follow-up a few days ago and did not act: a friendly check-in
      with two buttons, book a short chat or start a free trial. No urgency, no discount.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - email_clicked_event
    - pricing_page_visited_event
    - trial_started_event
    - meeting_scheduled_event
    - first_touch_delay
    - nudge_delay
    - throttle_window
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: Build an automation triggered when a user does {email_clicked_event} with {email_clicked_event.link_topic}
      equal to pricing, feature or case_study. It skips users who did {pricing_page_visited_event} or {trial_started_event}
      in the last 14 days or entered it in the last {throttle_window}. After {first_touch_delay} it sends, by {email_clicked_event.link_topic},
      the email from "Write the pricing follow-up", "Write the feature follow-up" or "Write the case-study follow-up". After
      {nudge_delay} more, when they did not do {meeting_scheduled_event} or {trial_started_event}, it sends the email from
      "Write the soft nudge".
---

# Email click follow up

Slash command: /email-click-retargeting

## Step 1: Write the pricing follow-up

Write a short, low-pressure email for contacts who clicked a pricing link in a marketing email. It reads as a continuation: 'You looked at pricing, want to talk it through?', answers three common pricing questions in one line each, and has one button to book a short call. It never says we tracked their click.

## Step 2: Write the feature follow-up

Write a short, educational email for contacts who clicked a feature link in a marketing email. It goes one level deeper on what the product's key features do, with a short customer story of a team using them, and one button to try it. It never says we tracked their click.

## Step 3: Write the case-study follow-up

Write a short email for contacts who clicked a case-study link in a marketing email. It offers one more customer story with the problem, what they did and the result in three short paragraphs, and one button to read it. It never says we tracked their click.

## Step 4: Write the soft nudge

Write a two-sentence email for contacts who got a follow-up a few days ago and did not act: a friendly check-in with two buttons, book a short chat or start a free trial. No urgency, no discount.

## Step 5: Follow up once, nudge once

Build an automation triggered when a user does email clicked event with link topic equal to pricing, feature or case_study. It skips users who did pricing page visited event or trial started event in the last 14 days or entered it in the last 7 d. After 1 d it sends, by link topic, the email from "Write the pricing follow-up", "Write the feature follow-up" or "Write the case-study follow-up". After 5 d more, when they did not do meeting scheduled event or trial started event, it sends the email from "Write the soft nudge".
