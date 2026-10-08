---
description: Loyal shoppers get a welcome back, lapsed ones get a win-back offer, and new shoppers get an introduction, based on the lifecycle stage already on their profile.
author:
  first_name: V
  last_name: Ranadheer
  job_title: Design Engineer
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce
  - media
---

# Homepage by customer lifecycle stage

Slash command: /lifecycle-stage-homepage-personalization

## Step 1: Set up the three lifecycle heroes

Create a CLIENT PERSONALIZATION on /experiences titled "Lifecycle Stage Homepage Personalization".
Different homepage experiences for different lifecycle stages, using the canonical Users.lifecycle_score enum (At risk, Needs attention, New customers, Promising, Regulars, Champions).
═══ PATH 1: Top-level configuration ═══
Experience type: client_personalization
Variants (each binds to a specific lifecycle audience):
- Control: standard homepage, audience = "all" (fallback for visitors whose lifecycle_score is null or for new sessions before the score is computed)
- Variant B: "Welcome back" experience, audience = "Champions OR Regulars"
 - Audience: Users.lifecycle_score IN ("Champions", "Regulars")
- Variant C: "We've missed you" win-back experience, audience = "At risk OR Needs attention"
 - Audience: Users.lifecycle_score IN ("At risk", "Needs attention")
- Variant D: "First-time browse" introduction, audience = "New customers OR Promising"
 - Audience: Users.lifecycle_score IN ("New customers", "Promising")
Targeting:
- Pages: page URL is the homepage "/"
- Devices: any
- Display frequency: once_per_session (don't change the experience mid-session)
Metrics (existing CRM/CDP):
- order_created within session (per lifecycle group conversion)
- Average order value per audience
- click_on engagement (which audiences engage with their personalized hero)
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
- Users.lifecycle_score is the canonical 6-stage enum: exact values: "At risk", "Needs attention", "New customers", "Promising", "Regulars", "Champions". Do NOT introduce textbook RFM segment names like "Loyal" or "VIP": the platform's lifecycle taxonomy is fixed at these six values.
- For the [first_name] personalization, ensure the Users object has first_name populated; if absent, the variant should gracefully fall back to "Welcome back" without the name.
- The "recommendations" block strategies (based-on-purchase-history, reorder-favorites, popular-with-new-customers) are application-level: typically powered by a recommendation API.
