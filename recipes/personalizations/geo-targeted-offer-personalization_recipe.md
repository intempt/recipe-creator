---
name: geo-targeted-offer-personalization
description: |
  Use when a user mentions "geo-targeted offer personalization", or asks for related help. Show different homepage offers based on visitor's geography (country, region) — different shipping promotions, currency display, and local promotions. Client personalization.
arguments: []
intempt:
  id: geo-targeted-offer-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  group: Personalizations
  shortDescription: "Show different homepage offers based on visitor's geography (country, region) — different shipping promotions, currency display, and local promotions. Client personalization."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [ecommerce]
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
      title: "Configure Website Personalization"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      description: "Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2)."
      prompt: |
        Create a CLIENT PERSONALIZATION on /experiences titled "Geo-Targeted Offer Personalization".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_personalization

        Variants (each binds to geographic audience):
        - Control (audience = all — fallback): default homepage with global shipping messaging
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

        Variant: Control (all — fallback, generic)
          Existing hero with global messaging.

        Variant: B (US visitors)
          HTML target selector: .promo-banner (and .price-display elements)
          Variant DOM:
          <div class="promo-banner" data-variant="b" data-region="US">
            <p>🇺🇸 Free shipping on orders over $50 — delivered in 2-5 days</p>
            <a href="/sale" class="banner-cta" id="banner-cta-us">Shop the US Sale</a>
          </div>
          Plus: data attribute on body — data-currency="USD" — application reads to format prices.

        Variant: C (UK + EU visitors)
          HTML target selector: .promo-banner
          Variant DOM:
          <div class="promo-banner" data-variant="c" data-region="EU">
            <p>🇪🇺 Free shipping on orders over €50 / £50 — delivered in 3-7 days</p>
            <a href="/sale-eu" class="banner-cta" id="banner-cta-eu">Shop the EU Sale</a>
          </div>
          Plus: data-currency="GBP" or "EUR" depending on country, and a GDPR notice strip if not already shown.

        Variant: D (APAC visitors)
          HTML target selector: .promo-banner
          Variant DOM:
          <div class="promo-banner" data-variant="d" data-region="APAC">
            <p>🌏 Free shipping to AU, JP, SG, HK, KR — delivered in 5-10 days</p>
            <a href="/sale-apac" class="banner-cta" id="banner-cta-apac">Shop APAC Sale</a>
            <div class="local-payment-methods">Pay with Alipay · GrabPay · KakaoPay</div>
          </div>

        The Visual Editor lets the user refine the regional messaging, payment-method icons, and shipping promise per region.

        Taxonomy notes:
        - Users.country is canonical (geo-IP enriched at session start). Use the ISO 3166-1 alpha-2 country code.
        - Currency display is application-side; this recipe sets the data-currency attribute, and the application's price-formatting logic reads it.
        - For prices to actually change, the application must read the currency hint and re-format. The recipe assumes price formatting is centralized in a JS helper that respects data-currency.
  outputs:
    - { name: personalization, type: personalization, cardinality: single, description: "Website personalization created on /experiences." }
---

# Geo-Targeted Offer Personalization

## Procedure

1. **Configure Website Personalization** [`create_personalization`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: personalization

   ```text
   Create a CLIENT PERSONALIZATION on /experiences titled "Geo-Targeted Offer Personalization".

   ═══ PATH 1: Top-level configuration ═══

   Experience type: client_personalization

   Variants (each binds to geographic audience):
   - Control (audience = all — fallback): default homepage with global shipping messaging
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

   Variant: Control (all — fallback, generic)
     Existing hero with global messaging.

   Variant: B (US visitors)
     HTML target selector: .promo-banner (and .price-display elements)
     Variant DOM:
     <div class="promo-banner" data-variant="b" data-region="US">
       <p>🇺🇸 Free shipping on orders over $50 — delivered in 2-5 days</p>
       <a href="/sale" class="banner-cta" id="banner-cta-us">Shop the US Sale</a>
     </div>
     Plus: data attribute on body — data-currency="USD" — application reads to format prices.

   Variant: C (UK + EU visitors)
     HTML target selector: .promo-banner
     Variant DOM:
     <div class="promo-banner" data-variant="c" data-region="EU">
       <p>🇪🇺 Free shipping on orders over €50 / £50 — delivered in 3-7 days</p>
       <a href="/sale-eu" class="banner-cta" id="banner-cta-eu">Shop the EU Sale</a>
     </div>
     Plus: data-currency="GBP" or "EUR" depending on country, and a GDPR notice strip if not already shown.

   Variant: D (APAC visitors)
     HTML target selector: .promo-banner
     Variant DOM:
     <div class="promo-banner" data-variant="d" data-region="APAC">
       <p>🌏 Free shipping to AU, JP, SG, HK, KR — delivered in 5-10 days</p>
       <a href="/sale-apac" class="banner-cta" id="banner-cta-apac">Shop APAC Sale</a>
       <div class="local-payment-methods">Pay with Alipay · GrabPay · KakaoPay</div>
     </div>

   The Visual Editor lets the user refine the regional messaging, payment-method icons, and shipping promise per region.

   Taxonomy notes:
   - Users.country is canonical (geo-IP enriched at session start). Use the ISO 3166-1 alpha-2 country code.
   - Currency display is application-side; this recipe sets the data-currency attribute, and the application's price-formatting logic reads it.
   - For prices to actually change, the application must read the currency hint and re-format. The recipe assumes price formatting is centralized in a JS helper that respects data-currency.
   ```
