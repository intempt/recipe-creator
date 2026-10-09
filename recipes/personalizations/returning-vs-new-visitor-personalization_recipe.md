---
name: returning-vs-new-visitor-personalization
description: |
  Use when a user mentions "returning vs new visitor personalization", or asks for related help. Show new visitors a value proposition; show returning visitors continuation cues (recently viewed, abandoned cart). Client personalization based on prior session history.
arguments: []
intempt:
  id: returning-vs-new-visitor-personalization
  version: 1.0.1
  slashCommand: /returning-vs-new-visitor-personalization
  group: Personalizations
  title: "New versus returning visitor hero"
  shortDescription: "First-time visitors get the value proposition. Returning visitors get picked up where they left off, with their abandoned cart if they have one."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [ecommerce, saas]
    complexity: standard
    executionMode: live
    tags: [personalization, client]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_personalization
  procedure:
    - step: 1
      title: "Set up the visitor-history heroes"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      description: "First-time visitors see a value proposition with social proof, returning visitors with an abandoned cart see a resume-cart hero, and other returning visitors see a continue-browsing hero."
      prompt: |
        Create a CLIENT PERSONALIZATION on /experiences titled "Returning vs New Visitor".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_personalization

        Variants (each binds to a specific behavioral audience):
        - Control (audience = all: fallback): standard hero
        - Variant B (audience = "first-time visitors"): value-proposition + social proof hero
          - Audience definition: first seen within the current session OR never seen before
          - In other words: this is the user's first visit, or they were never identified before
        - Variant C (audience = "returning visitors with abandoned cart"): cart resumption hero
          - Audience definition: ALL of the following:
            1. First seen before the current session (returning visitor: has prior session history)
            2. At least one Cart created event in the last 7 days
            3. NO Placed order event since that most-recent Cart created
            4. NO active session at the time of last Cart created (i.e., they left without checking out)
          - This composite definition expresses "returning visitor with an abandoned cart from a prior session"
        - Variant D (audience = "returning visitors without abandoned cart"): "continue browsing" hero
          - Audience definition: ALL of the following:
            1. First seen before the current session (returning visitor)
            2. NOT in the abandoned-cart audience (no Cart created in last 7 days OR a Placed order has occurred since last Cart created)

        Targeting:
        - Pages: homepage "/" and product category pages "/category/*"
        - Devices: any
        - Display frequency: once_per_session

        Metrics:
        - Click on engagement per audience
        - Placed order conversion per audience
        - For Variant C specifically: cart-resumption rate: visitors in the abandoned-cart audience who, after seeing this variant, complete a Placed order within session

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
              <!-- platform fills in items from the abandoned cart via {{cart.items}} template -->
              <button class="cta-primary" id="hero-cta-resume">Resume checkout</button>
            </div>
          </section>

        Variant: D (returning without abandoned cart)
          HTML target selector: .homepage-hero
          Variant DOM:
          <section class="homepage-hero" data-variant="d" data-audience="returning">
            <h1>Welcome back, {{user.first_name}}</h1>
            <p>Pick up where you left off.</p>
            <section class="recently-viewed" data-source="user-session-history">
              <h2>Recently viewed</h2>
              <!-- platform fills in last 4 viewed product pages from prior sessions via {{user.recently_viewed}} -->
            </section>
          </section>

        Notes:
        - First seen is the first-touch timestamp.
        - "Returning visitor" means first seen before the current session's start.
        - "Abandoned cart" logic:
            a Cart created in [now - 7 days, now]
            AND the latest Cart created is more recent than the user's last Placed order
            OR the user has no Placed order at all
          This composite condition (the last Cart created has no later Placed order from the same user) is the abandoned-cart pattern. Most personalization engines support this as a built-in audience template; otherwise it must be evaluated at audience-definition time using event history.
        - Variant precedence (most specific wins): C beats D beats B beats Control. Configure the audience evaluation order so abandoned-cart users get Variant C, not Variant D.
        - The {{cart.items}} and {{user.recently_viewed}} template tokens are filled at render time by the personalization engine reading from the user's event history.
  outputs:
    - { name: personalization, type: personalization, cardinality: single, description: "Website personalization created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# New versus returning visitor hero

First-time visitors get the value proposition. Returning visitors get picked up where they left off, with their abandoned cart if they have one.

## What it does

1. **Set up the visitor-history heroes** (`create_personalization`)

   First-time visitors see a value proposition with social proof, returning visitors with an abandoned cart see a resume-cart hero, and other returning visitors see a continue-browsing hero.

## What you end up with

- **personalization** (personalization): Website personalization created on /experiences.
