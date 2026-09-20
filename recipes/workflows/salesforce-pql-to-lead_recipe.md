---
name: salesforce-pql-to-lead
description: Use when a user mentions "PQL to Salesforce", "create lead from product signal", "product qualified lead salesforce", or asks for related help. Create a Salesforce lead the moment a product-qualified signal fires, so a signal the product saw becomes a record a rep can work.
arguments: []
intempt:
  id: salesforce-pql-to-lead
  title: "Product qualified signal to a Salesforce lead"
  version: 1.0.0
  slashCommand: /salesforce-pql-to-lead
  group: Workflows
  shortDescription: "Creates a Salesforce lead the moment product usage says someone is ready, so a signal the product saw becomes a record a rep can work."
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
      title: "Agree the qualifying signal"
      command: create_segment
      produces: segment
      bindsAs: pql
      description: "The usage threshold, the feature reached or the seats added, defined as a segment rather than buried inside the workflow. Sales and product will argue about this definition, so it has to live where both can see it."
      prompt: 'Create a segment describing the product-qualified signal (the usage threshold, the feature reached, the seats added) rather than encoding it inside the workflow. The definition is the thing sales and product will argue about, so it needs to live somewhere both can see it.'
    - step: 2
      title: "Upsert the lead, never double"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - pql
      description: "Members of the segment are enrolled and a Salesforce lead is created for each, by upsert against an external ID rather than a plain create, because a create with no match key generates duplicates the rep pays for. Only the fields Intempt owns are mapped, the score, the signal and the source, and Salesforce's own fields are left alone. A rejected lead is recorded and skipped rather than stopping the rest."
      prompt: 'Create a workflow enrolling members of the segment and creating a Salesforce lead for each. Use upsert with an external ID rather than create, because a create without a match key is a duplicate generator and the rep pays for it. Map only fields Intempt owns (the score, the signal, the source) and leave Salesforce-owned fields alone. Failure policy is skip-and-record so one rejected lead does not stop the rest.'
  outputs:
    - { name: pql, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product qualified signal to a Salesforce lead

Creates a Salesforce lead the moment product usage says someone is ready, so a signal the product saw becomes a record a rep can work.

## Before you run it

- Connect salesforce
- Send the `feature_used` event

## What it does

1. **Agree the qualifying signal** (`create_segment`)

   The usage threshold, the feature reached or the seats added, defined as a segment rather than buried inside the workflow. Sales and product will argue about this definition, so it has to live where both can see it.

2. **Upsert the lead, never double** (`create_workflow`)

   Members of the segment are enrolled and a Salesforce lead is created for each, by upsert against an external ID rather than a plain create, because a create with no match key generates duplicates the rep pays for. Only the fields Intempt owns are mapped, the score, the signal and the source, and Salesforce's own fields are left alone. A rejected lead is recorded and skipped rather than stopping the rest.

## What you end up with

- **pql** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
