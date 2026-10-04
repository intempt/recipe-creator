---
id: failed-payment-accounts
title: Users with a failed payment
slash_command: /failed-payment-accounts
group: Segments
owner: intempt
curator: harish
summary: Users whose payment was declined in the last two weeks, so you can recover the money before the
  subscription lapses.
description: >-
  Users with payment failure in last 14 days: dunning/recovery cohort.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
    - ecommerce
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
prerequisites:
  integrations:
    - value: stripe
      severity: blocking
touches:
  reads:
    - Your Stripe connection
    - The payment_failed, invoice_payment_failed, billing_failed and charge_failed events in your project
  writes:
    - A new segment, from step 1 "Build the failed-payment list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the failed-payment list
    summary: >-
      Users with any of payment_failed, invoice_payment_failed, billing_failed, or charge_failed in the
      last 14 days.
    builds: segment
    description: |-
      Build a segment of users named "Failed-Payment Users".
      A user is in the segment when any of these is true:
      - they did the payment_failed event at least once in the last 14 days
      - they did the invoice_payment_failed event at least once in the last 14 days
      - they did the billing_failed event at least once in the last 14 days
      - they did the charge_failed event at least once in the last 14 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Users with a failed payment

Users whose payment was declined in the last two weeks, so you can recover the money before the subscription lapses.

## Steps

1. **Build the failed-payment list** (builds segment)

   Users with any of payment_failed, invoice_payment_failed, billing_failed, or charge_failed in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- Your Stripe connection
- The payment_failed, invoice_payment_failed, billing_failed and charge_failed events in your project

Writes:

- A new segment, from step 1 "Build the failed-payment list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
