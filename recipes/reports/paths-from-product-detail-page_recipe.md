---
name: paths-from-product-detail-page
description: |
  Use when a user mentions "paths from product detail page", or asks for related help. Forward path from PDP page_viewed surfacing whether users add to cart, browse similar, search again, or exit.
arguments: []
intempt:
  id: paths-from-product-detail-page
  version: 1.0.0
  slashCommand: /paths-from-product-detail-page
  group: Reports
  shortDescription: "Produce a forward Path report anchored on /products/ page_viewed showing top 5-step paths and the share ending in cart_created, broken down by device_type."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [path]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_paths_report
  procedure:
    - step: 1
      title: "Build Path Report"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
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
        - The most common immediate-next event after PDP — typically: cart_created, another page_viewed (similar product), search/category navigation, or session exit

        Annotations:
        - Flag if PDP-exit rate exceeds 50% (typical strong signal of weak product page conversion).
        - Flag if the most common next event after PDP is "page_viewed on category/listing" — users are comparison-shopping, suggesting the PDP lacks comparison features or social proof.
        - Flag if mobile PDP exit rate is >10 points worse than desktop (mobile UX issue specific to product pages).
        - Highlight top 3 emerging "PDP → cart" paths — these are the high-conversion product flows; learn their characteristics and apply them.

        Use case: PDP is the highest-leverage page in ecommerce, and most teams optimize it without seeing where users actually go after viewing. Per the Solar Engine path-analysis case study, a 20% add-to-cart rate lift came from this exact analysis (discovering users went back to category to comparison-shop, prompting addition of a comparison carousel).

        Taxonomy notes:
        - page_viewed.page_url is used to identify PDPs. cart_created and order_created are canonical conversion events. session_end is the canonical exit signal.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Paths from Product Detail Page

## Procedure

1. **Build Path Report** [`build_paths_report`] — Configure and materialize the report described below. → produces: report

   ```text
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
   - The most common immediate-next event after PDP — typically: cart_created, another page_viewed (similar product), search/category navigation, or session exit

   Annotations:
   - Flag if PDP-exit rate exceeds 50% (typical strong signal of weak product page conversion).
   - Flag if the most common next event after PDP is "page_viewed on category/listing" — users are comparison-shopping, suggesting the PDP lacks comparison features or social proof.
   - Flag if mobile PDP exit rate is >10 points worse than desktop (mobile UX issue specific to product pages).
   - Highlight top 3 emerging "PDP → cart" paths — these are the high-conversion product flows; learn their characteristics and apply them.

   Use case: PDP is the highest-leverage page in ecommerce, and most teams optimize it without seeing where users actually go after viewing. Per the Solar Engine path-analysis case study, a 20% add-to-cart rate lift came from this exact analysis (discovering users went back to category to comparison-shop, prompting addition of a comparison carousel).

   Taxonomy notes:
   - page_viewed.page_url is used to identify PDPs. cart_created and order_created are canonical conversion events. session_end is the canonical exit signal.
   ```
