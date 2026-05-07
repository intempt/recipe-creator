---
name: Vip Customer Appreciation Program
description: Ongoing VIP recognition for top-LTV customers — quarterly check-ins, early-access perks, and exclusive offers.
  Builds whale retention without a formal loyalty platform.
intempt:
  id: vip-customer-appreciation-program
  version: 1.0.0
  slashCommand: /vip-customer-appreciation-program
  shortDescription: Ongoing VIP recognition for top-LTV customers — quarterly check-ins, early-access perks, and exclusive
    offers. Builds whale retention without a formal loyalty platform.
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
    - vip-and-loyalty
    - vip
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
    describe: 'Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency. (Tailored for: VIP customer
      appreciation program.)'
    produces: attribute
  - id: build-exclusive-personalization
    describe: 'Configure VIP-only personalizations: early access, exclusive products, free shipping. (Tailored for: VIP customer
      appreciation program.)'
    produces: personalization
  - id: build-vip-journey
    describe: 'Build a VIP-specific journey with appreciation touches and tier-up encouragement. (Tailored for: VIP customer
      appreciation program.)'
    produces: journey
  - id: build-experiment
    describe: 'Add experiments comparing reward types (discount vs experience vs status). (Tailored for: VIP customer appreciation
      program.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate. (Tailored for:
      VIP customer appreciation program.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Vip Customer Appreciation Program

Ongoing VIP recognition for top-LTV customers — quarterly check-ins, early-access perks, and exclusive offers. Builds whale retention without a formal loyalty platform.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived customer_value_tier attribute using LTV, frequency, and recency. (Tailored for: VIP customer appreciation program.)
2. Configure VIP-only personalizations: early access, exclusive products, free shipping. (Tailored for: VIP customer appreciation program.)
3. Build a VIP-specific journey with appreciation touches and tier-up encouragement. (Tailored for: VIP customer appreciation program.)
4. Add experiments comparing reward types (discount vs experience vs status). (Tailored for: VIP customer appreciation program.)
5. Compose a dashboard tracking VIP retention rate, average revenue per tier, and tier-up rate. (Tailored for: VIP customer appreciation program.)

## Prerequisites

- Integration: **shopify** (blocking)
