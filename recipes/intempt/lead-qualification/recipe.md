---
frontmatter_id: lead-qualification
slash_command: /lead-qualification
description: Scores inbound leads, emails each sales ready one to the sales team with its context attached, and puts warm
  leads into a two-email nurture.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores inbound leads, emails sales-ready ones with context to the sales team, and nurtures warm leads with two
    emails.
  parameters:
  - name: hot_threshold
    type: number
    label: Score at or above which a lead is sales-ready
    default: 75
    required: false
  - name: warm_threshold
    type: number
    label: Score at or above which a lead is warm
    default: 40
    required: false
  - name: nurture_cadence
    type: duration
    label: Wait between the nurture emails
    default: 7 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the sales team that gets sales-ready leads
    required: true
  requirements:
  - slot: inbound_lead_event
    kind: event
    meaning: A prospect submitted an inbound lead form or request
    properties:
    - name: company_size
      type: number
      meaning: Number of employees at the prospect's company
      optional: false
    - name: industry
      type: string
      meaning: Industry of the prospect's company
      optional: true
    - name: intent_signal
      type: string
      meaning: 'What the prospect asked for: demo, pricing, trial or content'
      optional: false
    - name: engagement_score
      type: number
      meaning: Engagement score from 0 to 100
      optional: false
  steps:
  - id: s1
    builds: attribute
    uses:
    - inbound_lead_event
    instruction: 'Build a computed attribute on users named "lead_qualification_score", a number from 0 to 100, from the user''s
      latest {inbound_lead_event}. Add up: 35 points when {inbound_lead_event.company_size} is 200 or more, 15 points when
      it is between 50 and 199; 35 points when {inbound_lead_event.intent_signal} is demo or pricing, 15 points when it is
      trial; 0.3 times {inbound_lead_event.engagement_score}. Cap the total at 100. Users who never did {inbound_lead_event}
      have no value.'
  - id: s2
    builds: segment
    uses:
    - s1
    - inbound_lead_event
    - hot_threshold
    dependsOn:
    - s1
    instruction: Build a new segment of users named "Sales-ready leads". A user is in it when their lead_qualification_score
      attribute from "Score every lead" is {hot_threshold} or more and they did {inbound_lead_event} at least once in the
      last 90 days.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - inbound_lead_event
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: Build an automation that starts when a user enters the segment from "Find sales-ready leads". It emails {alert_recipients}
      one plain-text alert with the user's name, email, lead_qualification_score from "Score every lead", and {inbound_lead_event.company_size},
      {inbound_lead_event.industry} and {inbound_lead_event.intent_signal} from their latest {inbound_lead_event}, asking
      the next rep in turn to take the lead. Nothing is sent to the lead.
  - id: s4
    builds: email
    instruction: Write a designed HTML nurture email for warm B2B leads who are not ready to buy yet. Share one practical
      tip and one short customer story with a measurable result, with one button to a case study and a soft offer to book
      a 20-minute call. Helpful, no pricing or discount language.
  - id: s5
    builds: automation
    uses:
    - s1
    - s4
    - inbound_lead_event
    - warm_threshold
    - hot_threshold
    - nurture_cadence
    dependsOn:
    - s1
    - s4
    instruction: Build an automation that starts when a user does {inbound_lead_event}. It waits {nurture_cadence}. Then,
      only if the user's lead_qualification_score attribute from "Score every lead" is {warm_threshold} or more and below
      {hot_threshold}, it sends the email from "Write the nurture emails" to the user. Users with a score of {hot_threshold}
      or more, or below {warm_threshold}, get nothing.
---

# Lead qualification and handoff

Slash command: /lead-qualification

## Step 1: Score every lead

Build a computed attribute on users named "lead_qualification_score", a number from 0 to 100, from the user's latest inbound lead event. Add up: 35 points when company size is 200 or more, 15 points when it is between 50 and 199; 35 points when intent signal is demo or pricing, 15 points when it is trial; 0.3 times engagement score. Cap the total at 100. Users who never did inbound lead event have no value.

## Step 2: Find sales-ready leads

Build a new segment of users named "Sales-ready leads". A user is in it when their lead_qualification_score attribute from "Score every lead" is 75 or more and they did inbound lead event at least once in the last 90 days.

## Step 3: Route hot leads to sales

Build an automation that starts when a user enters the segment from "Find sales-ready leads". It emails the email addresses of the sales team that gets sales-ready leads one plain-text alert with the user's name, email, lead_qualification_score from "Score every lead", and company size, industry and intent signal from their latest inbound lead event, asking the next rep in turn to take the lead. Nothing is sent to the lead.

## Step 4: Write the nurture emails

Write a designed HTML nurture email for warm B2B leads who are not ready to buy yet. Share one practical tip and one short customer story with a measurable result, with one button to a case study and a soft offer to book a 20-minute call. Helpful, no pricing or discount language.

## Step 5: Nurture warm and cold leads

Build an automation that starts when a user does inbound lead event. It waits 7 d. Then, only if the user's lead_qualification_score attribute from "Score every lead" is 40 or more and below 75, it sends the email from "Write the nurture emails" to the user. Users with a score of 75 or more, or below 40, get nothing.
