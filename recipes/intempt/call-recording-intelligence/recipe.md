---
frontmatter_id: call-recording-intelligence
slash_command: /call-recording-intelligence
description: Pulls the objections, the talk ratio, the sentiment and the buying signals out of every call recording, files them on the deal, and flags the bad calls.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Pulls objections, talk ratio, sentiment and buying signals from each call recording, files them on the deal, and
    alerts managers to at-risk calls with coaching context.
  parameters:
  - name: at_risk_threshold
    type: number
    label: At-risk score threshold that triggers a manager alert
    default: 70
    required: false
  - name: talk_ratio_flag_percent
    type: number
    label: Rep talk share (%) above which the alert flags talking too much
    default: 65
    required: false
  - name: manager_review_window
    type: duration
    label: Time allowed for the manager to review a flagged call
    default: 24 h
    required: false
  - name: healthy_talk_min_percent
    type: number
    label: Lower bound of healthy rep talk share (%) for dashboard
    default: 40
    required: false
  - name: healthy_talk_max_percent
    type: number
    label: Upper bound of healthy rep talk share (%) for dashboard
    default: 55
    required: false
  - name: min_discovery_questions
    type: number
    label: Discovery questions per call below which a rep is flagged
    default: 5
    required: false
  - name: dashboard_rolling_window
    type: duration
    label: Rolling window for the coaching dashboard
    default: 30 d
    required: false
  - name: alert_channel_name
    type: string
    label: Slack channel for manager alerts
    default: '#sales-coaching'
    required: false
  requirements:
  - slot: call_recording_event
    kind: event
    meaning: A sales call recording became available
    properties:
    - name: transcript
      type: text
      meaning: Full transcript of the call
      optional: false
    - name: rep_name
      type: string
      meaning: Name of the rep who ran the call
      optional: false
    - name: account_name
      type: string
      meaning: Account the call was with
      optional: false
    - name: deal_value
      type: number
      meaning: Value of the linked deal
      optional: true
    - name: deal_stage
      type: string
      meaning: Current stage of the linked deal
      optional: true
    - name: meeting_link
      type: string
      meaning: Link to jump to the recording
      optional: true
  - slot: sales_meeting_object
    kind: event
    meaning: A meeting record linked to a deal and an account
    properties:
    - name: notes
      type: text
      meaning: Notes field on the meeting record
      optional: false
  - slot: rep_manager
    kind: attribute
    meaning: The manager assigned to each sales rep
  - slot: sales_coaching_channel
    kind: integration
    meaning: A Slack workspace connection with the sales coaching channel
    channel: slack
  - slot: deal_record
    kind: destination
    meaning: The CRM deal the call insights are filed against
    channel: hubspot
  - slot: followup_task_exists
    kind: attribute
    meaning: Whether a follow-up next step already exists on the deal
  steps:
  - id: s1
    builds: attribute
    uses:
    - call_recording_event
    instruction: 'Create an AI-derived attribute on the Meeting object called ''call_insights'', computed when {call_recording_event}
      becomes available, from {call_recording_event.transcript}. Output a structured object with: (a) talk-listen ratio per
      participant; (b) objections detected, each with quote, timestamp and category (price, timing, competition, feature-gap,
      authority, trust); (c) sentiment trajectory across call phases (open, discovery, demo, close); (d) buying signals detected,
      each with quote, timestamp and category; (e) discovery question count; (f) at-risk score, a composite of high objections,
      low buying signals and negative sentiment shifts.'
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_coaching_channel
    - at_risk_threshold
    - talk_ratio_flag_percent
    instruction: 'Generate Slack alert content for sales managers when the at-risk score in s1 is at or above {at_risk_threshold}.
      Include: rep name {call_recording_event.rep_name}, account name {call_recording_event.account_name}, deal value {call_recording_event.deal_value}
      and stage {call_recording_event.deal_stage}; the 3 highest-severity objections from s1 with quoted clips; talk-listen
      ratio from s1, flagged if the rep talked more than {talk_ratio_flag_percent}%; and a deep link {call_recording_event.meeting_link}
      to the relevant transcript timestamps. Tone: coach-actionable, not punitive.'
  - id: s3
    builds: automation
    uses:
    - call_recording_event
    - s1
    - s2
    - deal_record
    - sales_coaching_channel
    - rep_manager
    - followup_task_exists
    - at_risk_threshold
    - manager_review_window
    instruction: 'Create a workflow that fires when {call_recording_event} becomes available. Step 1: compute the call_insights
      attribute from the transcript as defined in "Read every call transcript". Step 2: update the linked meeting record''s
      notes in {sales_meeting_object} with the structured insights from s1 and link the meeting to {deal_record}. Step 3:
      if the at-risk score is at or above {at_risk_threshold}, post the alert from "Write the manager alert" to {sales_coaching_channel}
      and create a task for {rep_manager} to review the call within {manager_review_window}. Step 4: if buying signals in
      s1 are strong and {followup_task_exists} is false, create a high-priority next-step task for the rep.'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - healthy_talk_min_percent
    - healthy_talk_max_percent
    - min_discovery_questions
    - dashboard_rolling_window
    - sales_coaching_channel
    instruction: Compose a coaching dashboard using the call insights from "Read every call transcript", the alerts from "Write
      the manager alert" and the workflow from "File it and flag the bad ones". Show talk-listen ratio by rep over the rolling
      {dashboard_rolling_window}, flagging any rep outside the {healthy_talk_min_percent}% to {healthy_talk_max_percent}%
      rep-talk range. Show the top 5 objection categories by frequency, network-level and per rep. Show the discovery question
      count distribution and flag reps consistently below {min_discovery_questions} per call. Show at-risk call count by rep
      and week. Show a leaderboard of calls with the highest buying-signal density as listen-back examples for team training.
