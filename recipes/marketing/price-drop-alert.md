---
name: Price Drop Alert
description: Fires when a product in the user's cart, wishlist, or recent browse history drops in price — reactivates price-sensitive
  interest.
intempt:
  id: price-drop-alert
  version: 1.0.0
  slashCommand: /price-drop-alert
  shortDescription: Fires when a product in the user's cart, wishlist, or recent browse history drops in price — reactivates
    price-sensitive interest.
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
    - cart-and-checkout-recovery
    - price
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
      (Tailored for: Price drop alert.)'
    produces: content
  - id: build-journey
    describe: 'Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday
      events. (Tailored for: Price drop alert.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type. (Tailored
      for: Price drop alert.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Price Drop Alert

Fires when a product in the user's cart, wishlist, or recent browse history drops in price — reactivates price-sensitive interest.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate alert email and SMS content templates for: back-in-stock, price-drop, birthday gift, and wishlist-on-sale. (Tailored for: Price drop alert.)
2. Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday events. (Tailored for: Price drop alert.)
3. Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type. (Tailored for: Price drop alert.)

## Prerequisites

- Integration: **shopify** (blocking)
