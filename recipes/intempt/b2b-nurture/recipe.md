---
frontmatter_id: b2b-nurture
slash_command: /b2b-nurture
description: Scores inbound leads, emails the sales team each sales-ready lead the moment it qualifies, and sends warm leads
  a nurture email matched to their stage.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores every inbound lead, alerts sales by email when a lead becomes sales-ready, and sends warm leads a nurture
    email.
  parameters:
  - name: hot_threshold
    type: number
    label: Score at or above which a lead is sales-ready
    default: 80
    required: false
  - name: warm_threshold
    type: number
    label: Score at or above which a lead is warm (nurture)
    default: 50
    required: false
  - name: nurture_delay
    type: duration
    label: Wait after the lead form before the nurture email
    default: 2 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the sales team that gets sales-ready leads
    required: true
  requirements:
  - slot: inbound_lead_event
    kind: event
    meaning: A prospect submitted an inbound lead form or requested information
    properties:
    - name: company_size
      type: number
      meaning: Number of employees at the prospect's company
      optional: false
    - name: industry
      type: string
      meaning: Industry of the prospect's company
      optional: true
    - name: intent_score
      type: number
      meaning: Score from 0 to 100 reflecting buying-intent signals
      optional: false
    - name: engagement_count
      type: number
      meaning: Number of engagement actions taken by the prospect
      optional: false
  steps:
  - id: s1
    builds: attribute
    uses:
    - inbound_lead_event
    instruction: 'Build a computed attribute on users named "lead_score", a number from 0 to 100, from the user''s latest
      {inbound_lead_event}. Add up: 40 points when {inbound_lead_event.company_size} is 200 or more, 20 points when it is
      between 50 and 199; 0.4 times {inbound_lead_event.intent_score}; 20 points when {inbound_lead_event.engagement_count}
      is 5 or more, 10 points when it is between 2 and 4. Cap the total at 100. Users who never did {inbound_lead_event} have
      no value.'
  - id: s2
    builds: segment
    uses:
    - s1
    - inbound_lead_event
    - hot_threshold
    dependsOn:
    - s1
    instruction: Build a new segment of users named "Sales-ready leads". A user is in it when their lead_score attribute from
      "Score every lead" is {hot_threshold} or more and they did {inbound_lead_event} at least once in the last 90 days.
  - id: s3
    builds: email
    instruction: 'Write a designed HTML nurture email for warm B2B leads who asked for information but are not ready to buy
      yet. Open by thanking them for getting in touch, share one short customer story showing a measurable result, and offer
      two next steps: read a case study or book a 20-minute call. Friendly, helpful, no discount or pricing language. Subject
      line under 50 characters.'
  - id: s4
    builds: automation
    uses:
    - s2
    - inbound_lead_event
    - alert_recipients
    dependsOn:
    - s2
    instruction: Build an automation that starts when a user enters the segment from "Find sales-ready leads". It emails {alert_recipients}
      one plain-text alert with the user's name, email, lead_score, and {inbound_lead_event.company_size}, {inbound_lead_event.industry}
      and {inbound_lead_event.intent_score} from their latest {inbound_lead_event}, asking a rep to take the lead. Nothing
      is sent to the lead.
  - id: s5
    builds: automation
    uses:
    - s1
    - s3
    - inbound_lead_event
    - warm_threshold
    - hot_threshold
    - nurture_delay
    dependsOn:
    - s1
    - s3
    instruction: Build an automation that starts when a user does {inbound_lead_event}. It waits {nurture_delay}. Then, only
      if the user's lead_score attribute from "Score every lead" is {warm_threshold} or more and below {hot_threshold}, it
      sends the email from "Write the warm-lead nurture email" to the user. Users with a lead_score of {hot_threshold} or
      more, or below {warm_threshold}, get nothing.
---

# B2B lead nurture and routing

Slash command: /b2b-nurture

## Step 1: Score every lead

Build a computed attribute on users named "lead_score", a number from 0 to 100, from the user's latest inbound lead event. Add up: 40 points when company size is 200 or more, 20 points when it is between 50 and 199; 0.4 times intent score; 20 points when engagement count is 5 or more, 10 points when it is between 2 and 4. Cap the total at 100. Users who never did inbound lead event have no value.

## Step 2: Find sales-ready leads

Build a new segment of users named "Sales-ready leads". A user is in it when their lead_score attribute from "Score every lead" is 80 or more and they did inbound lead event at least once in the last 90 days.

## Step 3: Write the warm-lead nurture email

Write a designed HTML nurture email for warm B2B leads who asked for information but are not ready to buy yet. Open by thanking them for getting in touch, share one short customer story showing a measurable result, and offer two next steps: read a case study or book a 20-minute call. Friendly, helpful, no discount or pricing language. Subject line under 50 characters.

## Step 4: Alert sales to each ready lead

Build an automation that starts when a user enters the segment from "Find sales-ready leads". It emails the email addresses of the sales team that gets sales-ready leads one plain-text alert with the user's name, email, lead_score, and company size, industry and intent score from their latest inbound lead event, asking a rep to take the lead. Nothing is sent to the lead.

## Step 5: Nurture the warm leads

Build an automation that starts when a user does inbound lead event. It waits 2 d. Then, only if the user's lead_score attribute from "Score every lead" is 50 or more and below 80, it sends the email from "Write the warm-lead nurture email" to the user. Users with a lead_score of 80 or more, or below 50, get nothing.
