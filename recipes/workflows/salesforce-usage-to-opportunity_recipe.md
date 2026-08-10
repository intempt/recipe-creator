---
name: salesforce-usage-to-opportunity
description: Use when a user mentions "usage to opportunity", "update salesforce opportunity from product", "forecast from usage", or asks for related help. Update an open Salesforce opportunity when product usage changes, so the forecast reflects what the account is actually doing rather than what it said in a call.
arguments: []
intempt:
  id: salesforce-usage-to-opportunity
  version: 1.0.0
  slashCommand: /salesforce-usage-to-opportunity
  group: Workflows
  shortDescription: "Update an open Salesforce opportunity when product usage changes, so the forecast reflects what the account is actually doing rather than what it said in a call."
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
      title: Compute The Usage Signal
      command: create_attribute
      produces: attribute
      bindsAs: usage_attrs
      description: 'Create account attributes describing engagement in the terms the forecast cares about: active seats, weekly active proportion, depth of feature adoption, trend over the last month. These are what a rep would otherwise assert from memory.'
      prompt: 'Create account attributes describing engagement in the terms the forecast cares about: active seats, weekly active proportion, depth of feature adoption, trend over the last month. These are what a rep would otherwise assert from memory.'
    - step: 2
      title: Write It To The Opportunity
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - usage_attrs
      description: 'Create a workflow that finds the open opportunity for the account and updates the usage fields on it. Only fields Intempt owns are written — never stage, never amount, never close date, which belong to the rep. A CDP that silently moves a stage is a forecasting incident that presents as an integration.'
      prompt: 'Create a workflow that finds the open opportunity for the account and updates the usage fields on it. Only fields Intempt owns are written — never stage, never amount, never close date, which belong to the rep. A CDP that silently moves a stage is a forecasting incident that presents as an integration.'
---
