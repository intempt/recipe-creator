---
frontmatter_id: product-page-layout-test
slash_command: /product-page-layout-test
description: Compares your current product page against a full-width hero with a floating details panel and a video-first layout.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Runs a three-way product page layout test (current page, full-width hero with floating details panel, video-first
    layout) and measures add-to-cart, orders, and time on page.
  parameters:
  - name: experimentTitle
    type: string
    label: Experiment title
    default: Product Page Layout
    required: false
  - name: targetingUrlContains
    type: string
    label: Page URL contains
    default: /products/
    required: false
  - name: controlTrafficPercent
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variantBTrafficPercent
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: variantCTrafficPercent
    type: number
    label: Variant C traffic share (%)
    default: 33
    required: false
  - name: testDuration
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: minUniqueVisitorsPerVariant
    type: number
    label: Minimum unique PDP visitors per variant
    default: 2000
    required: false
  - name: orderWindow
    type: duration
    label: Order attribution window after exposure
    default: 7 d
    required: false
  - name: bounceRateIncreaseLimit
    type: number
    label: Maximum allowed bounce rate increase (%)
    default: 5
    required: false
  requirements:
  - slot: product_page_views
    kind: event
    meaning: A customer viewed a product page
  - slot: cart_created
    kind: event
    meaning: A customer added a product to a new cart
    properties:
    - name: product_id
      type: string
      meaning: Identifier of the product added
      optional: false
    - name: quantity
      type: number
      meaning: Number of units added
      optional: false
    - name: order_total
      type: number
      meaning: Order total value after adding the product
      optional: false
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
  - slot: add_to_cart_click
    kind: event
    meaning: A visitor clicked a button with target id add-to-cart-button
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element
      optional: false
  steps:
  - id: s1
    builds: experiment
    uses:
    - experimentTitle
    - targetingUrlContains
    - controlTrafficPercent
    - variantBTrafficPercent
    - variantCTrafficPercent
    - product_page_views
    - cart_created
    - add_to_cart_click
    instruction: 'Create a client-side experiment on /experiences titled "{experimentTitle}". Target visitors on pages whose
      URL contains "{targetingUrlContains}", all devices, all visitors, display frequency always. Variants: Control ({controlTrafficPercent}%)
      keeps the existing product page with image gallery on the left and details on the right, with no DOM changes. Variant
      B ({variantBTrafficPercent}%) replaces the .product-detail structure with a full-width hero image and a floating details
      panel. Variant C ({variantCTrafficPercent}%) replaces .product-detail with a video-first layout featuring an autoplay
      muted looping product demo video above the product name, price and add-to-cart button, with description and reviews
      below. Variant B''s floating panel needs an explicit mobile design. Variant C''s autoplay must respect prefers-reduced-motion.
      Keep the element id add-to-cart-button identical across all variants so click rates are comparable. Use product_id,
      quantity and order_total from the cart-created event for the add-to-cart measurement.'
---

# Product page layout test

Slash command: /product-page-layout-test

## Step 1: Set up the layout test

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
Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on Cart created within session of exposure)
Secondary metrics:
- Click on where target_id = "add-to-cart-button"
- Placed order within 7 days of exposure
- Time on PDP (time from View page to next View page or Session end)
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
- Cart created is the canonical add-to-cart event; it fires with product_id, quantity, Order total.
- "add-to-cart-button" target_id must be preserved across variants for click-rate comparability.
