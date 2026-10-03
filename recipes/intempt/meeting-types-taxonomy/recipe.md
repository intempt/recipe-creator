---
id: meeting-types-taxonomy
title: Set up your meeting types
slash_command: /meeting-types-taxonomy
group: Meetings
owner: intempt
summary: Sorts your calls into a clean set of types so summaries, coaching and reporting all target the
  right kind of call instead of guessing.
description: >-
  Establish a clean meeting-type catalog (Discovery, Demo, Proposal, Close, Onboarding, QBR, Renewal,
  Customer Success, Internal) so every downstream recipe (summaries, coaching, reporting) can target the
  right call type without ambiguity.
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
    - meeting-types
    - taxonomy
steps:
  - id: s1
    title: Audit the types you have
    summary: >-
      Each existing meeting type marked keep, merge, retire or rename, based on whether it has a distinct
      purpose and real booking volume.
    builds: meeting_type
    description: >-
      List current meeting types in the project. For each existing type, classify: KEEP (clearly defined,
      distinct purpose, sufficient volume to justify), MERGE (overlaps with another type: e.g. 'product
      walkthrough' and 'demo' usually merge), RETIRE (dead type, no meetings booked in 90 days), or RENAME
      (purpose is right but name is unclear).
  - id: s2
    title: Create the Discovery type
    summary: >-
      30 minutes, offered to prospects who have not seen a demo. The notetaker joins by default. The call
      is complete once champion, pain, current tool, timeline and budget signal are captured.
    builds: meeting_type
    description: >-
      Create or update the 'Discovery' meeting type. Default duration: 30 min. Booking link visibility:
      prospects who haven't yet seen a demo. Required outcome on completion: champion identified, pain
      confirmed, current solution noted, timeline established, budget signal captured. Default notetaker
      autojoin: ON. Skip creation if a clean equivalent already exists (use the audit output). Use the
      result of "Audit the types you have".
    dependsOn:
      - s1
  - id: s3
    title: Create the Demo type
    summary: >-
      45 minutes, offered after discovery. The notetaker joins by default. The call is complete once features
      shown, technical questions, objections and the next step are logged.
    builds: meeting_type
    description: >-
      Create or update the 'Demo' meeting type. Default duration: 45 min. Booking link visibility: prospects
      who have completed discovery (or self-served past the qualifying threshold). Required outcome: features
      demonstrated logged, technical questions captured, objections logged, next-step proposed. Default
      notetaker autojoin: ON. Skip if a clean equivalent exists. Use the result of "Audit the types you
      have", "Create the Discovery type".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Create the Proposal type
    summary: >-
      30 minutes, offered at proposal stage. The notetaker joins by default. The call is complete once
      pricing, contract questions, decision-maker presence and expected close date are confirmed.
    builds: meeting_type
    description: >-
      Create or update the 'Proposal' meeting type. Default duration: 30 min. Booking link visibility:
      opportunities at proposal stage. Required outcome: pricing structure confirmed, contract questions
      captured, decision-maker presence verified, expected close date. Default notetaker autojoin: ON.
      Use the result of "Audit the types you have", "Create the Demo type".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Create the Renewal type
    summary: >-
      30 minutes, offered to customers within 90 days of contract end. The notetaker joins by default.
      The call is complete once usage health, stakeholders, expansion or contraction signals and contract
      terms are covered.
    builds: meeting_type
    description: >-
      Create or update the 'Renewal' meeting type. Default duration: 30 min. Booking link visibility:
      existing customers within 90 days of contract end. Required outcome: usage health confirmed, stakeholder
      confirmation, expansion/contraction signals, contract terms discussion. Default notetaker autojoin:
      ON. Use the result of "Audit the types you have", "Create the Proposal type".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Create the Check-in type
    summary: >-
      30 minutes for existing customers, reachable from the in-app help center. The notetaker joins by
      default. The call is complete once usage, blockers and expansion opportunities are noted.
    builds: meeting_type
    description: >-
      Create or update the 'Customer Success Check-in' meeting type. Default duration: 30 min. Booking
      link visibility: existing customers; reachable from in-app help center. Required outcome: usage
      patterns discussed, blockers captured, expansion opportunities noted. Default notetaker autojoin:
      ON. Use the result of "Audit the types you have", "Create the Renewal type".
    dependsOn:
      - s1
      - s5
outputs:
  - key: meeting_type_inventory
    producedByStep: s1
    type: meeting_type_inventory
    description: Meeting Type Inventory produced by this recipe.
  - key: meeting_type
    producedByStep: s6
    type: meeting_type
    description: Meeting Type produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Set up your meeting types

Sorts your calls into a clean set of types so summaries, coaching and reporting all target the right kind of call instead of guessing.

## Steps

1. **Audit the types you have** (builds meeting_type)

   Each existing meeting type marked keep, merge, retire or rename, based on whether it has a distinct purpose and real booking volume.

2. **Create the Discovery type** (builds meeting_type)

   30 minutes, offered to prospects who have not seen a demo. The notetaker joins by default. The call is complete once champion, pain, current tool, timeline and budget signal are captured.

3. **Create the Demo type** (builds meeting_type)

   45 minutes, offered after discovery. The notetaker joins by default. The call is complete once features shown, technical questions, objections and the next step are logged.

4. **Create the Proposal type** (builds meeting_type)

   30 minutes, offered at proposal stage. The notetaker joins by default. The call is complete once pricing, contract questions, decision-maker presence and expected close date are confirmed.

5. **Create the Renewal type** (builds meeting_type)

   30 minutes, offered to customers within 90 days of contract end. The notetaker joins by default. The call is complete once usage health, stakeholders, expansion or contraction signals and contract terms are covered.

6. **Create the Check-in type** (builds meeting_type)

   30 minutes for existing customers, reachable from the in-app help center. The notetaker joins by default. The call is complete once usage, blockers and expansion opportunities are noted.

## What you end up with

- **meeting_type_inventory** (meeting_type_inventory): Meeting Type Inventory produced by this recipe.
- **meeting_type** (meeting_type): Meeting Type produced by this recipe.

## Availability

Coming soon: waiting on the engine to build meeting_type.
