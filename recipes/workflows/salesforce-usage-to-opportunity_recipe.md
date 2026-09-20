---
name: salesforce-usage-to-opportunity
description: Use when a user mentions "usage to opportunity", "update salesforce opportunity from product", "forecast from usage", or asks for related help. Update an open Salesforce opportunity when product usage changes, so the forecast reflects what the account is actually doing rather than what it said in a call.
arguments: []
intempt:
  id: salesforce-usage-to-opportunity
  title: "Usage onto the Salesforce opportunity"
  version: 1.0.0
  slashCommand: /salesforce-usage-to-opportunity
  group: Workflows
  shortDescription: "Keeps the usage fields on an open opportunity current, so the forecast reflects what the account is doing rather than what was said on a call."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [salesforce, opportunity, forecast]
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
    - create_attribute
    - create_workflow
  procedure:
    - step: 1
      title: "Describe usage for the forecast"
      command: create_attribute
      produces: attribute
      bindsAs: usage_attrs
      description: "Active seats, the share of them active weekly, how deeply features are adopted, and the trend over the last month. These are the things a rep would otherwise assert from memory."
      prompt: 'Create account attributes describing engagement in the terms the forecast cares about: active seats, weekly active proportion, depth of feature adoption, trend over the last month. These are what a rep would otherwise assert from memory.'
    - step: 2
      title: "Update the open opportunity"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - usage_attrs
      description: "It finds the open opportunity for the account and writes the usage fields onto it. Only the fields Intempt owns are written, never the stage, the amount or the close date, which belong to the rep. A CDP that quietly moves a stage is a forecasting incident dressed up as an integration."
      prompt: 'Create a workflow that finds the open opportunity for the account and updates the usage fields on it. Only fields Intempt owns are written: never stage, never amount, never close date, which belong to the rep. A CDP that silently moves a stage is a forecasting incident that presents as an integration.'
  outputs:
    - { name: usage_attrs, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Usage onto the Salesforce opportunity

Keeps the usage fields on an open opportunity current, so the forecast reflects what the account is doing rather than what was said on a call.

## Before you run it

- Connect salesforce
- Send the `feature_used` event

## What it does

1. **Describe usage for the forecast** (`create_attribute`)

   Active seats, the share of them active weekly, how deeply features are adopted, and the trend over the last month. These are the things a rep would otherwise assert from memory.

2. **Update the open opportunity** (`create_workflow`)

   It finds the open opportunity for the account and writes the usage fields onto it. Only the fields Intempt owns are written, never the stage, the amount or the close date, which belong to the rep. A CDP that quietly moves a stage is a forecasting incident dressed up as an integration.

## What you end up with

- **usage_attrs** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
