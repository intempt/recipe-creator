---
name: call-recording-intelligence
description: Use when a user mentions "call recording AI", "call insights extraction", "call coaching automation", or asks for related help. When a call recording becomes available, run AI extraction for objections + talk-listen ratio + sentiment + next-step signals, log to the linked deal, and alert managers on at-risk calls.
arguments: []
intempt:
  id: call-recording-intelligence
  version: 1.0.0
  slashCommand: /call-recording-intelligence
  group: Workflows
  shortDescription: "Create a Meeting call_insights AI attribute with objections, talk-listen ratio, sentiment, and buying signals, then Slack-alert managers on at-risk calls."
  availability: coming-soon
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
    events:
      - { value: call_recording_available, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_slack_content
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build Call Insights AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: 'Create an AI-derived attribute on the Meeting object called ''call_insights''. Computed at call_recording_available from the transcript. Output: structured object with (a) talk-listen ratio per participant; (b) objections detected (list with quote + timestamp + category: price/timing/competition/feature-gap/authority/trust); (c) sentiment trajectory across call phases (open/discovery/demo/close); (d) buying signals detected (list with quote + timestamp + category); (e) discovery question count; (f) at-risk score (composite: high objections + low buying signals + negative sentiment shifts).'
      prompt: 'Create an AI-derived attribute on the Meeting object called ''call_insights''. Computed at call_recording_available from the transcript. Output: structured object with (a) talk-listen ratio per participant; (b) objections detected (list with quote + timestamp + category: price/timing/competition/feature-gap/authority/trust); (c) sentiment trajectory across call phases (open/discovery/demo/close); (d) buying signals detected (list with quote + timestamp + category); (e) discovery question count; (f) at-risk score (composite: high objections + low buying signals + negative sentiment shifts).'
    - step: 2
      title: Build Manager Alert Content
      command: create_slack_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute]
      description: 'Generate Slack alert content for sales managers when a call''s at-risk score crosses threshold. Include: rep name, account name, deal value/stage, the 3 highest-severity objections with quoted clips, talk-listen ratio (flag if rep talked >65%), and a deep link to jump to the relevant transcript timestamps. Tone: coach-actionable, not punitive.'
      prompt: 'Generate Slack alert content for sales managers when a call''s at-risk score crosses threshold. Include: rep name, account name, deal value/stage, the 3 highest-severity objections with quoted clips, talk-listen ratio (flag if rep talked >65%), and a deep link to jump to the relevant transcript timestamps. Tone: coach-actionable, not punitive.'
    - step: 3
      title: Build Recording Intelligence Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, asset]
      description: 'Create a workflow firing on call_recording_available. Step sequence: (1) compute call_insights attribute from the transcript; (2) update the linked Meeting record''s notes with the structured insights and link to the deal; (3) if at-risk score crosses threshold (>=70), post the manager alert to Slack #sales-coaching and create a task for the rep''s manager to review within 24h; (4) if buying signals are strong and no follow-up exists, create a high-priority next-step task for the rep.'
      prompt: 'Create a workflow firing on call_recording_available. Step sequence: (1) compute call_insights attribute from the transcript; (2) update the linked Meeting record''s notes with the structured insights and link to the deal; (3) if at-risk score crosses threshold (>=70), post the manager alert to Slack #sales-coaching and create a task for the rep''s manager to review within 24h; (4) if buying signals are strong and no follow-up exists, create a high-priority next-step task for the rep.'
    - step: 4
      title: Build Coaching Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, asset, workflow]
      description: 'Compose a coaching dashboard: talk-listen ratio by rep (rolling 30 days) flagging anyone outside the 40-55% rep-talk healthy range; top 5 objection categories by frequency (network-level + per-rep); discovery question count distribution (flag reps consistently below 5/call); at-risk call count by rep and week; and a leaderboard of calls with the highest buying-signal density (these are good listen-back examples for team training).'
      prompt: 'Compose a coaching dashboard: talk-listen ratio by rep (rolling 30 days) flagging anyone outside the 40-55% rep-talk healthy range; top 5 objection categories by frequency (network-level + per-rep); discovery question count distribution (flag reps consistently below 5/call); at-risk call count by rep and week; and a leaderboard of calls with the highest buying-signal density (these are good listen-back examples for team training).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Call Recording Intelligence

## Procedure

1. **Build Call Insights AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute on the Meeting object called 'call_insights'. Computed at call_recording_available from the transcript. Output: structured object with (a) talk-listen ratio per participant; (b) objections detected (list with quote + timestamp + category: price/timing/competition/feature-gap/authority/trust); (c) sentiment trajectory across call phases (open/discovery/demo/close); (d) buying signals detected (list with quote + timestamp + category); (e) discovery question count; (f) at-risk score (composite: high objections + low buying signals + negative sentiment shifts). → produces: attribute
2. **Build Manager Alert Content** [`create_slack_content`] — Generate Slack alert content for sales managers when a call's at-risk score crosses threshold. Include: rep name, account name, deal value/stage, the 3 highest-severity objections with quoted clips, talk-listen ratio (flag if rep talked >65%), and a deep link to jump to the relevant transcript timestamps. Tone: coach-actionable, not punitive. → produces: asset
3. **Build Recording Intelligence Workflow** [`create_workflow`] — Create a workflow firing on call_recording_available. Step sequence: (1) compute call_insights attribute from the transcript; (2) update the linked Meeting record's notes with the structured insights and link to the deal; (3) if at-risk score crosses threshold (>=70), post the manager alert to Slack #sales-coaching and create a task for the rep's manager to review within 24h; (4) if buying signals are strong and no follow-up exists, create a high-priority next-step task for the rep. → produces: workflow
4. **Build Coaching Dashboard** [`create_dashboard`] — Compose a coaching dashboard: talk-listen ratio by rep (rolling 30 days) flagging anyone outside the 40-55% rep-talk healthy range; top 5 objection categories by frequency (network-level + per-rep); discovery question count distribution (flag reps consistently below 5/call); at-risk call count by rep and week; and a leaderboard of calls with the highest buying-signal density (these are good listen-back examples for team training). → produces: dashboard
