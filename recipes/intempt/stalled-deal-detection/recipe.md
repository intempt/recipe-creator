---
frontmatter_id: stalled-deal-detection
slash_command: /stalled-deal-detection
description: Finds deals sitting in a stage far longer than usual with no activity, drafts a nudge that fits the stage, and escalates if they stay stuck.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds deals stuck in a stage far longer than usual with no recent activity, drafts a stage-fitting nudge for the
    rep to review, escalates to the manager if still stalled, and reports on stalled deals.
  parameters:
  - name: stage_percentile_threshold
    type: number
    label: Stage age percentile threshold (top quartile = 75)
    default: 75
    required: false
  - name: inactivity_window
    type: duration
    label: Minimum days without deal activity
    default: 14 d
    required: false
  - name: escalation_delay
    type: duration
    label: Time after first nudge before escalating to manager
    default: 14 d
    required: false
  - name: nudge_tone
    type: enum
    label: Nudge email tone
    default: direct
    required: false
    options:
    - direct
    - warm
    - formal
  - name: overdue_review_window
    type: duration
    label: Lookback window for stalled-deal reporting
    default: 30 d
    required: false
  requirements:
  - slot: deal_object
    kind: event
    meaning: A deal record moved through pipeline stages and carries stage, value, owner and open/closed status
    properties:
    - name: stage
      type: string
      meaning: Current pipeline stage of the deal
      optional: false
    - name: value
      type: number
      meaning: Deal amount in currency
      optional: false
    - name: owner
      type: string
      meaning: Rep who owns the deal
      optional: false
    - name: paused
      type: boolean
      meaning: Rep-set flag marking a legitimate pause
      optional: true
  - slot: activity_event
    kind: event
    meaning: A customer or rep interaction on a deal such as a meeting, email reply or completed task
    properties:
    - name: activity_type
      type: string
      meaning: 'Kind of activity: meeting, email reply or task completion'
      optional: false
    - name: occurred_at
      type: date
      meaning: When the activity happened
      optional: false
  - slot: stalled_deals_segment
    kind: segment
    meaning: Open deals that are in the top age quartile for their stage and have no activity for the inactivity window
    creatable: true
    definition: open deals where days_in_current_stage is in the top {stage_percentile_threshold} percentile for their stage
      AND days since last activity >= {inactivity_window}, excluding deals with paused flag set
  - slot: nudge_template
    kind: knowledge
    meaning: Stage-specific re-engagement email template with angles for discovery, demo, proposal and closing stalls
  - slot: rep_task_channel
    kind: integration
    meaning: Connected Slack workspace for direct messages to reps and the manager
    channel: slack
  steps:
  - id: s1
    builds: attribute
    uses:
    - deal_object
    - activity_event
    - stage_percentile_threshold
    instruction: Create an AI-derived attribute 'days_in_current_stage' on {deal_object}, refreshed daily. Compute (a) calendar
      days since the deal last changed stage; (b) the percentile of this age within the stage's historical median for similar
      deals (size, segment, owner). Flag deals whose age is at or above the {stage_percentile_threshold} percentile for that
      stage. Also compute 'days_since_last_activity' from any {activity_event} of type meeting, email reply or task completion
      on the deal.
  - id: s2
    builds: segment
    uses:
    - s1
    - stalled_deals_segment
    - deal_object
    - stage_percentile_threshold
    - inactivity_window
    instruction: Build segment '{stalled_deals_segment}' of open {deal_object} records where days_in_current_stage is at or
      above the {stage_percentile_threshold} percentile for the stage AND days_since_last_activity >= {inactivity_window}.
      Exclude deals where the owner has set the paused flag. Refresh daily. Use the result of "Measure how long it has sat".
  - id: s3
    builds: content
    uses:
    - s1
    - s2
    - nudge_tone
    instruction: 'Generate an AI-drafted re-engagement email template chosen by stalled stage: Discovery stalled re-asks the
      qualifying question that went unanswered; Demo stalled offers a technical deep-dive or proof of concept; Proposal stalled
      notes that pricing pushback usually means the decision-maker is not bought in and offers to align; Closing stalled asks
      directly for clarity on timeline and remaining blockers. Personalize to the last meeting summary when available. Tone:
      {nudge_tone}, low-pressure and honest. The rep reviews and sends; never auto-send. Use the result of "Measure how long
      it has sat" and "Find the genuinely stuck ones".'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - stalled_deals_segment
    - escalation_delay
    - rep_task_channel
    instruction: 'Create a workflow that fires daily for deals that crossed into {stalled_deals_segment} in the last 24 hours.
      Steps: (1) compose an AI nudge draft from the "Write a nudge per stage" template and the deal context; (2) create a
      task for the deal owner labeled ''Review and send: stalled deal nudge'' with the draft attached; (3) send a Slack direct
      message to the owner with the deal name, a draft preview and a review button, using {rep_task_channel}; (4) if the same
      deal is still in {stalled_deals_segment} {escalation_delay} after the first nudge task, send a Slack message to the
      manager via {rep_task_channel} suggesting the deal may need to be closed-lost. Do not auto-send any email; the rep must
      review. Use the results of "Measure how long it has sat", "Find the genuinely stuck ones" and "Write a nudge per stage".'
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - stalled_deals_segment
    - overdue_review_window
    instruction: 'Compose a stalled-deal dashboard over {overdue_review_window}: count of {stalled_deals_segment} deals by
      stage and owner; total deal value at risk (sum of stalled deal values); median days_in_current_stage of stalled deals;
      recovery rate (stalled deals that re-engaged and moved to a later stage); and closed-lost discipline rate (stalled deals
      that stayed stalled 30 or more days before being marked lost). Add a manager view showing which owners let deals stall
      repeatedly versus those who close deals lost promptly. Use the results of "Measure how long it has sat", "Find the genuinely
      stuck ones", "Write a nudge per stage" and "Draft it and chase the rep".'
