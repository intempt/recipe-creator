---
frontmatter_id: call-recording-intelligence
slash_command: /call-recording-intelligence
description: Pulls the objections, the talk ratio, the sentiment and the buying signals out of every call recording, emails
  managers about the bad calls, and emails a weekly coaching digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Reads every sales call transcript for objections, talk ratio, sentiment and buying signals, emails managers about
    at-risk calls and sends a weekly coaching digest.
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
  - name: healthy_talk_min_percent
    type: number
    label: Lower bound of healthy rep talk share (%)
    default: 40
    required: false
  - name: healthy_talk_max_percent
    type: number
    label: Upper bound of healthy rep talk share (%)
    default: 55
    required: false
  - name: min_discovery_questions
    type: number
    label: Discovery questions per call below which a rep is flagged
    default: 5
    required: false
  - name: coaching_window
    type: duration
    label: Window the coaching digest covers
    default: 30 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the sales managers who get at-risk call alerts
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
  steps:
  - id: s1
    builds: automation
    uses:
    - call_recording_event
    - at_risk_threshold
    - talk_ratio_flag_percent
    - alert_recipients
    instruction: 'Build an automation triggered when {call_recording_event} happens. An analysis step reads {call_recording_event.transcript}
      and writes: the rep''s share of talk time; each objection with its quote and category (price, timing, competition, feature-gap,
      authority, trust); the sentiment at the open, discovery, demo and close; each buying signal with its quote; the number
      of discovery questions; an at-risk score from 0 to 100 that rises with objections and negative sentiment and falls with
      buying signals. When the at-risk score is {at_risk_threshold} or more, it emails {alert_recipients} the rep {call_recording_event.rep_name},
      account {call_recording_event.account_name}, {call_recording_event.deal_value} and {call_recording_event.deal_stage},
      the 3 strongest objections with quotes, the talk share marked when above {talk_ratio_flag_percent}%, and {call_recording_event.meeting_link}.'
  - id: s2
    builds: automation
    uses:
    - call_recording_event
    - healthy_talk_min_percent
    - healthy_talk_max_percent
    - min_discovery_questions
    - coaching_window
    - at_risk_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the transcripts
      of {call_recording_event} in the last {coaching_window} and writes these figures: each rep''s average talk share, marked
      when outside {healthy_talk_min_percent}% to {healthy_talk_max_percent}%; the top 5 objection categories, overall and
      per rep; each rep''s average discovery questions per call, marked when below {min_discovery_questions}; at-risk calls
      (score {at_risk_threshold} or more) per rep; the 3 calls with the most buying signals, each with its {call_recording_event.meeting_link}.
      Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Call recording intelligence

Slash command: /call-recording-intelligence

## Step 1: Read every call and flag the bad ones

Build an automation triggered when call recording event happens. An analysis step reads transcript and writes: the rep's share of talk time; each objection with its quote and category (price, timing, competition, feature-gap, authority, trust); the sentiment at the open, discovery, demo and close; each buying signal with its quote; the number of discovery questions; an at-risk score from 0 to 100 that rises with objections and negative sentiment and falls with buying signals. When the at-risk score is 70 or more, it emails the email addresses of the sales managers who get at-risk call alerts the rep rep name, account account name, deal value and deal stage, the 3 strongest objections with quotes, the talk share marked when above 65%, and meeting link.

## Step 2: Email the weekly coaching digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the transcripts of call recording event in the last 30 d and writes these figures: each rep's average talk share, marked when outside 40% to 55%; the top 5 objection categories, overall and per rep; each rep's average discovery questions per call, marked when below 5; at-risk calls (score 70 or more) per rep; the 3 calls with the most buying signals, each with its meeting link. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
