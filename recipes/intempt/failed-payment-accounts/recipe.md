---
id: failed-payment-accounts
title: Users with a failed payment
slash_command: /failed-payment-accounts
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the failed-payment list
    summary: >-
      Users with any of payment_failed, invoice_payment_failed, billing_failed, or charge_failed in the
      last 14 days.
    builds: segment
    description: |-
      Create a segment called "Failed-Payment Users".
      Object: Users
      Rules (any condition matches: joined by OR):
      - Event: payment_failed occurred >= 1 time in last 14 days
      - OR Event: invoice_payment_failed occurred >= 1 time in last 14 days
      - OR Event: billing_failed occurred >= 1 time in last 14 days
      - OR Event: charge_failed occurred >= 1 time in last 14 days
      Description: Users with one or more payment failures in the last 14 days. Dunning-recovery cohort with the highest immediate-revenue ROI of any segment. Trigger an automated card-update email sequence; for high-LTV failures, escalate to manual CSM/AE outreach with a personal touch.
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

## Availability

Install now: every step builds something the engine supports today.
