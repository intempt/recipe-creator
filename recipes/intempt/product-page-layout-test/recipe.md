---
description: Compares your current product page against a full-width hero with a floating details panel and a video-first layout.
author:
  first_name: V
  last_name: Ranadheer
  job_title: Design Engineer
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
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
