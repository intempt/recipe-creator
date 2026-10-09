---
description: Moves a deal to the next stage when the task that gates it is completed, so the pipeline report is not wrong because somebody forgot.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Advance the deal when a task is done

Slash command: /task-completion-deal-advance

## Step 1: Map tasks to the stage they gate

Create an attribute on the Task object: 'advances_deal_to_stage'. For each task template, define the deal stage that completion should advance to. Examples: 'Send proposal' to advances deal to Proposal stage if currently Demo or earlier; 'Contract sent' to advances to Closing if currently Proposal; 'POC kickoff' to advances to Technical Evaluation. Tasks not on this list don't trigger advancement (they're informational tasks, not stage-gates).

## Step 2: Move it forward, never back

Create a workflow firing on Task completed. Step sequence: (1) check whether the task has 'advances_deal_to_stage' set; (2) look up the linked deal: IF the deal's current stage is earlier than the task's target stage, advance the deal via move_deal_stage; (3) if the deal is already at or past the target stage, skip (no regression, no double-advance); (4) on stage change, post a brief Slack notification to the AE owner ('Deal X advanced to Proposal: task Y completed') so they have realtime visibility; (5) if the advancement skips multiple stages (e.g. Discovery to Closing in one task), require human confirmation: don't auto-skip stages. Use the result of "Map tasks to the stage they gate".

## Step 3: Audit the mapping

Compose a stage-hygiene dashboard: stage-advancement rate (deals advanced via task-completion auto-advance vs. manual stage edit by rep), tasks completed without expected stage advance (signal of wrong task to stage mapping, OR rep marking task complete without doing the work), and median time-in-stage by stage (should decrease with reliable auto-advancement). Auditing tool for RevOps to validate the mapping is sane and reps are using tasks honestly. Use the result of "Map tasks to the stage they gate", "Move it forward, never back".
