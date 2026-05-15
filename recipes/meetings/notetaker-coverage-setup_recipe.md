---
name: notetaker-coverage-setup
description: Use when a user mentions "notetaker coverage", "notetaker autojoin setup", "configure meeting bot", or asks for related help. Configure which meetings the Blu notetaker auto-joins — by meeting type, host seniority, deal stage, and account tier. Set the rules once, get consistent coverage without per-meeting toggles.
arguments: []
intempt:
  id: notetaker-coverage-setup
  version: 1.0.0
  slashCommand: /notetaker-coverage-setup
  group: Meetings
  shortDescription: "Configure which meetings the Blu notetaker auto-joins — by meeting type, host seniority, deal stage, and account tier. Set the rules once, get consistent coverage without per-meeting toggles."
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
      title: Audit Current Meeting Types
      command: list_meeting_types
      produces: meeting_type_inventory
      bindsAs: meeting_type_inventory
      description: 'List all configured meeting types in the project. For each, surface: name, default duration, current notetaker auto-join setting, and meetings-per-month count over the last 90 days. This is the baseline for designing coverage rules — types with high volume and high revenue impact (demo, discovery, close, renewal) should have autojoin on; types with low strategic value (internal sync, recurring 1:1) likely shouldn''t.'
      prompt: 'List all configured meeting types in the project. For each, surface: name, default duration, current notetaker auto-join setting, and meetings-per-month count over the last 90 days. This is the baseline for designing coverage rules — types with high volume and high revenue impact (demo, discovery, close, renewal) should have autojoin on; types with low strategic value (internal sync, recurring 1:1) likely shouldn''t.'
    - step: 2
      title: Configure Autojoin Rules
      command: configure_notetaker_autojoin
      produces: notetaker_config
      bindsAs: notetaker_config
      dependsOn:
      - meeting_type_inventory
      description: 'Configure notetaker autojoin rules based on the meeting-type audit. Default policy: ON for Discovery, Demo, Proposal, Close, Renewal, and Customer Success calls; OFF for Internal Sync, 1:1, Recurring Standup, Interview. Layer on overrides: ON for any meeting linked to a deal with value > $50K regardless of type; OFF if any attendee has notetaker-opt-out flag. Hosts can manually override per-meeting via add_blu_to_live_meeting or the meeting record toggle.'
      prompt: 'Configure notetaker autojoin rules based on the meeting-type audit. Default policy: ON for Discovery, Demo, Proposal, Close, Renewal, and Customer Success calls; OFF for Internal Sync, 1:1, Recurring Standup, Interview. Layer on overrides: ON for any meeting linked to a deal with value > $50K regardless of type; OFF if any attendee has notetaker-opt-out flag. Hosts can manually override per-meeting via add_blu_to_live_meeting or the meeting record toggle.'
    - step: 3
      title: Build Coverage Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - meeting_type_inventory
      - notetaker_config
      description: 'Compose a notetaker coverage dashboard: % of meetings with notetaker present (target: 80%+ for revenue-impacting types), coverage broken down by meeting type and rep, failed-join count (notetaker invited but didn''t join — usually a calendar permission issue), and manual-add count (hosts having to invite Blu manually — signal of misconfigured rules). Flag any type with <60% coverage as a configuration gap.'
      prompt: 'Compose a notetaker coverage dashboard: % of meetings with notetaker present (target: 80%+ for revenue-impacting types), coverage broken down by meeting type and rep, failed-join count (notetaker invited but didn''t join — usually a calendar permission issue), and manual-add count (hosts having to invite Blu manually — signal of misconfigured rules). Flag any type with <60% coverage as a configuration gap.'
  outputs:
    - { name: meeting_type_inventory, type: meeting_type_inventory, cardinality: single, description: "Meeting Type Inventory produced by this recipe." }
    - { name: notetaker_config, type: notetaker_config, cardinality: single, description: "Notetaker Config produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Notetaker Coverage Setup

## Procedure

1. **Audit Current Meeting Types** [`list_meeting_types`] — List all configured meeting types in the project. For each, surface: name, default duration, current notetaker auto-join setting, and meetings-per-month count over the last 90 days. This is the baseline for designing coverage rules — types with high volume and high revenue impact (demo, discovery, close, renewal) should have autojoin on; types with low strategic value (internal sync, recurring 1:1) likely shouldn't. → produces: meeting_type_inventory
2. **Configure Autojoin Rules** [`configure_notetaker_autojoin`] — Configure notetaker autojoin rules based on the meeting-type audit. Default policy: ON for Discovery, Demo, Proposal, Close, Renewal, and Customer Success calls; OFF for Internal Sync, 1:1, Recurring Standup, Interview. Layer on overrides: ON for any meeting linked to a deal with value > $50K regardless of type; OFF if any attendee has notetaker-opt-out flag. Hosts can manually override per-meeting via add_blu_to_live_meeting or the meeting record toggle. → produces: notetaker_config
3. **Build Coverage Dashboard** [`create_dashboard`] — Compose a notetaker coverage dashboard: % of meetings with notetaker present (target: 80%+ for revenue-impacting types), coverage broken down by meeting type and rep, failed-join count (notetaker invited but didn't join — usually a calendar permission issue), and manual-add count (hosts having to invite Blu manually — signal of misconfigured rules). Flag any type with <60% coverage as a configuration gap. → produces: dashboard
