---
frontmatter_id: lead-to-mql-to-sql-funnel
slash_command: /lead-to-mql-to-sql-funnel
description: Shows how leads move through MQL, SQL, demo and closed won, where they stall, and how long the whole cycle takes.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows how leads move from creation through MQL, SQL, demo and closed won, where they stall, and how long the full
    sales cycle takes.
  parameters:
  - name: conversion_window
    type: duration
    label: Conversion window
    default: 90 d
    required: false
  - name: breakdown_top_n
    type: number
    label: Number of top sources to break down by
    default: 6
    required: false
  - name: comparison_period
    type: duration
    label: Comparison period (prior period length)
    default: 90 d
    required: false
  - name: mql_to_sql_threshold
    type: number
    label: MQL-to-SQL conversion flag threshold (%)
    default: 20
    required: false
  - name: sql_to_won_threshold
    type: number
    label: SQL-to-Closed-Won conversion flag threshold (%)
    default: 15
    required: false
  - name: high_volume_end_to_end_threshold
    type: number
    label: High-volume end-to-end conversion threshold (%)
    default: 5
    required: false
  requirements:
  - slot: lead_created_event
    kind: event
    meaning: A new user account was created with UTM source tracking
    properties:
    - name: utm_source
      type: string
      meaning: UTM source recorded on the user
      optional: false
  - slot: lead_stage_changed_event
    kind: event
    meaning: A lead's stage changed to a new lead stage
    properties:
    - name: new_stage
      type: string
      meaning: The lead stage the lead moved into, matched against the configured lead-stage records
      optional: false
    - name: score
      type: number
      meaning: Lead score at the time of the change
      optional: true
    - name: intent_trend
      type: string
      meaning: Direction of buyer intent at the time of the change
      optional: true
    - name: stage_changed_by
      type: string
      meaning: Who or what changed the stage
      optional: true
  - slot: deal_created_event
    kind: event
    meaning: A sales deal was created for a customer
    properties:
    - name: primary_user_id
      type: string
      meaning: Primary user linked to the deal
      optional: true
    - name: user_ids
      type: string
      meaning: User identifiers linked to the deal
      optional: true
  - slot: meeting_scheduled_event
    kind: event
    meaning: A customer meeting was scheduled
    properties:
    - name: canceled_at
      type: date
      meaning: When the meeting was canceled, empty if not canceled
      optional: true
    - name: end_time
      type: date
      meaning: When the meeting ends
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A sales deal was marked closed won
  - slot: lead_stage_configuration
    kind: knowledge
    meaning: The project's configured lead-stage records that define the MQL and SQL boundaries
  - slot: utm_source_user_attribute
    kind: attribute
    meaning: The UTM source recorded on a user, used to break down the funnel by traffic source
  steps:
  - id: s1
    builds: report
    uses:
    - lead_created_event
    - lead_stage_changed_event
    - deal_created_event
    - meeting_scheduled_event
    - deal_won_event
    - lead_stage_configuration
    - utm_source_user_attribute
    - conversion_window
    - breakdown_top_n
    - comparison_period
    - mql_to_sql_threshold
    - sql_to_won_threshold
    - high_volume_end_to_end_threshold
    instruction: 'Create a funnel report named "Lead Qualification Funnel" that tracks leads through five steps in order.
      Step 1 "Lead Created": a {lead_created_event} where {lead_created_event.utm_source} is not empty. Step 2 "Reached MQL":
      a {lead_stage_changed_event} where {lead_stage_changed_event.new_stage} matches the MQL stage in {lead_stage_configuration},
      counting unique users per lead. Step 3 "SQL Created": a {deal_created_event} linked to the user through {deal_created_event.primary_user_id}
      or {deal_created_event.user_ids}. Step 4 "Demo Completed": a {meeting_scheduled_event} where {meeting_scheduled_event.canceled_at}
      is empty and {meeting_scheduled_event.end_time} is before now. Step 5 "Closed Won": a {deal_won_event}. Use a conversion
      window of {conversion_window}. Break down by {utm_source_user_attribute} for the top {breakdown_top_n} sources. Compare
      against the previous {comparison_period}. For each step, show the median time to convert from the previous step, the
      per-source conversion rate at each stage, and stage velocity from Step 1 to Step 5 as full sales-cycle length. Annotate
      the largest stage drop-off. Flag any source where MQL-to-SQL conversion is below {mql_to_sql_threshold}% as a possible
      MQL definition issue. Flag any source where SQL-to-Closed-Won is below {sql_to_won_threshold}% as a deal-execution issue.
      Highlight sources that have high volume and end-to-end conversion above {high_volume_end_to_end_threshold}%. Surface
      the median sales-cycle length and whether it is increasing or decreasing versus the comparison period.'
---

# Lead qualification funnel

Slash command: /lead-to-mql-to-sql-funnel

## Step 1: Track leads through qualification

Create a Funnel report called "Lead Qualification Funnel".
Steps:
1. Event "User created" where Users.UTM source is not empty: "Lead Created"
2. Event "Lead stage changed" where new_stage indicates MQL (lead_stage relation matches MQL stage in the project's lead-stage configuration), aggregation: Count Unique Users per lead: "Reached MQL"
3. Event "Deal created" linked to the user (via primary_user_id or user_ids): "SQL Created"
4. Event "Meeting scheduled" where canceled_at is null AND end_time < now: "Demo Completed"
5. Event "Deal won": "Closed Won"
Conversion window: 90 days
Breakdown: By Users.UTM source (top 6 sources)
Compare: Previous period (prior 90 days)
For each step, also surface:
- Median time-to-convert from previous step
- Per-source conversion rate at each stage
- Stage velocity from Step 1 to Step 5 (full sales-cycle length)
Annotations:
- Flag the largest stage drop-off.
- Flag any source where MQL-to-SQL conversion is below 20% (MQL definition issue for that source).
- Flag any source where SQL-to-Closed-Won is below 15% (deal-execution issue).
- Highlight sources with high volume AND end-to-end conversion >5%.
Surface the median sales-cycle length and whether it's increasing or decreasing.
Taxonomy notes:
- "lead_score" as a property is not canonical. Lead progression is tracked via Lead stage changed events (which include score, intent_trend, stage_changed_by properties). The lead_stage relation on the User points to a configured lead-stage record.
- The MQL/SQL boundary is project-specific; the recipe uses the Lead stage changed.new_stage relation against the project's stage configuration.
