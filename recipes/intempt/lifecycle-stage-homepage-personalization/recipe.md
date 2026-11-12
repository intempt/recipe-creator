---
frontmatter_id: lifecycle-stage-homepage-personalization
slash_command: /lifecycle-stage-homepage-personalization
description: Loyal shoppers get a welcome back, lapsed ones get a win-back offer, and new shoppers get an introduction, based on the lifecycle stage already on their profile.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: 'Shows each shopper a homepage hero matched to their lifecycle stage: a welcome back for loyal shoppers, a win-back
    offer for lapsed ones, and an introduction for new ones.'
  parameters:
  - name: homepage_path
    type: string
    label: Homepage URL path
    default: /
    required: false
  - name: winback_discount_percent
    type: number
    label: Win-back discount (%)
    default: 15
    required: false
  - name: display_frequency
    type: enum
    label: Display frequency
    default: once_per_session
    required: false
    options:
    - once_per_session
    - always
  - name: fallback_first_name
    type: string
    label: Greeting when first name is missing
    default: Welcome back
    required: false
  requirements:
  - slot: lifecycle_stage_attribute
    kind: attribute
    meaning: The user's lifecycle stage score with values At risk, Needs attention, New customers, Promising, Regulars, Champions
  - slot: first_name_attribute
    kind: attribute
    meaning: The user's first name, used to greet them on the homepage
    optional: true
  - slot: homepage_hero_container
    kind: destination
    meaning: The homepage hero section (.homepage-hero) on the website where personalized content is rendered
    channel: email
  - slot: recommendation_service
    kind: integration
    meaning: A recommendation service that supplies purchase-history, reorder-favorites and popularity-based product recommendations
    channel: email
  steps:
  - id: s1
    builds: experiment
    uses:
    - lifecycle_stage_attribute
    - first_name_attribute
    - homepage_hero_container
    - recommendation_service
    - homepage_path
    - winback_discount_percent
    - display_frequency
    - fallback_first_name
    instruction: 'Create a client-side personalization titled "Lifecycle Stage Homepage Personalization" that replaces the
      contents of {homepage_hero_container} on {homepage_path} and runs continuously with display frequency {display_frequency},
      targeting all devices. Build four variants. Control: the standard homepage hero, shown to all visitors as the fallback
      for users whose {lifecycle_stage_attribute} is empty or not yet computed. Variant B "Welcome back": shown when {lifecycle_stage_attribute}
      is "Champions" or "Regulars"; heading "Welcome back, [first_name]" with the line "Your favorites are waiting: plus new
      arrivals tailored to you.", a "View past orders" link to /account/orders, a primary "Shop new arrivals" link to /new-arrivals
      with id hero-cta-new, and a "Picked for you" recommendations block using purchase-history recommendations from {recommendation_service}.
      Variant C "We''ve missed you": shown when {lifecycle_stage_attribute} is "At risk" or "Needs attention"; heading "We''ve
      missed you, [first_name]" with the line "Here''s {winback_discount_percent}% off your next order: welcome back.", a
      primary button "Claim {winback_discount_percent}% off" with id hero-cta-claim, and a "Stock up on what you love" recommendations
      block using reorder-favorites recommendations from {recommendation_service}. Variant D "First-time browse": shown when
      {lifecycle_stage_attribute} is "New customers" or "Promising"; heading "Welcome to [Brand]" with the line "Discover
      what makes us special: handpicked starters under $50.", a primary "Shop bestsellers" link to /best-sellers with id hero-cta-bestsellers,
      and a "Popular this week" recommendations block using popularity recommendations from {recommendation_service}. In every
      variant, [first_name] comes from {first_name_attribute}; if it is missing, fall back to "{fallback_first_name}" without
      a name. Track conversions as placed order within session per lifecycle group, average order value per audience, and
      clicks on the personalized hero per audience.'
---

# Homepage by customer lifecycle stage

Slash command: /lifecycle-stage-homepage-personalization

## Step 1: Set up the three lifecycle heroes

