---
name: call-recording-intelligence
description: Use when a user mentions "call recording AI", "call insights extraction", "call coaching automation", or asks for related help. When a call recording becomes available, run AI extraction for objections + talk-listen ratio + sentiment + next-step signals, log to the linked deal, and alert managers on at-risk calls.
arguments: []
intempt:
  id: call-recording-intelligence
  title: "Call recording intelligence"
  version: 1.0.0
  slashCommand: /call-recording-intelligence
  group: Workflows
  shortDescription: "Pulls the objections, the talk ratio, the sentiment and the buying signals out of every call recording, files them on the deal, and flags the bad calls."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [call-intelligence, sales-coaching]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: call_recording_available, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_slack_content
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Read every call transcript"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "From the transcript once the recording lands: who talked and for how long, every objection with its quote, timestamp and category of price, timing, competition, a missing feature, authority or trust, how sentiment moved through the call, the buying signals with quotes, how many discovery questions were asked, and an at risk score combining all of it."
      prompt: 'Create an AI-derived attribute on the Meeting object called ''call_insights''. Computed at call_recording_available from the transcript. Output: structured object with (a) talk-listen ratio per participant; (b) objections detected (list with quote + timestamp + category: price/timing/competition/feature-gap/authority/trust); (c) sentiment trajectory across call phases (open/discovery/demo/close); (d) buying signals detected (list with quote + timestamp + category); (e) discovery question count; (f) at-risk score (composite: high objections + low buying signals + negative sentiment shifts).'
    - step: 2
      title: "Write the manager alert"
      command: create_slack_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute]
      description: "For calls over the at risk threshold: the rep, the account, the deal value and stage, the three worst objections with the quotes, the talk ratio flagged if the rep spoke for more than 65%, and a link that jumps to the right point in the transcript. Written to coach, not to punish."
      prompt: 'Generate Slack alert content for sales managers when a call''s at-risk score crosses threshold. Include: rep name, account name, deal value/stage, the 3 highest-severity objections with quoted clips, talk-listen ratio (flag if rep talked >65%), and a deep link to jump to the relevant transcript timestamps. Tone: coach-actionable, not punitive.'
    - step: 3
      title: "File it and flag the bad ones"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, asset]
      description: "When a recording becomes available it computes the insights, writes them onto the meeting and links them to the deal, posts the manager alert and raises a 24 hour review task once the at risk score reaches 70, and creates a high priority follow up task when the buying signals are strong and nothing is scheduled."
      prompt: 'Create a workflow firing on call_recording_available. Step sequence: (1) compute call_insights attribute from the transcript; (2) update the linked Meeting record''s notes with the structured insights and link to the deal; (3) if at-risk score crosses threshold (>=70), post the manager alert to Slack #sales-coaching and create a task for the rep''s manager to review within 24h; (4) if buying signals are strong and no follow-up exists, create a high-priority next-step task for the rep.'
    - step: 4
      title: "Coach from the patterns"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, asset, workflow]
      description: "Talk ratio per rep over 30 days, flagging anyone outside 40 to 55%, the five most common objections across the team and per rep, discovery question counts with anyone under five per call flagged, at risk calls by rep and week, and the calls with the densest buying signals as listen back examples."
      prompt: 'Compose a coaching dashboard: talk-listen ratio by rep (rolling 30 days) flagging anyone outside the 40-55% rep-talk healthy range; top 5 objection categories by frequency (network-level + per-rep); discovery question count distribution (flag reps consistently below 5/call); at-risk call count by rep and week; and a leaderboard of calls with the highest buying-signal density (these are good listen-back examples for team training).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Call recording intelligence

Pulls the objections, the talk ratio, the sentiment and the buying signals out of every call recording, files them on the deal, and flags the bad calls.

## Before you run it

- Connect slack
- Send the `call_recording_available` event

## What it does

1. **Read every call transcript** (`create_ai_attribute`)

   From the transcript once the recording lands: who talked and for how long, every objection with its quote, timestamp and category of price, timing, competition, a missing feature, authority or trust, how sentiment moved through the call, the buying signals with quotes, how many discovery questions were asked, and an at risk score combining all of it.

2. **Write the manager alert** (`create_slack_content`)

   For calls over the at risk threshold: the rep, the account, the deal value and stage, the three worst objections with the quotes, the talk ratio flagged if the rep spoke for more than 65%, and a link that jumps to the right point in the transcript. Written to coach, not to punish.

3. **File it and flag the bad ones** (`create_workflow`)

   When a recording becomes available it computes the insights, writes them onto the meeting and links them to the deal, posts the manager alert and raises a 24 hour review task once the at risk score reaches 70, and creates a high priority follow up task when the buying signals are strong and nothing is scheduled.

4. **Coach from the patterns** (`create_dashboard`)

   Talk ratio per rep over 30 days, flagging anyone outside 40 to 55%, the five most common objections across the team and per rep, discovery question counts with anyone under five per call flagged, at risk calls by rep and week, and the calls with the densest buying signals as listen back examples.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
