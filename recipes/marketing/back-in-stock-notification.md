---
name: Back In Stock Notification
description: Fires when a product the user previously added to cart, wishlisted, or viewed returns to inventory — high-conversion
  trigger because intent is pre-qualified.
intempt:
  id: back-in-stock-notification
  version: 1.0.0
  slashCommand: /back-in-stock-notification
  shortDescription: Fires when a product the user previously added to cart, wishlisted, or viewed returns to inventory — high-conversion
    trigger because intent is pre-qualified.
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
    - back
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
      (Tailored for: Back-in-stock notification.)'
    produces: content
  - id: build-journey
    describe: 'Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday
      events. (Tailored for: Back-in-stock notification.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type. (Tailored
      for: Back-in-stock notification.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Back In Stock Notification

Fires when a product the user previously added to cart, wishlisted, or viewed returns to inventory — high-conversion trigger because intent is pre-qualified.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate alert email and SMS content templates for: back-in-stock, price-drop, birthday gift, and wishlist-on-sale. (Tailored for: Back-in-stock notification.)
2. Build event-triggered journeys firing on product_back_in_stock, product_price_decreased, and user_birthday events. (Tailored for: Back-in-stock notification.)
3. Compose a dashboard tracking alert send volume, click-through rate, and conversion rate by alert type. (Tailored for: Back-in-stock notification.)

## Prerequisites

- Integration: **shopify** (blocking)
