---
name: hubspot-lifecycle-writeback
description: Use when a user mentions "lifecycle to hubspot", "sync lifecycle stage", "write lifecycle back to CRM", or asks for related help. Write the lifecycle stage computed here back onto the HubSpot contact, so marketing and sales read the same status.
arguments: []
intempt:
  id: hubspot-lifecycle-writeback
  title: "Write lifecycle back to HubSpot"
  version: 1.0.0
  slashCommand: /hubspot-lifecycle-writeback
  group: Workflows
  shortDescription: "Pushes the lifecycle stage computed from real product and billing behaviour onto the HubSpot contact, so sales and marketing read the same thing."
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
      title: "Define the lifecycle honestly"
      command: create_attribute
      produces: attribute
      bindsAs: lifecycle
      description: "Trialing, active, at risk or churned, computed from product and billing reality rather than from whatever a form last said. That is the value worth holding in two systems."
      prompt: 'Create the lifecycle attribute from product and billing reality (trialing, active, at risk, churned) rather than from whatever a form last said. This is the value worth having in two systems.'
    - step: 2
      title: "Push it one way to HubSpot"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - lifecycle
      description: "The HubSpot contact property is updated whenever the lifecycle changes. This field travels one way: Intempt owns it and HubSpot displays it. A field written from both ends needs a stated winner, or the two systems quietly disagree for months."
      prompt: 'Create a workflow updating the HubSpot contact property when the lifecycle changes. The direction is one way on this field: Intempt owns it, HubSpot displays it. A field written from both sides needs a stated winner, and pretending otherwise is how a CRM and a CDP quietly disagree for months.'
  outputs:
    - { name: lifecycle, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Write lifecycle back to HubSpot

Pushes the lifecycle stage computed from real product and billing behaviour onto the HubSpot contact, so sales and marketing read the same thing.

## Before you run it

- Connect hubspot

## What it does

1. **Define the lifecycle honestly** (`create_attribute`)

   Trialing, active, at risk or churned, computed from product and billing reality rather than from whatever a form last said. That is the value worth holding in two systems.

2. **Push it one way to HubSpot** (`create_workflow`)

   The HubSpot contact property is updated whenever the lifecycle changes. This field travels one way: Intempt owns it and HubSpot displays it. A field written from both ends needs a stated winner, or the two systems quietly disagree for months.

## What you end up with

- **lifecycle** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