---

# Stalled deal detection

Slash command: /stalled-deal-detection

## Step 1: Measure how long it has sat

Create an AI-derived attribute 'days_in_current_stage' on the Deal object, refreshed daily. Compute: (a) calendar days since the deal last changed stage; (b) percentile of this age within the stage's historical median for similar deals (size, segment, rep). Flag deals where age is in the top quartile (75th+ percentile) for that stage. Also compute 'Days since last activity' (any meeting / email reply / task completion on the deal).

## Step 2: Find the genuinely stuck ones

Build a segment 'Stalled deals' capturing open deals where (a) days_in_current_stage is in the top quartile for that stage AND (b) Days since last activity >= 14 days. Excludes deals where the rep has manually set a 'paused' flag (legitimate pause, coming back next quarter, etc.). Refreshed daily. Use the result of "Measure how long it has sat".

## Step 3: Write a nudge per stage

Generate an AI-drafted re-engagement email template. The AI picks angle based on stalled-stage: (a) Discovery stalled (re-ask the qualifying question that wasn't answered; (b) Demo stalled) offer technical deep-dive or POC; (c) Proposal stalled (surface that pricing pushback usually means decision-maker isn't bought in, offer to align; (d) Closing stalled) explicit clarity-ask about timeline + remaining blockers. Personalized to last meeting summary if available. Tone: direct, low-pressure, honest. The rep reviews and sends: not auto-send. Use the result of "Measure how long it has sat", "Find the genuinely stuck ones".

## Step 4: Draft it and chase the rep

Create a workflow firing daily for newly-stalled deals (deals that crossed into stalled-segment in the last 24 hours). Step sequence: (1) compose AI nudge draft using the asset template + deal context; (2) create a task for the deal owner labeled 'Review and send: stalled deal nudge' with the draft pre-attached; (3) post Slack DM to the rep with deal name + draft preview + 'review' button; (4) escalate to manager via Slack if same deal is still stalled 14 days after first nudge task (signal: deal should probably be closed-lost). Don't auto-send the email: rep must review. Use the result of "Measure how long it has sat", "Find the genuinely stuck ones", "Write a nudge per stage".

## Step 5: See what is really dead

Compose a stalled-deal dashboard: count of stalled deals by stage and rep, total ARR at risk (sum of stalled deals' values), median age of stalled deals, recovery rate (stalled deals that re-engaged and moved stage forward), and dishonesty rate (stalled deals that should have been closed-lost: measured as deals that stay stalled 30+ days before eventually being marked lost). Manager view: which reps consistently let deals stall vs. honestly close-lost. Use the result of "Measure how long it has sat", "Find the genuinely stuck ones", "Write a nudge per stage", "Draft it and chase the rep".
