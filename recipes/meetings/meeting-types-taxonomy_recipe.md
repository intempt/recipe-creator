---
name: meeting-types-taxonomy
description: Use when a user mentions "meeting types taxonomy", "set up meeting type catalog", "sales meeting taxonomy", or asks for related help. Establish a clean meeting-type catalog (Discovery, Demo, Proposal, Close, Onboarding, QBR, Renewal, Customer Success, Internal) so every downstream recipe (summaries, coaching, reporting) can target the right call type without ambiguity.
arguments: []
intempt:
  id: meeting-types-taxonomy
  version: 1.0.0
  slashCommand: /meeting-types-taxonomy
  group: Meetings
  title: "Set up your meeting types"
  shortDescription: "Sorts your calls into a clean set of types so summaries, coaching and reporting all target the right kind of call instead of guessing."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [meeting-types, taxonomy]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - list_meeting_types
    - create_meeting_type
  procedure:
    - step: 1
      title: "Audit the types you have"
      command: list_meeting_types
      produces: meeting_type_inventory
      bindsAs: meeting_type_inventory
      description: "Each existing meeting type marked keep, merge, retire or rename, based on whether it has a distinct purpose and real booking volume."
      prompt: 'List current meeting types in the project. For each existing type, classify: KEEP (clearly defined, distinct purpose, sufficient volume to justify), MERGE (overlaps with another type: e.g. ''product walkthrough'' and ''demo'' usually merge), RETIRE (dead type, no meetings booked in 90 days), or RENAME (purpose is right but name is unclear).'
    - step: 2
      title: "Create the Discovery type"
      command: create_meeting_type
      produces: meeting_type
      bindsAs: discovery_type
      dependsOn:
      - meeting_type_inventory
      description: "30 minutes, offered to prospects who have not seen a demo. The notetaker joins by default. The call is complete once champion, pain, current tool, timeline and budget signal are captured."
      prompt: 'Create or update the ''Discovery'' meeting type. Default duration: 30 min. Booking link visibility: prospects who haven''t yet seen a demo. Required outcome on completion: champion identified, pain confirmed, current solution noted, timeline established, budget signal captured. Default notetaker autojoin: ON. Skip creation if a clean equivalent already exists (use the audit output).'
    - step: 3
      title: "Create the Demo type"
      command: create_meeting_type
      produces: meeting_type
      bindsAs: demo_type
      dependsOn:
      - meeting_type_inventory
      - discovery_type
      description: "45 minutes, offered after discovery. The notetaker joins by default. The call is complete once features shown, technical questions, objections and the next step are logged."
      prompt: 'Create or update the ''Demo'' meeting type. Default duration: 45 min. Booking link visibility: prospects who have completed discovery (or self-served past the qualifying threshold). Required outcome: features demonstrated logged, technical questions captured, objections logged, next-step proposed. Default notetaker autojoin: ON. Skip if a clean equivalent exists.'
    - step: 4
      title: "Create the Proposal type"
      command: create_meeting_type
      produces: meeting_type
      bindsAs: proposal_type
      dependsOn:
      - meeting_type_inventory
      - demo_type
      description: "30 minutes, offered at proposal stage. The notetaker joins by default. The call is complete once pricing, contract questions, decision-maker presence and expected close date are confirmed."
      prompt: 'Create or update the ''Proposal'' meeting type. Default duration: 30 min. Booking link visibility: opportunities at proposal stage. Required outcome: pricing structure confirmed, contract questions captured, decision-maker presence verified, expected close date. Default notetaker autojoin: ON.'
    - step: 5
      title: "Create the Renewal type"
      command: create_meeting_type
      produces: meeting_type
      bindsAs: renewal_type
      dependsOn:
      - meeting_type_inventory
      - proposal_type
      description: "30 minutes, offered to customers within 90 days of contract end. The notetaker joins by default. The call is complete once usage health, stakeholders, expansion or contraction signals and contract terms are covered."
      prompt: 'Create or update the ''Renewal'' meeting type. Default duration: 30 min. Booking link visibility: existing customers within 90 days of contract end. Required outcome: usage health confirmed, stakeholder confirmation, expansion/contraction signals, contract terms discussion. Default notetaker autojoin: ON.'
    - step: 6
      title: "Create the Check-in type"
      command: create_meeting_type
      produces: meeting_type
      bindsAs: cs_type
      dependsOn:
      - meeting_type_inventory
      - renewal_type
      description: "30 minutes for existing customers, reachable from the in-app help center. The notetaker joins by default. The call is complete once usage, blockers and expansion opportunities are noted."
      prompt: 'Create or update the ''Customer Success Check-in'' meeting type. Default duration: 30 min. Booking link visibility: existing customers; reachable from in-app help center. Required outcome: usage patterns discussed, blockers captured, expansion opportunities noted. Default notetaker autojoin: ON.'
  outputs:
    - { name: meeting_type_inventory, type: meeting_type_inventory, cardinality: single, description: "Meeting Type Inventory produced by this recipe." }
    - { name: meeting_type, type: meeting_type, cardinality: single, description: "Meeting Type produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Set up your meeting types

Sorts your calls into a clean set of types so summaries, coaching and reporting all target the right kind of call instead of guessing.

## What it does

1. **Audit the types you have** (`list_meeting_types`)

   Each existing meeting type marked keep, merge, retire or rename, based on whether it has a distinct purpose and real booking volume.

2. **Create the Discovery type** (`create_meeting_type`)

   30 minutes, offered to prospects who have not seen a demo. The notetaker joins by default. The call is complete once champion, pain, current tool, timeline and budget signal are captured.

3. **Create the Demo type** (`create_meeting_type`)

   45 minutes, offered after discovery. The notetaker joins by default. The call is complete once features shown, technical questions, objections and the next step are logged.

4. **Create the Proposal type** (`create_meeting_type`)

   30 minutes, offered at proposal stage. The notetaker joins by default. The call is complete once pricing, contract questions, decision-maker presence and expected close date are confirmed.

5. **Create the Renewal type** (`create_meeting_type`)

   30 minutes, offered to customers within 90 days of contract end. The notetaker joins by default. The call is complete once usage health, stakeholders, expansion or contraction signals and contract terms are covered.

6. **Create the Check-in type** (`create_meeting_type`)

   30 minutes for existing customers, reachable from the in-app help center. The notetaker joins by default. The call is complete once usage, blockers and expansion opportunities are noted.

## What you end up with

- **meeting_type_inventory** (meeting_type_inventory): Meeting Type Inventory produced by this recipe.
- **meeting_type** (meeting_type): Meeting Type produced by this recipe.
