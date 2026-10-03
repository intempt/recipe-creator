---
id: rep-coaching-program
title: Weekly rep coaching rollup
slash_command: /rep-coaching-program
group: Meetings
owner: intempt
curator: sid
summary: 'Sends each manager a Monday brief on their reps: talk time against the healthy range for that
  call type, the skill to work on, and the evidence from real calls.'
description: >-
  Set up a manager-facing weekly coaching rollup: per-rep talk-listen ratio + topic coverage + leaderboard,
  delivered to managers every Monday with action-item suggestions. Turns meeting intelligence into concrete
  coaching conversations.
version: 2.0.0
classification:
  product:
    - sales
  agent: meeting-notetaker
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - coaching
    - rep-development
    - manager-tools
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A meeting action, from step 1 "Measure talk time per rep"
    - A meeting action, from step 2 "Pull each rep's skill gaps"
    - A meeting action, from step 3 "Rank the team"
    - A new workflow, from step 4 "Send managers a Monday brief"
    - A new dashboard, from step 5 "Track whether coaching lands"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Measure talk time per rep
    summary: >-
      How much each rep talked over the last 30 days by call type, against the healthy range (around 40%
      on discovery, 55% on demo), with the trend on the prior month.
    builds: meeting
    description: >-
      Compute talk-listen ratio per rep across the last 30 days of meetings, broken down by meeting type
      (rep talk % is healthy in different ranges per type: Discovery should be ~40% rep, Demo ~55% rep,
      Renewal ~40% rep). Output: per-rep current ratio, target range, gap from target, and trend vs. prior
      30 days. Flag any rep consistently outside healthy range.
  - id: s2
    title: Pull each rep's skill gaps
    summary: >-
      The top three skill areas for each rep from the last 30 days of calls, each backed by the moment
      in the transcript that shows it.
    builds: meeting
    description: >-
      For each rep, pull the system-generated coaching insights from the last 30 days of meetings. Surface:
      top 3 skill development areas (e.g. 'asks fewer than 5 discovery questions per call', 'rarely confirms
      decision-maker presence', 'pushes price too early'), with verbatim meeting snippets as evidence.
      Combine with the talk-listen analysis to form a per-rep coaching brief. Use the result of "Measure
      talk time per rep".
    dependsOn:
      - s1
  - id: s3
    title: Rank the team
    summary: >-
      Reps ranked on discovery questions per call, meetings that move a deal forward, follow-up sent within
      24 hours, and objections resolved.
    builds: meeting
    description: >-
      Build a meeting performance leaderboard for the last 30 days, ranking reps on: (1) discovery question
      count per call, (2) meeting-to-deal-progression rate, (3) follow-up-sent-within-24hr rate, (4) objection-resolution
      rate. Each metric is comparable across reps. Surface top 3 and bottom 3 per metric: top 3 become
      coaching examples (their calls get marked as good listen-back material), bottom 3 become coaching
      focus. Use the result of "Pull each rep's skill gaps".
    dependsOn:
      - s2
  - id: s4
    title: Send managers a Monday brief
    summary: >-
      Every Monday at 8am each manager gets their team's ranking, a per-rep brief with quotes from real
      calls, and a suggested action for each rep.
    builds: workflow
    description: >-
      Create a weekly scheduled workflow firing Mondays at 8am. Step sequence: (1) refresh talk-listen
      analysis, coaching insights, and leaderboard; (2) compose a manager-facing summary email per manager
      containing: their team's leaderboard position, each rep's coaching brief (skill area + verbatim
      quote evidence + suggested next-call focus), and an action item recommendation per rep ('schedule
      1:1 with [rep] this week to address [specific skill area]'); (3) post the team leaderboard to the
      manager's #sales-coaching Slack channel. Use the result of "Measure talk time per rep", "Pull each
      rep's skill gaps", "Rank the team".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Track whether coaching lands
    summary: >-
      Share of reps who got a brief in the last 7 days, week-over-week movement on the tracked metrics,
      the biggest improvements, persistent gaps, and delivery rate per manager.
    builds: dashboard
    description: >-
      Compose a coaching program dashboard showing: program health (% of reps with active coaching briefs
      received in last 7 days), week-over-week improvement on the top tracked metrics, top 5 reps showing
      largest improvements (recognition + retention signal), top 5 reps with persistent gaps (escalation
      signal), and coaching-brief delivery rate per manager (low rate = manager isn't actually engaging
      with the program). Manager-of-managers view. Use the result of "Measure talk time per rep", "Pull
      each rep's skill gaps", "Rank the team", "Send managers a Monday brief".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: talk_listen_analysis
    producedByStep: s1
    type: talk_listen_analysis
    description: Talk-Listen Analysis produced by this recipe.
  - key: coaching_insights
    producedByStep: s2
    type: coaching_insights
    description: Coaching Insights produced by this recipe.
  - key: leaderboard
    producedByStep: s3
    type: leaderboard
    description: Meeting Leaderboard produced by this recipe.
  - key: workflow
    producedByStep: s4
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Weekly rep coaching rollup

Sends each manager a Monday brief on their reps: talk time against the healthy range for that call type, the skill to work on, and the evidence from real calls.

## Steps

1. **Measure talk time per rep** (builds meeting)

   How much each rep talked over the last 30 days by call type, against the healthy range (around 40% on discovery, 55% on demo), with the trend on the prior month.

2. **Pull each rep's skill gaps** (builds meeting)

   The top three skill areas for each rep from the last 30 days of calls, each backed by the moment in the transcript that shows it.

3. **Rank the team** (builds meeting)

   Reps ranked on discovery questions per call, meetings that move a deal forward, follow-up sent within 24 hours, and objections resolved.

4. **Send managers a Monday brief** (builds workflow)

   Every Monday at 8am each manager gets their team's ranking, a per-rep brief with quotes from real calls, and a suggested action for each rep.

5. **Track whether coaching lands** (builds dashboard)

   Share of reps who got a brief in the last 7 days, week-over-week movement on the tracked metrics, the biggest improvements, persistent gaps, and delivery rate per manager.

## What you end up with

- **talk_listen_analysis** (talk_listen_analysis): Talk-Listen Analysis produced by this recipe.
- **coaching_insights** (coaching_insights): Coaching Insights produced by this recipe.
- **leaderboard** (leaderboard): Meeting Leaderboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A meeting action, from step 1 "Measure talk time per rep"
- A meeting action, from step 2 "Pull each rep's skill gaps"
- A meeting action, from step 3 "Rank the team"
- A new workflow, from step 4 "Send managers a Monday brief"
- A new dashboard, from step 5 "Track whether coaching lands"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, meeting, workflow.
