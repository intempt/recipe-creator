---
frontmatter_id: task-completion-deal-advance
slash_command: /task-completion-deal-advance
description: Moves a deal to the next stage when the task that gates it is completed, so the pipeline report is not wrong because somebody forgot.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Moves a deal forward a stage when its gating task is completed, never backward, and notifies the deal owner, so
    pipeline reports stay accurate.
  parameters:
  - name: notify_channel
    type: string
    label: Slack channel or owner handle for stage-change alerts
    default: AE owner direct message
    required: false
  requirements:
  - slot: task_completed
    kind: event
    meaning: A user completed a task linked to a deal
    properties:
    - name: advances_deal_to_stage
      type: string
      meaning: Target deal stage that completing this task should advance the deal to
      optional: true
  - slot: deal_stage_attribute
    kind: attribute
    meaning: The current pipeline stage of a deal
  - slot: deal_owner_attribute
    kind: attribute
    meaning: The account executive who owns a deal
  - slot: task_stage_mapping
    kind: attribute
    meaning: A task attribute naming the deal stage that completing the task should advance the deal to
  - slot: slack_integration
    kind: integration
    meaning: A connected Slack workspace for posting notifications
    channel: slack
  - slot: deal_pipeline_stage_order
    kind: knowledge
    meaning: The ordered list of deal stages in the sales pipeline
  - slot: stage_hygiene_report
    kind: knowledge
    meaning: A dashboard space for reviewing stage advancement and task completion data
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - task_stage_mapping
    - deal_pipeline_stage_order
    instruction: 'Create a task attribute named ''advances_deal_to_stage'' ({task_stage_mapping}). For each task template,
      set the deal stage that its completion should advance the deal to. Examples: ''Send proposal'' advances to the Proposal
      stage if the deal is currently Demo or earlier; ''Contract sent'' advances to Closing if the deal is currently Proposal;
      ''POC kickoff'' advances to Technical Evaluation. Tasks not on this list do not trigger advancement; they are informational
      tasks, not stage gates.'
  - id: s2
    builds: automation
    uses:
    - task_completed
    - deal_stage_attribute
    - deal_owner_attribute
    - slack_integration
    - notify_channel
    - deal_pipeline_stage_order
    - s1
    instruction: 'Create a workflow that fires when a task is completed ({task_completed}). (1) Check whether the task has
      ''advances_deal_to_stage'' set. (2) Look up the linked deal''s current stage ({deal_stage_attribute}). If the current
      stage is earlier than the task''s target stage, advance the deal to the target stage. (3) If the deal is already at
      or past the target stage, skip it: no regression and no double advancement. (4) When the stage changes, post a brief
      Slack notification to the deal owner ({deal_owner_attribute}) in the form ''Deal X advanced to Proposal: task Y completed'',
      sent to {notify_channel} via {slack_integration}. (5) If the advancement skips multiple stages (for example Discovery
      to Closing from one task), require human confirmation and do not auto-skip stages.'
  - id: s3
    builds: dashboard
    uses:
    - task_completed
    - deal_stage_attribute
    - deal_pipeline_stage_order
    - stage_hygiene_report
    - s1
    - s2
    instruction: 'Build a stage-hygiene dashboard with three views: (a) stage-advancement rate, comparing deals advanced by
      task-completion automation against deals advanced by manual stage edits by reps; (b) tasks completed without the expected
      stage advancement, which signals either a wrong task-to-stage mapping or a rep marking a task complete without doing
      the work; (c) median time-in-stage for each pipeline stage. Use it to check that the mapping is sound and that reps
      are using tasks honestly.'
---

# Advance the deal when a task is done

Slash command: /task-completion-deal-advance

## Step 1: Map tasks to the stage they gate

Create an attribute on the Task object: 'advances_deal_to_stage'. For each task template, define the deal stage that completion should advance to. Examples: 'Send proposal' to advances deal to Proposal stage if currently Demo or earlier; 'Contract sent' to advances to Closing if currently Proposal; 'POC kickoff' to advances to Technical Evaluation. Tasks not on this list don't trigger advancement (they're informational tasks, not stage-gates).

## Step 2: Move it forward, never back

Create a workflow firing on Task completed. Step sequence: (1) check whether the task has 'advances_deal_to_stage' set; (2) look up the linked deal: IF the deal's current stage is earlier than the task's target stage, advance the deal via move_deal_stage; (3) if the deal is already at or past the target stage, skip (no regression, no double-advance); (4) on stage change, post a brief Slack notification to the AE owner ('Deal X advanced to Proposal: task Y completed') so they have realtime visibility; (5) if the advancement skips multiple stages (e.g. Discovery to Closing in one task), require human confirmation: don't auto-skip stages. Use the result of "Map tasks to the stage they gate".

## Step 3: Audit the mapping

Compose a stage-hygiene dashboard: stage-advancement rate (deals advanced via task-completion auto-advance vs. manual stage edit by rep), tasks completed without expected stage advance (signal of wrong task to stage mapping, OR rep marking task complete without doing the work), and median time-in-stage by stage (should decrease with reliable auto-advancement). Auditing tool for RevOps to validate the mapping is sane and reps are using tasks honestly. Use the result of "Map tasks to the stage they gate", "Move it forward, never back".
