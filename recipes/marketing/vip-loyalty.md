---
name: Vip Loyalty
description: Identify VIPs, exclusive experiences, retention experiments, and program performance dashboards.
intempt:
  id: vip-loyalty
  version: 1.0.0
  slashCommand: /vip-loyalty
  shortDescription: Identify VIPs, exclusive experiences, retention experiments, and program performance dashboards.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: experience-optimizer
    mode:
    - ecommerce
    complexity: advanced
    executionMode: live
    tags:
    - vip-loyalty
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: attribute
    type: attribute
    description: Attribute produced by this recipe.
  - name: personalization
    type: personalization
    description: Personalization produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: compute-customer-value
    describe: Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency.
    produces: attribute
  - id: build-exclusive-personalization
    describe: 'Configure VIP-only personalizations: early access, exclusive products, free shipping.'
    produces: personalization
  - id: build-vip-journey
    describe: Build a VIP-specific journey with appreciation touches and tier-up encouragement.
    produces: journey
  - id: build-experiment
    describe: Add experiments comparing reward types (discount vs experience vs status).
    produces: experiment
  - id: build-dashboard
    describe: Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate.
    produces: dashboard
---

# Vip Loyalty

Identify VIPs, exclusive experiences, retention experiments, and program performance dashboards.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency.
2. Configure VIP-only personalizations: early access, exclusive products, free shipping.
3. Build a VIP-specific journey with appreciation touches and tier-up encouragement.
4. Add experiments comparing reward types (discount vs experience vs status).
5. Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate.
