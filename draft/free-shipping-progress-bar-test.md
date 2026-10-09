---
description: Compares a cart bar counting down to free shipping against no bar at all, scored on revenue and average order value.
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

# Free shipping progress bar test

Slash command: /free-shipping-progress-bar-test

## Step 1: Set up the progress bar test

Create a CLIENT EXPERIMENT on /experiences titled "Free Shipping Progress Bar".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (50%): no progress bar (existing cart page)
- Variant B (50%): cart shows free-shipping progress bar with dynamic "$X away from free shipping" copy and progress meter
Targeting:
- Pages: page URL contains "/cart" OR mini-cart drawer is open on any page
- Devices: any
- Audience: visitors with at least one Cart created event in the current session AND cart subtotal > $0 AND cart subtotal < free_shipping_threshold
- Display frequency: always
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from Placed order within 24 hours of exposure)
Secondary metrics:
- AOV per variant (average Placed order.total_price (the key signal) does the progress bar lift AOV?)
- cart_updated count per session (does the bar drive add-more behavior?)
- Cart-to-order conversion rate (Cart created to Placed order within session)
- Percentage of orders that hit the free-shipping threshold
Guardrail: cart-abandonment rate must not increase >3% (some shoppers may walk away when they see they don't qualify)
Schedule: 14 days
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes)
Variant: B (progress bar)
 HTML target selector: .cart-summary (insert at the top, above the items list)
 Variant DOM:
 <div class="free-shipping-progress" data-variant="b">
 <div class="progress-message">
 <strong class="amount-remaining">$12</strong>
 <span class="message-text">away from <strong>free shipping</strong></span>
 </div>
 <div class="progress-bar-container" role="progressbar" aria-label="Free shipping progress">
 <div class="progress-bar-fill" style="width: 76%;"></div>
 </div>
 <div class="progress-cta">
 <a href="/shop" class="continue-shopping-link">Add more items</a>
 </div>
 </div>
 Lightweight JS that the user refines in the Visual Editor:
 - Subscribe to cart_updated events
 - Read cart subtotal and configured free_shipping_threshold
 - Update .amount-remaining and .progress-bar-fill width in real time
 - When subtotal >= threshold, swap to "🎉 You unlocked free shipping!" celebration state
When the cart subtotal crosses the threshold, fire a custom DOM event so analytics can capture the threshold-hit moment.
Taxonomy notes:
- This recipe assumes the merchant has a configured free shipping threshold. If you also run free-shipping-threshold-test (server experiment testing the dollar value), schedule them sequentially: don't run them concurrently to avoid interaction effects.
- "Cart subtotal" is read from cart state (Cart created, cart_updated events with Order total property).
- The progress bar's biggest signal is AOV lift; expect 8-15% AOV uplift for stores below the typical free-shipping threshold.
