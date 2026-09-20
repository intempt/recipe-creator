---
name: meeting-types-taxonomy
description: Use when a user mentions "meeting types taxonomy", "set up meeting type catalog", "sales meeting taxonomy", or asks for related help. Establish a clean meeting-type catalog — Discovery, Demo, Proposal, Close, Onboarding, QBR, Renewal, Customer Success, Internal — so every downstream recipe (summaries, coaching, reporting) can target the right call type without ambiguity.
arguments: []
intempt:
  id: meeting-types-taxonomy
  version: 1.0.0
  slashCommand: /meeting-types-taxonomy
  group: Meetings
  shortDescription: 'Establish a clean meeting-type catalog (Discovery, Demo, Proposal, Close, Onboarding, QBR, Renewal, Customer Success, Internal) so every downstream recipe (summaries, coaching, reporting) can target the right call type without ambiguity.'
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
      title: Audit Existing Types
      command: list_meeting_types
      produces: meeting_type_inventory
      bindsAs: meeting_type_inventory
      description: 'List current meeting types in the project. For each existing type, classify: KEEP (clearly defined, distinct purpose, sufficient volume to justify), MERGE (overlaps with another type — e.g. ''product walkthrough'' and ''demo'' usually merge), RETIRE (dead type, no meetings booked in 90 days), or RENAME (purpose is right but name is unclear).'
      prompt: 'List current meeting types in the project. For each existing type, classify: KEEP (clearly defined, distinct purpose, sufficient volume to justify), MERGE (overlaps with another type — e.g. ''product walkthrough'' and ''demo'' usually merge), RETIRE (dead type, no meetings booked in 90 days), or RENAME (purpose is right but name is unclear).'
    - step: 2
      title: Create Discovery Type
      command: create_meeting_type
      produces: meeting_type
      bindsAs: discovery_type
      dependsOn:
      - meeting_type_inventory
      description: 'Create or update the ''Discovery'' meeting type. Default duration: 30 min. Booking link visibility: prospects who haven''t yet seen a demo. Required outcome on completion: champion identified, pain confirmed, current solution noted, timeline established, budget signal captured. Default notetaker autojoin: ON. Skip creation if a clean equivalent already exists (use the audit output).'
      prompt: 'Create or update the ''Discovery'' meeting type. Default duration: 30 min. Booking link visibility: prospects who haven''t yet seen a demo. Required outcome on completion: champion identified, pain confirmed, current solution noted, timeline established, budget signal captured. Default notetaker autojoin: ON. Skip creation if a clean equivalent already exists (use the audit output).'
    - step: 3
      title: Create Demo Type
      command: create_meeting_type
      produces: meeting_type
      bindsAs: demo_type
      dependsOn:
      - meeting_type_inventory
      - discovery_type
      description: 'Create or update the ''Demo'' meeting type. Default duration: 45 min. Booking link visibility: prospects who have completed discovery (or self-served past the qualifying threshold). Required outcome: features demonstrated logged, technical questions captured, objections logged, next-step proposed. Default notetaker autojoin: ON. Skip if a clean equivalent exists.'
      prompt: 'Create or update the ''Demo'' meeting type. Default duration: 45 min. Booking link visibility: prospects who have completed discovery (or self-served past the qualifying threshold). Required outcome: features demonstrated logged, technical questions captured, objections logged, next-step proposed. Default notetaker autojoin: ON. Skip if a clean equivalent exists.'
    - step: 4
      title: Create Proposal Type
      command: create_meeting_type
      produces: meeting_type
      bindsAs: proposal_type
      dependsOn:
      - meeting_type_inventory
      - demo_type
      description: 'Create or update the ''Proposal'' meeting type. Default duration: 30 min. Booking link visibility: opportunities at proposal stage. Required outcome: pricing structure confirmed, contract questions captured, decision-maker presence verified, expected close date. Default notetaker autojoin: ON.'
      prompt: 'Create or update the ''Proposal'' meeting type. Default duration: 30 min. Booking link visibility: opportunities at proposal stage. Required outcome: pricing structure confirmed, contract questions captured, decision-maker presence verified, expected close date. Default notetaker autojoin: ON.'
    - step: 5
      title: Create Renewal Type
      command: create_meeting_type
      produces: meeting_type
      bindsAs: renewal_type
      dependsOn:
      - meeting_type_inventory
      - proposal_type
      description: 'Create or update the ''Renewal'' meeting type. Default duration: 30 min. Booking link visibility: existing customers within 90 days of contract end. Required outcome: usage health confirmed, stakeholder confirmation, expansion/contraction signals, contract terms discussion. Default notetaker autojoin: ON.'
      prompt: 'Create or update the ''Renewal'' meeting type. Default duration: 30 min. Booking link visibility: existing customers within 90 days of contract end. Required outcome: usage health confirmed, stakeholder confirmation, expansion/contraction signals, contract terms discussion. Default notetaker autojoin: ON.'
    - step: 6
      title: Create Customer Success Type
      command: create_meeting_type
      produces: meeting_type
      bindsAs: cs_type
      dependsOn:
      - meeting_type_inventory
      - renewal_type
      description: 'Create or update the ''Customer Success Check-in'' meeting type. Default duration: 30 min. Booking link visibility: existing customers; reachable from in-app help center. Required outcome: usage patterns discussed, blockers captured, expansion opportunities noted. Default notetaker autojoin: ON.'
      prompt: 'Create or update the ''Customer Success Check-in'' meeting type. Default duration: 30 min. Booking link visibility: existing customers; reachable from in-app help center. Required outcome: usage patterns discussed, blockers captured, expansion opportunities noted. Default notetaker autojoin: ON.'
  outputs:
    - { name: meeting_type_inventory, type: meeting_type_inventory, cardinality: single, description: "Meeting Type Inventory produced by this recipe." }
    - { name: meeting_type, type: meeting_type, cardinality: single, description: "Meeting Type produced by this recipe." }
