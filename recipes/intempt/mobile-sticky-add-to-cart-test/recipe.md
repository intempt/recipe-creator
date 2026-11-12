---
frontmatter_id: mobile-sticky-add-to-cart-test
slash_command: /mobile-sticky-add-to-cart-test
description: Compares a standard add-to-cart button against two sticky bottom bars on mobile product pages, scored on carts created.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests a standard add-to-cart button against two sticky bottom bars on mobile product pages, measuring which variant
    drives the most carts created.
  parameters:
  - name: test_duration
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: control_traffic_share
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variant_b_traffic_share
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic_share
    type: number
    label: Variant C traffic share (%)
    default: 33
    required: false
  - name: page_url_contains
    type: string
    label: Page URL contains
    default: /products/
    required: false
  - name: max_mobile_viewport_width
    type: number
    label: Mobile viewport max width (px, exclusive)
    default: 768
    required: false
  - name: order_window
    type: duration
    label: Post-exposure order window
    default: 24 h
    required: false
  - name: scroll_depth_max_drop
    type: number
    label: Maximum allowed PDP scroll depth drop (%)
    default: 10
    required: false
  requirements:
  - slot: add_to_cart_experiment_event
    kind: event
    meaning: A customer clicked an add-to-cart button on a product page
    properties:
    - name: target_id
      type: text
      meaning: Identifier of the clicked element (sticky or main add-to-cart button)
      optional: false
  - slot: cart_created_goal
    kind: event
    meaning: A customer created a cart within a session in which they were exposed to the experiment
    properties:
    - name: experience_id
      type: text
      meaning: Identifier of the experiment the customer was exposed to
      optional: false
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: experience_id
      type: text
      meaning: Identifier of the experiment the customer was exposed to, if any
      optional: true
  - slot: mobile_product_page_visitors
    kind: segment
    meaning: Mobile visitors viewing product pages
  steps:
  - id: s1
    builds: experiment
    uses:
    - add_to_cart_experiment_event
    - cart_created_goal
    - order_placed_event
    - mobile_product_page_visitors
    - test_duration
    - control_traffic_share
    - variant_b_traffic_share
    - variant_c_traffic_share
    - page_url_contains
    - max_mobile_viewport_width
    - order_window
    - scroll_depth_max_drop
    instruction: 'Create a client-side experiment titled "Mobile Sticky Add-to-Cart" on the experiences page. Targeting: pages
      whose URL contains {page_url_contains}; mobile devices only (viewport width below {max_mobile_viewport_width} px); audience
      is {mobile_product_page_visitors}; display frequency always. Variants: Control at {control_traffic_share}% traffic with
      the standard add-to-cart button that scrolls with page content and no DOM changes; Variant B at {variant_b_traffic_share}%
      traffic with a fixed bottom bar showing product title, price and an add-to-cart button (id sticky-add-to-cart-button);
      Variant C at {variant_c_traffic_share}% traffic with a fixed bottom bar showing product title, price, a quantity selector
      (decrease, numeric input defaulting to 1 with min 1 and max 99, increase) and an add-to-cart button (id sticky-add-to-cart-button).
      Both sticky bars are fixed to the bottom of the viewport across the full width with z-index 1000 and are hidden at viewport
      widths of {max_mobile_viewport_width} px or more. Primary metric: {cart_created_goal} filtered to this experiment''s
      id. Secondary metrics: clicks on {add_to_cart_experiment_event} where target_id is sticky-add-to-cart-button (Variants
      B and C); clicks where target_id is main-add-to-cart-button (Control and as fallback for B and C); {order_placed_event}
      within {order_window} of exposure; mobile time on product page. Guardrails: PDP scroll depth must not drop by more than
      {scroll_depth_max_drop}%; mobile checkout conversion rate must not decline. Run for {test_duration} on mobile traffic
      only.'
---

# Mobile sticky add to cart test

Slash command: /mobile-sticky-add-to-cart-test

## Step 1: Set up the sticky cart test

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
Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on Cart created within session of exposure)
Secondary metrics:
- Click on where target_id = "sticky-add-to-cart-button" (variant B and C only)
- Click on where target_id = "main-add-to-cart-button" (control + as fallback for B/C)
- Placed order within 24 hours of exposure (mobile checkout completion)
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
