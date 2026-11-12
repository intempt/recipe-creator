---
frontmatter_id: b2b-nurture
slash_command: /b2b-nurture
description: Scores inbound leads, hands the sales ready ones to a rep with an owner and a task, and keeps the rest warm with content matched to how close they are.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores inbound leads, routes sales-ready leads to a rep with an owner and task, and keeps other leads warm with
    content matched to their stage.
  parameters:
  - name: hot_threshold
    type: number
    label: Score at or above which a lead is hot (sales-ready)
    default: 80
    required: false
  - name: warm_threshold
    type: number
    label: Score at or above which a lead is warm (nurture)
    default: 50
    required: false
  - name: nurture_cadence
    type: duration
    label: Interval between nurture emails
    default: 7 d
    required: false
  - name: dashboard_window
    type: duration
    label: Reporting window for handoff and conversion metrics
    default: 30 d
    required: false
  requirements:
  - slot: inbound_lead_event
    kind: event
    meaning: A prospect submitted an inbound lead form or requested information
    properties:
    - name: company_size
      type: number
      meaning: Number of employees at the prospect's company
      optional: true
    - name: industry
      type: string
      meaning: Industry of the prospect's company
      optional: true
    - name: intent_score
      type: number
      meaning: Score reflecting buying-intent signals
      optional: true
    - name: engagement_count
      type: number
      meaning: Number of engagement actions taken by the prospect
      optional: true
  - slot: lead_score_attribute
    kind: attribute
    meaning: A user attribute holding the qualification score of a lead
  - slot: lead_stage_segment
    kind: segment
    meaning: Leads grouped by score into hot, warm and cold buckets
    creatable: true
    definition: users whose lead score is at or above {hot_threshold} (hot), between {warm_threshold} and {hot_threshold}
      (warm), or below {warm_threshold} (cold)
  - slot: sales_team_owner
    kind: integration
    meaning: A CRM connection that can assign an owner and create tasks for sales reps
    channel: hubspot
  - slot: marketing_email_channel
    kind: destination
    meaning: An email channel used to send nurture messages
    channel: email
  steps:
  - id: s1
    builds: attribute
    uses:
    - inbound_lead_event
    - lead_score_attribute
    instruction: Define a qualification score attribute on {lead_score_attribute} that weights firmographic fit (from {inbound_lead_event.company_size}
      and {inbound_lead_event.industry}), intent signals (from {inbound_lead_event.intent_score}), and engagement depth (from
      {inbound_lead_event.engagement_count}).
  - id: s2
    builds: segment
    uses:
    - lead_score_attribute
    - lead_stage_segment
    - hot_threshold
    - warm_threshold
    instruction: 'Split leads into three segments on {lead_stage_segment}: hot (score at or above {hot_threshold}, sales-ready),
      warm (score from {warm_threshold} up to {hot_threshold}, nurture), and cold (score below {warm_threshold}, long-cycle).
      Use the scores from "Score every lead".'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - sales_team_owner
    - marketing_email_channel
    - nurture_cadence
    instruction: Create a workflow that routes hot leads from the "Split into hot, warm and cold" segment to sales by assigning
      an owner and creating a follow-up task in {sales_team_owner}. Add warm and cold leads to nurture journeys on {marketing_email_channel}
      at a {nurture_cadence} interval.
  - id: s4
    builds: email
    uses:
    - s1
    - s2
    - s3
    instruction: 'Write a designed HTML email for each bucket from "Split into hot, warm and cold": hot leads get a demo offer;
      warm leads get case studies and an ROI calculator; cold leads get educational content. Base the tailoring on the scores
      from "Score every lead" and the routing from "Hand hot leads to a rep".'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - nurture_cadence
    instruction: Build a nurture journey for each segment from "Split into hot, warm and cold" with content from "Write content
      for each bucket", sending at a {nurture_cadence} interval and matching cadence to how close each bucket is to buying.
  - id: s6
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - dashboard_window
    instruction: Create a dashboard over the last {dashboard_window} showing score distribution from "Score every lead", hot-lead
      handoff rate from "Hand hot leads to a rep", and nurture-to-MQL conversion from "Nurture at the right pace".
---

# B2B lead nurture and routing

Slash command: /b2b-nurture

## Step 1: Score every lead

Define a Qualification scoring attribute weighting firmographic fit, intent signals, and engagement depth.

## Step 2: Split into hot, warm and cold

Segment leads into hot (sales-ready), warm (nurture), and cold (long-cycle) buckets based on score. Use the result of "Score every lead".

## Step 3: Hand hot leads to a rep

Create a workflow routing hot leads to sales (assign owner, create task) and adding warm/cold leads to nurture journeys. Use the result of "Score every lead", "Split into hot, warm and cold".

## Step 4: Write content for each bucket

This step builds a designed marketing email (HTML).
Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc, cold=education content. Use the result of "Score every lead", "Split into hot, warm and cold", "Hand hot leads to a rep".

## Step 5: Nurture at the right pace

Build per-segment nurture journeys with appropriate cadence and content. Use the result of "Score every lead", "Split into hot, warm and cold", "Hand hot leads to a rep", "Write content for each bucket".

## Step 6: Track handoffs and conversion

Compose a dashboard tracking score distribution, hot-lead handoff rate, and nurture-to-MQL conversion. Use the result of "Score every lead", "Split into hot, warm and cold", "Hand hot leads to a rep", "Write content for each bucket", "Nurture at the right pace".
