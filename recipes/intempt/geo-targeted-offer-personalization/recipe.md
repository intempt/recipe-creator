---
frontmatter_id: geo-targeted-offer-personalization
slash_command: /geo-targeted-offer-personalization
description: Visitors from the US, UK and EU, and APAC see region-specific homepage offer content instead of one global message. The recipe uses visitor geography to swap promotion copy.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows homepage visitors in the US, UK, EU and APAC region-specific free-shipping offer banners with local pricing
    instead of one global message.
  parameters:
  - name: us_free_shipping_threshold
    type: number
    label: US free shipping threshold (USD)
    default: 50
    required: false
  - name: eu_free_shipping_threshold
    type: number
    label: UK/EU free shipping threshold (GBP/EUR)
    default: 50
    required: false
  - name: display_frequency
    type: enum
    label: Display frequency
    default: once_per_session
    required: false
    options:
    - once_per_session
    - once_per_day
    - always
  - name: promo_tone
    type: enum
    label: Promo tone
    default: standard
    required: false
    options:
    - standard
    - friendly
    - urgent
  requirements:
  - slot: geo_offer_experience
    kind: destination
    meaning: A client-side personalization experience on the website homepage that can show different banner variants to visitors
      by audience.
    channel: email
  - slot: visitor_country
    kind: attribute
    meaning: The visitor's ISO 3166-1 alpha-2 country code, geo-IP enriched at session start.
  - slot: order_placed
    kind: event
    meaning: A customer placed an order.
    properties:
    - name: order_value
      type: number
      meaning: Total value of the order
      optional: false
  - slot: cta_click
    kind: event
    meaning: A visitor clicked a regional offer call-to-action button on the website.
    properties:
    - name: cta_id
      type: string
      meaning: Identifier of the clicked call-to-action
      optional: false
    optional: true
  steps:
  - id: s1
    builds: experiment
    uses:
    - geo_offer_experience
    - visitor_country
    - order_placed
    - cta_click
    - us_free_shipping_threshold
    - eu_free_shipping_threshold
    - display_frequency
    - promo_tone
    instruction: 'Create a client-side personalization titled "Geo-Targeted Offer Personalization" on the website experiences
      page, targeting the homepage "/" on any device, with display frequency {display_frequency} and continuous schedule.
      Create four variants: (1) Control, the fallback for all visitors, showing the default homepage hero with global shipping
      messaging. (2) Variant B, audience = visitors where {visitor_country} equals "US": in the .promo-banner element show
      a US promo with free shipping on orders over ${us_free_shipping_threshold} and USD prices, with a CTA linking to /sale.
      (3) Variant C, audience = visitors where {visitor_country} is one of "GB", "DE", "FR", "ES", "IT", "NL": in the .promo-banner
      element show a UK/EU promo with free shipping on orders over £{eu_free_shipping_threshold} / €{eu_free_shipping_threshold},
      delivered in 3-7 days, with a CTA linking to /sale-eu, and set the body currency attribute to GBP or EUR depending on
      country; show a GDPR notice strip if not already shown. (4) Variant D, audience = visitors where {visitor_country} is
      one of "AU", "JP", "SG", "HK", "KR": in the .promo-banner element show an APAC promo with free shipping to these countries
      delivered in 5-10 days, a CTA linking to /sale-apac, and a local payment methods callout (Alipay, GrabPay, KakaoPay).
      Apply the tone {promo_tone} to all banner copy. Also set the body currency attribute to USD for the US variant so the
      price helper formats prices. Track these metrics: orders placed per geographic audience and average order value per
      audience (from {order_placed.order_value}), and clicks on the geo-specific CTAs ({cta_click}).'
---

# Offers by visitor country

Slash command: /geo-targeted-offer-personalization

## Step 1: Set up the regional offers

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
- Placed order per geographic audience
- Average order value per audience
- Click on engagement on geo-specific CTAs
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
