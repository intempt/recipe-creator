---
name: hubspot-lifecycle-writeback
description: Use when a user mentions "lifecycle to hubspot", "sync lifecycle stage", "write lifecycle back to CRM", or asks for related help. Write the lifecycle stage computed here back onto the HubSpot contact, so marketing and sales read the same status.
arguments: []
intempt:
  id: hubspot-lifecycle-writeback
  version: 1.0.0
  slashCommand: /hubspot-lifecycle-writeback
  group: Workflows
  shortDescription: "Write the lifecycle stage computed here back onto the HubSpot contact, so marketing and sales read the same status."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [hubspot, lifecycle, sync]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    integrations:
      - { value: hubspot, severity: blocking }
  invokesCommands:
    - create_attribute
    - create_workflow
  procedure:
    - step: 1
      title: Compute Lifecycle Here
      command: create_attribute
      produces: attribute
      bindsAs: lifecycle
      description: 'Create the lifecycle attribute from product and billing reality — trialing, active, at risk, churned — rather than from whatever a form last said. This is the value worth having in two systems.'
      prompt: 'Create the lifecycle attribute from product and billing reality — trialing, active, at risk, churned — rather than from whatever a form last said. This is the value worth having in two systems.'
    - step: 2
      title: Write It To HubSpot
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - lifecycle
      description: 'Create a workflow updating the HubSpot contact property when the lifecycle changes. The direction is one way on this field: Intempt owns it, HubSpot displays it. A field written from both sides needs a stated winner, and pretending otherwise is how a CRM and a CDP quietly disagree for months.'
      prompt: 'Create a workflow updating the HubSpot contact property when the lifecycle changes. The direction is one way on this field: Intempt owns it, HubSpot displays it. A field written from both sides needs a stated winner, and pretending otherwise is how a CRM and a CDP quietly disagree for months.'
  outputs:
    - { name: lifecycle, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Hubspot Lifecycle Writeback

## Procedure

1. **Compute Lifecycle Here** [`create_attribute`] — Create the lifecycle attribute from product and billing reality — trialing, active, at risk, churned — rather than from whatever a form last said. This is the value worth having in two systems. → produces: attribute
2. **Write It To HubSpot** [`create_workflow`] — Create a workflow updating the HubSpot contact property when the lifecycle changes. The direction is one way on this field: Intempt owns it, HubSpot displays it. A field written from both sides needs a stated winner, and pretending otherwise is how a CRM and a CDP quietly disagree for months. → produces: workflow

## Prerequisites

- Integration **hubspot** (blocking)
