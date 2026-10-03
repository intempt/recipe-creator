---
id: paths-from-product-detail-page
title: Paths from a product page
slash_command: /paths-from-product-detail-page
group: Reports
owner: intempt
summary: 'Shows what shoppers do after landing on a product page: add to cart, keep browsing, search again,
  or leave.'
description: >-
  Forward path from PDP page_viewed surfacing whether users add to cart, browse similar, search again,
  or exit.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: quick
  executionMode: live
  tags:
    - path
steps:
  - id: s1
    title: See what follows a product view
    summary: >-
      The 5 steps after a product page view inside a 30 minute window over the last 30 days, split by
      device, with the share that adds to cart and the share that leaves without buying. Flags an exit
      rate over 50%.
    builds: report
    description: |-
      Create a Path report called "Paths from Product Detail Page".
      Anchor event: page_viewed where page_url contains "/products/" (PDP pattern)
      Direction: forward
      Depth: 5 steps
      Window: 30 minutes after the PDP view (in-session)
      Loop compression: on
      Time range: Last 30 days
      Breakdown: By "device_type" attribute on the Users object (desktop, mobile, tablet)
      Surface:
      - The top 10 most-common 5-step paths starting from a PDP view
      - The % of PDP views that result in a cart_created within the window (PDP-to-cart conversion)
      - The % of PDP views that result in a session_end without any cart_created OR order_created (PDP exit rate)
      - The most common immediate-next event after PDP: typically: cart_created, another page_viewed (similar product), search/category navigation, or session exit
      Annotations:
      - Flag if PDP-exit rate exceeds 50% (typical strong signal of weak product page conversion).
      - Flag if the most common next event after PDP is "page_viewed on category/listing": users are comparison-shopping, suggesting the PDP lacks comparison features or social proof.
      - Flag if mobile PDP exit rate is >10 points worse than desktop (mobile UX issue specific to product pages).
      - Highlight top 3 emerging "PDP to cart" paths: these are the high-conversion product flows; learn their characteristics and apply them.
      Use case: PDP is the highest-leverage page in ecommerce, and most teams optimize it without seeing where users actually go after viewing. Per the Solar Engine path-analysis case study, a 20% add-to-cart rate lift came from this exact analysis (discovering users went back to category to comparison-shop, prompting addition of a comparison carousel).
      Taxonomy notes:
      - page_viewed.page_url is used to identify PDPs. cart_created and order_created are canonical conversion events. session_end is the canonical exit signal.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Paths from a product page

Shows what shoppers do after landing on a product page: add to cart, keep browsing, search again, or leave.

## Steps

1. **See what follows a product view** (builds report)

   The 5 steps after a product page view inside a 30 minute window over the last 30 days, split by device, with the share that adds to cart and the share that leaves without buying. Flags an exit rate over 50%.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
