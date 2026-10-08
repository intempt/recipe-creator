---
id: renewal-call-summary-recipe
title: Renewal call summary fields
slash_command: /renewal-call-summary-recipe
group: Meetings
owner: intempt
curator: sid
summary: >-
  Customizes AI summaries for Renewal calls, extracting usage patterns, expansion signals, churn risks,
  stakeholder confirmation and contract changes.
description: >-
  A Renewal call summary recipe that extracts usage patterns, expansion signals, contraction risks,
  stakeholder confirmation and contract-term changes from the meeting.
version: 2.0.0
classification:
  product:
    - sales
  agent: meeting-notetaker
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
    - finance
    - media
  vertical: []
  complexity: standard
  executionMode: live
  tags:
    - summary-recipe
    - renewal
    - expansion
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new meeting type, from step 1 "Check the Renewal meeting type"
    - A meeting action, from step 2 "Set what renewals capture"
    - A new dashboard, from step 3 "Track renewal risk and upside"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Check the Renewal meeting type
    summary: >-
      Confirms a Renewal meeting type exists and the notetaker joins it automatically.
    builds: meeting_type
    description: >-
      Retrieve the Renewal meeting type from the meeting taxonomy. Confirm exists with notetaker autojoin
      enabled.
  - id: s2
    title: Set what renewals capture
    summary: >-
      Every renewal summary records which features the customer uses, struggles with or never tried, interest
      in more seats or a higher tier, churn signals and competitor evaluation, who was in the room, contract
      term asks, and the agreed next step.
    builds: meeting
    description: >-
      Configure the AI summary recipe for the Renewal meeting type. Extract: (1) Usage Patterns (features
      the customer mentioned actively using vs. struggling with vs. never tried; (2) Expansion Signals)
      explicit interest in additional seats, modules, tier upgrades; budget signal for expansion (verbatim
      quotes); (3) Contraction Risks: explicit signals of churn intent, reduced usage, team changes affecting
      fit, competitor evaluation; (4) Stakeholder Confirmation: was the decision-maker present, did stakeholders
      confirm continued commitment, any champion changes (departures, role changes); (5) Contract Terms
      Discussion (pricing pushback, term length preference, payment terms, custom contractual asks; (6)
      Health Score Movement) sentiment shift from prior interactions; (7) Next Step: proposal needed,
      additional stakeholders to loop in, agreement to terms. Use the result of "Check the Renewal meeting
      type".
    dependsOn:
      - s1
  - id: s3
    title: Track renewal risk and upside
    summary: >-
      Renewals at risk sorted by renewal date, accounts ready to expand sorted by revenue, champion departures,
      and how many upcoming renewals have had their call.
    builds: dashboard
    description: >-
      Compose a renewal risk + expansion dashboard reading from summaries: (1) at-risk renewals (accounts
      with contraction signals or unresolved competitor evaluation, sorted by renewal date; (2) expansion-ready)
      accounts with explicit interest signals, sorted by ARR opportunity; (3) churn precursors (accounts
      where champion departed or stakeholders signaled disengagement; (4) renewal-call coverage) % of
      upcoming renewals where the call has happened (target: 100% by 60 days before renewal date); (5)
      win/loss patterns from past renewal-call summaries. Group by CSM owner. Use the result of "Check
      the Renewal meeting type", "Set what renewals capture".
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

# Renewal call summary fields

Customizes AI summaries for Renewal calls, extracting usage patterns, expansion signals, churn risks, stakeholder confirmation and contract changes.

## Steps

1. **Check the Renewal meeting type** (builds meeting_type)

   Confirms a Renewal meeting type exists and the notetaker joins it automatically.

2. **Set what renewals capture** (builds meeting)

   Every renewal summary records which features the customer uses, struggles with or never tried, interest in more seats or a higher tier, churn signals and competitor evaluation, who was in the room, contract term asks, and the agreed next step.

3. **Track renewal risk and upside** (builds dashboard)

   Renewals at risk sorted by renewal date, accounts ready to expand sorted by revenue, champion departures, and how many upcoming renewals have had their call.

## What you end up with

- **meeting_type** (meeting_type): Meeting Type produced by this recipe.
- **meeting_summary_recipe** (meeting_summary_recipe): Meeting Summary Recipe produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new meeting type, from step 1 "Check the Renewal meeting type"
- A meeting action, from step 2 "Set what renewals capture"
- A new dashboard, from step 3 "Track renewal risk and upside"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, meeting, meeting_type.
