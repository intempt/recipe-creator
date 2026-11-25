---
frontmatter_id: browse-purchase-funnel
slash_command: /browse-purchase-funnel
description: Emails a weekly count of how many shoppers move from a category page to a product page, cart, checkout and a
  completed order, and where you lose them on each device.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of how many shoppers move from category page to product page, cart, checkout and order,
    and where they drop off on each device.
  parameters:
  - name: conversionWindow
    type: duration
    label: Time allowed from category page to order
    default: 7 d
    required: false
  - name: comparisonPeriod
    type: duration
    label: Window analyzed and compared with the one before
    default: 7 d
    required: false
  - name: dropOffWorsenThreshold
    type: number
    label: Drop-off worsening that is flagged (points)
    default: 3
    required: false
  - name: mobileLagThreshold
    type: number
    label: Mobile lag behind desktop that is flagged (points)
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: category_page_view
    kind: event
    meaning: A customer viewed a page in the browse flow
    properties:
    - name: page_url
      type: string
      meaning: URL of the viewed page
      optional: false
  - slot: product_page_view
    kind: event
    meaning: A customer viewed a product detail page
  - slot: cart_created
    kind: event
    meaning: A customer created a shopping cart
  - slot: checkout_created
    kind: event
    meaning: A customer created a checkout
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
  - slot: device_type
    kind: attribute
    meaning: The device type a user typically uses (desktop, mobile, tablet)
  steps:
  - id: s1
    builds: automation
    uses:
    - category_page_view
    - product_page_view
    - cart_created
    - checkout_created
    - order_placed
    - device_type
    - conversionWindow
    - comparisonPeriod
    - dropOffWorsenThreshold
    - mobileLagThreshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes customers who did
      {category_page_view} with {category_page_view.page_url} containing /collections/ or /category/ in the last {comparisonPeriod}
      and in the {comparisonPeriod} before, through these steps in order within {conversionWindow}: {product_page_view}, {cart_created},
      {checkout_created}, {order_placed}. It writes these figures for both windows: customers at each step; conversion % from
      the step before, overall and per {device_type}; median time from the step before. The first lines name the step with
      the largest drop-off, any step where mobile conversion is more than {mobileLagThreshold} points below desktop, and any
      step whose drop-off worsened more than {dropOffWorsenThreshold} points against the window before. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Browse to purchase funnel

Slash command: /browse-purchase-funnel

## Step 1: Email the weekly browse-to-purchase digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes customers who did category page view with page url containing /collections/ or /category/ in the last 7 d and in the 7 d before, through these steps in order within 7 d: product page view, cart created, checkout created, order placed. It writes these figures for both windows: customers at each step; conversion % from the step before, overall and per device type; median time from the step before. The first lines name the step with the largest drop-off, any step where mobile conversion is more than 10 points below desktop, and any step whose drop-off worsened more than 3 points against the window before. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
