---
name: Data Quality
description: Source health monitoring, event flow validation, schema drift alerts, identity resolution.
intempt:
  id: data-quality
  version: 1.0.0
  slashCommand: /data-quality
  shortDescription: Source health monitoring, event flow validation, schema drift alerts, identity resolution.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    - marketing
    agent: data-analyst
    mode:
    - all
    complexity: standard
    executionMode: live
    tags:
    - data-quality
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: event_mapping
    type: event-mapping
    description: Event Mapping produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: audit-event-mappings
    describe: Audit current event mappings for schema drift, missing required attributes, and identity resolution gaps.
    produces: event_mapping
  - id: build-quality-dashboard
    describe: Compose a dashboard showing source health, event flow rates, schema-drift incidents, and identity-resolution
      success rate.
    produces: dashboard
  - id: build-drift-alert-workflow
    describe: Create a workflow alerting the team when schema drift or source health drops below threshold.
    produces: workflow
---

# Data Quality

Source health monitoring, event flow validation, schema drift alerts, identity resolution.

## Outputs

- **event_mapping** (event-mapping): Event Mapping produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Audit current event mappings for schema drift, missing required attributes, and identity resolution gaps.
2. Compose a dashboard showing source health, event flow rates, schema-drift incidents, and identity-resolution success rate.
3. Create a workflow alerting the team when schema drift or source health drops below threshold.
