---
name: stalled-deal-detection
description: Use when a user mentions "stalled deal detection", "stale pipeline alert", "deal at risk workflow", or asks for related help. Detect deals stuck in a stage longer than typical for that stage's median age, with no recent activity, and surface them with AI-drafted re-engagement nudges so reps can either revive or honestly close-lost (no more pipeline lying).
arguments: []
intempt:
  id: stalled-deal-detection
  title: "Stalled deal detection"
  version: 1.0.0
  slashCommand: /stalled-deal-detection
  group: Workflows
  shortDescription: "Finds deals sitting in a stage far longer than usual with no activity, drafts a nudge that fits the stage, and escalates if they stay stuck."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [deal-hygiene, stalled-deals, pipeline-quality]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: deal_stage_changed, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Measure how long it has sat"
      command: create_ai_attribute
      produces: attribute
      bindsAs: stage_age
      description: "Refreshed daily: the days since the deal last changed stage, and where that sits against the historical median for that stage among similar deals by size, segment and rep. Anything in the top quartile is flagged, alongside the days since any meeting, email reply or completed task."
      prompt: 'Create an AI-derived attribute ''days_in_current_stage'' on the Deal object, refreshed daily. Compute: (a) calendar days since the deal last changed stage; (b) percentile of this age within the stage''s historical median for similar deals (size, segment, rep). Flag deals where age is in the top quartile (75th+ percentile) for that stage. Also compute ''days_since_last_activity'' (any meeting / email reply / task completion on the deal).'
    - step: 2
      title: "Find the genuinely stuck ones"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - stage_age
      description: "Open deals in the top quartile for time in stage with no activity for 14 days or more. Deals a rep has deliberately paused, for a restart next quarter or similar, are left out. Refreshed daily."
      prompt: Build a segment 'Stalled deals' capturing open deals where (a) days_in_current_stage is in the top quartile for that stage AND (b) days_since_last_activity >= 14 days. Excludes deals where the rep has manually set a 'paused' flag (legitimate pause, coming back next quarter, etc.). Refreshed daily.
    - step: 3
      title: "Write a nudge per stage"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - stage_age
      - segment
      description: "Discovery re-asks the qualifying question that never got answered. Demo offers a technical deep dive or a proof of concept. Proposal names the likely truth, that pricing pushback usually means the decision maker is not sold, and offers to align. Closing asks directly about the timeline and what is still in the way. Personalised from the last meeting summary, and sent by the rep."
      prompt: 'Generate an AI-drafted re-engagement email template. The AI picks angle based on stalled-stage: (a) Discovery stalled (re-ask the qualifying question that wasn''t answered; (b) Demo stalled) offer technical deep-dive or POC; (c) Proposal stalled (surface that pricing pushback usually means decision-maker isn''t bought in, offer to align; (d) Closing stalled) explicit clarity-ask about timeline + remaining blockers. Personalized to last meeting summary if available. Tone: direct, low-pressure, honest. The rep reviews and sends: not auto-send.'
    - step: 4
      title: "Draft it and chase the rep"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - stage_age
      - segment
      - asset
      description: "Daily, for deals that became stalled in the last 24 hours: it writes the nudge from the template and the deal context, creates a review task for the owner with the draft attached, messages them in Slack with a preview, and escalates to their manager if the same deal is still stalled 14 days after the first nudge, which usually means it should be closed lost. Nothing sends automatically."
      prompt: 'Create a workflow firing daily for newly-stalled deals (deals that crossed into stalled-segment in the last 24 hours). Step sequence: (1) compose AI nudge draft using the asset template + deal context; (2) create a task for the deal owner labeled ''Review and send: stalled deal nudge'' with the draft pre-attached; (3) post Slack DM to the rep with deal name + draft preview + ''review'' button; (4) escalate to manager via Slack if same deal is still stalled 14 days after first nudge task (signal: deal should probably be closed-lost). Don''t auto-send the email: rep must review.'
    - step: 5
      title: "See what is really dead"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - stage_age
      - segment
      - asset
      - workflow
      description: "Stalled deals by stage and rep, the ARR sitting in them, their median age, how many recover and move forward, and how many sit stalled for 30 days or more before being marked lost, which shows which reps let deals linger instead of closing them out honestly."
      prompt: 'Compose a stalled-deal dashboard: count of stalled deals by stage and rep, total ARR at risk (sum of stalled deals'' values), median age of stalled deals, recovery rate (stalled deals that re-engaged and moved stage forward), and dishonesty rate (stalled deals that should have been closed-lost: measured as deals that stay stalled 30+ days before eventually being marked lost). Manager view: which reps consistently let deals stall vs. honestly close-lost.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Stalled deal detection

Finds deals sitting in a stage far longer than usual with no activity, drafts a nudge that fits the stage, and escalates if they stay stuck.

## Before you run it

- Connect slack
- Send the `deal_stage_changed` event

## What it does

1. **Measure how long it has sat** (`create_ai_attribute`)

   Refreshed daily: the days since the deal last changed stage, and where that sits against the historical median for that stage among similar deals by size, segment and rep. Anything in the top quartile is flagged, alongside the days since any meeting, email reply or completed task.

2. **Find the genuinely stuck ones** (`create_segment`)

   Open deals in the top quartile for time in stage with no activity for 14 days or more. Deals a rep has deliberately paused, for a restart next quarter or similar, are left out. Refreshed daily.

3. **Write a nudge per stage** (`create_email_content`)

   Discovery re-asks the qualifying question that never got answered. Demo offers a technical deep dive or a proof of concept. Proposal names the likely truth, that pricing pushback usually means the decision maker is not sold, and offers to align. Closing asks directly about the timeline and what is still in the way. Personalised from the last meeting summary, and sent by the rep.

4. **Draft it and chase the rep** (`create_workflow`)

   Daily, for deals that became stalled in the last 24 hours: it writes the nudge from the template and the deal context, creates a review task for the owner with the draft attached, messages them in Slack with a preview, and escalates to their manager if the same deal is still stalled 14 days after the first nudge, which usually means it should be closed lost. Nothing sends automatically.

5. **See what is really dead** (`create_dashboard`)

   Stalled deals by stage and rep, the ARR sitting in them, their median age, how many recover and move forward, and how many sit stalled for 30 days or more before being marked lost, which shows which reps let deals linger instead of closing them out honestly.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
