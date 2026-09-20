---
name: notetaker-coverage-setup
description: Use when a user mentions "notetaker coverage", "notetaker autojoin setup", "configure meeting bot", or asks for related help. Configure which meetings the Blu notetaker auto-joins, by meeting type, host seniority, deal stage, and account tier. Set the rules once, get consistent coverage without per-meeting toggles.
arguments: []
intempt:
  id: notetaker-coverage-setup
  version: 1.0.0
  slashCommand: /notetaker-coverage-setup
  group: Meetings
  title: "Decide which calls get recorded"
  shortDescription: "Sets the rules for when the notetaker joins, by meeting type, deal value and attendee opt-out, so coverage is consistent without toggling it call by call."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [notetaker, meeting-capture]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - list_meeting_types
    - configure_notetaker_autojoin
    - create_dashboard
  procedure:
    - step: 1
      title: "Review your meeting types"
      command: list_meeting_types
      produces: meeting_type_inventory
      bindsAs: meeting_type_inventory
      description: "Every meeting type with its duration, current auto-join setting, and how many meetings it held in the last 90 days."
      prompt: 'List all configured meeting types in the project. For each, surface: name, default duration, current notetaker auto-join setting, and meetings-per-month count over the last 90 days. This is the baseline for designing coverage rules: types with high volume and high revenue impact (demo, discovery, close, renewal) should have autojoin on; types with low strategic value (internal sync, recurring 1:1) likely shouldn''t.'
    - step: 2
      title: "Set the auto-join rules"
      command: configure_notetaker_autojoin
      produces: notetaker_config
      bindsAs: notetaker_config
      dependsOn:
      - meeting_type_inventory
      description: "On for discovery, demo, proposal, close, renewal and customer success calls. Off for internal syncs, 1:1s, standups and interviews. Always on for deals over $50K, always off if an attendee has opted out."
      prompt: 'Configure notetaker autojoin rules based on the meeting-type audit. Default policy: ON for Discovery, Demo, Proposal, Close, Renewal, and Customer Success calls; OFF for Internal Sync, 1:1, Recurring Standup, Interview. Layer on overrides: ON for any meeting linked to a deal with value > $50K regardless of type; OFF if any attendee has notetaker-opt-out flag. Hosts can manually override per-meeting via add_blu_to_live_meeting or the meeting record toggle.'
    - step: 3
      title: "Track coverage and failures"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - meeting_type_inventory
      - notetaker_config
      description: "Share of meetings the notetaker attended by type and by rep, failed joins, and how often hosts had to add it by hand."
      prompt: 'Compose a notetaker coverage dashboard: % of meetings with notetaker present (target: 80%+ for revenue-impacting types), coverage broken down by meeting type and rep, failed-join count (notetaker invited but didn''t join (usually a calendar permission issue), and manual-add count (hosts having to invite Blu manually) signal of misconfigured rules). Flag any type with <60% coverage as a configuration gap.'
  outputs:
    - { name: meeting_type_inventory, type: meeting_type_inventory, cardinality: single, description: "Meeting Type Inventory produced by this recipe." }
    - { name: notetaker_config, type: notetaker_config, cardinality: single, description: "Notetaker Config produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Decide which calls get recorded

Sets the rules for when the notetaker joins, by meeting type, deal value and attendee opt-out, so coverage is consistent without toggling it call by call.

## What it does

1. **Review your meeting types** (`list_meeting_types`)

   Every meeting type with its duration, current auto-join setting, and how many meetings it held in the last 90 days.

2. **Set the auto-join rules** (`configure_notetaker_autojoin`)

   On for discovery, demo, proposal, close, renewal and customer success calls. Off for internal syncs, 1:1s, standups and interviews. Always on for deals over $50K, always off if an attendee has opted out.

3. **Track coverage and failures** (`create_dashboard`)

   Share of meetings the notetaker attended by type and by rep, failed joins, and how often hosts had to add it by hand.

## What you end up with

- **meeting_type_inventory** (meeting_type_inventory): Meeting Type Inventory produced by this recipe.
- **notetaker_config** (notetaker_config): Notetaker Config produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