---

# Call recording intelligence

Slash command: /call-recording-intelligence

## Step 1: Read every call transcript

Create an AI-derived attribute on the Meeting object called 'call_insights'. Computed at call_recording_available from the transcript. Output: structured object with (a) talk-listen ratio per participant; (b) objections detected (list with quote + timestamp + category: price/timing/competition/feature-gap/authority/trust); (c) sentiment trajectory across call phases (open/discovery/demo/close); (d) buying signals detected (list with quote + timestamp + category); (e) discovery question count; (f) at-risk score (composite: high objections + low buying signals + negative sentiment shifts).

## Step 2: Write the manager alert

Generate Slack alert content for sales managers when a call's at-risk score crosses threshold. Include: rep name, account name, deal value/stage, the 3 highest-severity objections with quoted clips, talk-listen ratio (flag if rep talked >65%), and a deep link to jump to the relevant transcript timestamps. Tone: coach-actionable, not punitive. Use the result of "Read every call transcript".

## Step 3: File it and flag the bad ones

Create a workflow firing on call_recording_available. Step sequence: (1) compute call_insights attribute from the transcript; (2) update the linked Meeting record's notes with the structured insights and link to the deal; (3) if at-risk score crosses threshold (>=70), post the manager alert to Slack #sales-coaching and create a task for the rep's manager to review within 24h; (4) if buying signals are strong and no follow-up exists, create a high-priority next-step task for the rep. Use the result of "Read every call transcript", "Write the manager alert".

## Step 4: Coach from the patterns

Compose a coaching dashboard: talk-listen ratio by rep (rolling 30 days) flagging anyone outside the 40-55% rep-talk healthy range; top 5 objection categories by frequency (network-level + per-rep); discovery question count distribution (flag reps consistently below 5/call); at-risk call count by rep and week; and a leaderboard of calls with the highest buying-signal density (these are good listen-back examples for team training). Use the result of "Read every call transcript", "Write the manager alert", "File it and flag the bad ones".
