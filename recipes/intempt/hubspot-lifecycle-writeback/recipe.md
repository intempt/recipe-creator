---
id: hubspot-lifecycle-writeback
title: Write lifecycle back to HubSpot
slash_command: /hubspot-lifecycle-writeback
group: Workflows
owner: intempt
summary: Pushes the lifecycle stage computed from real product and billing behaviour onto the HubSpot
  contact, so sales and marketing read the same thing.
description: >-
  Write the lifecycle stage computed here back onto the HubSpot contact, so marketing and sales read the
  same status.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - saas
  complexity: standard
  executionMode: live
  tags:
    - hubspot
    - lifecycle
    - sync
prerequisites:
  integrations:
    - value: hubspot
      severity: blocking
touches:
  reads:
    - Your HubSpot connection
  writes:
    - A new attribute, from step 1 "Define the lifecycle honestly"
    - A new workflow, from step 2 "Push it one way to HubSpot"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Define the lifecycle honestly
    summary: >-
      Trialing, active, at risk or churned, computed from product and billing reality rather than from
      whatever a form last said. That is the value worth holding in two systems.
    builds: attribute
    description: >-
      Create the lifecycle attribute from product and billing reality (trialing, active, at risk, churned)
      rather than from whatever a form last said. This is the value worth having in two systems.
  - id: s2
    title: Push it one way to HubSpot
    summary: >-
      The HubSpot contact property is updated whenever the lifecycle changes. This field travels one way:
      Intempt owns it and HubSpot displays it. A field written from both ends needs a stated winner, or
      the two systems quietly disagree for months.
    builds: workflow
    description: >-
      Create a workflow updating the HubSpot contact property when the lifecycle changes. The direction
      is one way on this field: Intempt owns it, HubSpot displays it. A field written from both sides
      needs a stated winner, and pretending otherwise is how a CRM and a CDP quietly disagree for months.
      Use the result of "Define the lifecycle honestly".
    dependsOn:
      - s1
outputs:
  - key: lifecycle
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Write lifecycle back to HubSpot

Pushes the lifecycle stage computed from real product and billing behaviour onto the HubSpot contact, so sales and marketing read the same thing.

## Steps

1. **Define the lifecycle honestly** (builds attribute)

   Trialing, active, at risk or churned, computed from product and billing reality rather than from whatever a form last said. That is the value worth holding in two systems.

2. **Push it one way to HubSpot** (builds workflow)

   The HubSpot contact property is updated whenever the lifecycle changes. This field travels one way: Intempt owns it and HubSpot displays it. A field written from both ends needs a stated winner, or the two systems quietly disagree for months.

## What you end up with

- **lifecycle** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## What this recipe touches

Reads:

- Your HubSpot connection

Writes:

- A new attribute, from step 1 "Define the lifecycle honestly"
- A new workflow, from step 2 "Push it one way to HubSpot"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
