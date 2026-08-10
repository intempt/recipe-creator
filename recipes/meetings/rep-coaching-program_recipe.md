---
name: rep-coaching-program
description: 'Use when a user mentions "rep coaching program", "sales coaching from meetings", "meeting-based coaching", or asks for related help. Set up a manager-facing weekly coaching rollup: per-rep talk-listen ratio + topic coverage + leaderboard, delivered to managers every Monday with action-item suggestions. Turns meeting intelligence into concrete coaching conversations.'
arguments: []
intempt:
  id: rep-coaching-program
  version: 1.0.0
  slashCommand: /rep-coaching-program
  group: Meetings
  shortDescription: "'Set up a manager-facing weekly coaching rollup: per-rep talk-listen ratio + topic coverage + leaderboard, delivered to managers every Monday with action-item suggestions. Turns meeting intelligence into concrete coaching conversations.'"
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
      title: Compute Talk-Listen Ratio
      command: analyze_talk_listen_ratio
      produces: talk_listen_analysis
      bindsAs: talk_listen
      description: 'Compute talk-listen ratio per rep across the last 30 days of meetings, broken down by meeting type (rep talk % is healthy in different ranges per type — Discovery should be ~40% rep, Demo ~55% rep, Renewal ~40% rep). Output: per-rep current ratio, target range, gap from target, and trend vs. prior 30 days. Flag any rep consistently outside healthy range.'
      prompt: 'Compute talk-listen ratio per rep across the last 30 days of meetings, broken down by meeting type (rep talk % is healthy in different ranges per type — Discovery should be ~40% rep, Demo ~55% rep, Renewal ~40% rep). Output: per-rep current ratio, target range, gap from target, and trend vs. prior 30 days. Flag any rep consistently outside healthy range.'
    - step: 2
      title: Pull Coaching Insights
      command: get_meeting_coaching_insights
      produces: coaching_insights
      bindsAs: insights
      dependsOn:
      - talk_listen
      description: 'For each rep, pull the system-generated coaching insights from the last 30 days of meetings. Surface: top 3 skill development areas (e.g. ''asks fewer than 5 discovery questions per call'', ''rarely confirms decision-maker presence'', ''pushes price too early''), with verbatim meeting snippets as evidence. Combine with the talk-listen analysis to form a per-rep coaching brief.'
      prompt: 'For each rep, pull the system-generated coaching insights from the last 30 days of meetings. Surface: top 3 skill development areas (e.g. ''asks fewer than 5 discovery questions per call'', ''rarely confirms decision-maker presence'', ''pushes price too early''), with verbatim meeting snippets as evidence. Combine with the talk-listen analysis to form a per-rep coaching brief.'
    - step: 3
      title: Build Leaderboard
      command: get_meeting_leaderboard
      produces: leaderboard
      bindsAs: leaderboard
      dependsOn:
      - insights
      description: 'Build a meeting performance leaderboard for the last 30 days, ranking reps on: (1) discovery question count per call, (2) meeting-to-deal-progression rate, (3) follow-up-sent-within-24hr rate, (4) objection-resolution rate. Each metric is comparable across reps. Surface top 3 and bottom 3 per metric — top 3 become coaching examples (their calls get marked as good listen-back material), bottom 3 become coaching focus.'
      prompt: 'Build a meeting performance leaderboard for the last 30 days, ranking reps on: (1) discovery question count per call, (2) meeting-to-deal-progression rate, (3) follow-up-sent-within-24hr rate, (4) objection-resolution rate. Each metric is comparable across reps. Surface top 3 and bottom 3 per metric — top 3 become coaching examples (their calls get marked as good listen-back material), bottom 3 become coaching focus.'
    - step: 4
      title: Build Coaching Delivery Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - talk_listen
      - insights
      - leaderboard
      description: 'Create a weekly scheduled workflow firing Mondays at 8am. Step sequence: (1) refresh talk-listen analysis, coaching insights, and leaderboard; (2) compose a manager-facing summary email per manager containing: their team''s leaderboard position, each rep''s coaching brief (skill area + verbatim quote evidence + suggested next-call focus), and an action item recommendation per rep (''schedule 1:1 with [rep] this week to address [specific skill area]''); (3) post the team leaderboard to the manager''s #sales-coaching Slack channel.'
      prompt: 'Create a weekly scheduled workflow firing Mondays at 8am. Step sequence: (1) refresh talk-listen analysis, coaching insights, and leaderboard; (2) compose a manager-facing summary email per manager containing: their team''s leaderboard position, each rep''s coaching brief (skill area + verbatim quote evidence + suggested next-call focus), and an action item recommendation per rep (''schedule 1:1 with [rep] this week to address [specific skill area]''); (3) post the team leaderboard to the manager''s #sales-coaching Slack channel.'
    - step: 5
      title: Build Coaching Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - talk_listen
      - insights
      - leaderboard
      - workflow
      description: 'Compose a coaching program dashboard showing: program health (% of reps with active coaching briefs received in last 7 days), week-over-week improvement on the top tracked metrics, top 5 reps showing largest improvements (recognition + retention signal), top 5 reps with persistent gaps (escalation signal), and coaching-brief delivery rate per manager (low rate = manager isn''t actually engaging with the program). Manager-of-managers view.'
      prompt: 'Compose a coaching program dashboard showing: program health (% of reps with active coaching briefs received in last 7 days), week-over-week improvement on the top tracked metrics, top 5 reps showing largest improvements (recognition + retention signal), top 5 reps with persistent gaps (escalation signal), and coaching-brief delivery rate per manager (low rate = manager isn''t actually engaging with the program). Manager-of-managers view.'
  outputs:
    - { name: talk_listen_analysis, type: talk_listen_analysis, cardinality: single, description: "Talk-Listen Analysis produced by this recipe." }
    - { name: coaching_insights, type: coaching_insights, cardinality: single, description: "Coaching Insights produced by this recipe." }
    - { name: leaderboard, type: leaderboard, cardinality: single, description: "Meeting Leaderboard produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Rep Coaching Program

## Procedure

1. **Compute Talk-Listen Ratio** [`analyze_talk_listen_ratio`] — Compute talk-listen ratio per rep across the last 30 days of meetings, broken down by meeting type (rep talk % is healthy in different ranges per type — Discovery should be ~40% rep, Demo ~55% rep, Renewal ~40% rep). Output: per-rep current ratio, target range, gap from target, and trend vs. prior 30 days. Flag any rep consistently outside healthy range. → produces: talk_listen_analysis
2. **Pull Coaching Insights** [`get_meeting_coaching_insights`] — For each rep, pull the system-generated coaching insights from the last 30 days of meetings. Surface: top 3 skill development areas (e.g. 'asks fewer than 5 discovery questions per call', 'rarely confirms decision-maker presence', 'pushes price too early'), with verbatim meeting snippets as evidence. Combine with the talk-listen analysis to form a per-rep coaching brief. → produces: coaching_insights
3. **Build Leaderboard** [`get_meeting_leaderboard`] — Build a meeting performance leaderboard for the last 30 days, ranking reps on: (1) discovery question count per call, (2) meeting-to-deal-progression rate, (3) follow-up-sent-within-24hr rate, (4) objection-resolution rate. Each metric is comparable across reps. Surface top 3 and bottom 3 per metric — top 3 become coaching examples (their calls get marked as good listen-back material), bottom 3 become coaching focus. → produces: leaderboard
4. **Build Coaching Delivery Workflow** [`create_workflow`] — Create a weekly scheduled workflow firing Mondays at 8am. Step sequence: (1) refresh talk-listen analysis, coaching insights, and leaderboard; (2) compose a manager-facing summary email per manager containing: their team's leaderboard position, each rep's coaching brief (skill area + verbatim quote evidence + suggested next-call focus), and an action item recommendation per rep ('schedule 1:1 with [rep] this week to address [specific skill area]'); (3) post the team leaderboard to the manager's #sales-coaching Slack channel. → produces: workflow
5. **Build Coaching Dashboard** [`create_dashboard`] — Compose a coaching program dashboard showing: program health (% of reps with active coaching briefs received in last 7 days), week-over-week improvement on the top tracked metrics, top 5 reps showing largest improvements (recognition + retention signal), top 5 reps with persistent gaps (escalation signal), and coaching-brief delivery rate per manager (low rate = manager isn't actually engaging with the program). Manager-of-managers view. → produces: dashboard
