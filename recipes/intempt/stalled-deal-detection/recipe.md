---
frontmatter_id: stalled-deal-detection
slash_command: /stalled-deal-detection
description: Finds deals sitting in a stage far longer than usual with no activity, emails the rep a nudge draft that fits
  the stage, escalates to the manager if they stay stuck, and emails a weekly stalled-deal digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds contacts on deals stuck in one stage with no activity, emails the rep a stage-fitting nudge draft, escalates
    if still stuck and sends a weekly digest.
  parameters:
  - name: stage_age_days
    type: number
    label: Days in the same stage after which a deal counts as stuck
    default: 30
    required: false
  - name: inactivity_window
    type: duration
    label: Window with no activity
    default: 14 d
    required: false
  - name: escalation_delay
    type: duration
    label: Wait before escalating to the manager
    default: 14 d
    required: false
  - name: nudge_tone
    type: enum
    label: Nudge tone
    default: direct
    required: false
    options:
    - direct
    - friendly
    - formal
  - name: rep_recipients
    type: string
    label: Email addresses of the reps who get nudge drafts
    required: true
  - name: manager_recipients
    type: string
    label: Email addresses of the sales managers who get escalations
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_stage_changed
    kind: event
    meaning: A deal the contact is on moved to a new pipeline stage
    properties:
    - name: stage
      type: string
      meaning: The stage the deal moved into, such as discovery, demo, proposal, closing, won or lost
      optional: false
    - name: value
      type: number
      meaning: Deal value
      optional: true
    - name: owner
      type: string
      meaning: Rep who owns the deal
      optional: true
  - slot: activity_event
    kind: event
    meaning: A customer or rep interaction on the deal, such as a meeting, email reply or completed task
  - slot: deal_paused
    kind: attribute
    meaning: User attribute that is true when the rep paused the deal on purpose
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - deal_stage_changed
    - activity_event
    - deal_paused
    - stage_age_days
    - inactivity_window
    instruction: 'Build a new segment of users named "Contacts on stalled deals". A user is in it when all of these are true:
      their latest {deal_stage_changed} happened more than {stage_age_days} days ago; in it {deal_stage_changed.stage} is
      not won or lost; they did not do {activity_event} in the last {inactivity_window}; their {deal_paused} attribute is
      not true.'
  - id: s2
    builds: automation
    uses:
    - s1
    - deal_stage_changed
    - nudge_tone
    - escalation_delay
    - rep_recipients
    - manager_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that starts when a user enters the segment from "Find the genuinely stuck ones". It
      writes a short re-engagement email draft in a {nudge_tone}, low-pressure tone that fits {deal_stage_changed.stage}:
      discovery re-asks the open qualifying question, demo offers a technical deep-dive, proposal offers to align with the
      decision-maker, closing asks plainly about timeline and blockers. It emails {rep_recipients} the contact''s name, email,
      {deal_stage_changed.owner}, {deal_stage_changed.stage}, {deal_stage_changed.value} and that draft to review and send
      themselves. It waits {escalation_delay}; if the user is still in the segment, it emails {manager_recipients} the same
      deal details. Nothing is sent to the contact.'
  - id: s3
    builds: automation
    uses:
    - s1
    - deal_stage_changed
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users in the
      segment from "Find the genuinely stuck ones" and writes these figures: how many are in it now and 7 days ago; the count
      by {deal_stage_changed.stage} and by {deal_stage_changed.owner}; the sum of {deal_stage_changed.value} at risk; how
      many users who left the segment in the last 7 days moved to a later stage and how many to lost. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Stalled deal detection

Slash command: /stalled-deal-detection

## Step 1: Find the genuinely stuck ones

Build a new segment of users named "Contacts on stalled deals". A user is in it when all of these are true: their latest deal stage changed happened more than 30 days ago; in it stage is not won or lost; they did not do activity event in the last 14 d; their deal paused attribute is not true.

## Step 2: Draft it and chase the rep

Build an automation that starts when a user enters the segment from "Find the genuinely stuck ones". It writes a short re-engagement email draft in a direct, low-pressure tone that fits stage: discovery re-asks the open qualifying question, demo offers a technical deep-dive, proposal offers to align with the decision-maker, closing asks plainly about timeline and blockers. It emails the email addresses of the reps who get nudge drafts the contact's name, email, owner, stage, value and that draft to review and send themselves. It waits 14 d; if the user is still in the segment, it emails the email addresses of the sales managers who get escalations the same deal details. Nothing is sent to the contact.

## Step 3: See what is really dead

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users in the segment from "Find the genuinely stuck ones" and writes these figures: how many are in it now and 7 days ago; the count by stage and by owner; the sum of value at risk; how many users who left the segment in the last 7 days moved to a later stage and how many to lost. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
