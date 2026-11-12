---
frontmatter_id: lead-qualification
slash_command: /lead-qualification
description: Scores inbound leads, sends the sales ready ones round robin to a rep with the context attached, and puts the rest into nurture.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores inbound leads, routes sales-ready leads round robin to a rep with context attached, and places the rest
    into nurture.
  parameters:
  - name: hot_threshold
    type: number
    label: Qualification score at or above which a lead is hot
    required: true
  - name: warm_threshold
    type: number
    label: Qualification score at or above which a lead is warm
    required: true
  - name: nurture_cadence
    type: duration
    label: Cadence between nurture touches
    required: true
  - name: dashboard_window
    type: duration
    label: Reporting window for the handoff dashboard
    default: 30 d
  requirements:
  - slot: inbound_lead_event
    kind: event
    meaning: A prospect submitted an inbound lead form or request
    properties:
    - name: company_size
      type: number
      meaning: Employee count of the prospect's company
      optional: true
    - name: industry
      type: string
      meaning: Industry of the prospect's company
      optional: true
    - name: intent_signal
      type: number
      meaning: Strength of buying intent signal
      optional: true
    - name: engagement_score
      type: number
      meaning: Engagement level of the prospect
      optional: true
  - slot: lead_qualification_attribute
    kind: attribute
    meaning: A lead qualification score combining firmographic fit, intent, and engagement
  - slot: hot_lead_segment
    kind: segment
    meaning: Leads at or above the hot qualification score
  - slot: warm_lead_segment
    kind: segment
    meaning: Leads at or above the warm qualification score and below hot
  - slot: cold_lead_segment
    kind: segment
    meaning: Leads below the warm qualification score
  - slot: sales_rep_team
    kind: integration
    meaning: A sales team whose reps can be assigned leads round robin
    channel: salesforce
  - slot: nurture_journey
    kind: destination
    meaning: An email channel used to send nurture messages to warm and cold leads
    channel: email
  - slot: handoff_dashboard_source
    kind: integration
    meaning: A reporting source tracking lead volume and opportunity conversion
    channel: hubspot
  steps:
  - id: s1
    builds: attribute
    uses:
    - inbound_lead_event
    - lead_qualification_attribute
    instruction: Define {lead_qualification_attribute} as a weighted score combining firmographic fit (from {inbound_lead_event.company_size}
      and {inbound_lead_event.industry}), intent (from {inbound_lead_event.intent_signal}), and engagement (from {inbound_lead_event.engagement_score}).
  - id: s2
    builds: segment
    uses:
    - s1
    - lead_qualification_attribute
    - hot_lead_segment
    - warm_lead_segment
    - cold_lead_segment
    - hot_threshold
    - warm_threshold
    instruction: Create {hot_lead_segment} for leads with {lead_qualification_attribute} at or above {hot_threshold}, {warm_lead_segment}
      for leads at or above {warm_threshold} and below {hot_threshold}, and {cold_lead_segment} for leads below {warm_threshold},
      using the result of "Score every lead".
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - hot_lead_segment
    - sales_rep_team
    instruction: Create a workflow for {hot_lead_segment} that assigns each lead to a sales rep in {sales_rep_team} using
      round-robin within the team, and creates a follow-up task for the rep that includes the lead's qualification context,
      using the results of "Score every lead" and "Split into hot, warm and cold".
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - warm_lead_segment
    - cold_lead_segment
    - nurture_journey
    - nurture_cadence
    instruction: Build a nurture journey for {warm_lead_segment} and {cold_lead_segment} sending messages through {nurture_journey}
      every {nurture_cadence}, using the results of "Score every lead", "Split into hot, warm and cold", and "Route hot leads
      round robin".
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - handoff_dashboard_source
    - dashboard_window
    - lead_qualification_attribute
    instruction: Compose a dashboard over the last {dashboard_window} from {handoff_dashboard_source} showing lead volume,
      distribution of {lead_qualification_attribute}, handoff rate, and conversion to opportunity, using the results of "Score
      every lead", "Split into hot, warm and cold", "Route hot leads round robin", and "Nurture warm and cold leads".
---

# Lead qualification and handoff

Slash command: /lead-qualification

## Step 1: Score every lead

Define a Qualification attribute weighting firmographic fit, intent, and engagement.

## Step 2: Split into hot, warm and cold

Segment leads into hot/warm/cold tiers based on qualification score. Use the result of "Score every lead".

## Step 3: Route hot leads round robin

Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. Use the result of "Score every lead", "Split into hot, warm and cold".

## Step 4: Nurture warm and cold leads

Build nurture journeys for warm and cold leads with appropriate cadence. Use the result of "Score every lead", "Split into hot, warm and cold", "Route hot leads round robin".

## Step 5: Track handoff to opportunity

Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. Use the result of "Score every lead", "Split into hot, warm and cold", "Route hot leads round robin", "Nurture warm and cold leads".
