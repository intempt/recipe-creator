---
name: renewal-call-summary-recipe
description: Use when a user mentions "renewal call summary recipe", "renewal AI summary", or asks for related help. Customize how the AI summarizes Renewal calls — capture usage patterns mentioned, expansion signals, contraction risks, stakeholder confirmation, and contract-term changes — feeding directly into renewal forecasting and CSM motion.
arguments: []
intempt:
  id: renewal-call-summary-recipe
  version: 1.0.0
  slashCommand: /renewal-call-summary-recipe
  group: Meetings
  shortDescription: 'Customize how the AI summarizes Renewal calls (capture usage patterns mentioned, expansion signals, contraction risks, stakeholder confirmation, and contract-term changes), feeding directly into renewal forecasting and CSM motion.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [summary-recipe, renewal, expansion]
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
      title: Confirm Renewal Meeting Type
      command: get_meeting_type
      produces: meeting_type
      bindsAs: renewal_type
      description: Retrieve the Renewal meeting type from the meeting taxonomy. Confirm exists with notetaker autojoin enabled.
      prompt: Retrieve the Renewal meeting type from the meeting taxonomy. Confirm exists with notetaker autojoin enabled.
    - step: 2
      title: Set Renewal Summary Recipe
      command: set_meeting_summary_recipe
      produces: meeting_summary_recipe
      bindsAs: summary_recipe
      dependsOn:
      - renewal_type
      description: 'Configure the AI summary recipe for the Renewal meeting type. Extract: (1) Usage Patterns — features the customer mentioned actively using vs. struggling with vs. never tried; (2) Expansion Signals — explicit interest in additional seats, modules, tier upgrades; budget signal for expansion (verbatim quotes); (3) Contraction Risks — explicit signals of churn intent, reduced usage, team changes affecting fit, competitor evaluation; (4) Stakeholder Confirmation — was the decision-maker present, did stakeholders confirm continued commitment, any champion changes (departures, role changes); (5) Contract Terms Discussion — pricing pushback, term length preference, payment terms, custom contractual asks; (6) Health Score Movement — sentiment shift from prior interactions; (7) Next Step — proposal needed, additional stakeholders to loop in, agreement to terms.'
      prompt: 'Configure the AI summary recipe for the Renewal meeting type. Extract: (1) Usage Patterns — features the customer mentioned actively using vs. struggling with vs. never tried; (2) Expansion Signals — explicit interest in additional seats, modules, tier upgrades; budget signal for expansion (verbatim quotes); (3) Contraction Risks — explicit signals of churn intent, reduced usage, team changes affecting fit, competitor evaluation; (4) Stakeholder Confirmation — was the decision-maker present, did stakeholders confirm continued commitment, any champion changes (departures, role changes); (5) Contract Terms Discussion — pricing pushback, term length preference, payment terms, custom contractual asks; (6) Health Score Movement — sentiment shift from prior interactions; (7) Next Step — proposal needed, additional stakeholders to loop in, agreement to terms.'
    - step: 3
      title: Build Renewal Risk Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - renewal_type
      - summary_recipe
      description: 'Compose a renewal risk + expansion dashboard reading from summaries: (1) at-risk renewals — accounts with contraction signals or unresolved competitor evaluation, sorted by renewal date; (2) expansion-ready — accounts with explicit interest signals, sorted by ARR opportunity; (3) churn precursors — accounts where champion departed or stakeholders signaled disengagement; (4) renewal-call coverage — % of upcoming renewals where the call has happened (target: 100% by 60 days before renewal date); (5) win/loss patterns from past renewal-call summaries. Group by CSM owner.'
      prompt: 'Compose a renewal risk + expansion dashboard reading from summaries: (1) at-risk renewals — accounts with contraction signals or unresolved competitor evaluation, sorted by renewal date; (2) expansion-ready — accounts with explicit interest signals, sorted by ARR opportunity; (3) churn precursors — accounts where champion departed or stakeholders signaled disengagement; (4) renewal-call coverage — % of upcoming renewals where the call has happened (target: 100% by 60 days before renewal date); (5) win/loss patterns from past renewal-call summaries. Group by CSM owner.'
  outputs:
    - { name: meeting_type, type: meeting_type, cardinality: single, description: "Meeting Type produced by this recipe." }
    - { name: meeting_summary_recipe, type: meeting_summary_recipe, cardinality: single, description: "Meeting Summary Recipe produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Renewal Call Summary Recipe

## Procedure

1. **Confirm Renewal Meeting Type** [`get_meeting_type`] — Retrieve the Renewal meeting type from the meeting taxonomy. Confirm exists with notetaker autojoin enabled. → produces: meeting_type
2. **Set Renewal Summary Recipe** [`set_meeting_summary_recipe`] — Configure the AI summary recipe for the Renewal meeting type. Extract: (1) Usage Patterns — features the customer mentioned actively using vs. struggling with vs. never tried; (2) Expansion Signals — explicit interest in additional seats, modules, tier upgrades; budget signal for expansion (verbatim quotes); (3) Contraction Risks — explicit signals of churn intent, reduced usage, team changes affecting fit, competitor evaluation; (4) Stakeholder Confirmation — was the decision-maker present, did stakeholders confirm continued commitment, any champion changes (departures, role changes); (5) Contract Terms Discussion — pricing pushback, term length preference, payment terms, custom contractual asks; (6) Health Score Movement — sentiment shift from prior interactions; (7) Next Step — proposal needed, additional stakeholders to loop in, agreement to terms. → produces: meeting_summary_recipe
3. **Build Renewal Risk Dashboard** [`create_dashboard`] — Compose a renewal risk + expansion dashboard reading from summaries: (1) at-risk renewals — accounts with contraction signals or unresolved competitor evaluation, sorted by renewal date; (2) expansion-ready — accounts with explicit interest signals, sorted by ARR opportunity; (3) churn precursors — accounts where champion departed or stakeholders signaled disengagement; (4) renewal-call coverage — % of upcoming renewals where the call has happened (target: 100% by 60 days before renewal date); (5) win/loss patterns from past renewal-call summaries. Group by CSM owner. → produces: dashboard
