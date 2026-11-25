---
frontmatter_id: geo-targeted-offer-personalization
slash_command: /geo-targeted-offer-personalization
description: Visitors from the US, UK and EU, and APAC see a region-specific homepage offer banner instead of one global message,
  using the visitor's country to swap the promotion copy.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows homepage visitors in the US, UK and EU, and APAC a region-specific free-shipping offer banner instead of
    one global message.
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
  - slot: visitor_country
    kind: attribute
    meaning: The visitor's two-letter country code, from geo-IP at session start
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
    properties:
    - name: order_value
      type: number
      meaning: Order total
      optional: false
  - slot: cta_click
    kind: event
    meaning: A visitor clicked a regional offer button on the website
    optional: true
  steps:
  - id: s1
    builds: personalization
    uses:
    - visitor_country
    - order_placed
    - cta_click
    - us_free_shipping_threshold
    - eu_free_shipping_threshold
    - display_frequency
    - promo_tone
    instruction: 'Create a website personalization named "Geo-Targeted Offer Personalization" on the homepage "/", any device,
      display frequency {display_frequency}, running continuously, with variants by audience. Default: all other visitors
      see the current banner with global shipping copy. Visitors whose {visitor_country} is US: the .promo-banner element
      says free shipping on orders over ${us_free_shipping_threshold}, with a button to /sale. {visitor_country} is GB, DE,
      FR, ES, IT or NL: free shipping on orders over £{eu_free_shipping_threshold} or €{eu_free_shipping_threshold} by country,
      delivered in 3-7 days, with a button to /sale-eu. {visitor_country} is AU, JP, SG, HK or KR: free shipping to their
      country, delivered in 5-10 days, with a button to /sale-apac. Write all banner copy in a {promo_tone} tone. Measure
      {order_placed} count and average {order_placed.order_value} per audience, and {cta_click} per banner.'
---

# Offers by visitor country

Slash command: /geo-targeted-offer-personalization

## Step 1: Set up the regional offers

Create a website personalization named "Geo-Targeted Offer Personalization" on the homepage "/", any device, display frequency once_per_session, running continuously, with variants by audience. Default: all other visitors see the current banner with global shipping copy. Visitors whose visitor country is US: the .promo-banner element says free shipping on orders over $50, with a button to /sale. visitor country is GB, DE, FR, ES, IT or NL: free shipping on orders over £50 or €50 by country, delivered in 3-7 days, with a button to /sale-eu. visitor country is AU, JP, SG, HK or KR: free shipping to their country, delivered in 5-10 days, with a button to /sale-apac. Write all banner copy in a standard tone. Measure order placed count and average order value per audience, and cta click per banner.
