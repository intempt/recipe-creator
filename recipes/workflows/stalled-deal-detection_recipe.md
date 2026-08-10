---
name: stalled-deal-detection
description: Use when a user mentions "stalled deal detection", "stale pipeline alert", "deal at risk workflow", or asks for related help. Detect deals stuck in a stage longer than typical for that stage's median age, with no recent activity, and surface them with AI-drafted re-engagement nudges so reps can either revive or honestly close-lost (no more pipeline lying).
arguments: []
intempt:
  id: stalled-deal-detection
  version: 1.0.0
  slashCommand: /stalled-deal-detection
  group: Workflows
  shortDescription: "Detect deals stuck in a stage longer than typical for that stage's median age, with no recent activity, and surface them with AI-drafted re-engagement nudges so reps can either revive or honestly close-lost (no more pipeline lying)."
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
      title: Compute Deal Stage Age
      command: create_ai_attribute
      produces: attribute
      bindsAs: stage_age
      description: 'Create an AI-derived attribute ''days_in_current_stage'' on the Deal object, refreshed daily. Compute: (a) calendar days since the deal last changed stage; (b) percentile of this age within the stage''s historical median for similar deals (size, segment, rep). Flag deals where age is in the top quartile (75th+ percentile) for that stage. Also compute ''days_since_last_activity'' (any meeting / email reply / task completion on the deal).'
      prompt: 'Create an AI-derived attribute ''days_in_current_stage'' on the Deal object, refreshed daily. Compute: (a) calendar days since the deal last changed stage; (b) percentile of this age within the stage''s historical median for similar deals (size, segment, rep). Flag deals where age is in the top quartile (75th+ percentile) for that stage. Also compute ''days_since_last_activity'' (any meeting / email reply / task completion on the deal).'
    - step: 2
      title: Identify Stalled Deals
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - stage_age
      description: Build a segment 'Stalled deals' capturing open deals where (a) days_in_current_stage is in the top quartile for that stage AND (b) days_since_last_activity >= 14 days. Excludes deals where the rep has manually set a 'paused' flag (legitimate pause — coming back next quarter, etc.). Refreshed daily.
      prompt: Build a segment 'Stalled deals' capturing open deals where (a) days_in_current_stage is in the top quartile for that stage AND (b) days_since_last_activity >= 14 days. Excludes deals where the rep has manually set a 'paused' flag (legitimate pause — coming back next quarter, etc.). Refreshed daily.
    - step: 3
      title: Build AI Nudge Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - stage_age
      - segment
      description: 'Generate an AI-drafted re-engagement email template. The AI picks angle based on stalled-stage: (a) Discovery stalled — re-ask the qualifying question that wasn''t answered; (b) Demo stalled — offer technical deep-dive or POC; (c) Proposal stalled — surface that pricing pushback usually means decision-maker isn''t bought in, offer to align; (d) Closing stalled — explicit clarity-ask about timeline + remaining blockers. Personalized to last meeting summary if available. Tone: direct, low-pressure, honest. The rep reviews and sends — not auto-send.'
      prompt: 'Generate an AI-drafted re-engagement email template. The AI picks angle based on stalled-stage: (a) Discovery stalled — re-ask the qualifying question that wasn''t answered; (b) Demo stalled — offer technical deep-dive or POC; (c) Proposal stalled — surface that pricing pushback usually means decision-maker isn''t bought in, offer to align; (d) Closing stalled — explicit clarity-ask about timeline + remaining blockers. Personalized to last meeting summary if available. Tone: direct, low-pressure, honest. The rep reviews and sends — not auto-send.'
    - step: 4
      title: Build Stalled-Deal Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - stage_age
      - segment
      - asset
      description: 'Create a workflow firing daily for newly-stalled deals (deals that crossed into stalled-segment in the last 24 hours). Step sequence: (1) compose AI nudge draft using the asset template + deal context; (2) create a task for the deal owner labeled ''Review and send: stalled deal nudge'' with the draft pre-attached; (3) post Slack DM to the rep with deal name + draft preview + ''review'' button; (4) escalate to manager via Slack if same deal is still stalled 14 days after first nudge task (signal: deal should probably be closed-lost). Don''t auto-send the email — rep must review.'
      prompt: 'Create a workflow firing daily for newly-stalled deals (deals that crossed into stalled-segment in the last 24 hours). Step sequence: (1) compose AI nudge draft using the asset template + deal context; (2) create a task for the deal owner labeled ''Review and send: stalled deal nudge'' with the draft pre-attached; (3) post Slack DM to the rep with deal name + draft preview + ''review'' button; (4) escalate to manager via Slack if same deal is still stalled 14 days after first nudge task (signal: deal should probably be closed-lost). Don''t auto-send the email — rep must review.'
    - step: 5
      title: Build Stalled-Deal Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - stage_age
      - segment
      - asset
      - workflow
      description: 'Compose a stalled-deal dashboard: count of stalled deals by stage and rep, total ARR at risk (sum of stalled deals'' values), median age of stalled deals, recovery rate (stalled deals that re-engaged and moved stage forward), and dishonesty rate (stalled deals that should have been closed-lost — measured as deals that stay stalled 30+ days before eventually being marked lost). Manager view: which reps consistently let deals stall vs. honestly close-lost.'
      prompt: 'Compose a stalled-deal dashboard: count of stalled deals by stage and rep, total ARR at risk (sum of stalled deals'' values), median age of stalled deals, recovery rate (stalled deals that re-engaged and moved stage forward), and dishonesty rate (stalled deals that should have been closed-lost — measured as deals that stay stalled 30+ days before eventually being marked lost). Manager view: which reps consistently let deals stall vs. honestly close-lost.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Stalled Deal Detection

