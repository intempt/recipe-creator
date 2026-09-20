---
name: source-based-personalization
description: |
  Use when a user mentions "source-based personalization", or asks for related help. Match landing page hero / messaging to the ad source the visitor came from (utm_source, utm_campaign, referrer). Cited as "the simplest high-impact personalization implementation."
arguments: []
intempt:
  id: source-based-personalization
  version: 1.0.0
  slashCommand: /source-based-personalization
  group: Personalizations
  title: "Landing page matched to the ad"
  shortDescription: "The hero repeats the promise of the ad the visitor clicked, so a competitor search, a LinkedIn enterprise ad and a partner referral each land somewhere that matches."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [saas, b2b, ecommerce]
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
      title: "Set up the source variants"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      description: "Five variants matched on utm_source, utm_campaign and referrer: competitor search ads, LinkedIn enterprise ads, Facebook SMB ads, partner referrals and branded organic search. Direct traffic keeps the generic hero."
      prompt: |
        Create a CLIENT PERSONALIZATION on /experiences titled "Source-Based Personalization".

        This is the simplest high-impact personalization. Visitors from different sources (Google Ads, LinkedIn Ads, Facebook Ads, organic search, direct, partner referrals) see hero content matched to the source.

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_personalization

        Variants (each binds to a source audience):
        - Control (audience = all: fallback): generic hero for direct / organic / unattributed traffic
        - Variant B (audience = "Google Ads: competitor terms"): hero matches the competitor-comparison query
          - Audience: utm_source = "google" AND utm_campaign CONTAINS "competitor" or "alternative"
        - Variant C (audience = "LinkedIn Ads: enterprise"): hero matches the LinkedIn ad's enterprise messaging
          - Audience: utm_source = "linkedin" AND utm_campaign CONTAINS "enterprise"
        - Variant D (audience = "Facebook Ads: SMB"): hero matches the Facebook ad's SMB messaging
          - Audience: utm_source = "facebook" AND utm_campaign CONTAINS "smb"
        - Variant E (audience = "Partner referral"): hero matches the partner brand and offers a partner-specific incentive
          - Audience: referrer CONTAINS "partner-domain.com" OR utm_source = "partner_xyz"
        - Variant F (audience = "Organic: branded search"): hero matches the brand-search intent
          - Audience: utm_source = "google" AND utm_medium = "organic" AND landing_page contains "/" (homepage)

        Targeting:
        - Pages: homepage "/" and key landing pages (/lp, /landing-*)
        - Devices: any
        - Display frequency: always (within session: source attribution sticks for the session)

        Metrics:
        - form_submitted on demo / contact / signup form per source
        - click_on on primary CTA per source
        - Conversion rate per source (existing CRM/CDP attribution metric)

        Schedule: continuous

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes: fallback for direct/organic/unattributed traffic)

        Variant: B (Google Ads: competitor terms)
          HTML target selector: .homepage-hero
          Variant DOM:
          <section class="homepage-hero" data-variant="b" data-source="google-competitor">
            <h1>Looking for an alternative to [Competitor]?</h1>
            <p>Here's why teams switching from [Competitor] choose [Brand]:</p>
            <ul class="comparison-bullets">
              <li>Better [feature 1]: [outcome]</li>
              <li>Faster [feature 2]: [outcome]</li>
              <li>Lower cost at scale: [outcome]</li>
            </ul>
            <button class="primary-cta" id="hero-cta-comparison">See the comparison</button>
          </section>

        Variant: C (LinkedIn Ads: enterprise)
          Same structure with enterprise-targeted copy:
          <h1>Enterprise-grade [solution]: without the enterprise complexity</h1>
          <p>Trusted by Fortune 500 teams. SOC2, SAML SSO, dedicated support.</p>
          <button class="primary-cta" id="hero-cta-enterprise-demo">Book an enterprise demo</button>

        Variant: D (Facebook Ads: SMB)
          Same structure with SMB-targeted copy:
          <h1>The [solution] built for growing teams</h1>
          <p>Free for teams up to 5. No credit card required.</p>
          <button class="primary-cta" id="hero-cta-smb-signup">Start free trial</button>

        Variant: E (Partner referral)
          Same structure with partner co-branding:
          <h1>[Brand] + [Partner]: special offer for [Partner] customers</h1>
          <p>20% off your first year when you join through [Partner].</p>
          <img class="partner-logo" src="/partner-logos/[partner].svg" alt="[Partner]" />
          <button class="primary-cta" id="hero-cta-partner-signup">Claim partner offer</button>

        Variant: F (Organic: branded search)
          Same structure with brand-search intent (visitor already knows you):
          <h1>Welcome: get started with [Brand]</h1>
          <p>You searched for us. Here's how to start.</p>
          <button class="primary-cta" id="hero-cta-direct-signup">Start free trial</button>

        The Visual Editor allows the user to refine copy, swap images, and adjust CTAs per source segment. Ensure the [Competitor] / [Partner] placeholders are populated correctly per variant.

        Taxonomy notes:
        - The canonical Users-object UTM attributes are: utm_source, utm_medium, utm_campaign, utm_content, utm_term: all standard. Plus referrer and landing_page.
        - These attributes are populated automatically on session_start from URL parameters and HTTP referrer header.
        - For source attribution to persist beyond the entry session, the platform stores the first-touch UTM values on the user record (Users.utm_source, etc.). This is the canonical pattern.
        - Don't over-segment: 4-6 source segments is the sweet spot. Too many segments to low traffic per variant to unmeasurable.
        - Combine with industry-vertical or ABM personalization for compounding effect, but order precedence carefully (per-account beats per-source beats per-industry beats default).
  outputs:
    - { name: personalization, type: personalization, cardinality: single, description: "Website personalization created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Landing page matched to the ad

The hero repeats the promise of the ad the visitor clicked, so a competitor search, a LinkedIn enterprise ad and a partner referral each land somewhere that matches.

## What it does

1. **Set up the source variants** (`create_personalization`)

   Five variants matched on utm_source, utm_campaign and referrer: competitor search ads, LinkedIn enterprise ads, Facebook SMB ads, partner referrals and branded organic search. Direct traffic keeps the generic hero.

## What you end up with

- **personalization** (personalization): Website personalization created on /experiences.
