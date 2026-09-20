---
name: product-page-layout-test
description: |
  Use when a user mentions "product page layout test", or asks for related help. Test which PDP layout drives the highest add-to-cart rate. Client experiment with three layouts.
arguments: []
intempt:
  id: product-page-layout-test
  version: 1.0.0
  slashCommand: /product-page-layout-test
  group: Experiments
  title: 'Product page layout test'
  shortDescription: 'Compares your current product page against a full-width hero with a floating details panel and a video-first layout.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [ecommerce]
    complexity: standard
    executionMode: live
    tags: [experiment, client]
    experimentType: a-b
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_experiment
  procedure:
    - step: 1
      title: 'Set up the layout test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits product page traffic three ways: the existing gallery-left and details-right layout, a full-width hero image with a floating details panel, and an autoplay product demo. The winner creates the most carts in the same session.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Product Page Layout".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (34%): existing PDP: image gallery on left, details on right
        - Variant B (33%): full-width hero image with floating details panel
        - Variant C (33%): video-first layout with autoplay product demo

        Targeting:
        - Pages: page URL contains "/products/"
        - Devices: any (note: variant B's floating panel needs explicit mobile design; variant C autoplay should respect prefers-reduced-motion)
        - Audience: all visitors
        - Display frequency: always

        Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on cart_created within session of exposure)
        Secondary metrics:
        - click_on where target_id = "add-to-cart-button"
        - order_created within 7 days of exposure
        - Time on PDP (time from page_viewed to next page_viewed or session_end)

        Guardrail: bounce rate on PDPs must not increase >5%

        Schedule: 14 days, 2,000 unique PDP visitors per variant minimum

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes)

        Variant: B (full-width hero + floating panel)
          HTML target selector: .product-detail (replace structure)
          Replacement HTML:
          <article class="pdp-hero-layout" data-variant="b">
            <div class="hero-image-wrapper">
              <img src="[primary product image]" alt="[product name]" class="hero-image" />
            </div>
            <aside class="floating-details-panel">
              <h1 class="product-title">[Product name]</h1>
              <div class="product-price">[$X.XX]</div>
              <div class="product-rating">★★★★☆ (123 reviews)</div>
              <div class="variant-selectors"><!-- size, color etc --></div>
              <button class="add-to-cart-btn" id="add-to-cart-button" data-variant="b">Add to Cart</button>
            </aside>
            <section class="product-description"><!-- collapsed below the fold --></section>
          </article>

        Variant: C (video-first)
          HTML target selector: .product-detail (replace structure)
          Replacement HTML:
          <article class="pdp-video-layout" data-variant="c">
            <div class="video-hero">
              <video autoplay muted loop playsinline poster="[product poster]">
                <source src="[product demo video]" type="video/mp4" />
              </video>
            </div>
            <div class="product-actions">
              <h1>[Product name]</h1>
              <div class="product-price">[$X.XX]</div>
              <button class="add-to-cart-btn" id="add-to-cart-button" data-variant="c">Add to Cart</button>
            </div>
            <section class="product-info"><!-- description, reviews --></section>
          </article>

        Taxonomy notes:
        - cart_created is the canonical add-to-cart event; it fires with product_id, quantity, total_amount.
        - "add-to-cart-button" target_id must be preserved across variants for click-rate comparability.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product page layout test

Compares your current product page against a full-width hero with a floating details panel and a video-first layout.

## What it does

1. **Set up the layout test** (`create_experiment`)

   Splits product page traffic three ways: the existing gallery-left and details-right layout, a full-width hero image with a floating details panel, and an autoplay product demo. The winner creates the most carts in the same session.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
