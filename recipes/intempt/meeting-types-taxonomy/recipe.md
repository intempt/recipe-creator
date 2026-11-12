---
frontmatter_id: meeting-types-taxonomy
slash_command: /meeting-types-taxonomy
description: Organizes calls with the notetaker's built in All, My, and Shared views so downstream summaries and reporting pull from the right call set.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Organizes sales and customer calls into clear meeting types (Discovery, Demo, Proposal, Renewal, Check-in) so summaries
    and reports draw from the right set of calls.
  parameters:
  - name: discovery_duration
    type: duration
    label: Discovery call default duration
    default: 30 min
    required: false
  - name: demo_duration
    type: duration
    label: Demo call default duration
    default: 45 min
    required: false
  - name: proposal_duration
    type: duration
    label: Proposal call default duration
    default: 30 min
    required: false
  - name: renewal_duration
    type: duration
    label: Renewal call default duration
    default: 30 min
    required: false
  - name: checkin_duration
    type: duration
    label: Customer Success Check-in default duration
    default: 30 min
    required: false
  - name: renewal_window
    type: duration
    label: Renewal booking window before contract end
    default: 90 d
    required: false
  - name: stale_type_window
    type: duration
    label: Window with no bookings after which a meeting type is considered dead
    default: 90 d
    required: false
  - name: notetaker_autojoin
    type: boolean
    label: Notetaker autojoins meetings by default
    default: true
    required: false
  requirements:
  - slot: meeting_types
    kind: knowledge
    meaning: The project's current list of meeting types and their booking settings, used to audit and avoid duplicates
  - slot: prospect_stage
    kind: attribute
    meaning: The sales stage of a prospect or opportunity (for example, has seen a demo, has completed discovery, at proposal
      stage)
  - slot: contract_end
    kind: attribute
    meaning: The date an existing customer's contract ends
  - slot: customer_status
    kind: attribute
    meaning: Whether a contact is an existing customer
  - slot: notetaker
    kind: integration
    meaning: The meeting notetaker tool that records and summarizes calls
    channel: hubspot
  - slot: help_center
    kind: destination
    meaning: The in-app help center where customers can book a check-in
    optional: true
    channel: hubspot
  steps:
  - id: s1
    builds: report
    instruction: List the current meeting types in {meeting_types}. For each existing type, classify it as KEEP (clearly defined,
      distinct purpose, sufficient volume to justify it), MERGE (overlaps with another type, for example a product walkthrough
      and a demo), RETIRE (no meetings booked in {stale_type_window}), or RENAME (purpose is right but the name is unclear).
  - id: s2
    builds: event
    uses:
    - s1
    - meeting_types
    - prospect_stage
    - notetaker
    - notetaker_autojoin
    - discovery_duration
    instruction: 'Create or update the ''Discovery'' meeting type unless the audit in "Audit the types you have" shows a clean
      equivalent already exists. Set default duration to {discovery_duration}. Set booking link visibility to prospects in
      {prospect_stage} who have not yet seen a demo. Set required outcome on completion: champion identified, pain confirmed,
      current solution noted, timeline established, budget signal captured. Set default notetaker autojoin to {notetaker_autojoin}
      on {notetaker}.'
  - id: s3
    builds: event
    uses:
    - s1
    - s2
    - prospect_stage
    - notetaker
    - notetaker_autojoin
    - demo_duration
    instruction: 'Create or update the ''Demo'' meeting type unless a clean equivalent exists per "Audit the types you have".
      Set default duration to {demo_duration}. Set booking link visibility to prospects in {prospect_stage} who have completed
      discovery or self-served past the qualifying threshold. Set required outcome on completion: features demonstrated logged,
      technical questions captured, objections logged, next step proposed. Set default notetaker autojoin to {notetaker_autojoin}
      on {notetaker}. Use the results of "Audit the types you have" and "Create the Discovery type".'
  - id: s4
    builds: event
    uses:
    - s1
    - s3
    - prospect_stage
    - notetaker
    - notetaker_autojoin
    - proposal_duration
    instruction: 'Create or update the ''Proposal'' meeting type. Set default duration to {proposal_duration}. Set booking
      link visibility to opportunities in {prospect_stage} at proposal stage. Set required outcome on completion: pricing
      structure confirmed, contract questions captured, decision-maker presence verified, expected close date noted. Set default
      notetaker autojoin to {notetaker_autojoin} on {notetaker}. Use the results of "Audit the types you have" and "Create
      the Demo type".'
  - id: s5
    builds: event
    uses:
    - s1
    - s4
    - customer_status
    - contract_end
    - renewal_window
    - notetaker
    - notetaker_autojoin
    - renewal_duration
    instruction: 'Create or update the ''Renewal'' meeting type. Set default duration to {renewal_duration}. Set booking link
      visibility to existing customers in {customer_status} whose {contract_end} falls within {renewal_window}. Set required
      outcome on completion: usage health confirmed, stakeholder confirmation, expansion or contraction signals, contract
      terms discussed. Set default notetaker autojoin to {notetaker_autojoin} on {notetaker}. Use the results of "Audit the
      types you have" and "Create the Proposal type".'
  - id: s6
    builds: event
    uses:
    - s1
    - s5
    - customer_status
    - help_center
    - notetaker
    - notetaker_autojoin
    - checkin_duration
    instruction: 'Create or update the ''Customer Success Check-in'' meeting type. Set default duration to {checkin_duration}.
      Set booking link visibility to existing customers in {customer_status} and make it reachable from {help_center}. Set
      required outcome on completion: usage patterns discussed, blockers captured, expansion opportunities noted. Set default
      notetaker autojoin to {notetaker_autojoin} on {notetaker}. Use the results of "Audit the types you have" and "Create
      the Renewal type".'
