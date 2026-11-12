---
frontmatter_id: ai-stalled-deal-nudge
slash_command: /ai-stalled-deal-nudge
description: Drafts a personalized re-engagement email for stalled deals using CRM deal context, leaving it for the rep to review and send.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: When a deal is flagged as stalled, drafts a personalized re-engagement email from CRM context for the rep to review,
    then tracks nudge results against manual nudges.
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
  requirements:
  - slot: stalled_deal_detected
    kind: event
    meaning: A deal was newly detected as stalled
    properties:
    - name: deal_stage
      type: string
      meaning: Stage the deal stalled in (Discovery, Demo, Proposal, or Closing)
      optional: false
  - slot: deal_meeting_summary
    kind: knowledge
    meaning: Meeting summaries and call notes attached to the deal, including agreed next steps, objections and timelines
    optional: true
  - slot: deal_contact
    kind: attribute
    meaning: The primary contact on the deal and their engagement status
  - slot: rep_outbox
    kind: integration
    meaning: Email connection used to save drafts to the deal owner's outbox
    channel: email
  - slot: rep_task_list
    kind: integration
    meaning: Task system where the deal owner receives review tasks
    channel: hubspot
  - slot: rep_slack
    kind: integration
    meaning: Slack workspace used to send direct messages to deal owners and managers
    channel: slack
  - slot: nudge_context
    kind: attribute
    meaning: 'AI-derived context on a stalled deal: stalled stage, agreed next step, latest objection, expiring timeline,
      and replacement stakeholder candidates'
  - slot: nudge_outcome_data
    kind: segment
    meaning: Deals that received AI nudge drafts, with their replies, stage advances and ARR, plus manual-nudge control deals
  steps:
  - id: s1
    builds: attribute
    uses:
    - stalled_deal_detected
    - deal_meeting_summary
    - deal_contact
    - nudge_context
    instruction: 'Create the AI-derived attribute {nudge_context} on the Deal object, computed when the deal enters stalled
      status. Aggregate: (a) the stage the deal stalled in (Discovery, Demo, Proposal, or Closing; each needs a different
      nudge angle); (b) the last {deal_meeting_summary}, prioritising the agreed next step that does not appear to have happened;
      (c) the most recent objection raised in call summaries; (d) any mentioned timeline or decision window that may now be
      expiring; (e) replacement-stakeholder candidates if {deal_contact} has gone quiet.'
  - id: s2
    builds: automation
    uses:
    - stalled_deal_detected
    - rep_outbox
    - rep_task_list
    - rep_slack
    - nudge_context
    - escalation_window
    - include_manager_escalation
    - s1
    instruction: 'Create a workflow that fires when {stalled_deal_detected} occurs. Step 1: compute {nudge_context} as described
      in "Recall why it stalled". Step 2: generate an AI-drafted re-engagement email using {nudge_context}. Make it highly
      personalised using meeting-summary specifics, quoting the objection verbatim where available (for example: ''Last time
      we talked, you mentioned [objection]. Has anything changed on [blocker]?''). Step 3: save the draft to the deal owner''s
      outbox via {rep_outbox}. Do not send it. Step 4: create a task in {rep_task_list} titled ''Review AI-drafted nudge:
      deal [deal name]'' with the draft preview attached. Step 5: send the deal owner a Slack DM via {rep_slack} with the
      deal context. Every draft requires rep review before sending. If the deal is still stalled {escalation_window} after
      the first nudge draft was sent, and {include_manager_escalation} is true, escalate to the manager with a manager-version
      draft; this escalation requires human sign-off before it is sent.'
  - id: s3
    builds: dashboard
    uses:
    - nudge_outcome_data
    - s1
    - s2
    instruction: 'Build a dashboard of AI nudge effectiveness from {nudge_outcome_data}. Show: stalled deals that received
      AI nudge drafts versus drafts not yet reviewed (backlog); reply rate to AI-nudge-drafted emails compared with baseline
      manual nudges; revival rate (deals that advanced a stage after an AI nudge); and ARR resurrected through this workflow.
      Use manual-nudge deals, where the rep wrote their own nudge, as the control group. Use the results of "Recall why it
      stalled" and "Draft a nudge that names it" to define the cohorts. Reference point: AI-drafted personalised nudges typically
      win on reply rate by 1.5 to 2 times over the control.'
---

# AI nudge for a stalled deal

Slash command: /ai-stalled-deal-nudge

## Step 1: Recall why it stalled

Create an AI-derived attribute 'nudge_context' on the Deal object, computed when the deal enters stalled status. Aggregates: (a) which stage stalled (Discovery / Demo / Proposal / Closing (each requires different nudge angle); (b) last meeting_summary if available) most useful is the 'next step' that was agreed and apparently not happening; (c) most recent objection raised (from call summaries); (d) any mentioned timeline / decision-window that may now be expiring; (e) replacement-stakeholder candidates if the original contact has gone quiet.

## Step 2: Draft a nudge that names it

Create a workflow firing when a deal is newly detected as stalled (consumer of the stalled-deal-detection workflow's output). Step sequence: (1) compute nudge_context; (2) generate AI-drafted nudge email using the context. Distinct from the template-based nudge in stalled-deal-detection: this version is HIGHLY personalized using meeting-summary specifics ('Last time we talked, you mentioned [verbatim objection]. Has anything changed on [specific blocker]?'); (3) save draft to rep's outbox; (4) create rep task labeled 'Review AI-drafted nudge: deal [name]' with the draft preview; (5) Slack DM with deal context. Always rep-reviewed-before-send. If deal stays stalled 14 days after first nudge draft sent, escalate to manager with manager-version draft (this needs your sign-off). Use the result of "Recall why it stalled".

## Step 3: Compare against a rep's own

Compose an AI nudge effectiveness dashboard: stalled-deals that received AI nudge drafts (vs. drafts not yet reviewed = backlog), reply rate to AI-nudge-drafted emails vs. baseline manual nudges, revival rate (deals stage-advanced after AI nudge), and ARR resurrected via this workflow. Compare to control: stalled deals where reps wrote their own nudge: typically AI-drafted personalized nudges win on reply rate by 1.5-2x. Use the result of "Recall why it stalled", "Draft a nudge that names it".
