---
frontmatter_id: checkout-form-friction
slash_command: /checkout-form-friction
description: Shows which checkout step loses you orders, how long shoppers sit on each one, and where mobile is worse than desktop.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows which checkout step loses the most orders, how long shoppers spend on each step, and where mobile drop-off
    is worse than desktop.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 1 h
    required: false
  - name: comparisonPeriod
    type: duration
    label: Comparison period (prior period length)
    default: 30 d
    required: false
  - name: timeThreshold
    type: number
    label: Median time-on-page flag threshold (seconds)
    default: 90
    required: false
  - name: mobileGapThreshold
    type: number
    label: Mobile vs desktop drop-off gap flag (percentage points)
    default: 15
    required: false
  - name: shippingPathPattern
    type: string
    label: Shipping step URL pattern
    default: /checkout/shipping
    required: false
  - name: paymentPathPattern
    type: string
    label: Payment step URL pattern
    default: /checkout/payment
    required: false
  - name: reviewPathPattern
    type: string
    label: Review step URL pattern
    default: /checkout/review
    required: false
  requirements:
  - slot: checkout_started_event
    kind: event
    meaning: A customer started a checkout
  - slot: checkout_completed_event
    kind: event
    meaning: A customer completed a checkout and placed an order
  - slot: page_view_event
    kind: event
    meaning: A customer viewed a web page
    properties:
    - name: page_url
      type: string
      meaning: URL of the page viewed
      optional: false
  - slot: device_type_attribute
    kind: attribute
    meaning: The device type a user browses on (mobile or desktop)
  - slot: abandoned_checkout_event
    kind: event
    meaning: A customer abandoned a checkout without completing it
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - checkout_started_event
    - page_view_event
    - checkout_completed_event
    - device_type_attribute
    - abandoned_checkout_event
    - conversionWindow
    - comparisonPeriod
    - timeThreshold
    - mobileGapThreshold
    - shippingPathPattern
    - paymentPathPattern
    - reviewPathPattern
    instruction: 'Create a funnel report called "Checkout Form Friction" with these steps in order: 1) {checkout_started_event};
      2) {page_view_event} where page_url contains {shippingPathPattern} (shipping step), labeled "Reached Shipping"; 3) {page_view_event}
      where page_url contains {paymentPathPattern} (payment step), labeled "Reached Payment"; 4) {page_view_event} where page_url
      contains {reviewPathPattern} (review step), labeled "Reached Review"; 5) {checkout_completed_event}, labeled "Completed
      Order". Set the conversion window to {conversionWindow}. Break down by {device_type_attribute}. Compare against the
      previous {comparisonPeriod}. For each step, also show the median and 75th-percentile time on that step''s page, the
      drop-off rate versus the previous period, and, for users who reached but did not pass each step, their last in-checkout
      action. Annotate the step with the largest drop-off as the primary checkout bottleneck. Flag any step where median time-on-page
      exceeds {timeThreshold} seconds. Flag any step where mobile drop-off exceeds desktop drop-off by more than {mobileGapThreshold}
      percentage points. Highlight the volume of {abandoned_checkout_event} in the same period as recoverable users to pair
      with abandoned-cart recovery.'
---

# Checkout friction

Slash command: /checkout-form-friction

## Step 1: Find the stalling checkout step

Create a Funnel report called "Checkout Form Friction".
Steps:
1. Event "Checkout created": "Started Checkout"
2. Event "View page" where Page URL contains "/checkout/shipping" or equivalent shipping step: "Reached Shipping"
3. Event "View page" where Page URL contains "/checkout/payment" or equivalent payment step: "Reached Payment"
4. Event "View page" where Page URL contains "/checkout/review" or equivalent review step: "Reached Review"
5. Event "Checkout completed" OR "Placed order": "Completed Order"
Conversion window: 1 hour (in-session checkout completion)
Breakdown: By "device_type" attribute on the Users object (mobile checkout typically 30% lower conversion than desktop)
Compare: Previous period (prior 30 days)
For each step, also surface:
- Median and 75th-percentile time on the step page (long times suggest friction)
- Drop-off rate vs. previous period
- For users who reached but didn't pass each step: what was their last in-checkout action (helps identify the specific field/element that caused exit)
Annotations:
- Flag the step with the largest drop-off (the primary checkout bottleneck).
- Flag any step where median time-on-page exceeds 90 seconds (typically signals form complexity, validation issues, or payment-method confusion).
- Flag if mobile drop-off at any step is >15 percentage points worse than desktop (mobile-specific UX issue at that step).
- Highlight the Abandoned checkout volume in the same period: these are recoverable users; pair this report with abandoned-cart recovery.
Industry benchmarks: average ecommerce checkout completion rate is ~50%; top-quartile is 70%+. Step-level: shipping to payment typically 80%+ of the drop-off.
Use case: every ecommerce team optimizes the checkout but most see only the top-line drop-off, not the per-step diagnosis. This recipe surfaces exactly where the friction lives.
Taxonomy notes:
- Checkout created and Checkout completed are canonical (Stripe-sourced).
- Abandoned checkout (Shopify) is canonical and complementary.
- Per-step pages are derived from View page.Page URL patterns since separate canonical events for each checkout substep don't exist.
