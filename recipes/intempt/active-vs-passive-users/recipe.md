---
frontmatter_id: active-vs-passive-users
slash_command: /active-vs-passive-users
description: Classifies each user as Producer, Consumer, Lurker or Inactive from their event activity, and emails a weekly
  digest of how active users split across these types, with revenue concentration.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Classifies each user as Producer, Consumer, Lurker or Inactive from 30-day activity and emails a weekly digest
    of the split and where revenue comes from.
  parameters:
  - name: producer_click_min
    type: number
    label: Clicks needed for Producer
    default: 10
    required: false
  - name: producer_submit_min
    type: number
    label: Submissions needed for Producer
    default: 1
    required: false
  - name: consumer_session_min
    type: number
    label: Sessions needed for Consumer
    default: 3
    required: false
  - name: consumer_view_min
    type: number
    label: Page views needed for Consumer
    default: 10
    required: false
  - name: consumer_click_max
    type: number
    label: Clicks a Consumer stays under
    default: 5
    required: false
  - name: classification_window
    type: duration
    label: Activity window
    default: 30 d
    required: false
  - name: producer_share_low
    type: number
    label: Producer share that flags risk (%)
    default: 15
    required: false
  - name: revenue_concentration_threshold
    type: number
    label: Producer revenue share that flags concentration (%)
    default: 70
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: click_event
    kind: event
    meaning: A customer clicked on something in the product or site
  - slot: submit_event
    kind: event
    meaning: A customer submitted a form on the site, never a survey or NPS answer
  - slot: view_page_event
    kind: event
    meaning: A customer viewed a page
  - slot: session_start_event
    kind: event
    meaning: A customer started a session
  - slot: revenue_event
    kind: event
    meaning: A customer paid, such as a subscription start or a purchase
    properties:
    - name: amount
      type: number
      meaning: Amount paid
      optional: false
  - slot: user_plan_attribute
    kind: attribute
    meaning: The subscription plan a user is on
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - click_event
    - submit_event
    - view_page_event
    - session_start_event
    - producer_click_min
    - producer_submit_min
    - consumer_session_min
    - consumer_view_min
    - consumer_click_max
    - classification_window
    instruction: 'Build a new attribute on users named "activity_type", counted over the last {classification_window}. Producer:
      at least {producer_click_min} {click_event} and at least {producer_submit_min} {submit_event}. Consumer, when not Producer:
      at least {consumer_session_min} {session_start_event}, at least {consumer_view_min} {view_page_event} and fewer than
      {consumer_click_max} {click_event}. Lurker: at least 1 {session_start_event} and neither Producer nor Consumer. Inactive:
      no {session_start_event}. It refreshes daily.'
  - id: s2
    builds: automation
    uses:
    - s1
    - revenue_event
    - user_plan_attribute
    - classification_window
    - producer_share_low
    - revenue_concentration_threshold
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users by the attribute
      from "Classify users by activity" and writes these figures: users per type now and 7 days ago; each type''s share of
      active users (all but Inactive); the sum of {revenue_event.amount} in the last {classification_window} per type and
      its share of the total; Producer share per {user_plan_attribute}. The first line says so when Producer share is below
      {producer_share_low}%, or when Producers are under 20% of active users but over {revenue_concentration_threshold}% of
      revenue. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else
      is sent.'
---

# Active versus passive users

Slash command: /active-vs-passive-users

## Step 1: Classify users by activity

Build a new attribute on users named "activity_type", counted over the last 30 d. Producer: at least 10 click event and at least 1 submit event. Consumer, when not Producer: at least 3 session start event, at least 10 view page event and fewer than 5 click event. Lurker: at least 1 session start event and neither Producer nor Consumer. Inactive: no session start event. It refreshes daily.

## Step 2: Email the weekly activity digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users by the attribute from "Classify users by activity" and writes these figures: users per type now and 7 days ago; each type's share of active users (all but Inactive); the sum of amount in the last 30 d per type and its share of the total; Producer share per user plan attribute. The first line says so when Producer share is below 15%, or when Producers are under 20% of active users but over 70% of revenue. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
