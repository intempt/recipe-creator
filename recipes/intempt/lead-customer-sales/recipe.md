---
frontmatter_id: lead-customer-sales
slash_command: /lead-customer-sales
description: Shows how many demo requests turn into booked meetings, completed demos, proposals and closed deals, and which lead sources actually convert.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows how demo requests progress to booked meetings, completed demos, proposals and closed deals, and which lead
    sources convert best.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 60 d
    required: false
  - name: comparisonPeriod
    type: enum
    label: Comparison period
    default: previous_period
    required: false
    options:
    - previous_period
    - none
  - name: topSources
    type: number
    label: Number of lead sources to break down
    default: 8
    required: false
  - name: deadStageDays
    type: number
    label: Median stage velocity alert threshold (days)
    default: 14
    required: false
  requirements:
  - slot: demo_request_form_event
    kind: event
    meaning: A customer submitted a form, including demo-request forms
    properties:
    - name: form_id
      type: string
      meaning: Identifier of the submitted form, used to match the demo-request form
      optional: false
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a lead or customer user
    properties:
    - name: primary_user_id
      type: string
      meaning: User the meeting is linked to
      optional: true
    - name: user_ids
      type: array
      meaning: Users attached to the meeting
      optional: true
    - name: canceled_at
      type: date
      meaning: Time the meeting was canceled, empty if not canceled
      optional: true
    - name: start_time
      type: date
      meaning: Meeting start time
      optional: false
    - name: end_time
      type: date
      meaning: Meeting end time
      optional: false
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal moved to a different stage in the sales pipeline
    properties:
    - name: previous_stage
      type: string
      meaning: Stage the deal left
      optional: true
    - name: new_stage
      type: string
      meaning: Stage the deal entered, used to match the proposal stage
      optional: false
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked as won (closed customer deal)
    properties:
    - name: amount
      type: number
      meaning: Amount of the won deal
      optional: true
  - slot: deal_created_event
    kind: event
    meaning: A new deal was created, used as an alternative start for the funnel
    properties:
    - name: stage
      type: string
      meaning: Stage the deal was created in, used to match discovery stage
      optional: true
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
    optional: true
  - slot: user_utm_source_attribute
    kind: attribute
    meaning: The first-touch lead source (UTM source) recorded on the user record
  - slot: deal_stage_attribute
    kind: attribute
    meaning: The current sales pipeline stage of a deal
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - demo_request_form_event
    - deal_created_event
    - meeting_scheduled_event
    - deal_stage_changed_event
    - deal_won_event
    - user_utm_source_attribute
    - deal_stage_attribute
    - conversionWindow
    - comparisonPeriod
    - topSources
    - deadStageDays
    instruction: 'Create a funnel report named "Lead to Customer" with these steps in order: 1) {demo_request_form_event}
      where form_id matches the demo-request form (alternative start: {deal_created_event} with stage matching Discovery or
      similar); 2) {meeting_scheduled_event} linked to the same user via primary_user_id or user_ids; 3) {meeting_scheduled_event}
      where canceled_at is empty and end_time is before now, with no later meeting cancellation; 4) {deal_stage_changed_event}
      where new_stage matches a Proposal pattern; 5) {deal_won_event}. Use a conversion window of {conversionWindow}. Break
      down by the {user_utm_source_attribute} attribute and show the top {topSources} sources. Compare against the {comparisonPeriod}
      of equal length. For each step show median time-to-convert from the previous step, per-source conversion rate at each
      stage, and forecast revenue as the sum of amounts for deals currently at that stage (from {deal_stage_attribute} and
      {deal_stage_changed_event.amount}) multiplied by historical conversion-to-won rate. Surface projected closed-won revenue
      for the period from current pipeline volumes. Annotations: flag the source with the highest end-to-end win rate and
      volume as the place to invest more; flag any stage whose median velocity exceeds {deadStageDays} days as a deal-stalled
      signal; highlight any source with rising volume but falling win rate as lead-quality erosion.'
---

# Lead to customer

Slash command: /lead-customer-sales

## Step 1: Trace demo requests to closed deals

Create a Funnel report called "Lead to Customer".
Steps:
1. Event "Form submitted" where form_id matches a demo-request form: "Requested Demo"
 (alternative: Deal created with stage matching "Discovery" or similar)
2. Event "Meeting scheduled" linked to the user (via primary_user_id or user_ids): "Scheduled Demo"
3. Event "Meeting scheduled" where canceled_at is null AND end_time < now (i.e. meeting actually happened, no subsequent meeting_canceled): "Completed Demo"
4. Event "Deal stage changed" where new_stage matches a "Proposal" pattern: "Proposal Sent"
5. Event "Deal won": "Deal Closed"
Conversion window: 60 days
Breakdown: By Users.UTM source attribute (first-touch lead source on the User record). Top 8 sources.
Compare: Previous period (prior 60 days)
For each step, also surface:
- Median time-to-convert from previous step (stage velocity)
- Per-source conversion rate at each stage
- Forecast revenue: Sum of Deal created.amount (or current Deal stage changed.amount) for deals currently at this stage × historical conversion-to-won rate
Annotations:
- Flag the lead source with highest end-to-end win rate AND volume: invest more there.
- Flag any stage where median velocity exceeded 14 days (deal-stalled signal).
- Highlight any source with rising volume but falling win rate (lead-quality erosion).
Surface the projected closed-won revenue for the period based on current pipeline volumes.
Taxonomy notes:
- "demo_requested", "demo_completed", "proposal_sent" as standalone events do not exist. They are derived from Form submitted, Meeting scheduled, and Deal stage changed.new_stage respectively.
- Deal stage changed has previous_stage and new_stage properties; deal stages are project-configured (the Deals object has stage as a relation attribute).
- Meeting scheduled has canceled_at, start_time, end_time: completion is derived from these.
- Users.UTM source is the canonical lead-source User attribute.
