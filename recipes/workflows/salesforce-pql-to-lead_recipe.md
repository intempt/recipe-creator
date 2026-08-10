---
name: salesforce-pql-to-lead
description: Use when a user mentions "PQL to Salesforce", "create lead from product signal", "product qualified lead salesforce", or asks for related help. Create a Salesforce lead the moment a product-qualified signal fires, so a signal the product saw becomes a record a rep can work.
arguments: []
intempt:
  id: salesforce-pql-to-lead
  version: 1.0.0
  slashCommand: /salesforce-pql-to-lead
  group: Workflows
  shortDescription: "Create a Salesforce lead the moment a product-qualified signal fires, so a signal the product saw becomes a record a rep can work."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b]
    complexity: standard
    executionMode: live
    tags: [salesforce, pql, lead-creation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    events:
      - { value: feature_used, severity: recommended }
    integrations:
      - { value: salesforce, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
  procedure:
    - step: 1
      title: Define The Qualifying Signal
      command: create_segment
      produces: segment
      bindsAs: pql
      description: 'Create a segment describing the product-qualified signal — the usage threshold, the feature reached, the seats added — rather than encoding it inside the workflow. The definition is the thing sales and product will argue about, so it needs to live somewhere both can see it.'
      prompt: 'Create a segment describing the product-qualified signal — the usage threshold, the feature reached, the seats added — rather than encoding it inside the workflow. The definition is the thing sales and product will argue about, so it needs to live somewhere both can see it.'
    - step: 2
      title: Create The Lead In Salesforce
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - pql
      description: 'Create a workflow enrolling members of the segment and creating a Salesforce lead for each. Use upsert with an external ID rather than create, because a create without a match key is a duplicate generator and the rep pays for it. Map only fields Intempt owns — the score, the signal, the source — and leave Salesforce-owned fields alone. Failure policy is skip-and-record so one rejected lead does not stop the rest.'
      prompt: 'Create a workflow enrolling members of the segment and creating a Salesforce lead for each. Use upsert with an external ID rather than create, because a create without a match key is a duplicate generator and the rep pays for it. Map only fields Intempt owns — the score, the signal, the source — and leave Salesforce-owned fields alone. Failure policy is skip-and-record so one rejected lead does not stop the rest.'
  outputs:
    - { name: pql, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Salesforce Pql To Lead

> **Not runnable yet.** Creating a lead in Salesforce has no backend. The connector reads today and cannot write, and Airbyte does not close that gap — its destinations write to warehouses, not into Salesforce. This recipe is published so the demand is recorded and the workflow is designed, and it will fail at the write step until the operation ships.

## Procedure

1. **Define The Qualifying Signal** [`create_segment`] — Create a segment describing the product-qualified signal — the usage threshold, the feature reached, the seats added — rather than encoding it inside the workflow. The definition is the thing sales and product will argue about, so it needs to live somewhere both can see it. → produces: segment
2. **Create The Lead In Salesforce** [`create_workflow`] — Create a workflow enrolling members of the segment and creating a Salesforce lead for each. Use upsert with an external ID rather than create, because a create without a match key is a duplicate generator and the rep pays for it. Map only fields Intempt owns — the score, the signal, the source — and leave Salesforce-owned fields alone. Failure policy is skip-and-record so one rejected lead does not stop the rest. → produces: workflow

## Prerequisites

- Event `feature_used` (recommended)
- Integration **salesforce** (blocking)
