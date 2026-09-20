---
name: rep-coaching-program
description: 'Use when a user mentions "rep coaching program", "sales coaching from meetings", "meeting-based coaching", or asks for related help. Set up a manager-facing weekly coaching rollup: per-rep talk-listen ratio + topic coverage + leaderboard, delivered to managers every Monday with action-item suggestions. Turns meeting intelligence into concrete coaching conversations.'
arguments: []
intempt:
  id: rep-coaching-program
  version: 1.0.0
  slashCommand: /rep-coaching-program
  group: Meetings
  title: "Weekly rep coaching rollup"
  shortDescription: "Sends each manager a Monday brief on their reps: talk time against the healthy range for that call type, the skill to work on, and the evidence from real calls."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [coaching, rep-development, manager-tools]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - analyze_talk_listen_ratio
    - get_meeting_coaching_insights
    - get_meeting_leaderboard
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Measure talk time per rep"
      command: analyze_talk_listen_ratio
      produces: talk_listen_analysis
      bindsAs: talk_listen
      description: "How much each rep talked over the last 30 days by call type, against the healthy range (around 40% on discovery, 55% on demo), with the trend on the prior month."
      prompt: 'Compute talk-listen ratio per rep across the last 30 days of meetings, broken down by meeting type (rep talk % is healthy in different ranges per type: Discovery should be ~40% rep, Demo ~55% rep, Renewal ~40% rep). Output: per-rep current ratio, target range, gap from target, and trend vs. prior 30 days. Flag any rep consistently outside healthy range.'
    - step: 2
      title: "Pull each rep's skill gaps"
      command: get_meeting_coaching_insights
      produces: coaching_insights
      bindsAs: insights
      dependsOn:
      - talk_listen
      description: "The top three skill areas for each rep from the last 30 days of calls, each backed by the moment in the transcript that shows it."
      prompt: 'For each rep, pull the system-generated coaching insights from the last 30 days of meetings. Surface: top 3 skill development areas (e.g. ''asks fewer than 5 discovery questions per call'', ''rarely confirms decision-maker presence'', ''pushes price too early''), with verbatim meeting snippets as evidence. Combine with the talk-listen analysis to form a per-rep coaching brief.'
    - step: 3
      title: "Rank the team"
      command: get_meeting_leaderboard
      produces: leaderboard
      bindsAs: leaderboard
      dependsOn:
      - insights
      description: "Reps ranked on discovery questions per call, meetings that move a deal forward, follow-up sent within 24 hours, and objections resolved."
      prompt: 'Build a meeting performance leaderboard for the last 30 days, ranking reps on: (1) discovery question count per call, (2) meeting-to-deal-progression rate, (3) follow-up-sent-within-24hr rate, (4) objection-resolution rate. Each metric is comparable across reps. Surface top 3 and bottom 3 per metric: top 3 become coaching examples (their calls get marked as good listen-back material), bottom 3 become coaching focus.'
    - step: 4
      title: "Send managers a Monday brief"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - talk_listen
      - insights
      - leaderboard
      description: "Every Monday at 8am each manager gets their team's ranking, a per-rep brief with quotes from real calls, and a suggested action for each rep."
      prompt: 'Create a weekly scheduled workflow firing Mondays at 8am. Step sequence: (1) refresh talk-listen analysis, coaching insights, and leaderboard; (2) compose a manager-facing summary email per manager containing: their team''s leaderboard position, each rep''s coaching brief (skill area + verbatim quote evidence + suggested next-call focus), and an action item recommendation per rep (''schedule 1:1 with [rep] this week to address [specific skill area]''); (3) post the team leaderboard to the manager''s #sales-coaching Slack channel.'
    - step: 5
      title: "Track whether coaching lands"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - talk_listen
      - insights
      - leaderboard
      - workflow
      description: "Share of reps who got a brief in the last 7 days, week-over-week movement on the tracked metrics, the biggest improvements, persistent gaps, and delivery rate per manager."
      prompt: 'Compose a coaching program dashboard showing: program health (% of reps with active coaching briefs received in last 7 days), week-over-week improvement on the top tracked metrics, top 5 reps showing largest improvements (recognition + retention signal), top 5 reps with persistent gaps (escalation signal), and coaching-brief delivery rate per manager (low rate = manager isn''t actually engaging with the program). Manager-of-managers view.'
  outputs:
    - { name: talk_listen_analysis, type: talk_listen_analysis, cardinality: single, description: "Talk-Listen Analysis produced by this recipe." }
    - { name: coaching_insights, type: coaching_insights, cardinality: single, description: "Coaching Insights produced by this recipe." }
    - { name: leaderboard, type: leaderboard, cardinality: single, description: "Meeting Leaderboard produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Weekly rep coaching rollup

Sends each manager a Monday brief on their reps: talk time against the healthy range for that call type, the skill to work on, and the evidence from real calls.

## Before you run it

- Connect slack

## What it does

1. **Measure talk time per rep** (`analyze_talk_listen_ratio`)

   How much each rep talked over the last 30 days by call type, against the healthy range (around 40% on discovery, 55% on demo), with the trend on the prior month.

2. **Pull each rep's skill gaps** (`get_meeting_coaching_insights`)

   The top three skill areas for each rep from the last 30 days of calls, each backed by the moment in the transcript that shows it.

3. **Rank the team** (`get_meeting_leaderboard`)

   Reps ranked on discovery questions per call, meetings that move a deal forward, follow-up sent within 24 hours, and objections resolved.

4. **Send managers a Monday brief** (`create_workflow`)

   Every Monday at 8am each manager gets their team's ranking, a per-rep brief with quotes from real calls, and a suggested action for each rep.

5. **Track whether coaching lands** (`create_dashboard`)

   Share of reps who got a brief in the last 7 days, week-over-week movement on the tracked metrics, the biggest improvements, persistent gaps, and delivery rate per manager.

## What you end up with

- **talk_listen_analysis** (talk_listen_analysis): Talk-Listen Analysis produced by this recipe.
- **coaching_insights** (coaching_insights): Coaching Insights produced by this recipe.
- **leaderboard** (leaderboard): Meeting Leaderboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
