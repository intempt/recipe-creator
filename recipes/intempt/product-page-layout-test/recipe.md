---
frontmatter_id: product-page-layout-test
slash_command: /product-page-layout-test
description: Compares your current product page against a full-width hero with a floating details panel and a video-first layout.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Runs a three-way product page layout test (current page, full-width hero with floating details panel, video-first
    layout) and measures add-to-cart, orders, and time on page.
  parameters:
  - name: experimentTitle
    type: string
    label: Experiment title
    default: Product Page Layout
    required: false
  - name: targetingUrlContains
    type: string
    label: Page URL contains
    default: /products/
    required: false
  - name: controlTrafficPercent
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variantBTrafficPercent
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: variantCTrafficPercent
    type: number
    label: Variant C traffic share (%)
    default: 33
    required: false
  - name: testDuration
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: minUniqueVisitorsPerVariant
    type: number
    label: Minimum unique PDP visitors per variant
    default: 2000
    required: false
  - name: orderWindow
    type: duration
    label: Order attribution window after exposure
    default: 7 d
    required: false
  - name: bounceRateIncreaseLimit
    type: number
    label: Maximum allowed bounce rate increase (%)
    default: 5
    required: false
  requirements:
  - slot: product_page_views
    kind: event
    meaning: A customer viewed a product page
  - slot: cart_created
    kind: event
    meaning: A customer added a product to a new cart
    properties:
    - name: product_id
      type: string
      meaning: Identifier of the product added
      optional: false
    - name: quantity
      type: number
      meaning: Number of units added
      optional: false
    - name: order_total
      type: number
      meaning: Order total value after adding the product
      optional: false
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
  - slot: add_to_cart_click
    kind: event
    meaning: A visitor clicked a button with target id add-to-cart-button
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element
      optional: false
  steps:
  - id: s1
    builds: experiment
    uses:
    - add_to_cart_click
    - bounceRateIncreaseLimit
    - cart_created
    - controlTrafficPercent
    - experimentTitle
    - minUniqueVisitorsPerVariant
    - orderWindow
    - order_placed
    - product_page_views
    - targetingUrlContains
    - testDuration
    - variantBTrafficPercent
    - variantCTrafficPercent
    instruction: 'Create a client experiment titled "{experimentTitle}" on the experiences page. Target visitors on pages
      whose URL contains "{targetingUrlContains}", all devices, all visitors, display frequency always. Variants: Control
      ({controlTrafficPercent}%) keeps the existing product page, image gallery on the left and details on the right. Variant
      B ({variantBTrafficPercent}%) shows a full-width hero image with a floating details panel, with its own mobile layout.
      Variant C ({variantCTrafficPercent}%) puts a muted, looping product video above the product name, price and add-to-cart
      button, with description and reviews below; it does not autoplay for visitors who prefer reduced motion. Keep the add-to-cart
      button id add-to-cart-button the same in all variants. Primary metric: add-to-cart rate, from {add_to_cart_click} and
      {cart_created}. Secondary metrics: share of {product_page_views} visitors who do {order_placed} within {orderWindow};
      time on page. Guardrail: bounce rate must not rise by more than {bounceRateIncreaseLimit}%. Run for {testDuration} and
      until each variant has {minUniqueVisitorsPerVariant} unique visitors.'
---

# Product page layout test

Slash command: /product-page-layout-test

## Step 1: Set up the layout test

Create a client experiment titled "Product Page Layout" on the experiences page. Target visitors on pages whose URL contains "/products/", all devices, all visitors, display frequency always. Variants: Control (34%) keeps the existing product page, image gallery on the left and details on the right. Variant B (33%) shows a full-width hero image with a floating details panel, with its own mobile layout. Variant C (33%) puts a muted, looping product video above the product name, price and add-to-cart button, with description and reviews below; it does not autoplay for visitors who prefer reduced motion. Keep the add-to-cart button id add-to-cart-button the same in all variants. Primary metric: add-to-cart rate, from add to cart click and cart created. Secondary metrics: share of product page views visitors who do order placed within 7 d; time on page. Guardrail: bounce rate must not rise by more than 5%. Run for 14 d and until each variant has 2000 unique visitors.
