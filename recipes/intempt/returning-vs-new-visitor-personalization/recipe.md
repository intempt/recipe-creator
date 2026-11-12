---
frontmatter_id: returning-vs-new-visitor-personalization
slash_command: /returning-vs-new-visitor-personalization
description: First-time visitors get the value proposition. Returning visitors get picked up where they left off, with their abandoned cart if they have one.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows first-time visitors a value-proposition hero, returning visitors with an abandoned cart a cart-resumption
    hero, and other returning visitors a continue-browsing hero.
  parameters:
  - name: cart_window
    type: duration
    label: Window for recent cart created events
    default: 7 d
    required: false
  - name: display_frequency
    type: enum
    label: How often the hero is shown per visitor
    default: once_per_session
    required: false
    options:
    - once_per_session
    - once_per_visit
    - always
  - name: target_pages
    type: text
    label: Pages where the hero appears
    default: / and /category/*
    required: false
  requirements:
  - slot: user_first_seen
    kind: attribute
    meaning: The timestamp when a user was first seen (first-touch timestamp)
    definition: Users.First seen
  - slot: cart_created_event
    kind: event
    meaning: A customer created a cart
    properties:
    - name: timestamp
      type: date
      meaning: When the cart was created
      optional: false
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: timestamp
      type: date
      meaning: When the order was placed
      optional: false
  - slot: abandoned_cart_audience
    kind: segment
    meaning: Returning visitors whose most recent cart in the last 7 days has no later placed order
    creatable: true
    definition: users whose First seen is older than the current session AND who did {cart_created_event} in the last {cart_window}
      AND whose latest {cart_created_event} is later than their latest {placed_order_event}
  - slot: homepage_hero_experiment
    kind: destination
    meaning: A client-side personalization surface on the website homepage and category pages where hero variants can be served
    channel: email
  steps:
  - id: s1
    builds: experiment
    uses:
    - user_first_seen
    - cart_created_event
    - placed_order_event
    - abandoned_cart_audience
    - homepage_hero_experiment
    - cart_window
    - display_frequency
    - target_pages
    instruction: 'Create a client-side personalization experiment titled "Returning vs New Visitor" on the homepage hero surface
      {homepage_hero_experiment}. Targeting: pages {target_pages}, all devices, display frequency {display_frequency}. Schedule:
      continuous. Evaluate audiences in this precedence order, most specific first: abandoned-cart returning visitors, then
      other returning visitors, then first-time visitors, then fallback control.


      Variants:

      - Control (fallback, audience = all): no DOM changes; standard hero.

      - Variant B (audience = first-time visitors): the user''s {user_first_seen} is within the current session or is empty.
      Target selector .homepage-hero. Replace the hero with a section of class homepage-hero containing an h1 ''The [category]
      designed for [target audience]'', a paragraph ''Loved by 50,000+ customers worldwide.'', a social-proof row with a 4.8
      star rating (2,400 reviews), ''Free shipping over $50'', and ''30-day returns'', and a primary button with id hero-cta-explore
      labelled ''Shop bestsellers''.

      - Variant C (audience = returning visitors with abandoned cart): all of the following hold: {user_first_seen} is older
      than the current session; the user is in {abandoned_cart_audience}, meaning at least one {cart_created_event} in the
      last {cart_window}, no {placed_order_event} after the most recent {cart_created_event}, and no active session at the
      time of that last cart creation. Target selector .homepage-hero. Replace the hero with a section of class homepage-hero
      containing an h1 ''Welcome back: your cart''s still here'', a paragraph ''Items in your cart from your last visit.'',
      an abandoned-cart preview block filled with the items from the abandoned cart, and a primary button with id hero-cta-resume
      labelled ''Resume checkout''.

      - Variant D (audience = returning visitors without abandoned cart): {user_first_seen} is older than the current session
      and the user is NOT in {abandoned_cart_audience}. Target selector .homepage-hero. Replace the hero with a section of
      class homepage-hero containing an h1 ''Welcome back, the user''s first name'', a paragraph ''Pick up where you left
      off.'', and a recently viewed section titled ''Recently viewed'' filled with the last four product pages viewed in prior
      sessions.


      Metrics to record per audience: click engagement and placed order conversion. For Variant C also record cart-resumption
      rate: the share of visitors in the abandoned-cart audience who complete a placed order within the session after seeing
      this variant.'
---

# New versus returning visitor hero

Slash command: /returning-vs-new-visitor-personalization

## Step 1: Set up the visitor-history heroes

Create a CLIENT PERSONALIZATION on /experiences titled "Returning vs New Visitor".
═══ PATH 1: Top-level configuration ═══
Experience type: client_personalization
Variants (each binds to a specific behavioral audience):
- Control (audience = all: fallback): standard hero
- Variant B (audience = "first-time visitors"): value-proposition + social proof hero
 - Audience definition: Users.First seen is within the current session OR Users.First seen is null
 - In other words: this is the user's first visit, or they were never identified before
- Variant C (audience = "returning visitors with abandoned cart"): cart resumption hero
 - Audience definition: ALL of the following:
 1. Users.First seen is older than the current session (returning visitor: has prior session history)
 2. At least one Cart created event in the last 7 days
 3. NO Placed order event since that most-recent Cart created
 4. NO active session at the time of last Cart created (i.e., they left without checking out)
 - This composite definition expresses "returning visitor with an abandoned cart from a prior session"
- Variant D (audience = "returning visitors without abandoned cart"): "continue browsing" hero
 - Audience definition: ALL of the following:
 1. Users.First seen is older than the current session (returning visitor)
 2. NOT in the abandoned-cart audience (no Cart created in last 7 days OR an Placed order has occurred since last Cart created)
Targeting:
- Pages: homepage "/" and product category pages "/category/*"
- Devices: any
- Display frequency: once_per_session
Metrics:
- Click on engagement per audience
- Placed order conversion per audience
- For Variant C specifically: cart-resumption rate: visitors in the abandoned-cart audience who, after seeing this variant, complete Placed order within session
Schedule: continuous
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes: fallback)
Variant: B (first-time visitors)
 HTML target selector: .homepage-hero
 Variant DOM:
 <section class="homepage-hero" data-variant="b" data-audience="first-time">
 <h1>The [category] designed for [target audience]</h1>
 <p>Loved by 50,000+ customers worldwide.</p>
 <div class="social-proof-row">
 <div class="proof-item"><span class="rating">★★★★★</span><span>4.8 (2,400 reviews)</span></div>
 <div class="proof-item">Free shipping over $50</div>
 <div class="proof-item">30-day returns</div>
 </div>
 <button class="cta-primary" id="hero-cta-explore">Shop bestsellers</button>
 </section>
Variant: C (returning with abandoned cart)
 HTML target selector: .homepage-hero
 Variant DOM:
 <section class="homepage-hero" data-variant="c" data-audience="cart-resumer">
 <h1>Welcome back: your cart's still here</h1>
 <p>Items in your cart from your last visit.</p>
 <div class="abandoned-cart-preview">
 <!-- platform fills in items from the abandoned Cart created via the cart's items template -->
 <button class="cta-primary" id="hero-cta-resume">Resume checkout</button>
 </div>
 </section>
Variant: D (returning without abandoned cart)
 HTML target selector: .homepage-hero
 Variant DOM:
 <section class="homepage-hero" data-variant="d" data-audience="returning">
 <h1>Welcome back, the user's first name</h1>
 <p>Pick up where you left off.</p>
 <section class="recently-viewed" data-source="user-session-history">
 <h2>Recently viewed</h2>
 <!-- platform fills in last 4 View page PDPs from prior sessions via the user's recently viewed -->
 </section>
 </section>
Taxonomy notes:
- Users.First seen is the canonical first-touch timestamp.
- "Returning visitor" detection: Users.First seen older than the current Session start timestamp.
- "Abandoned cart" derivation in canonical events:
 Cart created in [now - 7 days, now]
 AND latest_cart_created.timestamp > MAX(Placed order.timestamp WHERE customer_id = current_user)
 OR no Placed order exists for this user
 This composite condition (last Cart created has no subsequent Placed order from the same user) is the canonical abandoned-cart pattern. Most personalization engines support this as a built-in audience template; otherwise it must be evaluated at audience-definition time using event history.
- Variant precedence (most specific wins): C beats D beats B beats Control. Configure the audience evaluation order so abandoned-cart users get Variant C, not Variant D.
- The the cart's items and the user's recently viewed template tokens are filled at render time by the personalization engine reading from the user's event history.
