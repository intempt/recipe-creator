---
id: salesforce-segment-to-campaign
title: Segment into a Salesforce campaign
slash_command: /salesforce-segment-to-campaign
group: Workflows
owner: intempt
curator: trishik
summary: Puts a segment's members into a Salesforce campaign, which is how an audience built here becomes
  something a sales team can run against.
description: >-
  Add a segment's members to a Salesforce campaign, which is how a CDP audience becomes something a sales
  team can actually run against.
version: 2.0.0
classification:
  product:
    - marketing
  agent: revops-automator
  mode:
    - b2b
  complexity: standard
  executionMode: live
  tags:
    - salesforce
    - campaign
    - audience-activation
prerequisites:
  integrations:
    - value: salesforce
      severity: blocking
touches:
  reads:
    - Your Salesforce connection
  writes:
    - A new segment, from step 1 "Define the audience once"
    - A new workflow, from step 2 "Add members without doubling"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Define the audience once
    summary: >-
      The segment whose members belong in the campaign, defined here rather than rebuilt in Salesforce,
      so there is one answer to who is in it.
    builds: segment
    description: >-
      Create the segment whose members belong in the campaign. Keep the definition here rather than duplicating
      it in Salesforce, so there is one answer to who is in the audience.
  - id: s2
    title: Add members without doubling
    summary: >-
      Each member is added to the named campaign with a member status. Adding is idempotent, so anyone
      already in it is left alone. Removal is deliberately not part of this: campaign membership records
      who was contacted, and deleting it destroys the attribution.
    builds: workflow
    description: >-
      Create a workflow that adds each member to the named Salesforce campaign with a campaign member
      status. Adding is idempotent (a member already in the campaign is left alone rather than duplicated)
      and removal is deliberately not part of this recipe, because campaign membership is a record of
      who was contacted and deleting it destroys attribution. Use the result of "Define the audience once".
    dependsOn:
      - s1
outputs:
  - key: audience
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Segment into a Salesforce campaign

Puts a segment's members into a Salesforce campaign, which is how an audience built here becomes something a sales team can run against.

## Steps

1. **Define the audience once** (builds segment)

   The segment whose members belong in the campaign, defined here rather than rebuilt in Salesforce, so there is one answer to who is in it.

2. **Add members without doubling** (builds workflow)

   Each member is added to the named campaign with a member status. Adding is idempotent, so anyone already in it is left alone. Removal is deliberately not part of this: campaign membership records who was contacted, and deleting it destroys the attribution.

## What you end up with

- **audience** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## What this recipe touches

Reads:

- Your Salesforce connection

Writes:

- A new segment, from step 1 "Define the audience once"
- A new workflow, from step 2 "Add members without doubling"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
