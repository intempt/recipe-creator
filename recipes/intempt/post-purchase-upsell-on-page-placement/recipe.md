---
description: Compares three places to put the upsell on the order confirmation page, scored on extra revenue within 24 hours.
author:
  first_name: V
  last_name: Ranadheer
  job_title: Design Engineer
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce
  - finance
---

# Post-purchase upsell placement test

Slash command: /post-purchase-upsell-on-page-placement

## Step 1: Set up the upsell placement test

Create a CLIENT EXPERIMENT on /experiences titled "Post-Purchase Upsell: On-Page Placement".
NOTE: This recipe was previously authored with email and push notification variants. The current product scope is website-only personalizations and experiments: email and push are outside the product. The recipe now focuses exclusively on the on-page placement dimension.
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (34%): upsell carousel above order details on the confirmation page
- Variant B (33%): upsell strip below order details on the confirmation page
- Variant C (33%): inline modal that appears 5 seconds after order confirmation page loads
Targeting:
- Pages: page URL contains "/order-confirmation" OR "/thank-you"
- Devices: any
- Audience: customers who just completed an order_created event
- Display frequency: once (per order)
Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on additional order_created within 24 hours of upsell exposure: incremental revenue)
Secondary metrics:
- click_on where target_id starts with "upsell-product-" (upsell engagement rate)
- Add-to-second-order rate (cart_created within 1 hour for any user shown the upsell)
- Average upsell value when accepted
Guardrail: customer satisfaction (feedback_submitted score within 7 days of order) must not drop; modal-dismiss rate (variant C) must not exceed 80% (high dismissal = annoyance signal)
Schedule: 30 days
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (above order details)
 HTML target selector: .order-confirmation (insert before)
 Variant DOM:
 <section class="post-purchase-upsell" data-variant="control" data-placement="above-order">
 <h2>Customers like you also bought</h2>
 <div class="upsell-carousel">
 <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-1">Add to Order</button></article>
 <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-2">Add to Order</button></article>
 <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-3">Add to Order</button></article>
 </div>
 </section>
Variant: B (below order details)
 HTML target selector: .order-confirmation (append after)
 Same upsell carousel HTML as Control.
Variant: C (inline modal, 5s delay)
 HTML target selector: body (append modal)
 Variant DOM:
 <div class="upsell-modal-overlay" data-variant="c" data-trigger="5s-delay" hidden>
 <div class="upsell-modal">
 <button class="modal-close" id="upsell-modal-dismiss" aria-label="Close">×</button>
 <h2>One more thing: customers also love these</h2>
 <div class="upsell-carousel">
 <!-- 3 upsell products with id="upsell-product-1/2/3" -->
 </div>
 </div>
 </div>
 Trigger JS: setTimeout 5000ms after page_viewed on /order-confirmation, set overlay hidden=false. Pair with a CSS modal animation.
Taxonomy notes:
- Email and push variants from the original template are explicitly removed because the product scope is website-only.
- The "incremental revenue" measurement requires the upsell-attributed order_created to be distinguished from the original purchase: typically done by session tracking joining click_on (target_id starts with "upsell-") to a subsequent order_created within the attribution window.
