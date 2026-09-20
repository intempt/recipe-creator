---
name: discovery-call-summary-recipe
description: Use when a user mentions "discovery call summary recipe", "qualification call AI summary", or asks for related help. Customize how the AI summarizes Discovery calls, extracting the qualification framework explicitly (champion, pain, current solution, decision criteria, timeline, budget) so the summary feeds directly into deal qualification scoring.
arguments: []
intempt:
  id: discovery-call-summary-recipe
  version: 1.0.0
  slashCommand: /discovery-call-summary-recipe
  group: Meetings
  title: "Discovery call qualification fields"
  shortDescription: "Tells the notetaker to pull the qualification story out of every discovery call: champion, pain, current tool, decision criteria, timeline and budget."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [summary-recipe, discovery, qualification]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - get_meeting_type
    - set_meeting_summary_recipe
    - create_dashboard
  procedure:
    - step: 1
      title: "Check the Discovery meeting type"
      command: get_meeting_type
      produces: meeting_type
      bindsAs: discovery_type
      description: "Confirms a Discovery meeting type exists and the notetaker joins it automatically. Stops if it does not, and points you at the meeting types recipe."
      prompt: Retrieve the Discovery meeting type from the project's meeting taxonomy. Confirm it exists and has notetaker autojoin enabled, both are prerequisites for the custom summary recipe to fire on real meetings. If the type doesn't exist, halt and prompt the user to run /meeting-types-taxonomy first.
    - step: 2
      title: "Set what discovery captures"
      command: set_meeting_summary_recipe
      produces: meeting_summary_recipe
      bindsAs: summary_recipe
      dependsOn:
      - discovery_type
      description: "Every discovery summary records the champion and how bought-in they are, the pain in the buyer's own words with its severity, what they use today, their decision criteria, timeline, budget signal, and the agreed next step. Anything not discussed is marked as such rather than guessed."
      prompt: 'Configure the AI summary recipe for the Discovery meeting type. Extract structured fields: (1) Champion (name, title, level of buy-in (high/medium/low/none), explicit quotes showing commitment; (2) Pain) pain statement in prospect''s own words, severity (must-solve/should-solve/nice-to-have), business impact discussed (revenue, cost, time, risk); (3) Current Solution (what they use today (vendor name + version), what works, what doesn''t; (4) Decision Criteria) explicit criteria mentioned (price, features, integration, security, etc.), priority ranking if discussed; (5) Timeline (target go-live, urgency drivers; (6) Budget) explicit number, range, or signal (no budget signal = flag); (7) Next Step: what was agreed, with owner and due date. If a field is not discussed, return ''not_discussed'' rather than guessing.'
    - step: 3
      title: "Check discovery quality by rep"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - discovery_type
      - summary_recipe
      description: "Share of discovery calls with all seven fields captured, which fields get missed most, and calls flagged with no budget signal, split by rep."
      prompt: 'Compose a Discovery call quality dashboard reading from the structured summaries: % of discovery calls with all 7 fields captured (target: 70%+); breakdown of most-frequently-missed fields (signals coaching opportunities); discoveries with ''no budget signal'' flagged for follow-up; champion strength distribution across recent discoveries; pain severity distribution. Group by rep so managers can spot reps consistently missing qualification fields.'
  outputs:
    - { name: meeting_type, type: meeting_type, cardinality: single, description: "Meeting Type produced by this recipe." }
    - { name: meeting_summary_recipe, type: meeting_summary_recipe, cardinality: single, description: "Meeting Summary Recipe produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Discovery call qualification fields

Tells the notetaker to pull the qualification story out of every discovery call: champion, pain, current tool, decision criteria, timeline and budget.

## What it does

1. **Check the Discovery meeting type** (`get_meeting_type`)

   Confirms a Discovery meeting type exists and the notetaker joins it automatically. Stops if it does not, and points you at the meeting types recipe.

2. **Set what discovery captures** (`set_meeting_summary_recipe`)

   Every discovery summary records the champion and how bought-in they are, the pain in the buyer's own words with its severity, what they use today, their decision criteria, timeline, budget signal, and the agreed next step. Anything not discussed is marked as such rather than guessed.

3. **Check discovery quality by rep** (`create_dashboard`)

   Share of discovery calls with all seven fields captured, which fields get missed most, and calls flagged with no budget signal, split by rep.

## What you end up with

- **meeting_type** (meeting_type): Meeting Type produced by this recipe.
- **meeting_summary_recipe** (meeting_summary_recipe): Meeting Summary Recipe produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
