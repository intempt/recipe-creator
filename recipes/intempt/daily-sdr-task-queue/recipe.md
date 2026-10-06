---
id: daily-sdr-task-queue
title: Daily SDR task queue
slash_command: /daily-sdr-task-queue
group: Workflows
owner: intempt
curator: trishik
summary: >-
  Build a prioritized report of each SDR's open tasks, ranked by signal strength and recency.
description: >-
  Use PQL, PQA, pricing-page intent, and target-account match signals to rank open SDR tasks by strength and
  recency, helping teams focus on higher-value work first.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
  vertical:
    - plg
    - sales-led
  complexity: advanced
  executionMode: live
  tags:
    - sdr-prioritization
    - daily-queue
    - scheduled-rollup
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Rank every task by signal"
    - A new report, from step 2 "Cut it to 25 a day"
    - A new workflow, from step 3 "Deliver it at 8am"
    - A new dashboard, from step 4 "Check the ranking is right"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Rank every task by signal
    summary: >-
      A score out of 150 per task. The source is worth 50 for a product qualified account, 40 for a product
      qualified lead, 35 for pricing intent, 30 for a target account and 10 for a cold follow up. Signals
      under a day old are multiplied by 1.5 and anything over a week by 0.4, ideal ICP fit by 1.3 and
      marginal by 0.5, and enterprise accounts by 1.5.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'task_priority_score' on the Task object. Composite: (a) signal source
      weight: PQA: 50, PQL: 40, pricing-intent: 35, named-account-touch: 30, generic-inbound: 20, cold-outbound-followup:
      10; (b) recency multiplier (fresh signal (<24hr) × 1.5, day-2 × 1.0, day-3-7 × 0.7, day-8+ × 0.4;
      (c) ICP fit boost) ideal-tier accounts × 1.3, viable × 1.0, marginal × 0.5; (d) account size weight:
      enterprise tier × 1.5. Output: 0-150 score for ranking.
  - id: s2
    title: Cut it to 25 a day
    summary: >-
      Per SDR, the top 25 open tasks by that score, each showing the signal, the account, its ICP tier,
      how many days since the signal fired, and a suggested opening angle. It stops at 25 because that
      is roughly what one person can work in a day.
    builds: report
    description: >-
      Build a report 'SDR daily queue snapshot' computing, per SDR, their top 25 open tasks ranked by
      task_priority_score, with each task showing: signal source (PQL / PQA / intent), account name, ICP
      tier, days since signal fired, suggested first-touch angle (based on signal type and account context).
      Caps queue at 25 because SDR daily-touch capacity is realistically 20-25 outreaches. Use the result
      of "Rank every task by signal".
    dependsOn:
      - s1
  - id: s3
    title: Deliver it at 8am
    summary: >-
      Every working day in each SDR's own timezone: it rescores the open tasks so overnight signals count,
      builds each queue, sends it by Slack DM with a link per task, and gives the manager the team picture,
      including anyone under 10 tasks or over 50. Weekends and holidays are skipped.
    builds: workflow
    description: >-
      Create a scheduled workflow firing every business day at 8am local time per SDR (timezone-aware).
      Step sequence: (1) refresh task_priority_score across all open SDR tasks (catches new signals from
      overnight); (2) generate each SDR's top-25 queue; (3) deliver via Slack DM to the SDR with the prioritized
      list and one-click links to each task; (4) post a team-level summary to the SDR manager: queue-size
      distribution (any SDR with <10 tasks = underfed, >50 = backlog), top signal sources today, ICP-tier
      mix. Skip on weekends and holidays. Use the result of "Rank every task by signal", "Cut it to 25
      a day".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Check the ranking is right
    summary: >-
      How many SDRs actually get their queue, how many tasks they work against how many they were sent,
      whether the top five convert better than the rest, and a leaderboard on how fast signals become
      meetings.
    builds: dashboard
    description: >-
      Compose an SDR productivity dashboard: daily-queue delivery rate (% of SDRs receiving their queue
      daily: operational health), tasks worked per SDR per day vs. queue-size delivered (working-rate),
      top-of-queue conversion (% of #1-#5 priority tasks that converted to meeting vs. lower-ranked),
      and rep-leaderboard on signal-to-meeting velocity. Surfaces whether the prioritization model is
      actually directing SDRs to the right targets. Use the result of "Rank every task by signal", "Cut
      it to 25 a day", "Deliver it at 8am".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: report
    producedByStep: s2
    type: report
    description: Insights Report produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Daily SDR task queue

Build a prioritized report of each SDR's open tasks, ranked by signal strength and recency.

## Steps

1. **Rank every task by signal** (builds attribute)

   A score out of 150 per task. The source is worth 50 for a product qualified account, 40 for a product qualified lead, 35 for pricing intent, 30 for a target account and 10 for a cold follow up. Signals under a day old are multiplied by 1.5 and anything over a week by 0.4, ideal ICP fit by 1.3 and marginal by 0.5, and enterprise accounts by 1.5.

2. **Cut it to 25 a day** (builds report)

   Per SDR, the top 25 open tasks by that score, each showing the signal, the account, its ICP tier, how many days since the signal fired, and a suggested opening angle. It stops at 25 because that is roughly what one person can work in a day.

3. **Deliver it at 8am** (builds workflow)

   Every working day in each SDR's own timezone: it rescores the open tasks so overnight signals count, builds each queue, sends it by Slack DM with a link per task, and gives the manager the team picture, including anyone under 10 tasks or over 50. Weekends and holidays are skipped.

4. **Check the ranking is right** (builds dashboard)

   How many SDRs actually get their queue, how many tasks they work against how many they were sent, whether the top five convert better than the rest, and a leaderboard on how fast signals become meetings.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **report** (report): Insights Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new attribute, from step 1 "Rank every task by signal"
- A new report, from step 2 "Cut it to 25 a day"
- A new workflow, from step 3 "Deliver it at 8am"
- A new dashboard, from step 4 "Check the ranking is right"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, report, workflow.
