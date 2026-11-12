---
frontmatter_id: discovery-call-summary-recipe
slash_command: /discovery-call-summary-recipe
description: Generates an AI summary for Discovery calls from meeting data using the qualification framework in the summary recipe.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Automatically summarizes Discovery calls into seven qualification fields (champion, pain, current solution, decision
    criteria, timeline, budget, next step) and builds a rep-level quality dashboard.
  parameters:
  - name: target_capture_rate
    type: number
    label: Target share of discovery calls with all 7 fields captured (%)
    default: 70
    required: false
  - name: discovery_meeting_type
    type: string
    label: Meeting type name for Discovery calls
    default: Discovery
    required: false
  - name: unknown_value_label
    type: string
    label: Value to return when a field was not discussed
    default: not_discussed
    required: false
  requirements:
  - slot: meeting_recording
    kind: event
    meaning: A customer meeting was recorded and transcribed for a Discovery call
    properties:
    - name: meeting_type
      type: string
      meaning: The meeting type assigned to the call
      optional: false
    - name: rep_name
      type: string
      meaning: The sales rep who ran the call
      optional: false
    - name: transcript
      type: text
      meaning: Full transcript of the call
      optional: false
  - slot: ai_summary_recipe
    kind: knowledge
    meaning: An AI summary recipe that can be configured per meeting type to extract custom structured fields from meeting
      transcripts
  steps:
  - id: s1
    builds: event
    uses:
    - discovery_meeting_type
    instruction: Retrieve the meeting type named {discovery_meeting_type} from the project's meeting taxonomy. Confirm it
      exists and has notetaker autojoin enabled; both are prerequisites for the custom summary recipe to fire on real meetings.
      If the meeting type does not exist, halt and prompt the user to run the meeting types taxonomy setup first.
  - id: s2
    builds: automation
    uses:
    - ai_summary_recipe
    - s1
    - unknown_value_label
    instruction: 'Configure the {ai_summary_recipe} for the meeting type confirmed in "Check the Discovery meeting type".
      Extract these structured fields from each call: (1) Champion: name, title, level of buy-in (high, medium, low, none),
      and explicit quotes showing commitment. (2) Pain: pain statement in the prospect''s own words, severity (must-solve,
      should-solve, nice-to-have), and business impact discussed (revenue, cost, time, risk). (3) Current Solution: what they
      use today (vendor name and version), what works, and what does not work. (4) Decision Criteria: explicit criteria mentioned
      (price, features, integration, security, etc.) and priority ranking if discussed. (5) Timeline: target go-live and urgency
      drivers. (6) Budget: explicit number, range, or signal; flag when there is no budget signal. (7) Next Step: what was
      agreed, with owner and due date. If a field is not discussed, return {unknown_value_label} rather than guessing.'
  - id: s3
    builds: dashboard
    uses:
    - s1
    - s2
    - target_capture_rate
    - meeting_recording
    instruction: 'Build a Discovery call quality dashboard from the structured summaries produced in "Set what discovery captures".
      Show: percentage of discovery calls with all 7 fields captured, against the target of {target_capture_rate}%; the most
      frequently missed fields, to surface coaching opportunities; discoveries with no budget signal flagged for follow-up;
      champion strength distribution across recent discoveries; and pain severity distribution. Group every metric by rep
      so managers can spot reps who consistently miss qualification fields.'
---

# Discovery call qualification fields

Slash command: /discovery-call-summary-recipe

## Step 1: Check the Discovery meeting type

Retrieve the Discovery meeting type from the project's meeting taxonomy. Confirm it exists and has notetaker autojoin enabled, both are prerequisites for the custom summary recipe to fire on real meetings. If the type doesn't exist, halt and prompt the user to run /meeting-types-taxonomy first.

## Step 2: Set what discovery captures

Configure the AI summary recipe for the Discovery meeting type. Extract structured fields: (1) Champion (name, title, level of buy-in (high/medium/low/none), explicit quotes showing commitment; (2) Pain) pain statement in prospect's own words, severity (must-solve/should-solve/nice-to-have), business impact discussed (revenue, cost, time, risk); (3) Current Solution (what they use today (vendor name + version), what works, what doesn't; (4) Decision Criteria) explicit criteria mentioned (price, features, integration, security, etc.), priority ranking if discussed; (5) Timeline (target go-live, urgency drivers; (6) Budget) explicit number, range, or signal (no budget signal = flag); (7) Next Step: what was agreed, with owner and due date. If a field is not discussed, return 'not_discussed' rather than guessing. Use the result of "Check the Discovery meeting type".

## Step 3: Check discovery quality by rep

Compose a Discovery call quality dashboard reading from the structured summaries: % of discovery calls with all 7 fields captured (target: 70%+); breakdown of most-frequently-missed fields (signals coaching opportunities); discoveries with 'no budget signal' flagged for follow-up; champion strength distribution across recent discoveries; pain severity distribution. Group by rep so managers can spot reps consistently missing qualification fields. Use the result of "Check the Discovery meeting type", "Set what discovery captures".
