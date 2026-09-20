---
name: demo-call-summary-recipe
description: Use when a user mentions "demo call summary recipe", "demo AI summary configuration", or asks for related help. Customize how the AI summarizes Demo calls (extract features shown, questions asked, objections raised, technical concerns flagged, and the proposed follow-up) so demo data feeds into product feedback, sales coaching, and deal-stage progression in parallel.
arguments: []
intempt:
  id: demo-call-summary-recipe
  version: 1.0.0
  slashCommand: /demo-call-summary-recipe
  group: Meetings
  title: "Demo call summary fields"
  shortDescription: "Tells the notetaker what to pull out of every demo: features shown, questions asked, objections raised, who from the buying side attended, and the agreed next step."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [summary-recipe, demo]
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
      title: "Check the Demo meeting type"
      command: get_meeting_type
      produces: meeting_type
      bindsAs: demo_type
      description: "Confirms a Demo meeting type exists and the notetaker joins it automatically. Stops if it does not."
      prompt: Retrieve the Demo meeting type from the meeting taxonomy. Confirm it exists with notetaker autojoin enabled. If absent, halt and direct the user to /meeting-types-taxonomy.
    - step: 2
      title: "Set what the demo summary captures"
      command: set_meeting_summary_recipe
      produces: meeting_summary_recipe
      bindsAs: summary_recipe
      dependsOn:
      - demo_type
      description: "Every demo summary records the features shown and how the room reacted, questions by category, objections and whether they were handled, technical blockers, whether a decision maker attended, what the buyer asked for next, and the agreed next step. Anything not discussed is marked as such rather than guessed."
      prompt: 'Configure the AI summary recipe for the Demo meeting type. Extract structured fields: (1) Features Demoed: list of product features shown, with engagement signal per feature (attendee asked questions / silent / pushed back); (2) Questions Asked (list of attendee questions with category (capability, integration, pricing, security, onboarding, other); (3) Objections) list of objections raised verbatim, with category (price/timing/competition/feature-gap/authority/trust) and resolution status (handled/parked/unresolved); (4) Technical Concerns: specific technical questions or blockers (integrations needed, data residency, SSO, compliance); (5) Decision-Maker Signal (was a decision-maker on the call, were they engaged; (6) Follow-up Requested) what attendee asked for (case study, trial, technical demo, custom proposal, references); (7) Next Step: what was agreed. Use ''not_discussed'' for missing fields rather than guessing.'
    - step: 3
      title: "Track what demos reveal"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - demo_type
      - summary_recipe
      description: "Most-demoed features, most-common objections, how often a decision maker attends, and what buyers ask for after a demo, split by rep."
      prompt: 'Compose a demo insights dashboard reading from structured summaries: top 10 features by demo frequency (which features sell themselves vs. need more pitch); top 10 objections by frequency (objection-handling content priorities); decision-maker attendance rate (low % = multi-threading problem); follow-up-requested distribution (what does the market actually want); and most-asked technical concern categories (product / engineering input). Group by rep and time period.'
  outputs:
    - { name: meeting_type, type: meeting_type, cardinality: single, description: "Meeting Type produced by this recipe." }
    - { name: meeting_summary_recipe, type: meeting_summary_recipe, cardinality: single, description: "Meeting Summary Recipe produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Demo call summary fields

Tells the notetaker what to pull out of every demo: features shown, questions asked, objections raised, who from the buying side attended, and the agreed next step.

## What it does

1. **Check the Demo meeting type** (`get_meeting_type`)

   Confirms a Demo meeting type exists and the notetaker joins it automatically. Stops if it does not.

2. **Set what the demo summary captures** (`set_meeting_summary_recipe`)

   Every demo summary records the features shown and how the room reacted, questions by category, objections and whether they were handled, technical blockers, whether a decision maker attended, what the buyer asked for next, and the agreed next step. Anything not discussed is marked as such rather than guessed.

3. **Track what demos reveal** (`create_dashboard`)

   Most-demoed features, most-common objections, how often a decision maker attends, and what buyers ask for after a demo, split by rep.

## What you end up with

- **meeting_type** (meeting_type): Meeting Type produced by this recipe.
- **meeting_summary_recipe** (meeting_summary_recipe): Meeting Summary Recipe produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
