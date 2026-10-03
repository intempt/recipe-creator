---
id: mobile-sticky-add-to-cart-test
title: Mobile sticky add to cart test
slash_command: /mobile-sticky-add-to-cart-test
group: Experiments
owner: intempt
summary: Compares a standard add-to-cart button against two sticky bottom bars on mobile product pages,
  scored on carts created.
description: >-
  Test whether a sticky add-to-cart bar on mobile improves conversion. Client experiment, mobile-only.
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - ecommerce
  complexity: standard
  executionMode: live
  tags:
    - experiment
    - client
  experimentType: a-b
steps:
  - id: s1
    title: Set up the sticky cart test
    summary: >-
      Runs on mobile viewports only and splits product page traffic three ways: the normal button that
      scrolls away, a sticky bottom bar with price, and a sticky bar with a quantity selector. The winner
      creates the most carts in the same session.
    builds: experiment
    description: |-
      Create a CLIENT EXPERIMENT on /experiences titled "Mobile Sticky Add-to-Cart".
      ═══ PATH 1: Top-level configuration ═══
      Experience type: client_experiment
      Variants:
      - Control (34%): standard add-to-cart button (scrolls with page content)
      - Variant B (33%): sticky bottom bar with "Add to Cart" + price
      - Variant C (33%): sticky bar with quantity selector + "Add to Cart"
      Targeting:
      - Pages: page URL contains "/products/"
      - Devices: MOBILE ONLY (viewport width < 768px): this is a mobile-specific UX test
      - Audience: all visitors
      - Display frequency: always
      Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on cart_created within session of exposure)
      Secondary metrics:
      - click_on where target_id = "sticky-add-to-cart-button" (variant B and C only)
      - click_on where target_id = "main-add-to-cart-button" (control + as fallback for B/C)
      - order_created within 24 hours of exposure (mobile checkout completion)
      - Time-on-PDP (mobile dwell time)
      Guardrail: PDP scroll depth must not drop >10% (sticky bar shouldn't disincentivize content reading); checkout conversion rate must not drop on mobile
      Schedule: 14 days, mobile traffic only
      ═══ PATH 2: Variant HTML content (Visual Editor) ═══
      Variant: Control (no DOM changes)
       Existing PDP layout: main "Add to Cart" button scrolls with page.
      Variant: B (sticky bar with price)
       HTML target selector: body (append fixed-position element)
       Variant DOM:
       <div class="sticky-cart-bar" data-variant="b" data-mobile-only="true" style="position:fixed;bottom:0;left:0;right:0;padding:12px 16px;background:#fff;border-top:1px solid #eee;display:flex;align-items:center;justify-content:space-between;z-index:1000;">
       <div class="sticky-product-info">
       <span class="product-title-mini">[Product name]</span>
       <span class="product-price">[$X.XX]</span>
       </div>
       <button class="sticky-add-cart-btn" id="sticky-add-to-cart-button" data-variant="b">Add to Cart</button>
       </div>
       CSS guard: hide on viewport width >= 768px so it never shows on tablet/desktop.
      Variant: C (sticky bar with quantity selector)
       Same wrapper, with quantity selector added:
       <div class="sticky-cart-bar" data-variant="c" data-mobile-only="true" style="position:fixed;bottom:0;left:0;right:0;padding:12px 16px;background:#fff;border-top:1px solid #eee;display:flex;align-items:center;gap:12px;z-index:1000;">
       <div class="sticky-product-info">
       <span class="product-title-mini">[Product name]</span>
       <span class="product-price">[$X.XX]</span>
       </div>
       <div class="quantity-selector">
       <button class="qty-decrease" aria-label="Decrease">−</button>
       <input type="number" value="1" min="1" max="99" class="qty-input" />
       <button class="qty-increase" aria-label="Increase">+</button>
       </div>
       <button class="sticky-add-cart-btn" id="sticky-add-to-cart-button" data-variant="c">Add to Cart</button>
       </div>
      The Visual Editor allows the user to fine-tune the bar's color scheme, animation (slide-up reveal on scroll), and quantity-selector behavior.
      Taxonomy notes:
      - "Mobile only" is enforced via the experience-level device targeting (targetDevice = "mobile") which Lovable applies at the SDK level; the CSS guard is belt-and-braces.
      - target_id = "sticky-add-to-cart-button" is shared across variants B and C; control uses "main-add-to-cart-button". This lets you compare sticky-bar engagement vs. main-button engagement.
outputs:
  - key: experiment
    producedByStep: s1
    type: experiment
    description: Website experiment created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Mobile sticky add to cart test

Compares a standard add-to-cart button against two sticky bottom bars on mobile product pages, scored on carts created.

## Steps

1. **Set up the sticky cart test** (builds experiment)

   Runs on mobile viewports only and splits product page traffic three ways: the normal button that scrolls away, a sticky bottom bar with price, and a sticky bar with a quantity selector. The winner creates the most carts in the same session.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.

## Availability

Coming soon: waiting on the engine to build experiment.
