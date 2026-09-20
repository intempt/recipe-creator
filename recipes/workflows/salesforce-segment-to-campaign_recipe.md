---
name: salesforce-segment-to-campaign
description: Use when a user mentions "segment to salesforce campaign", "add leads to campaign", "campaign membership from segment", or asks for related help. Add a segment's members to a Salesforce campaign, which is how a CDP audience becomes something a sales team can actually run against.
arguments: []
intempt:
  id: salesforce-segment-to-campaign
  title: "Segment into a Salesforce campaign"
  version: 1.0.0
  slashCommand: /salesforce-segment-to-campaign
  group: Workflows
  shortDescription: "Puts a segment's members into a Salesforce campaign, which is how an audience built here becomes something a sales team can run against."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: revops-automator
    mode: [b2b]
    complexity: standard
    executionMode: live
    tags: [salesforce, campaign, audience-activation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    integrations:
      - { value: salesforce, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
  procedure:
    - step: 1
      title: "Define the audience once"
      command: create_segment
      produces: segment
      bindsAs: audience
      description: "The segment whose members belong in the campaign, defined here rather than rebuilt in Salesforce, so there is one answer to who is in it."
      prompt: 'Create the segment whose members belong in the campaign. Keep the definition here rather than duplicating it in Salesforce, so there is one answer to who is in the audience.'
    - step: 2
      title: "Add members without doubling"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - audience
      description: "Each member is added to the named campaign with a member status. Adding is idempotent, so anyone already in it is left alone. Removal is deliberately not part of this: campaign membership records who was contacted, and deleting it destroys the attribution."
      prompt: 'Create a workflow that adds each member to the named Salesforce campaign with a campaign member status. Adding is idempotent (a member already in the campaign is left alone rather than duplicated) and removal is deliberately not part of this recipe, because campaign membership is a record of who was contacted and deleting it destroys attribution.'
  outputs:
    - { name: audience, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Segment into a Salesforce campaign

Puts a segment's members into a Salesforce campaign, which is how an audience built here becomes something a sales team can run against.

## Before you run it

- Connect salesforce

## What it does

1. **Define the audience once** (`create_segment`)

   The segment whose members belong in the campaign, defined here rather than rebuilt in Salesforce, so there is one answer to who is in it.

2. **Add members without doubling** (`create_workflow`)

   Each member is added to the named campaign with a member status. Adding is idempotent, so anyone already in it is left alone. Removal is deliberately not part of this: campaign membership records who was contacted, and deleting it destroys the attribution.

## What you end up with

- **audience** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
