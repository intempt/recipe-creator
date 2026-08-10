---
name: hubspot-pql-to-deal
description: Use when a user mentions "PQL to hubspot deal", "create deal from product signal", "product led pipeline", or asks for related help. Create a HubSpot deal from a product-qualified signal, so the pipeline reflects product evidence and not only outbound activity.
arguments: []
intempt:
  id: hubspot-pql-to-deal
  version: 1.0.0
  slashCommand: /hubspot-pql-to-deal
  group: Workflows
  shortDescription: "Create a HubSpot deal from a product-qualified signal, so the pipeline reflects product evidence and not only outbound activity."
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
      title: Define The Signal
      command: create_segment
      produces: segment
      bindsAs: pql
      description: 'Create the segment describing the product-qualified account — the usage that means someone is ready to buy, agreed once and reused.'
      prompt: 'Create the segment describing the product-qualified account — the usage that means someone is ready to buy, agreed once and reused.'
    - step: 2
      title: Create The Deal
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - pql
      description: 'Create a workflow that creates a HubSpot deal for each qualifying account, matched on a key so a second signal updates the deal instead of opening a duplicate. Set only the fields Intempt owns — source, the signal that triggered it, the score — and leave stage and amount to the rep.'
      prompt: 'Create a workflow that creates a HubSpot deal for each qualifying account, matched on a key so a second signal updates the deal instead of opening a duplicate. Set only the fields Intempt owns — source, the signal that triggered it, the score — and leave stage and amount to the rep.'
  outputs:
    - { name: pql, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Hubspot Pql To Deal

## Procedure

1. **Define The Signal** [`create_segment`] — Create the segment describing the product-qualified account — the usage that means someone is ready to buy, agreed once and reused. → produces: segment
2. **Create The Deal** [`create_workflow`] — Create a workflow that creates a HubSpot deal for each qualifying account, matched on a key so a second signal updates the deal instead of opening a duplicate. Set only the fields Intempt owns — source, the signal that triggered it, the score — and leave stage and amount to the rep. → produces: workflow

## Prerequisites

- Event `feature_used` (recommended)
- Integration **hubspot** (blocking)
