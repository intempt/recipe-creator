---
id: notetaker-coverage-setup
title: Decide which calls get recorded
slash_command: /notetaker-coverage-setup
group: Meetings
owner: intempt
curator: sid
summary: >-
  Configures the Blu notetaker auto-join setting using one of five coarse modes. It sets broad meeting
  coverage, not opt-out or deal value rules.
description: >-
  Choose one of five coarse auto-join modes for the Blu notetaker. The recipe controls broad meeting coverage
  only. It does not include attendee opt-out, deal value thresholds, or a meeting dashboard.
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
  vertical: []
  complexity: standard
  executionMode: live
  tags:
    - notetaker
    - meeting-capture
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new meeting type, from step 1 "Review your meeting types"
    - A meeting action, from step 2 "Set the auto-join rules"
    - A new dashboard, from step 3 "Track coverage and failures"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Review your meeting types
    summary: >-
      Every meeting type with its duration, current auto-join setting, and how many meetings it held in
      the last 90 days.
    builds: meeting_type
    description: >-
      List all configured meeting types in the project. For each, surface: name, default duration, current
      notetaker auto-join setting, and meetings-per-month count over the last 90 days. This is the baseline
      for designing coverage rules: types with high volume and high revenue impact (demo, discovery, close,
      renewal) should have autojoin on; types with low strategic value (internal sync, recurring 1:1)
      likely shouldn't.
  - id: s2
    title: Set the auto-join rules
    summary: >-
      On for discovery, demo, proposal, close, renewal and customer success calls. Off for internal syncs,
      1:1s, standups and interviews. Always on for deals over $50K, always off if an attendee has opted
      out.
    builds: meeting
    description: >-
      Configure notetaker autojoin rules based on the meeting-type audit. Default policy: ON for Discovery,
      Demo, Proposal, Close, Renewal, and Customer Success calls; OFF for Internal Sync, 1:1, Recurring
      Standup, Interview. Layer on overrides: ON for any meeting linked to a deal with value > $50K regardless
      of type; OFF if any attendee has notetaker-opt-out flag. Hosts can manually override per-meeting
      via add_blu_to_live_meeting or the meeting record toggle. Use the result of "Review your meeting
      types".
    dependsOn:
      - s1
  - id: s3
    title: Track coverage and failures
    summary: >-
      Share of meetings the notetaker attended by type and by rep, failed joins, and how often hosts had
      to add it by hand.
    builds: dashboard
    description: >-
      Compose a notetaker coverage dashboard: % of meetings with notetaker present (target: 80%+ for revenue-impacting
      types), coverage broken down by meeting type and rep, failed-join count (notetaker invited but didn't
      join (usually a calendar permission issue), and manual-add count (hosts having to invite Blu manually)
      signal of misconfigured rules). Flag any type with <60% coverage as a configuration gap. Use the
      result of "Review your meeting types", "Set the auto-join rules".
    dependsOn:
      - s1
      - s2
outputs:
  - key: meeting_type_inventory
    producedByStep: s1
    type: meeting_type_inventory
    description: Meeting Type Inventory produced by this recipe.
  - key: notetaker_config
    producedByStep: s2
    type: notetaker_config
    description: Notetaker Config produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Decide which calls get recorded

Configures the Blu notetaker auto-join setting using one of five coarse modes. It sets broad meeting coverage, not opt-out or deal value rules.

## Steps

1. **Review your meeting types** (builds meeting_type)

   Every meeting type with its duration, current auto-join setting, and how many meetings it held in the last 90 days.

2. **Set the auto-join rules** (builds meeting)

   On for discovery, demo, proposal, close, renewal and customer success calls. Off for internal syncs, 1:1s, standups and interviews. Always on for deals over $50K, always off if an attendee has opted out.

3. **Track coverage and failures** (builds dashboard)

   Share of meetings the notetaker attended by type and by rep, failed joins, and how often hosts had to add it by hand.

## What you end up with

- **meeting_type_inventory** (meeting_type_inventory): Meeting Type Inventory produced by this recipe.
- **notetaker_config** (notetaker_config): Notetaker Config produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new meeting type, from step 1 "Review your meeting types"
- A meeting action, from step 2 "Set the auto-join rules"
- A new dashboard, from step 3 "Track coverage and failures"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, meeting, meeting_type.
