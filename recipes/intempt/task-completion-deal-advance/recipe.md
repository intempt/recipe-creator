---
id: task-completion-deal-advance
title: Advance the deal when a task is done
slash_command: /task-completion-deal-advance
group: Workflows
owner: intempt
summary: Moves a deal to the next stage when the task that gates it is completed, so the pipeline report
  is not wrong because somebody forgot.
description: >-
  When a task on a deal is completed (proposal sent, contract delivered, demo done), conditionally advance
  the deal's stage and notify stakeholders, removes the 'forgot to move the deal stage' problem that breaks
  every pipeline report.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - deal-hygiene
    - auto-advance
    - stage-management
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: task_completed
      severity: blocking
touches:
  reads:
    - The task_completed event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Map tasks to the stage they gate"
    - A new workflow, from step 2 "Move it forward, never back"
    - A new dashboard, from step 3 "Audit the mapping"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Map tasks to the stage they gate
    summary: >-
      Per task template, the stage that completing it should move the deal to. Sending a proposal moves
      it to proposal if it is at demo or earlier, a contract sent moves it to closing from proposal, a
      proof of concept kickoff moves it to technical evaluation. Tasks not on this list are informational
      and move nothing.
    builds: attribute
    description: >-
      Create an attribute on the Task object: 'advances_deal_to_stage'. For each task template, define
      the deal stage that completion should advance to. Examples: 'Send proposal' to advances deal to
      Proposal stage if currently Demo or earlier; 'Contract sent' to advances to Closing if currently
      Proposal; 'POC kickoff' to advances to Technical Evaluation. Tasks not on this list don't trigger
      advancement (they're informational tasks, not stage-gates).
  - id: s2
    title: Move it forward, never back
    summary: >-
      When a task completes it checks whether that task gates a stage, finds the linked deal, and advances
      it only if the deal is behind that stage, never when it is already at or past it. On a move it posts
      a short Slack note to the AE. A jump of more than one stage needs a human to confirm.
    builds: workflow
    description: >-
      Create a workflow firing on task_completed. Step sequence: (1) check whether the task has 'advances_deal_to_stage'
      set; (2) look up the linked deal: IF the deal's current stage is earlier than the task's target
      stage, advance the deal via move_deal_stage; (3) if the deal is already at or past the target stage,
      skip (no regression, no double-advance); (4) on stage change, post a brief Slack notification to
      the AE owner ('Deal X advanced to Proposal: task Y completed') so they have realtime visibility;
      (5) if the advancement skips multiple stages (e.g. Discovery to Closing in one task), require human
      confirmation: don't auto-skip stages. Use the result of "Map tasks to the stage they gate".
    dependsOn:
      - s1
  - id: s3
    title: Audit the mapping
    summary: >-
      How many deals advance automatically against how many reps move by hand, how often a gating task
      is completed with no advance, which means the mapping is wrong or the work was not really done,
      and the median time in each stage, which should fall as the automation becomes reliable.
    builds: dashboard
    description: >-
      Compose a stage-hygiene dashboard: stage-advancement rate (deals advanced via task-completion auto-advance
      vs. manual stage edit by rep), tasks completed without expected stage advance (signal of wrong task
      to stage mapping, OR rep marking task complete without doing the work), and median time-in-stage
      by stage (should decrease with reliable auto-advancement). Auditing tool for RevOps to validate
      the mapping is sane and reps are using tasks honestly. Use the result of "Map tasks to the stage
      they gate", "Move it forward, never back".
    dependsOn:
      - s1
      - s2
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Advance the deal when a task is done

Moves a deal to the next stage when the task that gates it is completed, so the pipeline report is not wrong because somebody forgot.

## Steps

1. **Map tasks to the stage they gate** (builds attribute)

   Per task template, the stage that completing it should move the deal to. Sending a proposal moves it to proposal if it is at demo or earlier, a contract sent moves it to closing from proposal, a proof of concept kickoff moves it to technical evaluation. Tasks not on this list are informational and move nothing.

2. **Move it forward, never back** (builds workflow)

   When a task completes it checks whether that task gates a stage, finds the linked deal, and advances it only if the deal is behind that stage, never when it is already at or past it. On a move it posts a short Slack note to the AE. A jump of more than one stage needs a human to confirm.

3. **Audit the mapping** (builds dashboard)

   How many deals advance automatically against how many reps move by hand, how often a gating task is completed with no advance, which means the mapping is wrong or the work was not really done, and the median time in each stage, which should fall as the automation becomes reliable.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The task_completed event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Map tasks to the stage they gate"
- A new workflow, from step 2 "Move it forward, never back"
- A new dashboard, from step 3 "Audit the mapping"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
