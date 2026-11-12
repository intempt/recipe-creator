---
frontmatter_id: salesforce-usage-to-opportunity
slash_command: /salesforce-usage-to-opportunity
description: Keeps the usage fields on an open opportunity current, so the forecast reflects what the account is doing rather than what was said on a call.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Keeps usage fields on an account's open opportunity current so the forecast reflects actual product usage instead
    of call notes, without touching stage, amount, or close date.
  parameters:
  - name: activeWindow
    type: duration
    label: Window for active seat and engagement measures
    default: 30 d
    required: false
  requirements:
  - slot: account_usage_event
    kind: event
    meaning: A customer used the product (a session or feature action)
    properties:
    - name: feature
      type: string
      meaning: Feature used
      optional: true
  - slot: open_opportunity
    kind: integration
    meaning: Salesforce account with open opportunities that usage fields can be written to
    channel: salesforce
  - slot: usage_active_seats
    kind: attribute
    meaning: Number of active seats for the account
  - slot: usage_weekly_active_proportion
    kind: attribute
    meaning: Share of licensed seats active in a given week
  - slot: usage_feature_adoption_depth
    kind: attribute
    meaning: Depth of feature adoption across the account
  - slot: usage_monthly_trend
    kind: attribute
    meaning: Direction of usage over the last month
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_usage_event
    - activeWindow
    instruction: 'Create account attributes describing engagement in the terms the forecast cares about: active seats, weekly
      active proportion, depth of feature adoption, and trend over the last {activeWindow}. These are the figures a rep would
      otherwise assert from memory.'
  - id: s2
    builds: automation
    uses:
    - open_opportunity
    - usage_active_seats
    - usage_weekly_active_proportion
    - usage_feature_adoption_depth
    - usage_monthly_trend
    - s1
    instruction: 'Create a workflow that finds the open opportunity for the account in {open_opportunity} and updates only
      the usage fields on it with the values from "Describe usage for the forecast". Write only fields owned by Intempt: never
      write stage, amount, or close date, which belong to the rep.'
---

# Usage onto the Salesforce opportunity

Slash command: /salesforce-usage-to-opportunity

## Step 1: Describe usage for the forecast

Create account attributes describing engagement in the terms the forecast cares about: active seats, weekly active proportion, depth of feature adoption, trend over the last month. These are what a rep would otherwise assert from memory.

## Step 2: Update the open opportunity

Create a workflow that finds the open opportunity for the account and updates the usage fields on it. Only fields Intempt owns are written: never stage, never amount, never close date, which belong to the rep. A CDP that silently moves a stage is a forecasting incident that presents as an integration. Use the result of "Describe usage for the forecast".
