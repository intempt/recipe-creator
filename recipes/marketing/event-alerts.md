---
name: Event Alerts
description: Back-in-stock, price-drop, and birthday alerts driven by user signals and product events.
intempt:
  id: event-alerts
  version: 1.0.0
  slashCommand: /event-alerts
  shortDescription: Back-in-stock, price-drop, and birthday alerts driven by user signals and product events.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - event-alerts
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-content
    describe: 'Generate alert email and SMS content templates for: back-in-stock, price-drop, birthday gift, and wishlist-on-sale.'
    produces: content
  - id: build-journey
    describe: Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday events.
    produces: journey
  - id: build-dashboard
    describe: Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type.
    produces: dashboard
---

# Event Alerts

Back-in-stock, price-drop, and birthday alerts driven by user signals and product events.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate alert email and SMS content templates for: back-in-stock, price-drop, birthday gift, and wishlist-on-sale.
2. Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday events.
3. Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type.
