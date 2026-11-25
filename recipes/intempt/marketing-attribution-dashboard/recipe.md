---
frontmatter_id: marketing-attribution-dashboard
slash_command: /marketing-attribution-dashboard
description: Emails a weekly digest of where revenue comes from across paid, organic, email and search, with lifetime value
  per channel. ROAS and CAC need ad-spend data and are not included.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of revenue by first-touch channel against last year, email, paid and organic totals, and
    lifetime value per channel (ROAS and CAC excluded).
  parameters:
  - name: defaultDateRange
    type: duration
    label: Window the figures cover
    default: 30 d
    required: false
  - name: emailUtmSource
    type: string
    label: UTM source value for email
    default: email
    required: false
  - name: paidUtmSources
    type: text
    label: UTM source values for paid channels
    default: paid_search, paid_social, paid_other
    required: false
  - name: organicUtmSources
    type: text
    label: UTM source values for organic channels
    default: organic, direct, organic_social
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total
      optional: false
  - slot: utm_source_attribute
    kind: attribute
    meaning: The first-touch UTM source recorded on the user
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - utm_source_attribute
    - defaultDateRange
    - emailUtmSource
    - paidUtmSources
    - organicUtmSources
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes orders by the buyer''s
      {utm_source_attribute} and writes these figures: the sum of {placed_order_event.total_price} in the last {defaultDateRange}
      per {utm_source_attribute}, against the same window one year earlier, ranked; the revenue in the last {defaultDateRange}
      from users whose {utm_source_attribute} is {emailUtmSource}, is one of {paidUtmSources}, and is one of {organicUtmSources},
      each with its share of the total; the count of first-time buyers in the last {defaultDateRange} per {utm_source_attribute};
      the average cumulative {placed_order_event.total_price} per customer in the 12 months after the first order, per {utm_source_attribute},
      for customers whose first order was between 12 and 24 months ago. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Revenue by marketing channel

Slash command: /marketing-attribution-dashboard

## Step 1: Email the weekly channel revenue digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes orders by the buyer's utm source attribute and writes these figures: the sum of total price in the last 30 d per utm source attribute, against the same window one year earlier, ranked; the revenue in the last 30 d from users whose utm source attribute is email, is one of paid_search, paid_social, paid_other, and is one of organic, direct, organic_social, each with its share of the total; the count of first-time buyers in the last 30 d per utm source attribute; the average cumulative total price per customer in the 12 months after the first order, per utm source attribute, for customers whose first order was between 12 and 24 months ago. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
