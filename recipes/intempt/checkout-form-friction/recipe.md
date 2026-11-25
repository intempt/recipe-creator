---
frontmatter_id: checkout-form-friction
slash_command: /checkout-form-friction
description: Emails a weekly digest of which checkout step loses you orders, how long shoppers sit on each one, and where
  mobile is worse than desktop.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of which checkout step loses the most orders, how long shoppers spend on each step, and
    where mobile drop-off is worse than desktop.
  parameters:
  - name: conversionWindow
    type: duration
    label: Time allowed from checkout start to order
    default: 1 h
    required: false
  - name: comparisonPeriod
    type: duration
    label: Window analyzed and compared with the one before
    default: 7 d
    required: false
  - name: timeThreshold
    type: number
    label: Median seconds on a step that are flagged
    default: 90
    required: false
  - name: mobileGapThreshold
    type: number
    label: Mobile drop-off gap over desktop that is flagged (points)
    default: 15
    required: false
  - name: shippingPathPattern
    type: string
    label: Shipping step URL contains
    default: /checkout/shipping
    required: false
  - name: paymentPathPattern
    type: string
    label: Payment step URL contains
    default: /checkout/payment
    required: false
  - name: reviewPathPattern
    type: string
    label: Review step URL contains
    default: /checkout/review
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
      meaning: URL of the viewed page
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
    builds: automation
    uses:
    - checkout_started_event
    - checkout_completed_event
    - page_view_event
    - device_type_attribute
    - abandoned_checkout_event
    - conversionWindow
    - comparisonPeriod
    - timeThreshold
    - mobileGapThreshold
    - shippingPathPattern
    - paymentPathPattern
    - reviewPathPattern
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes customers who did
      {checkout_started_event} in the last {comparisonPeriod} and in the {comparisonPeriod} before, through these steps in
      order within {conversionWindow}: {page_view_event} with {page_view_event.page_url} containing {shippingPathPattern};
      then containing {paymentPathPattern}; then containing {reviewPathPattern}; then {checkout_completed_event}. It writes
      these figures for both windows: customers at each step and drop-off % from the step before, overall and per {device_type_attribute};
      median and 75th percentile seconds on each step''s page; the count of {abandoned_checkout_event}. The first lines name
      the step with the largest drop-off, any step whose median time is over {timeThreshold} seconds, and any step where mobile
      drop-off is more than {mobileGapThreshold} points above desktop. Then it emails these figures as plain-text lines, each
      with its window, to {digest_recipients}. Nothing else is sent.'
---

# Checkout friction

Slash command: /checkout-form-friction

## Step 1: Email the weekly checkout friction digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes customers who did checkout started event in the last 7 d and in the 7 d before, through these steps in order within 1 h: page view event with page url containing /checkout/shipping; then containing /checkout/payment; then containing /checkout/review; then checkout completed event. It writes these figures for both windows: customers at each step and drop-off % from the step before, overall and per device type attribute; median and 75th percentile seconds on each step's page; the count of abandoned checkout event. The first lines name the step with the largest drop-off, any step whose median time is over 90 seconds, and any step where mobile drop-off is more than 15 points above desktop. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
