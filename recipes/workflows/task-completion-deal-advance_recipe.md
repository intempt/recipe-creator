---
name: task-completion-deal-advance
description: Use when a user mentions "task completion deal advance", "auto-advance deal on task complete", "task-driven stage progression", or asks for related help. When a task on a deal is completed (proposal sent, contract delivered, demo done), conditionally advance the deal's stage and notify stakeholders, removes the 'forgot to move the deal stage' problem that breaks every pipeline report.
arguments: []
intempt:
  id: task-completion-deal-advance
  title: "Advance the deal when a task is done"
  version: 1.0.0
  slashCommand: /task-completion-deal-advance
  group: Workflows
  shortDescription: "Moves a deal to the next stage when the task that gates it is completed, so the pipeline report is not wrong because somebody forgot."
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
      title: "Map tasks to the stage they gate"
      command: create_attribute
      produces: attribute
      bindsAs: task_stage_map
      description: "Per task template, the stage that completing it should move the deal to. Sending a proposal moves it to proposal if it is at demo or earlier, a contract sent moves it to closing from proposal, a proof of concept kickoff moves it to technical evaluation. Tasks not on this list are informational and move nothing."
      prompt: 'Create an attribute on the Task object: ''advances_deal_to_stage''. For each task template, define the deal stage that completion should advance to. Examples: ''Send proposal'' to advances deal to Proposal stage if currently Demo or earlier; ''Contract sent'' to advances to Closing if currently Proposal; ''POC kickoff'' to advances to Technical Evaluation. Tasks not on this list don''t trigger advancement (they''re informational tasks, not stage-gates).'
    - step: 2
      title: "Move it forward, never back"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - task_stage_map
      description: "When a task completes it checks whether that task gates a stage, finds the linked deal, and advances it only if the deal is behind that stage, never when it is already at or past it. On a move it posts a short Slack note to the AE. A jump of more than one stage needs a human to confirm."
      prompt: 'Create a workflow firing on task_completed. Step sequence: (1) check whether the task has ''advances_deal_to_stage'' set; (2) look up the linked deal: IF the deal''s current stage is earlier than the task''s target stage, advance the deal via move_deal_stage; (3) if the deal is already at or past the target stage, skip (no regression, no double-advance); (4) on stage change, post a brief Slack notification to the AE owner (''Deal X advanced to Proposal: task Y completed'') so they have realtime visibility; (5) if the advancement skips multiple stages (e.g. Discovery to Closing in one task), require human confirmation: don''t auto-skip stages.'
    - step: 3
      title: "Audit the mapping"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - task_stage_map
      - workflow
      description: "How many deals advance automatically against how many reps move by hand, how often a gating task is completed with no advance, which means the mapping is wrong or the work was not really done, and the median time in each stage, which should fall as the automation becomes reliable."
      prompt: 'Compose a stage-hygiene dashboard: stage-advancement rate (deals advanced via task-completion auto-advance vs. manual stage edit by rep), tasks completed without expected stage advance (signal of wrong task to stage mapping, OR rep marking task complete without doing the work), and median time-in-stage by stage (should decrease with reliable auto-advancement). Auditing tool for RevOps to validate the mapping is sane and reps are using tasks honestly.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Advance the deal when a task is done

Moves a deal to the next stage when the task that gates it is completed, so the pipeline report is not wrong because somebody forgot.

## Before you run it

- Connect slack
- Send the `task_completed` event

## What it does

1. **Map tasks to the stage they gate** (`create_attribute`)

   Per task template, the stage that completing it should move the deal to. Sending a proposal moves it to proposal if it is at demo or earlier, a contract sent moves it to closing from proposal, a proof of concept kickoff moves it to technical evaluation. Tasks not on this list are informational and move nothing.

2. **Move it forward, never back** (`create_workflow`)

   When a task completes it checks whether that task gates a stage, finds the linked deal, and advances it only if the deal is behind that stage, never when it is already at or past it. On a move it posts a short Slack note to the AE. A jump of more than one stage needs a human to confirm.

3. **Audit the mapping** (`create_dashboard`)

   How many deals advance automatically against how many reps move by hand, how often a gating task is completed with no advance, which means the mapping is wrong or the work was not really done, and the median time in each stage, which should fall as the automation becomes reliable.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
