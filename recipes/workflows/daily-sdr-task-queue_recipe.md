---
name: daily-sdr-task-queue
description: Use when a user mentions "daily SDR task queue", "SDR prioritized queue", "outbound prioritization workflow", or asks for related help. Every morning, build each SDR a prioritized daily task queue — ranked by signal strength (PQL / PQA / pricing-page intent / target-account match) and recency, capped at a manageable daily volume — so SDRs work the highest-value signals first instead of working their queue chronologically.
arguments: []
intempt:
  id: daily-sdr-task-queue
  version: 1.0.0
  slashCommand: /daily-sdr-task-queue
  group: Workflows
  shortDescription: "Every morning, build each SDR a prioritized daily task queue — ranked by signal strength (PQL / PQA / pricing-page intent / target-account match) and recency, capped at a manageable daily volume — so SDRs work the highest-value signals first instead of working their queue chronologically."
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
  invokesCommands:
    - create_ai_attribute
    - build_insights_report
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build Task Priority Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: task_priority
      description: 'Create an AI-derived attribute ''task_priority_score'' on the Task object. Composite: (a) signal source weight — PQA: 50, PQL: 40, pricing-intent: 35, named-account-touch: 30, generic-inbound: 20, cold-outbound-followup: 10; (b) recency multiplier — fresh signal (<24hr) × 1.5, day-2 × 1.0, day-3-7 × 0.7, day-8+ × 0.4; (c) ICP fit boost — ideal-tier accounts × 1.3, viable × 1.0, marginal × 0.5; (d) account size weight — enterprise tier × 1.5. Output: 0-150 score for ranking.'
      prompt: 'Create an AI-derived attribute ''task_priority_score'' on the Task object. Composite: (a) signal source weight — PQA: 50, PQL: 40, pricing-intent: 35, named-account-touch: 30, generic-inbound: 20, cold-outbound-followup: 10; (b) recency multiplier — fresh signal (<24hr) × 1.5, day-2 × 1.0, day-3-7 × 0.7, day-8+ × 0.4; (c) ICP fit boost — ideal-tier accounts × 1.3, viable × 1.0, marginal × 0.5; (d) account size weight — enterprise tier × 1.5. Output: 0-150 score for ranking.'
    - step: 2
      title: Build SDR Queue Report
      command: build_insights_report
      produces: report
      bindsAs: report
      dependsOn:
      - task_priority
      description: 'Build a report ''SDR daily queue snapshot'' computing, per SDR, their top 25 open tasks ranked by task_priority_score, with each task showing: signal source (PQL / PQA / intent), account name, ICP tier, days since signal fired, suggested first-touch angle (based on signal type and account context). Caps queue at 25 because SDR daily-touch capacity is realistically 20-25 outreaches.'
      prompt: 'Build a report ''SDR daily queue snapshot'' computing, per SDR, their top 25 open tasks ranked by task_priority_score, with each task showing: signal source (PQL / PQA / intent), account name, ICP tier, days since signal fired, suggested first-touch angle (based on signal type and account context). Caps queue at 25 because SDR daily-touch capacity is realistically 20-25 outreaches.'
    - step: 3
      title: Build Daily Queue Delivery Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - task_priority
      - report
      description: 'Create a scheduled workflow firing every business day at 8am local time per SDR (timezone-aware). Step sequence: (1) refresh task_priority_score across all open SDR tasks (catches new signals from overnight); (2) generate each SDR''s top-25 queue; (3) deliver via Slack DM to the SDR with the prioritized list and one-click links to each task; (4) post a team-level summary to the SDR manager: queue-size distribution (any SDR with <10 tasks = underfed, >50 = backlog), top signal sources today, ICP-tier mix. Skip on weekends and holidays.'
      prompt: 'Create a scheduled workflow firing every business day at 8am local time per SDR (timezone-aware). Step sequence: (1) refresh task_priority_score across all open SDR tasks (catches new signals from overnight); (2) generate each SDR''s top-25 queue; (3) deliver via Slack DM to the SDR with the prioritized list and one-click links to each task; (4) post a team-level summary to the SDR manager: queue-size distribution (any SDR with <10 tasks = underfed, >50 = backlog), top signal sources today, ICP-tier mix. Skip on weekends and holidays.'
    - step: 4
      title: Build SDR Productivity Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - task_priority
      - report
      - workflow
      description: 'Compose an SDR productivity dashboard: daily-queue delivery rate (% of SDRs receiving their queue daily — operational health), tasks worked per SDR per day vs. queue-size delivered (working-rate), top-of-queue conversion (% of #1-#5 priority tasks that converted to meeting vs. lower-ranked), and rep-leaderboard on signal-to-meeting velocity. Surfaces whether the prioritization model is actually directing SDRs to the right targets.'
      prompt: 'Compose an SDR productivity dashboard: daily-queue delivery rate (% of SDRs receiving their queue daily — operational health), tasks worked per SDR per day vs. queue-size delivered (working-rate), top-of-queue conversion (% of #1-#5 priority tasks that converted to meeting vs. lower-ranked), and rep-leaderboard on signal-to-meeting velocity. Surfaces whether the prioritization model is actually directing SDRs to the right targets.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Insights Report produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Daily Sdr Task Queue

## Procedure

1. **Build Task Priority Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'task_priority_score' on the Task object. Composite: (a) signal source weight — PQA: 50, PQL: 40, pricing-intent: 35, named-account-touch: 30, generic-inbound: 20, cold-outbound-followup: 10; (b) recency multiplier — fresh signal (<24hr) × 1.5, day-2 × 1.0, day-3-7 × 0.7, day-8+ × 0.4; (c) ICP fit boost — ideal-tier accounts × 1.3, viable × 1.0, marginal × 0.5; (d) account size weight — enterprise tier × 1.5. Output: 0-150 score for ranking. → produces: attribute
2. **Build SDR Queue Report** [`build_insights_report`] — Build a report 'SDR daily queue snapshot' computing, per SDR, their top 25 open tasks ranked by task_priority_score, with each task showing: signal source (PQL / PQA / intent), account name, ICP tier, days since signal fired, suggested first-touch angle (based on signal type and account context). Caps queue at 25 because SDR daily-touch capacity is realistically 20-25 outreaches. → produces: report
3. **Build Daily Queue Delivery Workflow** [`create_workflow`] — Create a scheduled workflow firing every business day at 8am local time per SDR (timezone-aware). Step sequence: (1) refresh task_priority_score across all open SDR tasks (catches new signals from overnight); (2) generate each SDR's top-25 queue; (3) deliver via Slack DM to the SDR with the prioritized list and one-click links to each task; (4) post a team-level summary to the SDR manager: queue-size distribution (any SDR with <10 tasks = underfed, >50 = backlog), top signal sources today, ICP-tier mix. Skip on weekends and holidays. → produces: workflow
4. **Build SDR Productivity Dashboard** [`create_dashboard`] — Compose an SDR productivity dashboard: daily-queue delivery rate (% of SDRs receiving their queue daily — operational health), tasks worked per SDR per day vs. queue-size delivered (working-rate), top-of-queue conversion (% of #1-#5 priority tasks that converted to meeting vs. lower-ranked), and rep-leaderboard on signal-to-meeting velocity. Surfaces whether the prioritization model is actually directing SDRs to the right targets. → produces: dashboard
