---
id: discovery-call-summary-recipe
title: Discovery call qualification fields
slash_command: /discovery-call-summary-recipe
group: Meetings
owner: intempt
curator: sid
summary: 'Tells the notetaker to pull the qualification story out of every discovery call: champion, pain,
  current tool, decision criteria, timeline and budget.'
description: >-
  Customize how the AI summarizes Discovery calls, extracting the qualification framework explicitly (champion,
  pain, current solution, decision criteria, timeline, budget) so the summary feeds directly into deal
  qualification scoring.
version: 2.0.0
classification:
  product:
    - sales
  agent: meeting-notetaker
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - summary-recipe
    - discovery
    - qualification
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new meeting type, from step 1 "Check the Discovery meeting type"
    - A meeting action, from step 2 "Set what discovery captures"
    - A new dashboard, from step 3 "Check discovery quality by rep"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Check the Discovery meeting type
    summary: >-
      Confirms a Discovery meeting type exists and the notetaker joins it automatically. Stops if it does
      not, and points you at the meeting types recipe.
    builds: meeting_type
    description: >-
      Retrieve the Discovery meeting type from the project's meeting taxonomy. Confirm it exists and has
      notetaker autojoin enabled, both are prerequisites for the custom summary recipe to fire on real
      meetings. If the type doesn't exist, halt and prompt the user to run /meeting-types-taxonomy first.
  - id: s2
    title: Set what discovery captures
    summary: >-
      Every discovery summary records the champion and how bought-in they are, the pain in the buyer's
      own words with its severity, what they use today, their decision criteria, timeline, budget signal,
      and the agreed next step. Anything not discussed is marked as such rather than guessed.
    builds: meeting
    description: >-
      Configure the AI summary recipe for the Discovery meeting type. Extract structured fields: (1) Champion
      (name, title, level of buy-in (high/medium/low/none), explicit quotes showing commitment; (2) Pain)
      pain statement in prospect's own words, severity (must-solve/should-solve/nice-to-have), business
      impact discussed (revenue, cost, time, risk); (3) Current Solution (what they use today (vendor
      name + version), what works, what doesn't; (4) Decision Criteria) explicit criteria mentioned (price,
      features, integration, security, etc.), priority ranking if discussed; (5) Timeline (target go-live,
      urgency drivers; (6) Budget) explicit number, range, or signal (no budget signal = flag); (7) Next
      Step: what was agreed, with owner and due date. If a field is not discussed, return 'not_discussed'
      rather than guessing. Use the result of "Check the Discovery meeting type".
    dependsOn:
      - s1
  - id: s3
    title: Check discovery quality by rep
    summary: >-
      Share of discovery calls with all seven fields captured, which fields get missed most, and calls
      flagged with no budget signal, split by rep.
    builds: dashboard
    description: >-
      Compose a Discovery call quality dashboard reading from the structured summaries: % of discovery
      calls with all 7 fields captured (target: 70%+); breakdown of most-frequently-missed fields (signals
      coaching opportunities); discoveries with 'no budget signal' flagged for follow-up; champion strength
      distribution across recent discoveries; pain severity distribution. Group by rep so managers can
      spot reps consistently missing qualification fields. Use the result of "Check the Discovery meeting
      type", "Set what discovery captures".
    dependsOn:
      - s1
      - s2
outputs:
  - key: meeting_type
    producedByStep: s1
    type: meeting_type
    description: Meeting Type produced by this recipe.
  - key: meeting_summary_recipe
    producedByStep: s2
    type: meeting_summary_recipe
    description: Meeting Summary Recipe produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Discovery call qualification fields

Tells the notetaker to pull the qualification story out of every discovery call: champion, pain, current tool, decision criteria, timeline and budget.

## Steps

1. **Check the Discovery meeting type** (builds meeting_type)

   Confirms a Discovery meeting type exists and the notetaker joins it automatically. Stops if it does not, and points you at the meeting types recipe.

2. **Set what discovery captures** (builds meeting)

   Every discovery summary records the champion and how bought-in they are, the pain in the buyer's own words with its severity, what they use today, their decision criteria, timeline, budget signal, and the agreed next step. Anything not discussed is marked as such rather than guessed.

3. **Check discovery quality by rep** (builds dashboard)

   Share of discovery calls with all seven fields captured, which fields get missed most, and calls flagged with no budget signal, split by rep.

## What you end up with

- **meeting_type** (meeting_type): Meeting Type produced by this recipe.
- **meeting_summary_recipe** (meeting_summary_recipe): Meeting Summary Recipe produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new meeting type, from step 1 "Check the Discovery meeting type"
- A meeting action, from step 2 "Set what discovery captures"
- A new dashboard, from step 3 "Check discovery quality by rep"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, meeting, meeting_type.
