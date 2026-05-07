---
name: Contract Renewal B2B Account
description: 120/90/60/30/14 day renewal cadence for B2B contracts. CSM-owned with usage recap, upsell opportunities, and
  legal lead-time. Critical for NRR.
intempt:
  id: contract-renewal-b2b-account
  version: 1.0.0
  slashCommand: /contract-renewal-b2b-account
  shortDescription: 120/90/60/30/14 day renewal cadence for B2B contracts. CSM-owned with usage recap, upsell opportunities,
    and legal lead-time. Critical for NRR.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - customer-success-and-renewal
    - contract
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: attribute
    type: attribute
    description: Attribute produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: compute-churn-risk
    describe: 'Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage
      signals. (Tailored for: Contract renewal — B2B account.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: Contract renewal — B2B account.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: Contract renewal — B2B account.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      Contract renewal — B2B account.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Contract
      renewal — B2B account.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: Contract renewal — B2B account.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# Contract Renewal B2B Account

120/90/60/30/14 day renewal cadence for B2B contracts. CSM-owned with usage recap, upsell opportunities, and legal lead-time. Critical for NRR.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: Contract renewal — B2B account.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: Contract renewal — B2B account.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: Contract renewal — B2B account.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: Contract renewal — B2B account.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Contract renewal — B2B account.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: Contract renewal — B2B account.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
