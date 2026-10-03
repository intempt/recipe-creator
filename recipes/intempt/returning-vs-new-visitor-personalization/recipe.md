---
id: returning-vs-new-visitor-personalization
title: New versus returning visitor hero
slash_command: /returning-vs-new-visitor-personalization
group: Personalizations
owner: intempt
summary: First-time visitors get the value proposition. Returning visitors get picked up where they left
  off, with their abandoned cart if they have one.
description: >-
  Show new visitors a value proposition; show returning visitors continuation cues (recently viewed, abandoned
  cart). Client personalization based on prior session history.
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - ecommerce
    - saas
  complexity: standard
  executionMode: live
  tags:
    - personalization
    - client
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new website personalization, from step 1 "Set up the visitor-history heroes"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Set up the visitor-history heroes
    summary: >-
      First-time visitors see a value proposition with social proof, returning visitors with an abandoned
      cart see a resume-cart hero, and other returning visitors see a continue-browsing hero.
    builds: personalization
    description: |-
      Create a CLIENT PERSONALIZATION on /experiences titled "Returning vs New Visitor".
      ═══ PATH 1: Top-level configuration ═══
      Experience type: client_personalization
      Variants (each binds to a specific behavioral audience):
      - Control (audience = all: fallback): standard hero
      - Variant B (audience = "first-time visitors"): value-proposition + social proof hero
       - Audience definition: Users.first_seen_at is within the current session OR Users.first_seen_at is null
       - In other words: this is the user's first visit, or they were never identified before
      - Variant C (audience = "returning visitors with abandoned cart"): cart resumption hero
       - Audience definition: ALL of the following:
       1. Users.first_seen_at is older than the current session (returning visitor: has prior session history)
       2. At least one cart_created event in the last 7 days
       3. NO order_created event since that most-recent cart_created
       4. NO active session at the time of last cart_created (i.e., they left without checking out)
       - This composite definition expresses "returning visitor with an abandoned cart from a prior session"
      - Variant D (audience = "returning visitors without abandoned cart"): "continue browsing" hero
       - Audience definition: ALL of the following:
       1. Users.first_seen_at is older than the current session (returning visitor)
       2. NOT in the abandoned-cart audience (no cart_created in last 7 days OR an order_created has occurred since last cart_created)
      Targeting:
      - Pages: homepage "/" and product category pages "/category/*"
      - Devices: any
      - Display frequency: once_per_session
      Metrics:
      - click_on engagement per audience
      - order_created conversion per audience
      - For Variant C specifically: cart-resumption rate: visitors in the abandoned-cart audience who, after seeing this variant, complete order_created within session
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
       <!-- platform fills in items from the abandoned cart_created via the cart's items template -->
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
       <!-- platform fills in last 4 page_viewed PDPs from prior sessions via the user's recently viewed -->
       </section>
       </section>
      Taxonomy notes:
      - Users.first_seen_at is the canonical first-touch timestamp.
      - "Returning visitor" detection: Users.first_seen_at older than the current session_start timestamp.
      - "Abandoned cart" derivation in canonical events:
       cart_created in [now - 7 days, now]
       AND latest_cart_created.timestamp > MAX(order_created.timestamp WHERE customer_id = current_user)
       OR no order_created exists for this user
       This composite condition (last cart_created has no subsequent order_created from the same user) is the canonical abandoned-cart pattern. Most personalization engines support this as a built-in audience template; otherwise it must be evaluated at audience-definition time using event history.
      - Variant precedence (most specific wins): C beats D beats B beats Control. Configure the audience evaluation order so abandoned-cart users get Variant C, not Variant D.
      - The the cart's items and the user's recently viewed template tokens are filled at render time by the personalization engine reading from the user's event history.
outputs:
  - key: personalization
    producedByStep: s1
    type: personalization
    description: Website personalization created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# New versus returning visitor hero

First-time visitors get the value proposition. Returning visitors get picked up where they left off, with their abandoned cart if they have one.

## Steps

1. **Set up the visitor-history heroes** (builds personalization)

   First-time visitors see a value proposition with social proof, returning visitors with an abandoned cart see a resume-cart hero, and other returning visitors see a continue-browsing hero.

## What you end up with

- **personalization** (personalization): Website personalization created on /experiences.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new website personalization, from step 1 "Set up the visitor-history heroes"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build personalization.
