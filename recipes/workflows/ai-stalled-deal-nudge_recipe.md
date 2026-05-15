---
name: ai-stalled-deal-nudge
description: Use when a user mentions "AI stalled deal nudge", "AI re-engagement draft", "personalized stalled-deal outreach", or asks for related help. When a deal is detected as stalled, generate a personalized AI-drafted re-engagement message that references the specific blocker, last meeting context, and an offered next step — rep reviews and sends. Higher revival rate than generic 'just checking in' messages.
arguments: []
intempt:
  id: ai-stalled-deal-nudge
  version: 1.0.0
  slashCommand: /ai-stalled-deal-nudge
  group: Workflows
  shortDescription: "When a deal is detected as stalled, generate a personalized AI-drafted re-engagement message that references the specific blocker, last meeting context, and an offered next step — rep reviews and sends. Higher revival rate than generic 'just checking in' messages."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [ai-draft, deal-revival, stalled-deal]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build Stalled-Deal Nudge Context
      command: create_ai_attribute
      produces: attribute
      bindsAs: nudge_context
      description: 'Create an AI-derived attribute ''nudge_context'' on the Deal object, computed when the deal enters stalled status. Aggregates: (a) which stage stalled (Discovery / Demo / Proposal / Closing — each requires different nudge angle); (b) last meeting_summary if available — most useful is the ''next step'' that was agreed and apparently not happening; (c) most recent objection raised (from call summaries); (d) any mentioned timeline / decision-window that may now be expiring; (e) replacement-stakeholder candidates if the original contact has gone quiet.'
      prompt: 'Create an AI-derived attribute ''nudge_context'' on the Deal object, computed when the deal enters stalled status. Aggregates: (a) which stage stalled (Discovery / Demo / Proposal / Closing — each requires different nudge angle); (b) last meeting_summary if available — most useful is the ''next step'' that was agreed and apparently not happening; (c) most recent objection raised (from call summaries); (d) any mentioned timeline / decision-window that may now be expiring; (e) replacement-stakeholder candidates if the original contact has gone quiet.'
    - step: 2
      title: Build AI Nudge Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - nudge_context
      description: 'Create a workflow firing when a deal is newly detected as stalled (consumer of the stalled-deal-detection workflow''s output). Step sequence: (1) compute nudge_context; (2) generate AI-drafted nudge email using the context. Distinct from the template-based nudge in stalled-deal-detection: this version is HIGHLY personalized using meeting-summary specifics (''Last time we talked, you mentioned [verbatim objection]. Has anything changed on [specific blocker]?''); (3) save draft to rep''s outbox; (4) create rep task labeled ''Review AI-drafted nudge: deal [name]'' with the draft preview; (5) Slack DM with deal context. Always rep-reviewed-before-send. If deal stays stalled 14 days after first nudge draft sent, escalate to manager with manager-version draft (this needs your sign-off).'
      prompt: 'Create a workflow firing when a deal is newly detected as stalled (consumer of the stalled-deal-detection workflow''s output). Step sequence: (1) compute nudge_context; (2) generate AI-drafted nudge email using the context. Distinct from the template-based nudge in stalled-deal-detection: this version is HIGHLY personalized using meeting-summary specifics (''Last time we talked, you mentioned [verbatim objection]. Has anything changed on [specific blocker]?''); (3) save draft to rep''s outbox; (4) create rep task labeled ''Review AI-drafted nudge: deal [name]'' with the draft preview; (5) Slack DM with deal context. Always rep-reviewed-before-send. If deal stays stalled 14 days after first nudge draft sent, escalate to manager with manager-version draft (this needs your sign-off).'
    - step: 3
      title: Build AI Nudge Effectiveness Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - nudge_context
      - workflow
      description: 'Compose an AI nudge effectiveness dashboard: stalled-deals that received AI nudge drafts (vs. drafts not yet reviewed = backlog), reply rate to AI-nudge-drafted emails vs. baseline manual nudges, revival rate (deals stage-advanced after AI nudge), and ARR resurrected via this workflow. Compare to control: stalled deals where reps wrote their own nudge — typically AI-drafted personalized nudges win on reply rate by 1.5-2x.'
      prompt: 'Compose an AI nudge effectiveness dashboard: stalled-deals that received AI nudge drafts (vs. drafts not yet reviewed = backlog), reply rate to AI-nudge-drafted emails vs. baseline manual nudges, revival rate (deals stage-advanced after AI nudge), and ARR resurrected via this workflow. Compare to control: stalled deals where reps wrote their own nudge — typically AI-drafted personalized nudges win on reply rate by 1.5-2x.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Ai Stalled Deal Nudge

## Procedure

1. **Build Stalled-Deal Nudge Context** [`create_ai_attribute`] — Create an AI-derived attribute 'nudge_context' on the Deal object, computed when the deal enters stalled status. Aggregates: (a) which stage stalled (Discovery / Demo / Proposal / Closing — each requires different nudge angle); (b) last meeting_summary if available — most useful is the 'next step' that was agreed and apparently not happening; (c) most recent objection raised (from call summaries); (d) any mentioned timeline / decision-window that may now be expiring; (e) replacement-stakeholder candidates if the original contact has gone quiet. → produces: attribute
2. **Build AI Nudge Workflow** [`create_workflow`] — Create a workflow firing when a deal is newly detected as stalled (consumer of the stalled-deal-detection workflow's output). Step sequence: (1) compute nudge_context; (2) generate AI-drafted nudge email using the context. Distinct from the template-based nudge in stalled-deal-detection: this version is HIGHLY personalized using meeting-summary specifics ('Last time we talked, you mentioned [verbatim objection]. Has anything changed on [specific blocker]?'); (3) save draft to rep's outbox; (4) create rep task labeled 'Review AI-drafted nudge: deal [name]' with the draft preview; (5) Slack DM with deal context. Always rep-reviewed-before-send. If deal stays stalled 14 days after first nudge draft sent, escalate to manager with manager-version draft (this needs your sign-off). → produces: workflow
3. **Build AI Nudge Effectiveness Dashboard** [`create_dashboard`] — Compose an AI nudge effectiveness dashboard: stalled-deals that received AI nudge drafts (vs. drafts not yet reviewed = backlog), reply rate to AI-nudge-drafted emails vs. baseline manual nudges, revival rate (deals stage-advanced after AI nudge), and ARR resurrected via this workflow. Compare to control: stalled deals where reps wrote their own nudge — typically AI-drafted personalized nudges win on reply rate by 1.5-2x. → produces: dashboard