---

# Meeting Types Taxonomy

## Procedure

1. **Audit Existing Types** [`list_meeting_types`] — List current meeting types in the project. For each existing type, classify: KEEP (clearly defined, distinct purpose, sufficient volume to justify), MERGE (overlaps with another type — e.g. 'product walkthrough' and 'demo' usually merge), RETIRE (dead type, no meetings booked in 90 days), or RENAME (purpose is right but name is unclear). → produces: meeting_type_inventory
2. **Create Discovery Type** [`create_meeting_type`] — Create or update the 'Discovery' meeting type. Default duration: 30 min. Booking link visibility: prospects who haven't yet seen a demo. Required outcome on completion: champion identified, pain confirmed, current solution noted, timeline established, budget signal captured. Default notetaker autojoin: ON. Skip creation if a clean equivalent already exists (use the audit output). → produces: meeting_type
3. **Create Demo Type** [`create_meeting_type`] — Create or update the 'Demo' meeting type. Default duration: 45 min. Booking link visibility: prospects who have completed discovery (or self-served past the qualifying threshold). Required outcome: features demonstrated logged, technical questions captured, objections logged, next-step proposed. Default notetaker autojoin: ON. Skip if a clean equivalent exists. → produces: meeting_type
4. **Create Proposal Type** [`create_meeting_type`] — Create or update the 'Proposal' meeting type. Default duration: 30 min. Booking link visibility: opportunities at proposal stage. Required outcome: pricing structure confirmed, contract questions captured, decision-maker presence verified, expected close date. Default notetaker autojoin: ON. → produces: meeting_type
5. **Create Renewal Type** [`create_meeting_type`] — Create or update the 'Renewal' meeting type. Default duration: 30 min. Booking link visibility: existing customers within 90 days of contract end. Required outcome: usage health confirmed, stakeholder confirmation, expansion/contraction signals, contract terms discussion. Default notetaker autojoin: ON. → produces: meeting_type
6. **Create Customer Success Type** [`create_meeting_type`] — Create or update the 'Customer Success Check-in' meeting type. Default duration: 30 min. Booking link visibility: existing customers; reachable from in-app help center. Required outcome: usage patterns discussed, blockers captured, expansion opportunities noted. Default notetaker autojoin: ON. → produces: meeting_type
