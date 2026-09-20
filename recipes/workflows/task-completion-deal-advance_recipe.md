---
name: task-completion-deal-advance
description: Use when a user mentions "task completion deal advance", "auto-advance deal on task complete", "task-driven stage progression", or asks for related help. When a task on a deal is completed (proposal sent, contract delivered, demo done), conditionally advance the deal's stage and notify stakeholders — removes the 'forgot to move the deal stage' problem that breaks every pipeline report.
arguments: []
intempt:
  id: task-completion-deal-advance
  version: 1.0.0
  slashCommand: /task-completion-deal-advance
  group: Workflows
  shortDescription: 'When a task on a deal is completed (proposal sent, contract delivered, demo done), conditionally advance the deal''s stage and notify stakeholders: removes the ''forgot to move the deal stage'' problem that breaks every pipeline report.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [deal-hygiene, auto-advance, stage-management]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: task_completed, severity: blocking }
  invokesCommands:
    - create_attribute
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build Task-to-Stage Mapping
      command: create_attribute
      produces: attribute
      bindsAs: task_stage_map
      description: 'Create an attribute on the Task object: ''advances_deal_to_stage''. For each task template, define the deal stage that completion should advance to. Examples: ''Send proposal'' → advances deal to Proposal stage if currently Demo or earlier; ''Contract sent'' → advances to Closing if currently Proposal; ''POC kickoff'' → advances to Technical Evaluation. Tasks not on this list don''t trigger advancement (they''re informational tasks, not stage-gates).'
      prompt: 'Create an attribute on the Task object: ''advances_deal_to_stage''. For each task template, define the deal stage that completion should advance to. Examples: ''Send proposal'' → advances deal to Proposal stage if currently Demo or earlier; ''Contract sent'' → advances to Closing if currently Proposal; ''POC kickoff'' → advances to Technical Evaluation. Tasks not on this list don''t trigger advancement (they''re informational tasks, not stage-gates).'
    - step: 2
      title: Build Auto-Advance Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - task_stage_map
      description: 'Create a workflow firing on task_completed. Step sequence: (1) check whether the task has ''advances_deal_to_stage'' set; (2) look up the linked deal — IF the deal''s current stage is earlier than the task''s target stage, advance the deal via move_deal_stage; (3) if the deal is already at or past the target stage, skip (no regression, no double-advance); (4) on stage change, post a brief Slack notification to the AE owner (''Deal X advanced to Proposal — task Y completed'') so they have realtime visibility; (5) if the advancement skips multiple stages (e.g. Discovery → Closing in one task), require human confirmation — don''t auto-skip stages.'
      prompt: 'Create a workflow firing on task_completed. Step sequence: (1) check whether the task has ''advances_deal_to_stage'' set; (2) look up the linked deal — IF the deal''s current stage is earlier than the task''s target stage, advance the deal via move_deal_stage; (3) if the deal is already at or past the target stage, skip (no regression, no double-advance); (4) on stage change, post a brief Slack notification to the AE owner (''Deal X advanced to Proposal — task Y completed'') so they have realtime visibility; (5) if the advancement skips multiple stages (e.g. Discovery → Closing in one task), require human confirmation — don''t auto-skip stages.'
    - step: 3
      title: Build Stage Hygiene Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - task_stage_map
      - workflow
      description: 'Compose a stage-hygiene dashboard: stage-advancement rate (deals advanced via task-completion auto-advance vs. manual stage edit by rep), tasks completed without expected stage advance (signal of wrong task→stage mapping, OR rep marking task complete without doing the work), and median time-in-stage by stage (should decrease with reliable auto-advancement). Auditing tool for RevOps to validate the mapping is sane and reps are using tasks honestly.'
      prompt: 'Compose a stage-hygiene dashboard: stage-advancement rate (deals advanced via task-completion auto-advance vs. manual stage edit by rep), tasks completed without expected stage advance (signal of wrong task→stage mapping, OR rep marking task complete without doing the work), and median time-in-stage by stage (should decrease with reliable auto-advancement). Auditing tool for RevOps to validate the mapping is sane and reps are using tasks honestly.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Task Completion Deal Advance

## Procedure

1. **Build Task-to-Stage Mapping** [`create_attribute`] — Create an attribute on the Task object: 'advances_deal_to_stage'. For each task template, define the deal stage that completion should advance to. Examples: 'Send proposal' → advances deal to Proposal stage if currently Demo or earlier; 'Contract sent' → advances to Closing if currently Proposal; 'POC kickoff' → advances to Technical Evaluation. Tasks not on this list don't trigger advancement (they're informational tasks, not stage-gates). → produces: attribute
2. **Build Auto-Advance Workflow** [`create_workflow`] — Create a workflow firing on task_completed. Step sequence: (1) check whether the task has 'advances_deal_to_stage' set; (2) look up the linked deal — IF the deal's current stage is earlier than the task's target stage, advance the deal via move_deal_stage; (3) if the deal is already at or past the target stage, skip (no regression, no double-advance); (4) on stage change, post a brief Slack notification to the AE owner ('Deal X advanced to Proposal — task Y completed') so they have realtime visibility; (5) if the advancement skips multiple stages (e.g. Discovery → Closing in one task), require human confirmation — don't auto-skip stages. → produces: workflow
3. **Build Stage Hygiene Dashboard** [`create_dashboard`] — Compose a stage-hygiene dashboard: stage-advancement rate (deals advanced via task-completion auto-advance vs. manual stage edit by rep), tasks completed without expected stage advance (signal of wrong task→stage mapping, OR rep marking task complete without doing the work), and median time-in-stage by stage (should decrease with reliable auto-advancement). Auditing tool for RevOps to validate the mapping is sane and reps are using tasks honestly. → produces: dashboard
