---
frontmatter_id: demo-call-summary-recipe
slash_command: /demo-call-summary-recipe
description: 'Built in Demo call summary recipe: one of nine fixed recipes that summarizes demo meetings.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
visibility: draft
rejected: Its purpose is configuring the Demo meeting type's AI summary fields; meeting and meeting-type setup is not planned
  on Blu.
portable:
  summary: Turns each Demo meeting into structured notes on features shown, questions, objections, decision-makers and next
    steps, plus demo insights.
  parameters:
  - name: meetingTypeName
    type: string
    label: Meeting type name
    default: Demo
    required: false
  - name: notetakerAutojoin
    type: boolean
    label: Require notetaker autojoin on the meeting type
    default: true
    required: false
  - name: dashboardGroupBy
    type: enum
    label: Group dashboard by
    default: rep
    required: false
    options:
    - rep
    - time_period
  - name: timePeriod
    type: duration
    label: Dashboard time window
    default: 30 d
    required: false
  requirements:
  - slot: demo_meeting_type
    kind: event
    meaning: A meeting type named Demo with notetaker autojoin enabled
  - slot: meeting_summary_recipe
    kind: integration
    meaning: An AI meeting summary capability that extracts structured fields from meetings of a given meeting type
    channel: hubspot
  - slot: demo_summaries
    kind: segment
    meaning: Meetings of the Demo meeting type that have structured summaries
  steps:
  - id: s1
    builds: json
    uses:
    - demo_meeting_type
    - meetingTypeName
    - notetakerAutojoin
    instruction: Retrieve the {meetingTypeName} meeting type from the meeting types list. Confirm it exists with notetaker
      autojoin enabled ({notetakerAutojoin}). If it is absent, stop and tell the user to create it first.
  - id: s2
    builds: automation
    uses:
    - s1
    - meeting_summary_recipe
    dependsOn:
    - s1
    instruction: 'Configure the AI summary recipe for the {meetingTypeName} meeting type using the meeting type confirmed
      in "Check the Demo meeting type". Extract these structured fields and use ''not_discussed'' for any field missing from
      the call rather than guessing: (1) Features Demoed: list of product features shown, each with an engagement signal (attendee
      asked questions / silent / pushed back); (2) Questions Asked: list of attendee questions, each with category (capability,
      integration, pricing, security, onboarding, other); (3) Objections: list of objections raised verbatim, each with category
      (price, timing, competition, feature-gap, authority, trust) and resolution status (handled, parked, unresolved); (4)
      Technical Concerns: specific technical questions or blockers such as integrations needed, data residency, SSO, compliance;
      (5) Decision-Maker Signal: whether a decision-maker was on the call and whether they were engaged; (6) Follow-up Requested:
      what the attendee asked for (case study, trial, technical demo, custom proposal, references); (7) Next Step: what was
      agreed.'
  - id: s3
    builds: report
    uses:
    - s1
    - s2
    - demo_summaries
    - timePeriod
    - dashboardGroupBy
    dependsOn:
    - s1
    instruction: 'Compose a demo insights dashboard reading from the structured summaries produced in "Set what the demo summary
      captures", covering the last {timePeriod}. Include: top 10 features by demo frequency (which features sell themselves
      versus need more pitch); top 10 objections by frequency (objection-handling content priorities); decision-maker attendance
      rate (a low percentage signals a multi-threading problem); follow-up-requested distribution (what the market wants);
      and most-asked technical concern categories (product and engineering input). Group the views by {dashboardGroupBy}.'
---

# Demo call summary fields

Slash command: /demo-call-summary-recipe

## Step 1: Check the Demo meeting type

Retrieve the Demo meeting type from the meeting types list. Confirm it exists with notetaker autojoin enabled (True). If it is absent, stop and tell the user to create it first.

## Step 2: Set what the demo summary captures

Configure the AI summary recipe for the Demo meeting type using the meeting type confirmed in "Check the Demo meeting type". Extract these structured fields and use 'not_discussed' for any field missing from the call rather than guessing: (1) Features Demoed: list of product features shown, each with an engagement signal (attendee asked questions / silent / pushed back); (2) Questions Asked: list of attendee questions, each with category (capability, integration, pricing, security, onboarding, other); (3) Objections: list of objections raised verbatim, each with category (price, timing, competition, feature-gap, authority, trust) and resolution status (handled, parked, unresolved); (4) Technical Concerns: specific technical questions or blockers such as integrations needed, data residency, SSO, compliance; (5) Decision-Maker Signal: whether a decision-maker was on the call and whether they were engaged; (6) Follow-up Requested: what the attendee asked for (case study, trial, technical demo, custom proposal, references); (7) Next Step: what was agreed.

## Step 3: Track what demos reveal

Compose a demo insights dashboard reading from the structured summaries produced in "Set what the demo summary captures", covering the last 30 d. Include: top 10 features by demo frequency (which features sell themselves versus need more pitch); top 10 objections by frequency (objection-handling content priorities); decision-maker attendance rate (a low percentage signals a multi-threading problem); follow-up-requested distribution (what the market wants); and most-asked technical concern categories (product and engineering input). Group the views by rep.
