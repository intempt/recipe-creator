---
name: daily-sdr-task-queue
description: Use when a user mentions "daily SDR task queue", "SDR prioritized queue", "outbound prioritization workflow", or asks for related help. Every morning, build each SDR a prioritized daily task queue, ranked by signal strength (PQL / PQA / pricing-page intent / target-account match) and recency, capped at a manageable daily volume, so SDRs work the highest-value signals first instead of working their queue chronologically.
arguments: []
intempt:
  id: daily-sdr-task-queue
  title: "Daily SDR task queue"
  version: 1.0.0
  slashCommand: /daily-sdr-task-queue
  group: Workflows
  shortDescription: "Ranks each SDR's open tasks by how strong and how fresh the signal is and sends them the top 25 every morning, instead of a chronological list."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [sdr-prioritization, daily-queue, scheduled-rollup]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - build_insights_report
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Rank every task by signal"
      command: create_ai_attribute
      produces: attribute
      bindsAs: task_priority
      description: "A score out of 150 per task. The source is worth 50 for a product qualified account, 40 for a product qualified lead, 35 for pricing intent, 30 for a target account and 10 for a cold follow up. Signals under a day old are multiplied by 1.5 and anything over a week by 0.4, ideal ICP fit by 1.3 and marginal by 0.5, and enterprise accounts by 1.5."
      prompt: 'Create an AI-derived attribute ''task_priority_score'' on the Task object. Composite: (a) signal source weight: PQA: 50, PQL: 40, pricing-intent: 35, named-account-touch: 30, generic-inbound: 20, cold-outbound-followup: 10; (b) recency multiplier (fresh signal (<24hr) × 1.5, day-2 × 1.0, day-3-7 × 0.7, day-8+ × 0.4; (c) ICP fit boost) ideal-tier accounts × 1.3, viable × 1.0, marginal × 0.5; (d) account size weight: enterprise tier × 1.5. Output: 0-150 score for ranking.'
    - step: 2
      title: "Cut it to 25 a day"
      command: build_insights_report
      produces: report
      bindsAs: report
      dependsOn:
      - task_priority
      description: "Per SDR, the top 25 open tasks by that score, each showing the signal, the account, its ICP tier, how many days since the signal fired, and a suggested opening angle. It stops at 25 because that is roughly what one person can work in a day."
      prompt: 'Build a report ''SDR daily queue snapshot'' computing, per SDR, their top 25 open tasks ranked by task_priority_score, with each task showing: signal source (PQL / PQA / intent), account name, ICP tier, days since signal fired, suggested first-touch angle (based on signal type and account context). Caps queue at 25 because SDR daily-touch capacity is realistically 20-25 outreaches.'
    - step: 3
      title: "Deliver it at 8am"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - task_priority
      - report
      description: "Every working day in each SDR's own timezone: it rescores the open tasks so overnight signals count, builds each queue, sends it by Slack DM with a link per task, and gives the manager the team picture, including anyone under 10 tasks or over 50. Weekends and holidays are skipped."
      prompt: 'Create a scheduled workflow firing every business day at 8am local time per SDR (timezone-aware). Step sequence: (1) refresh task_priority_score across all open SDR tasks (catches new signals from overnight); (2) generate each SDR''s top-25 queue; (3) deliver via Slack DM to the SDR with the prioritized list and one-click links to each task; (4) post a team-level summary to the SDR manager: queue-size distribution (any SDR with <10 tasks = underfed, >50 = backlog), top signal sources today, ICP-tier mix. Skip on weekends and holidays.'
    - step: 4
      title: "Check the ranking is right"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - task_priority
      - report
      - workflow
      description: "How many SDRs actually get their queue, how many tasks they work against how many they were sent, whether the top five convert better than the rest, and a leaderboard on how fast signals become meetings."
      prompt: 'Compose an SDR productivity dashboard: daily-queue delivery rate (% of SDRs receiving their queue daily: operational health), tasks worked per SDR per day vs. queue-size delivered (working-rate), top-of-queue conversion (% of #1-#5 priority tasks that converted to meeting vs. lower-ranked), and rep-leaderboard on signal-to-meeting velocity. Surfaces whether the prioritization model is actually directing SDRs to the right targets.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Insights Report produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Daily SDR task queue

Ranks each SDR's open tasks by how strong and how fresh the signal is and sends them the top 25 every morning, instead of a chronological list.

## Before you run it

- Connect slack

## What it does

1. **Rank every task by signal** (`create_ai_attribute`)

   A score out of 150 per task. The source is worth 50 for a product qualified account, 40 for a product qualified lead, 35 for pricing intent, 30 for a target account and 10 for a cold follow up. Signals under a day old are multiplied by 1.5 and anything over a week by 0.4, ideal ICP fit by 1.3 and marginal by 0.5, and enterprise accounts by 1.5.

2. **Cut it to 25 a day** (`build_insights_report`)

   Per SDR, the top 25 open tasks by that score, each showing the signal, the account, its ICP tier, how many days since the signal fired, and a suggested opening angle. It stops at 25 because that is roughly what one person can work in a day.

3. **Deliver it at 8am** (`create_workflow`)

   Every working day in each SDR's own timezone: it rescores the open tasks so overnight signals count, builds each queue, sends it by Slack DM with a link per task, and gives the manager the team picture, including anyone under 10 tasks or over 50. Weekends and holidays are skipped.

4. **Check the ranking is right** (`create_dashboard`)

   How many SDRs actually get their queue, how many tasks they work against how many they were sent, whether the top five convert better than the rest, and a leaderboard on how fast signals become meetings.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **report** (report): Insights Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
