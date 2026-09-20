---
name: hubspot-pql-to-deal
description: Use when a user mentions "PQL to hubspot deal", "create deal from product signal", "product led pipeline", or asks for related help. Create a HubSpot deal from a product-qualified signal, so the pipeline reflects product evidence and not only outbound activity.
arguments: []
intempt:
  id: hubspot-pql-to-deal
  title: "Product qualified signal to a HubSpot deal"
  version: 1.0.0
  slashCommand: /hubspot-pql-to-deal
  group: Workflows
  shortDescription: "Opens a HubSpot deal when an account's usage says they are ready to buy, so the pipeline reflects product evidence and not only outbound activity."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [hubspot, pql, deal-creation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    events:
      - { value: feature_used, severity: recommended }
    integrations:
      - { value: hubspot, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
  procedure:
    - step: 1
      title: "Define what ready to buy means"
      command: create_segment
      produces: segment
      bindsAs: pql
      description: "A segment describing the product qualified account: the usage that means someone is ready to buy, agreed once and reused."
      prompt: 'Create the segment describing the product-qualified account: the usage that means someone is ready to buy, agreed once and reused.'
    - step: 2
      title: "Open the deal, leave the rest"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - pql
      description: "A HubSpot deal is created for each qualifying account, matched on a key so a second signal updates that deal rather than opening a duplicate. Only the fields Intempt owns are set: the source, the signal that triggered it and the score. Stage and amount are left to the rep."
      prompt: 'Create a workflow that creates a HubSpot deal for each qualifying account, matched on a key so a second signal updates the deal instead of opening a duplicate. Set only the fields Intempt owns (source, the signal that triggered it, the score) and leave stage and amount to the rep.'
  outputs:
    - { name: pql, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product qualified signal to a HubSpot deal

Opens a HubSpot deal when an account's usage says they are ready to buy, so the pipeline reflects product evidence and not only outbound activity.

## Before you run it

- Connect hubspot
- Send the `feature_used` event

## What it does

1. **Define what ready to buy means** (`create_segment`)

   A segment describing the product qualified account: the usage that means someone is ready to buy, agreed once and reused.

2. **Open the deal, leave the rest** (`create_workflow`)

   A HubSpot deal is created for each qualifying account, matched on a key so a second signal updates that deal rather than opening a duplicate. Only the fields Intempt owns are set: the source, the signal that triggered it and the score. Stage and amount are left to the rep.

## What you end up with

- **pql** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
