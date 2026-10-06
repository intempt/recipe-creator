---
id: geo-targeted-offer-personalization
title: Offers by visitor country
slash_command: /geo-targeted-offer-personalization
group: Personalizations
owner: intempt
curator: rana
summary: >-
  Visitors from the US, UK and EU, and APAC see region-specific homepage offer content instead of one global
  message. The recipe uses visitor geography to swap promotion copy.
description: >-
  Show different homepage promotion content based on visitor geography such as country or region. The recipe
  swaps offer copy only, not currency pricing or payment methods.
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - ecommerce
  industry:
    - ecommerce
    - media
  vertical: []
  complexity: standard
  executionMode: live
  tags:
    - personalization
    - client
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new website personalization, from step 1 "Set up the regional offers"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Set up the regional offers
    summary: >-
      US visitors see free shipping over $50 priced in dollars, UK and EU visitors see local currency
      and a GDPR-compliant footer, APAC visitors see regional shipping and local payment methods. Every
      other country keeps the global message.
    builds: personalization
    description: |-
      Create a CLIENT PERSONALIZATION on /experiences titled "Geo-Targeted Offer Personalization".
      ═══ PATH 1: Top-level configuration ═══
      Experience type: client_personalization
      Variants (each binds to geographic audience):
      - Control (audience = all: fallback): default homepage with global shipping messaging
      - Variant B (audience = US visitors): US-specific promo (free shipping over $50, USD prices)
       - Audience: Users.country = "US"
      - Variant C (audience = UK + EU visitors): UK/EU-specific promo (free shipping over £50/€50, local currency, GDPR-compliant footer)
       - Audience: Users.country IN ("GB", "DE", "FR", "ES", "IT", "NL")
      - Variant D (audience = APAC visitors): APAC-specific promo (regional shipping, local payment methods callout)
       - Audience: Users.country IN ("AU", "JP", "SG", "HK", "KR")
      Targeting:
      - Pages: homepage "/"
      - Devices: any
      - Display frequency: once_per_session
      Metrics:
      - order_created per geographic audience
      - Average order value per audience
      - click_on engagement on geo-specific CTAs
      Schedule: continuous
      ═══ PATH 2: Variant HTML content (Visual Editor) ═══
      Variant: Control (all: fallback, generic)
       Existing hero with global messaging.
      Variant: B (US visitors)
       HTML target selector: .promo-banner (and .price-display elements)
       Variant DOM:
       <div class="promo-banner" data-variant="b" data-region="US">
       <p>🇺🇸 Free shipping on orders over $50: delivered in 2-5 days</p>
       <a href="/sale" class="banner-cta" id="banner-cta-us">Shop the US Sale</a>
       </div>
       Plus: data attribute on body (data-currency="USD") application reads to format prices.
      Variant: C (UK + EU visitors)
       HTML target selector: .promo-banner
       Variant DOM:
       <div class="promo-banner" data-variant="c" data-region="EU">
       <p>🇪🇺 Free shipping on orders over €50 / £50: delivered in 3-7 days</p>
       <a href="/sale-eu" class="banner-cta" id="banner-cta-eu">Shop the EU Sale</a>
       </div>
       Plus: data-currency="GBP" or "EUR" depending on country, and a GDPR notice strip if not already shown.
      Variant: D (APAC visitors)
       HTML target selector: .promo-banner
       Variant DOM:
       <div class="promo-banner" data-variant="d" data-region="APAC">
       <p>🌏 Free shipping to AU, JP, SG, HK, KR: delivered in 5-10 days</p>
       <a href="/sale-apac" class="banner-cta" id="banner-cta-apac">Shop APAC Sale</a>
       <div class="local-payment-methods">Pay with Alipay · GrabPay · KakaoPay</div>
       </div>
      The Visual Editor lets the user refine the regional messaging, payment-method icons, and shipping promise per region.
      Taxonomy notes:
      - Users.country is canonical (geo-IP enriched at session start). Use the ISO 3166-1 alpha-2 country code.
      - Currency display is application-side; this recipe sets the data-currency attribute, and the application's price-formatting logic reads it.
      - For prices to actually change, the application must read the currency hint and re-format. The recipe assumes price formatting is centralized in a JS helper that respects data-currency.
outputs:
  - key: personalization
    producedByStep: s1
    type: personalization
    description: Website personalization created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Offers by visitor country

Visitors from the US, UK and EU, and APAC see region-specific homepage offer content instead of one global message. The recipe uses visitor geography to swap promotion copy.

## Steps

1. **Set up the regional offers** (builds personalization)

   US visitors see free shipping over $50 priced in dollars, UK and EU visitors see local currency and a GDPR-compliant footer, APAC visitors see regional shipping and local payment methods. Every other country keeps the global message.

## What you end up with

- **personalization** (personalization): Website personalization created on /experiences.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new website personalization, from step 1 "Set up the regional offers"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build personalization.
