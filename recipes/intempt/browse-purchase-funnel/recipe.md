---
frontmatter_id: browse-purchase-funnel
slash_command: /browse-purchase-funnel
description: Shows how many shoppers move from a category page to a product page, cart, checkout and a completed order, and where you lose them on each device.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows how many shoppers move from a category page to a product page, cart, checkout and completed order, and where
    they drop off on each device.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 7 d
    required: false
  - name: comparisonPeriod
    type: duration
    label: Comparison period (prior period)
    default: 7 d
    required: false
  - name: dropOffWorsenThreshold
    type: number
    label: Drop-off worsening threshold (percentage points)
    default: 3
    required: false
  - name: mobileLagThreshold
    type: number
    label: Mobile vs desktop conversion lag threshold (percentage points)
    default: 10
    required: false
  - name: fashionBenchmark
    type: text
    label: Fashion browse-to-buy benchmark
    default: 2-3%
    required: false
  - name: electronicsBenchmark
    type: text
    label: Electronics browse-to-buy benchmark
    default: 4-6%
    required: false
  requirements:
  - slot: category_page_view
    kind: event
    meaning: A customer viewed a page in the browse flow
    properties:
    - name: content_type
      type: text
      meaning: Type of page viewed, such as category or listing
      optional: true
    - name: page_url
      type: text
      meaning: URL path of the page viewed
      optional: false
  - slot: product_page_view
    kind: event
    meaning: A customer viewed a product detail page
    properties:
    - name: page_url
      type: text
      meaning: URL path of the page viewed
      optional: false
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
    builds: report
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
    - fashionBenchmark
    - electronicsBenchmark
    instruction: 'Create a Funnel report called "Browse to Purchase" with these steps in order: 1) {category_page_view} where
      content_type indicates a category or listing page (or page_url contains /collections/ or /category/), labeled "Browsed
      Category"; 2) {product_page_view} where page_url indicates a product detail page (for example contains /products/),
      labeled "Viewed Product Detail"; 3) {cart_created}, labeled "Added to Cart"; 4) {checkout_created}, labeled "Started
      Checkout"; 5) {order_placed}, labeled "Completed Purchase". Set the conversion window to {conversionWindow}. Break down
      by {device_type} on the Users object (desktop, mobile, tablet). Compare against the previous period of {comparisonPeriod}.
      For each step, also show the median time-to-convert from the previous step and the per-device conversion rate at each
      step. Annotations: flag the step with the largest drop-off as the primary bottleneck; flag any step where mobile conversion
      lags desktop by more than {mobileLagThreshold} percentage points as a mobile UX issue; highlight any step where overall
      drop-off worsened by more than {dropOffWorsenThreshold} percentage points versus the previous period. Show industry
      benchmarks for reference: {fashionBenchmark} browse-to-buy for fashion and {electronicsBenchmark} for electronics. Use
      Category page content_type or URL path patterns and Placed order as the purchase event; do not use nonexistent events
      such as product_list_viewed, product_viewed or checkout_started.'
---

# Browse to purchase funnel

Slash command: /browse-purchase-funnel

## Step 1: Trace category page to order

Create a Funnel report called "Browse to Purchase".
Steps:
1. Event "View page" where content_type indicates a category/listing page (or Page URL contains /collections/ or /category/): "Browsed Category"
2. Event "View page" where Page URL indicates a product detail page (e.g. contains /products/): "Viewed Product Detail"
3. Event "Cart created": "Added to Cart"
4. Event "Checkout created": "Started Checkout"
5. Event "Placed order": "Completed Purchase"
Conversion window: 7 days
Breakdown: By "device_type" attribute on the Users object (desktop, mobile, tablet)
Compare: Previous period (prior 7 days)
For each step, also surface:
- Median time-to-convert from previous step
- Per-device conversion rate at each step
Annotations:
- Flag the step with the largest drop-off (the primary bottleneck).
- Flag any step where mobile conversion lags desktop by >10 percentage points (mobile UX issue).
- Highlight any step where overall drop-off worsened by >3 percentage points vs. previous period.
Industry benchmarks: 2-3% browse-to-buy for fashion, 4-6% for electronics.
Taxonomy notes:
- "product_list_viewed" and "product_viewed" as standalone events do not exist. Page-type discrimination is done via View page.Page URL path patterns or View page.content_type.
- "checkout_started" does not exist; Checkout created is the canonical pre-payment marker.
- Placed order is the canonical purchase event (cart_converted is also valid for cart-source attribution).
