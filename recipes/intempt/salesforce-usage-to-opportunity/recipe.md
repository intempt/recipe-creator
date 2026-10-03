---
id: salesforce-usage-to-opportunity
title: Usage onto the Salesforce opportunity
slash_command: /salesforce-usage-to-opportunity
group: Workflows
owner: intempt
summary: Keeps the usage fields on an open opportunity current, so the forecast reflects what the account
  is doing rather than what was said on a call.
description: >-
  Update an open Salesforce opportunity when product usage changes, so the forecast reflects what the
  account is actually doing rather than what it said in a call.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
  complexity: advanced
  executionMode: live
  tags:
    - salesforce
    - opportunity
    - forecast
prerequisites:
  events:
    - value: feature_used
      severity: recommended
  integrations:
    - value: salesforce
      severity: blocking
touches:
  reads:
    - The feature_used event in your project
    - Your Salesforce connection
  writes:
    - A new attribute, from step 1 "Describe usage for the forecast"
    - A new workflow, from step 2 "Update the open opportunity"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Describe usage for the forecast
    summary: >-
      Active seats, the share of them active weekly, how deeply features are adopted, and the trend over
      the last month. These are the things a rep would otherwise assert from memory.
    builds: attribute
    description: >-
      Create account attributes describing engagement in the terms the forecast cares about: active seats,
      weekly active proportion, depth of feature adoption, trend over the last month. These are what a
      rep would otherwise assert from memory.
  - id: s2
    title: Update the open opportunity
    summary: >-
      It finds the open opportunity for the account and writes the usage fields onto it. Only the fields
      Intempt owns are written, never the stage, the amount or the close date, which belong to the rep.
      A CDP that quietly moves a stage is a forecasting incident dressed up as an integration.
    builds: workflow
    description: >-
      Create a workflow that finds the open opportunity for the account and updates the usage fields on
      it. Only fields Intempt owns are written: never stage, never amount, never close date, which belong
      to the rep. A CDP that silently moves a stage is a forecasting incident that presents as an integration.
      Use the result of "Describe usage for the forecast".
    dependsOn:
      - s1
outputs:
  - key: usage_attrs
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Usage onto the Salesforce opportunity

Keeps the usage fields on an open opportunity current, so the forecast reflects what the account is doing rather than what was said on a call.

## Steps

1. **Describe usage for the forecast** (builds attribute)

   Active seats, the share of them active weekly, how deeply features are adopted, and the trend over the last month. These are the things a rep would otherwise assert from memory.

2. **Update the open opportunity** (builds workflow)

   It finds the open opportunity for the account and writes the usage fields onto it. Only the fields Intempt owns are written, never the stage, the amount or the close date, which belong to the rep. A CDP that quietly moves a stage is a forecasting incident dressed up as an integration.

## What you end up with

- **usage_attrs** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## What this recipe touches

Reads:

- The feature_used event in your project
- Your Salesforce connection

Writes:

- A new attribute, from step 1 "Describe usage for the forecast"
- A new workflow, from step 2 "Update the open opportunity"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
