---
name: Back In Stock Push Alert
description: Push notification when a product the user showed interest in returns to stock — faster than email for restock
  moments where scarcity matters.
intempt:
  id: back-in-stock-push-alert
  version: 1.0.0
  slashCommand: /back-in-stock-push-alert
  shortDescription: Push notification when a product the user showed interest in returns to stock — faster than email for
    restock moments where scarcity matters.
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
    - back
    - push-and-mobile
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
    describe: 'Generate alert email and SMS content templates for: back-in-stock, price-drop, birthday gift, and wishlist-on-sale.
      (Tailored for: Back-in-stock push alert.)'
    produces: content
  - id: build-journey
    describe: 'Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday
      events. (Tailored for: Back-in-stock push alert.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type. (Tailored
      for: Back-in-stock push alert.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: firebase
      severity: blocking
    - value: shopify
      severity: blocking
---

# Back In Stock Push Alert

Push notification when a product the user showed interest in returns to stock — faster than email for restock moments where scarcity matters.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate alert email and SMS content templates for: back-in-stock, price-drop, birthday gift, and wishlist-on-sale. (Tailored for: Back-in-stock push alert.)
2. Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday events. (Tailored for: Back-in-stock push alert.)
3. Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type. (Tailored for: Back-in-stock push alert.)

## Prerequisites

- Integration: **firebase** (blocking)
- Integration: **shopify** (blocking)
