---
id: demo-call-summary-recipe
title: Demo call summary fields
slash_command: /demo-call-summary-recipe
group: Meetings
owner: intempt
curator: sid
summary: 'Tells the notetaker what to pull out of every demo: features shown, questions asked, objections
  raised, who from the buying side attended, and the agreed next step.'
description: >-
  Customize how the AI summarizes Demo calls (extract features shown, questions asked, objections raised,
  technical concerns flagged, and the proposed follow-up) so demo data feeds into product feedback, sales
  coaching, and deal-stage progression in parallel.
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
    - demo
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new meeting type, from step 1 "Check the Demo meeting type"
    - A meeting action, from step 2 "Set what the demo summary captures"
    - A new dashboard, from step 3 "Track what demos reveal"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Check the Demo meeting type
    summary: >-
      Confirms a Demo meeting type exists and the notetaker joins it automatically. Stops if it does not.
    builds: meeting_type
    description: >-
      Retrieve the Demo meeting type from the meeting taxonomy. Confirm it exists with notetaker autojoin
      enabled. If absent, halt and direct the user to /meeting-types-taxonomy.
  - id: s2
    title: Set what the demo summary captures
    summary: >-
      Every demo summary records the features shown and how the room reacted, questions by category, objections
      and whether they were handled, technical blockers, whether a decision maker attended, what the buyer
      asked for next, and the agreed next step. Anything not discussed is marked as such rather than guessed.
    builds: meeting
    description: >-
      Configure the AI summary recipe for the Demo meeting type. Extract structured fields: (1) Features
      Demoed: list of product features shown, with engagement signal per feature (attendee asked questions
      / silent / pushed back); (2) Questions Asked (list of attendee questions with category (capability,
      integration, pricing, security, onboarding, other); (3) Objections) list of objections raised verbatim,
      with category (price/timing/competition/feature-gap/authority/trust) and resolution status (handled/parked/unresolved);
      (4) Technical Concerns: specific technical questions or blockers (integrations needed, data residency,
      SSO, compliance); (5) Decision-Maker Signal (was a decision-maker on the call, were they engaged;
      (6) Follow-up Requested) what attendee asked for (case study, trial, technical demo, custom proposal,
      references); (7) Next Step: what was agreed. Use 'not_discussed' for missing fields rather than
      guessing. Use the result of "Check the Demo meeting type".
    dependsOn:
      - s1
  - id: s3
    title: Track what demos reveal
    summary: >-
      Most-demoed features, most-common objections, how often a decision maker attends, and what buyers
      ask for after a demo, split by rep.
    builds: dashboard
    description: >-
      Compose a demo insights dashboard reading from structured summaries: top 10 features by demo frequency
      (which features sell themselves vs. need more pitch); top 10 objections by frequency (objection-handling
      content priorities); decision-maker attendance rate (low % = multi-threading problem); follow-up-requested
      distribution (what does the market actually want); and most-asked technical concern categories (product
      / engineering input). Group by rep and time period. Use the result of "Check the Demo meeting type",
      "Set what the demo summary captures".
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

# Demo call summary fields

Tells the notetaker what to pull out of every demo: features shown, questions asked, objections raised, who from the buying side attended, and the agreed next step.

## Steps

1. **Check the Demo meeting type** (builds meeting_type)

   Confirms a Demo meeting type exists and the notetaker joins it automatically. Stops if it does not.

2. **Set what the demo summary captures** (builds meeting)

   Every demo summary records the features shown and how the room reacted, questions by category, objections and whether they were handled, technical blockers, whether a decision maker attended, what the buyer asked for next, and the agreed next step. Anything not discussed is marked as such rather than guessed.

3. **Track what demos reveal** (builds dashboard)

   Most-demoed features, most-common objections, how often a decision maker attends, and what buyers ask for after a demo, split by rep.

## What you end up with

- **meeting_type** (meeting_type): Meeting Type produced by this recipe.
- **meeting_summary_recipe** (meeting_summary_recipe): Meeting Summary Recipe produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new meeting type, from step 1 "Check the Demo meeting type"
- A meeting action, from step 2 "Set what the demo summary captures"
- A new dashboard, from step 3 "Track what demos reveal"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, meeting, meeting_type.
