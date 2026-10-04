---
id: hubspot-pql-to-deal
title: Product qualified signal to a HubSpot deal
slash_command: /hubspot-pql-to-deal
group: Workflows
owner: intempt
curator: trishik
summary: Opens a HubSpot deal when an account's usage says they are ready to buy, so the pipeline reflects
  product evidence and not only outbound activity.
description: >-
  Create a HubSpot deal from a product-qualified signal, so the pipeline reflects product evidence and
  not only outbound activity.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - saas
  complexity: standard
  executionMode: live
  tags:
    - hubspot
    - pql
    - deal-creation
prerequisites:
  events:
    - value: feature_used
      severity: recommended
  integrations:
    - value: hubspot
      severity: blocking
touches:
  reads:
    - The feature_used event in your project
    - Your HubSpot connection
  writes:
    - A new segment, from step 1 "Define what ready to buy means"
    - A new workflow, from step 2 "Open the deal, leave the rest"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Define what ready to buy means
    summary: >-
      A segment describing the product qualified account: the usage that means someone is ready to buy,
      agreed once and reused.
    builds: segment
    description: >-
      Create the segment describing the product-qualified account: the usage that means someone is ready
      to buy, agreed once and reused.
  - id: s2
    title: Open the deal, leave the rest
    summary: >-
      A HubSpot deal is created for each qualifying account, matched on a key so a second signal updates
      that deal rather than opening a duplicate. Only the fields Intempt owns are set: the source, the
      signal that triggered it and the score. Stage and amount are left to the rep.
    builds: workflow
    description: >-
      Create a workflow that creates a HubSpot deal for each qualifying account, matched on a key so a
      second signal updates the deal instead of opening a duplicate. Set only the fields Intempt owns
      (source, the signal that triggered it, the score) and leave stage and amount to the rep. Use the
      result of "Define what ready to buy means".
    dependsOn:
      - s1
outputs:
  - key: pql
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product qualified signal to a HubSpot deal

Opens a HubSpot deal when an account's usage says they are ready to buy, so the pipeline reflects product evidence and not only outbound activity.

## Steps

1. **Define what ready to buy means** (builds segment)

   A segment describing the product qualified account: the usage that means someone is ready to buy, agreed once and reused.

2. **Open the deal, leave the rest** (builds workflow)

   A HubSpot deal is created for each qualifying account, matched on a key so a second signal updates that deal rather than opening a duplicate. Only the fields Intempt owns are set: the source, the signal that triggered it and the score. Stage and amount are left to the rep.

## What you end up with

- **pql** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## What this recipe touches

Reads:

- The feature_used event in your project
- Your HubSpot connection

Writes:

- A new segment, from step 1 "Define what ready to buy means"
- A new workflow, from step 2 "Open the deal, leave the rest"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