---

# Set up your meeting types

Slash command: /meeting-types-taxonomy

## Step 1: Audit the types you have

List current meeting types in the project. For each existing type, classify: KEEP (clearly defined, distinct purpose, sufficient volume to justify), MERGE (overlaps with another type: e.g. 'product walkthrough' and 'demo' usually merge), RETIRE (dead type, no meetings booked in 90 days), or RENAME (purpose is right but name is unclear).

## Step 2: Create the Discovery type

Create or update the 'Discovery' meeting type. Default duration: 30 min. Booking link visibility: prospects who haven't yet seen a demo. Required outcome on completion: champion identified, pain confirmed, current solution noted, timeline established, budget signal captured. Default notetaker autojoin: ON. Skip creation if a clean equivalent already exists (use the audit output). Use the result of "Audit the types you have".

## Step 3: Create the Demo type

Create or update the 'Demo' meeting type. Default duration: 45 min. Booking link visibility: prospects who have completed discovery (or self-served past the qualifying threshold). Required outcome: features demonstrated logged, technical questions captured, objections logged, next-step proposed. Default notetaker autojoin: ON. Skip if a clean equivalent exists. Use the result of "Audit the types you have", "Create the Discovery type".

## Step 4: Create the Proposal type

Create or update the 'Proposal' meeting type. Default duration: 30 min. Booking link visibility: opportunities at proposal stage. Required outcome: pricing structure confirmed, contract questions captured, decision-maker presence verified, expected close date. Default notetaker autojoin: ON. Use the result of "Audit the types you have", "Create the Demo type".

## Step 5: Create the Renewal type

Create or update the 'Renewal' meeting type. Default duration: 30 min. Booking link visibility: existing customers within 90 days of contract end. Required outcome: usage health confirmed, stakeholder confirmation, expansion/contraction signals, contract terms discussion. Default notetaker autojoin: ON. Use the result of "Audit the types you have", "Create the Proposal type".

## Step 6: Create the Check-in type

Create or update the 'Customer Success Check-in' meeting type. Default duration: 30 min. Booking link visibility: existing customers; reachable from in-app help center. Required outcome: usage patterns discussed, blockers captured, expansion opportunities noted. Default notetaker autojoin: ON. Use the result of "Audit the types you have", "Create the Renewal type".
