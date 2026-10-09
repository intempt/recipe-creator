---
name: paths-from-product-detail-page
description: |
  Use when a user mentions "paths from product detail page", or asks for related help. Forward path from a product page view surfacing whether users add to cart, browse similar, search again, or exit.
arguments: []
intempt:
  id: paths-from-product-detail-page
  version: 1.0.0
  slashCommand: /paths-from-product-detail-page
  group: Reports
  title: "Paths from a product page"
  shortDescription: "Shows what shoppers do after landing on a product page: add to cart, keep browsing, search again, or leave."
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
      title: "See what follows a product view"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "The 5 steps after a product page view inside a 30 minute window over the last 30 days, split by device, with the share that adds to cart and the share that leaves without buying. Flags an exit rate over 50%."
      prompt: |
        Create a Path report called "Paths from Product Detail Page".

        Anchor event: View page where the page URL contains "/products/" (PDP pattern)
        Direction: forward
        Depth: 5 steps
        Window: 30 minutes after the PDP view (in-session)
        Loop compression: on
        Time range: Last 30 days
        Breakdown: By the Device type attribute on the Users object (desktop, mobile, tablet)

        Surface:
        - The top 10 most-common 5-step paths starting from a PDP view
        - The % of PDP views that result in a Cart created within the window (PDP-to-cart conversion)
        - The % of PDP views that result in a Session end without any Cart created OR Placed order (PDP exit rate)
        - The most common immediate-next event after PDP: typically: Cart created, another View page (similar product), search/category navigation, or session exit

        Annotations:
        - Flag if PDP-exit rate exceeds 50% (typical strong signal of weak product page conversion).
        - Flag if the most common next event after PDP is "View page on category/listing": users are comparison-shopping, suggesting the PDP lacks comparison features or social proof.
        - Flag if mobile PDP exit rate is >10 points worse than desktop (mobile UX issue specific to product pages).
        - Highlight top 3 emerging "PDP to cart" paths: these are the high-conversion product flows; learn their characteristics and apply them.

        Use case: PDP is the highest-leverage page in ecommerce, and most teams optimize it without seeing where users actually go after viewing. Per the Solar Engine path-analysis case study, a 20% add-to-cart rate lift came from this exact analysis (discovering users went back to category to comparison-shop, prompting addition of a comparison carousel).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Paths from a product page

Shows what shoppers do after landing on a product page: add to cart, keep browsing, search again, or leave.

## What it does

1. **See what follows a product view** (`build_paths_report`)

   The 5 steps after a product page view inside a 30 minute window over the last 30 days, split by device, with the share that adds to cart and the share that leaves without buying. Flags an exit rate over 50%.

## What you end up with

- **report** (report): Report produced by this recipe.
