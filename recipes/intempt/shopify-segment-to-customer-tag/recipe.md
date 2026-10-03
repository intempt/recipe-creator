---
id: shopify-segment-to-customer-tag
title: Tag Shopify customers from a segment
slash_command: /shopify-segment-to-customer-tag
group: Workflows
owner: intempt
summary: Pushes a cohort computed here onto Shopify customers as a tag, so the store can merchandise against
  it.
description: >-
  Tag Shopify customers from a segment computed here, so a cohort the CDP understands becomes something
  the store can merchandise against.
version: 2.0.0
classification:
  product:
    - marketing
  agent: revops-automator
  mode:
    - ecommerce
  complexity: standard
  executionMode: live
  tags:
    - shopify
    - tagging
    - audience-activation
prerequisites:
  integrations:
    - value: shopify
      severity: blocking
touches:
  reads:
    - Your Shopify connection
  writes:
    - A new segment, from step 1 "Define the cohort to tag"
    - A new workflow, from step 2 "Write the tag into Shopify"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Define the cohort to tag
    summary: >-
      High lifetime value, repeat buyer, lapsed, or whatever the store wants to treat differently. The
      segment is the definition and the tag is only its shadow in Shopify.
    builds: segment
    description: >-
      Create the segment to tag: high lifetime value, repeat buyer, lapsed, whatever the store wants to
      treat differently. The segment is the definition; the tag is only its shadow in Shopify.
  - id: s2
    title: Write the tag into Shopify
    summary: >-
      Each member is tagged in Shopify. Tags are additive, and the workflow names the one tag it manages,
      because a tag the store team also edits by hand gets fought over silently. Shopify's own rejection
      is shown as it came, since a tag limit and a permission error need different responses.
    builds: workflow
    description: >-
      Create a workflow that tags each member in Shopify. Tags are additive and the workflow states which
      tag it manages, because a tag the store team also edits by hand will otherwise be fought over silently.
      Shopify's own rejection is surfaced verbatim: a tag limit and a permission error need different
      responses. Use the result of "Define the cohort to tag".
    dependsOn:
      - s1
outputs:
  - key: cohort
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Tag Shopify customers from a segment

Pushes a cohort computed here onto Shopify customers as a tag, so the store can merchandise against it.

## Steps

1. **Define the cohort to tag** (builds segment)

   High lifetime value, repeat buyer, lapsed, or whatever the store wants to treat differently. The segment is the definition and the tag is only its shadow in Shopify.

2. **Write the tag into Shopify** (builds workflow)

   Each member is tagged in Shopify. Tags are additive, and the workflow names the one tag it manages, because a tag the store team also edits by hand gets fought over silently. Shopify's own rejection is shown as it came, since a tag limit and a permission error need different responses.

## What you end up with

- **cohort** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## What this recipe touches

Reads:

- Your Shopify connection

Writes:

- A new segment, from step 1 "Define the cohort to tag"
- A new workflow, from step 2 "Write the tag into Shopify"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
