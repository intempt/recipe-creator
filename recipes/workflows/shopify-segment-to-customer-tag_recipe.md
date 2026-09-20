---
name: shopify-segment-to-customer-tag
description: Use when a user mentions "tag shopify customers", "segment to shopify tag", "customer tagging from segment", or asks for related help. Tag Shopify customers from a segment computed here, so a cohort the CDP understands becomes something the store can merchandise against.
arguments: []
intempt:
  id: shopify-segment-to-customer-tag
  title: "Tag Shopify customers from a segment"
  version: 1.0.0
  slashCommand: /shopify-segment-to-customer-tag
  group: Workflows
  shortDescription: "Pushes a cohort computed here onto Shopify customers as a tag, so the store can merchandise against it."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: revops-automator
    mode: [ecommerce]
    complexity: standard
    executionMode: live
    tags: [shopify, tagging, audience-activation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
  procedure:
    - step: 1
      title: "Define the cohort to tag"
      command: create_segment
      produces: segment
      bindsAs: cohort
      description: "High lifetime value, repeat buyer, lapsed, or whatever the store wants to treat differently. The segment is the definition and the tag is only its shadow in Shopify."
      prompt: 'Create the segment to tag: high lifetime value, repeat buyer, lapsed, whatever the store wants to treat differently. The segment is the definition; the tag is only its shadow in Shopify.'
    - step: 2
      title: "Write the tag into Shopify"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - cohort
      description: "Each member is tagged in Shopify. Tags are additive, and the workflow names the one tag it manages, because a tag the store team also edits by hand gets fought over silently. Shopify's own rejection is shown as it came, since a tag limit and a permission error need different responses."
      prompt: 'Create a workflow that tags each member in Shopify. Tags are additive and the workflow states which tag it manages, because a tag the store team also edits by hand will otherwise be fought over silently. Shopify''s own rejection is surfaced verbatim: a tag limit and a permission error need different responses.'
  outputs:
    - { name: cohort, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Tag Shopify customers from a segment

Pushes a cohort computed here onto Shopify customers as a tag, so the store can merchandise against it.

## Before you run it

- Connect shopify

## What it does

1. **Define the cohort to tag** (`create_segment`)

   High lifetime value, repeat buyer, lapsed, or whatever the store wants to treat differently. The segment is the definition and the tag is only its shadow in Shopify.

2. **Write the tag into Shopify** (`create_workflow`)

   Each member is tagged in Shopify. Tags are additive, and the workflow names the one tag it manages, because a tag the store team also edits by hand gets fought over silently. Shopify's own rejection is shown as it came, since a tag limit and a permission error need different responses.

## What you end up with

- **cohort** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