Create a CLIENT PERSONALIZATION on /experiences titled "Lifecycle Stage Homepage Personalization".
Different homepage experiences for different lifecycle stages, using the canonical Users.Lifecycle score enum (At risk, Needs attention, New customers, Promising, Regulars, Champions).
═══ PATH 1: Top-level configuration ═══
Experience type: client_personalization
Variants (each binds to a specific lifecycle audience):
- Control: standard homepage, audience = "all" (fallback for visitors whose Lifecycle score is null or for new sessions before the score is computed)
- Variant B: "Welcome back" experience, audience = "Champions OR Regulars"
 - Audience: Users.Lifecycle score IN ("Champions", "Regulars")
- Variant C: "We've missed you" win-back experience, audience = "At risk OR Needs attention"
 - Audience: Users.Lifecycle score IN ("At risk", "Needs attention")
- Variant D: "First-time browse" introduction, audience = "New customers OR Promising"
 - Audience: Users.Lifecycle score IN ("New customers", "Promising")
Targeting:
- Pages: page URL is the homepage "/"
- Devices: any
- Display frequency: once_per_session (don't change the experience mid-session)
Metrics (existing CRM/CDP):
- Placed order within session (per lifecycle group conversion)
- Average order value per audience
- Click on engagement (which audiences engage with their personalized hero)
Schedule: continuous
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (all: fallback)
 Existing homepage hero remains.
Variant: B (Champions + Regulars: "Welcome back")
 HTML target selector: .homepage-hero (replace contents)
 Variant DOM:
 <section class="homepage-hero" data-variant="b" data-audience="champions-regulars">
 <h1>Welcome back, [first_name]</h1>
 <p>Your favorites are waiting: plus new arrivals tailored to you.</p>
 <div class="hero-cta-row">
 <a href="/account/orders" class="cta-link">View past orders</a>
 <a href="/new-arrivals" class="cta-primary" id="hero-cta-new">Shop new arrivals</a>
 </div>
 <section class="recommendations" data-rec-strategy="based-on-purchase-history">
 <h2>Picked for you</h2>
 <!-- recs based on user's order history -->
 </section>
 </section>
Variant: C (At risk + Needs attention: "We've missed you")
 HTML target selector: .homepage-hero (replace contents)
 Variant DOM:
 <section class="homepage-hero" data-variant="c" data-audience="at-risk">
 <h1>We've missed you, [first_name]</h1>
 <p>Here's 15% off your next order: welcome back.</p>
 <div class="hero-cta-row">
 <button class="cta-primary" id="hero-cta-claim">Claim 15% off</button>
 </div>
 <section class="recommendations" data-rec-strategy="reorder-favorites">
 <h2>Stock up on what you love</h2>
 <!-- recs based on past favorites -->
 </section>
 </section>
Variant: D (New customers + Promising: "First-time browse")
 HTML target selector: .homepage-hero (replace contents)
 Variant DOM:
 <section class="homepage-hero" data-variant="d" data-audience="new-promising">
 <h1>Welcome to [Brand]</h1>
 <p>Discover what makes us special: handpicked starters under $50.</p>
 <div class="hero-cta-row">
 <a href="/best-sellers" class="cta-primary" id="hero-cta-bestsellers">Shop bestsellers</a>
 </div>
 <section class="recommendations" data-rec-strategy="popular-with-new-customers">
 <h2>Popular this week</h2>
 <!-- popularity-based recs -->
 </section>
 </section>
The Visual Editor lets the user adjust copy, image selection, and recommendation block styling per audience. The [first_name] placeholder is replaced at render time from the Users object.
Taxonomy notes:
- Users.Lifecycle score is the canonical 6-stage enum: exact values: "At risk", "Needs attention", "New customers", "Promising", "Regulars", "Champions". Do NOT introduce textbook RFM segment names like "Loyal" or "VIP": the platform's lifecycle taxonomy is fixed at these six values.
- For the [first_name] personalization, ensure the Users object has first_name populated; if absent, the variant should gracefully fall back to "Welcome back" without the name.
- The "recommendations" block strategies (based-on-purchase-history, reorder-favorites, popular-with-new-customers) are application-level: typically powered by a recommendation API.
