---
frontmatter_id: post-demo-nurture
slash_command: /post-demo-nurture
description: Keeps a demo warm for 90 days with a playbook, a case study, an ROI calculator and a customer story, and pulls the AE in early if they bite.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Keeps recent demo attendees warm for 90 days with five timed emails (playbook, case study, ROI calculator, customer
    story, AE check-in) and alerts the AE early on buying signals.
  parameters:
  - name: demo_window
    type: duration
    label: Lookback window for recent demo attendees
    default: 90 d
    required: false
  - name: high_engagement_touches
    type: text
    label: Touches whose clicks trigger AE outreach
    default: touch 1 or touch 2
    required: false
  - name: reply_rate_flag_threshold
    type: number
    label: Reply rate below which a touch is flagged (%)
    default: 1
    required: false
  - name: nurture_length
    type: duration
    label: Total nurture length
    default: 90 d
    required: false
  requirements:
  - slot: demo_meeting_event
    kind: event
    meaning: A customer completed a meeting, with meeting type and attendance recorded
    properties:
    - name: meeting_type
      type: string
      meaning: Type of meeting, such as demo
      optional: false
    - name: attendance
      type: boolean
      meaning: Whether the prospect attended
      optional: false
    - name: meeting_summary
      type: text
      meaning: Notes summarizing the demo discussion and signals
      optional: true
  - slot: deal_won_status
    kind: attribute
    meaning: Whether the customer has a deal won
  - slot: active_deal_cadence_segment
    kind: segment
    meaning: Customers already in active deal-stage cadences handled by an account executive
    optional: true
  - slot: email_sending_integration
    kind: integration
    meaning: An email marketing platform connected to send the nurture emails
    channel: email
  - slot: ae_task_destination
    kind: destination
    meaning: A place where account executive outreach tasks are created
    optional: true
    channel: hubspot
  - slot: post_demo_segment
    kind: segment
    meaning: Recent demo attendees with no won deal, created by this recipe
    creatable: true
    optional: true
    definition: users who completed a {demo_meeting_event} with meeting_type demo and attendance true within {demo_window},
      and no {deal_won_status}, excluding users in {active_deal_cadence_segment}
  - slot: case_study_library
    kind: knowledge
    meaning: Collection of playbooks, case studies, ROI calculator, and customer stories to reference in emails
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - demo_meeting_event
    - deal_won_status
    - active_deal_cadence_segment
    - demo_window
    - post_demo_segment
    instruction: Build the segment {post_demo_segment} of users who completed a {demo_meeting_event} with meeting_type demo
      and attendance true within {demo_window}, with no {deal_won_status}, excluding anyone in {active_deal_cadence_segment}
      since the account executive handles those manually.
  - id: s2
    builds: email
    uses:
    - s1
    - case_study_library
    - demo_meeting_event
    - nurture_length
    instruction: 'Write a five-touch post-demo email sequence for the segment from "Find recent demo attendees", spread across
      {nurture_length}. Touch 1 (Day 7): value content, a playbook or guide directly relevant to the use case discussed in
      the demo. Touch 2 (Day 14): a case study matching the prospect''s industry and company size. Touch 3 (Day 30): an ROI
      calculator link with the prospect''s discussed metrics pre-filled where possible. Touch 4 (Day 60): a customer story
      (video or article) showing six-month outcomes from a similar customer. Touch 5 (Day 90): a decision-stage check-in from
      the account executive asking direct, low-pressure questions about timing, budget and champion status. Personalize each
      email using meeting_summary signals from the original demo. Use {case_study_library} for assets.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - demo_meeting_event
    - high_engagement_touches
    - nurture_length
    - ae_task_destination
    instruction: 'Build a five-touch journey for {post_demo_segment}, sending touch 1 from "Write five follow ups" at Day
      7, touch 2 at Day 14, touch 3 at Day 30, touch 4 at Day 60 and touch 5 at Day 90, all counted from the demo meeting
      completion on {demo_meeting_event}. Add a high-engagement branch: if the prospect clicks {high_engagement_touches},
      create an account executive outreach task in {ae_task_destination} and stop the automated cadence for that prospect.
      Exit the journey when a deal is created, when a meeting is scheduled (re-engagement), or when the prospect unsubscribes.'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - reply_rate_flag_threshold
    instruction: Create a dashboard tracking post-demo nurture conversion for {post_demo_segment}, showing demo-to-deal conversion
      rate at 60 days and 90 days, drop-off by touch from "Write five follow ups" to show which touches lose the most attention,
      the count of account executive handoffs triggered by the high-engagement branch in "Send over 90 days", and deal velocity
      compared between demos that went through the cadence and those that did not. Flag any touch with a reply rate below
      {reply_rate_flag_threshold} percent as a content failure signal.
---

# Post demo nurture

Slash command: /post-demo-nurture

## Step 1: Find recent demo attendees

Build a segment 'Recent demo attendees - last 90 days' capturing users with a meeting_completed event where meeting_type = demo in the last 90 days, attendance = true, and no deal won yet. Excludes users already in active deal-stage cadences (handled by AE manually).

## Step 2: Write five follow ups

This step builds a designed marketing email (HTML).
Generate 5-touch post-demo content. Touch 1 (Day 7): value content - a playbook or guide directly relevant to use case discussed in demo. Touch 2 (Day 14): case study matching the prospect's industry + company size. Touch 3 (Day 30): ROI calculator link with prospect's discussed metrics pre-filled where possible. Touch 4 (Day 60): customer story (video or article) showing 6-month outcomes from a similar customer. Touch 5 (Day 90): decision-stage check-in from the AE asking direct, low-pressure questions about timing/budget/champion status. Personalize using meeting_summary signals from the original demo. Use the result of "Find recent demo attendees".

## Step 3: Send over 90 days

Build a 5-touch journey wired to the post-demo segment: touch 1 at Day 7, touch 2 at Day 14, touch 3 at Day 30, touch 4 at Day 60, touch 5 at Day 90, all relative to meeting_completed. Add a high-engagement branch: if the prospect clicks on touch 1 or 2, route to a dedicated AE-outreach task instead of continuing the automated cadence (signal of buying intent). Exit conditions: Deal created, Meeting scheduled (re-engagement), or unsubscribe. Use the result of "Find recent demo attendees", "Write five follow ups".

## Step 4: Track demo to deal

Compose a dashboard tracking post-demo nurture conversion: demo-to-deal conversion rate (60d, 90d), drop-off by touch (which touches lose the most attention), AE-outreach handoffs triggered (count of high-engagement branches), and deal-velocity comparison between demos that went through the cadence vs not. Flag touches with reply rate below 1% (content failure signal). Use the result of "Find recent demo attendees", "Write five follow ups", "Send over 90 days".
