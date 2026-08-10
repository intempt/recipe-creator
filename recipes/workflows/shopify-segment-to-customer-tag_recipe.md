---
name: shopify-segment-to-customer-tag
description: Use when a user mentions "tag shopify customers", "segment to shopify tag", "customer tagging from segment", or asks for related help. Tag Shopify customers from a segment computed here, so a cohort the CDP understands becomes something the store can merchandise against.
arguments: []
intempt:
  id: shopify-segment-to-customer-tag
  version: 1.0.0
  slashCommand: /shopify-segment-to-customer-tag
  group: Workflows
  shortDescription: "Tag Shopify customers from a segment computed here, so a cohort the CDP understands becomes something the store can merchandise against."
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
      title: Define The Cohort
      command: create_segment
      produces: segment
      bindsAs: cohort
      description: 'Create the segment to tag — high lifetime value, repeat buyer, lapsed, whatever the store wants to treat differently. The segment is the definition; the tag is only its shadow in Shopify.'
      prompt: 'Create the segment to tag — high lifetime value, repeat buyer, lapsed, whatever the store wants to treat differently. The segment is the definition; the tag is only its shadow in Shopify.'
    - step: 2
      title: Tag Them In Shopify
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - cohort
      description: 'Create a workflow that tags each member in Shopify. Tags are additive and the workflow states which tag it manages, because a tag the store team also edits by hand will otherwise be fought over silently. Shopify''s own rejection is surfaced verbatim — a tag limit and a permission error need different responses.'
      prompt: 'Create a workflow that tags each member in Shopify. Tags are additive and the workflow states which tag it manages, because a tag the store team also edits by hand will otherwise be fought over silently. Shopify''s own rejection is surfaced verbatim — a tag limit and a permission error need different responses.'
  outputs:
    - { name: cohort, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Shopify Segment To Customer Tag

## Procedure

1. **Define The Cohort** [`create_segment`] — Create the segment to tag — high lifetime value, repeat buyer, lapsed, whatever the store wants to treat differently. The segment is the definition; the tag is only its shadow in Shopify. → produces: segment
2. **Tag Them In Shopify** [`create_workflow`] — Create a workflow that tags each member in Shopify. Tags are additive and the workflow states which tag it manages, because a tag the store team also edits by hand will otherwise be fought over silently. Shopify's own rejection is surfaced verbatim — a tag limit and a permission error need different responses. → produces: workflow

## Prerequisites

- Integration **shopify** (blocking)
