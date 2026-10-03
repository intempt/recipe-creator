---
id: salesforce-pql-to-lead
title: Product qualified signal to a Salesforce lead
slash_command: /salesforce-pql-to-lead
group: Workflows
owner: intempt
summary: Creates a Salesforce lead the moment product usage says someone is ready, so a signal the product
  saw becomes a record a rep can work.
description: >-
  Create a Salesforce lead the moment a product-qualified signal fires, so a signal the product saw becomes
  a record a rep can work.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
  complexity: standard
  executionMode: live
  tags:
    - salesforce
    - pql
    - lead-creation
prerequisites:
  events:
    - value: feature_used
      severity: recommended
  integrations:
    - value: salesforce
      severity: blocking
steps:
  - id: s1
    title: Agree the qualifying signal
    summary: >-
      The usage threshold, the feature reached or the seats added, defined as a segment rather than buried
      inside the workflow. Sales and product will argue about this definition, so it has to live where
      both can see it.
    builds: segment
    description: >-
      Create a segment describing the product-qualified signal (the usage threshold, the feature reached,
      the seats added) rather than encoding it inside the workflow. The definition is the thing sales
      and product will argue about, so it needs to live somewhere both can see it.
  - id: s2
    title: Upsert the lead, never double
    summary: >-
      Members of the segment are enrolled and a Salesforce lead is created for each, by upsert against
      an external ID rather than a plain create, because a create with no match key generates duplicates
      the rep pays for. Only the fields Intempt owns are mapped, the score, the signal and the source,
      and Salesforce's own fields are left alone. A rejected lead is recorded and skipped rather than
      stopping the rest.
    builds: workflow
    description: >-
      Create a workflow enrolling members of the segment and creating a Salesforce lead for each. Use
      upsert with an external ID rather than create, because a create without a match key is a duplicate
      generator and the rep pays for it. Map only fields Intempt owns (the score, the signal, the source)
      and leave Salesforce-owned fields alone. Failure policy is skip-and-record so one rejected lead
      does not stop the rest. Use the result of "Agree the qualifying signal".
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

# Product qualified signal to a Salesforce lead

Creates a Salesforce lead the moment product usage says someone is ready, so a signal the product saw becomes a record a rep can work.

## Steps

1. **Agree the qualifying signal** (builds segment)

   The usage threshold, the feature reached or the seats added, defined as a segment rather than buried inside the workflow. Sales and product will argue about this definition, so it has to live where both can see it.

2. **Upsert the lead, never double** (builds workflow)

   Members of the segment are enrolled and a Salesforce lead is created for each, by upsert against an external ID rather than a plain create, because a create with no match key generates duplicates the rep pays for. Only the fields Intempt owns are mapped, the score, the signal and the source, and Salesforce's own fields are left alone. A rejected lead is recorded and skipped rather than stopping the rest.

## What you end up with

- **pql** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Availability

Coming soon: waiting on the engine to build workflow.
