---
description: Build a prioritized report of each SDR's open tasks, ranked by signal strength and recency.
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

# Daily SDR task queue

Slash command: /daily-sdr-task-queue

## Step 1: Rank every task by signal

Create an AI-derived attribute 'task_priority_score' on the Task object. Composite: (a) signal source weight: PQA: 50, PQL: 40, pricing-intent: 35, named-account-touch: 30, generic-inbound: 20, cold-outbound-followup: 10; (b) recency multiplier (fresh signal (<24hr) × 1.5, day-2 × 1.0, day-3-7 × 0.7, day-8+ × 0.4; (c) ICP fit boost) ideal-tier accounts × 1.3, viable × 1.0, marginal × 0.5; (d) account size weight: enterprise tier × 1.5. Output: 0-150 score for ranking.

## Step 2: Cut it to 25 a day

Build a report 'SDR daily queue snapshot' computing, per SDR, their top 25 open tasks ranked by task_priority_score, with each task showing: signal source (PQL / PQA / intent), account name, ICP tier, days since signal fired, suggested first-touch angle (based on signal type and account context). Caps queue at 25 because SDR daily-touch capacity is realistically 20-25 outreaches. Use the result of "Rank every task by signal".

## Step 3: Deliver it at 8am

Create a scheduled workflow firing every business day at 8am local time per SDR (timezone-aware). Step sequence: (1) refresh task_priority_score across all open SDR tasks (catches new signals from overnight); (2) generate each SDR's top-25 queue; (3) deliver via Slack DM to the SDR with the prioritized list and one-click links to each task; (4) post a team-level summary to the SDR manager: queue-size distribution (any SDR with <10 tasks = underfed, >50 = backlog), top signal sources today, ICP-tier mix. Skip on weekends and holidays. Use the result of "Rank every task by signal", "Cut it to 25 a day".

## Step 4: Check the ranking is right

Compose an SDR productivity dashboard: daily-queue delivery rate (% of SDRs receiving their queue daily: operational health), tasks worked per SDR per day vs. queue-size delivered (working-rate), top-of-queue conversion (% of #1-#5 priority tasks that converted to meeting vs. lower-ranked), and rep-leaderboard on signal-to-meeting velocity. Surfaces whether the prioritization model is actually directing SDRs to the right targets. Use the result of "Rank every task by signal", "Cut it to 25 a day", "Deliver it at 8am".