## Procedure

1. **Compute Deal Stage Age** [`create_ai_attribute`] — Create an AI-derived attribute 'days_in_current_stage' on the Deal object, refreshed daily. Compute: (a) calendar days since the deal last changed stage; (b) percentile of this age within the stage's historical median for similar deals (size, segment, rep). Flag deals where age is in the top quartile (75th+ percentile) for that stage. Also compute 'days_since_last_activity' (any meeting / email reply / task completion on the deal). → produces: attribute
2. **Identify Stalled Deals** [`create_segment`] — Build a segment 'Stalled deals' capturing open deals where (a) days_in_current_stage is in the top quartile for that stage AND (b) days_since_last_activity >= 14 days. Excludes deals where the rep has manually set a 'paused' flag (legitimate pause — coming back next quarter, etc.). Refreshed daily. → produces: segment
3. **Build AI Nudge Content** [`create_email_content`] — Generate an AI-drafted re-engagement email template. The AI picks angle based on stalled-stage: (a) Discovery stalled — re-ask the qualifying question that wasn't answered; (b) Demo stalled — offer technical deep-dive or POC; (c) Proposal stalled — surface that pricing pushback usually means decision-maker isn't bought in, offer to align; (d) Closing stalled — explicit clarity-ask about timeline + remaining blockers. Personalized to last meeting summary if available. Tone: direct, low-pressure, honest. The rep reviews and sends — not auto-send. → produces: asset
4. **Build Stalled-Deal Workflow** [`create_workflow`] — Create a workflow firing daily for newly-stalled deals (deals that crossed into stalled-segment in the last 24 hours). Step sequence: (1) compose AI nudge draft using the asset template + deal context; (2) create a task for the deal owner labeled 'Review and send: stalled deal nudge' with the draft pre-attached; (3) post Slack DM to the rep with deal name + draft preview + 'review' button; (4) escalate to manager via Slack if same deal is still stalled 14 days after first nudge task (signal: deal should probably be closed-lost). Don't auto-send the email — rep must review. → produces: workflow
5. **Build Stalled-Deal Dashboard** [`create_dashboard`] — Compose a stalled-deal dashboard: count of stalled deals by stage and rep, total ARR at risk (sum of stalled deals' values), median age of stalled deals, recovery rate (stalled deals that re-engaged and moved stage forward), and dishonesty rate (stalled deals that should have been closed-lost — measured as deals that stay stalled 30+ days before eventually being marked lost). Manager view: which reps consistently let deals stall vs. honestly close-lost. → produces: dashboard
