---
frontmatter_id: ai-stalled-deal-nudge
slash_command: /ai-stalled-deal-nudge
description: Drafts a personalized re-engagement email for each stalled deal from its call notes and emails it to the rep
  to review and send, with a manager escalation if the deal stays stalled.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: When a deal stalls, drafts a personalized re-engagement email from its context and emails it to the rep to review
    and send, escalating to a manager if it stays stalled.
  parameters:
  - name: escalation_window
    type: duration
    label: Days stalled after first nudge before manager escalation
    default: 14 d
    required: false
  - name: include_manager_escalation
    type: boolean
    label: Escalate to manager if deal stays stalled
    default: true
    required: false
  - name: manager_recipients
    type: string
    label: Email addresses of the sales managers who get escalations
    required: true
  requirements:
  - slot: stalled_deal_detected
    kind: event
    meaning: A deal was newly detected as stalled
    properties:
    - name: deal_stage
      type: string
      meaning: Stage the deal stalled in (Discovery, Demo, Proposal, or Closing)
      optional: false
    - name: deal_name
      type: string
      meaning: Name of the deal
      optional: false
    - name: owner_email
      type: string
      meaning: Email address of the deal owner
      optional: false
  - slot: deal_stage_changed
    kind: event
    meaning: A deal moved to another stage
    properties:
    - name: deal_name
      type: string
      meaning: Name of the deal
      optional: false
  - slot: deal_meeting_summary
    kind: knowledge
    meaning: Meeting summaries and call notes attached to the deal, including agreed next steps, objections and timelines
    optional: true
  - slot: deal_contact
    kind: attribute
    meaning: The primary contact on the deal and their engagement status
  steps:
  - id: s1
    builds: automation
    uses:
    - stalled_deal_detected
    - deal_stage_changed
    - deal_meeting_summary
    - deal_contact
    - escalation_window
    - include_manager_escalation
    - manager_recipients
    instruction: 'Build an automation triggered when {stalled_deal_detected} happens. An analysis step reads the deal''s {stalled_deal_detected.deal_stage},
      its latest {deal_meeting_summary} and {deal_contact}, and writes: the agreed next step that did not happen, the latest
      objection in the customer''s words, any timeline now expiring, and another stakeholder to try if the contact went quiet.
      Then it emails {stalled_deal_detected.owner_email} a draft re-engagement email to the contact built from those points,
      with no placeholders, for the rep to review and send themselves. When {include_manager_escalation} is true it waits
      {escalation_window}; if no {deal_stage_changed} happened for {stalled_deal_detected.deal_name} in that time, it emails
      {manager_recipients} the deal name, stage, the analysis and the draft.'
---

# AI nudge for a stalled deal

Slash command: /ai-stalled-deal-nudge

## Step 1: Draft a nudge that names it

Build an automation triggered when stalled deal detected happens. An analysis step reads the deal's deal stage, its latest deal meeting summary and deal contact, and writes: the agreed next step that did not happen, the latest objection in the customer's words, any timeline now expiring, and another stakeholder to try if the contact went quiet. Then it emails owner email a draft re-engagement email to the contact built from those points, with no placeholders, for the rep to review and send themselves. When True is true it waits 14 d; if no deal stage changed happened for deal name in that time, it emails the email addresses of the sales managers who get escalations the deal name, stage, the analysis and the draft.
