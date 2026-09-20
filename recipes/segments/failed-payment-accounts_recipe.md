---
name: failed-payment-accounts
description: |
  Use when a user mentions "failed-payment users", or asks for related help. Users with payment failure in last 14 days: dunning/recovery cohort.
arguments: []
intempt:
  id: failed-payment-accounts
  version: 1.0.0
  slashCommand: /failed-payment-accounts
  group: Segments
  title: 'Users with a failed payment'
  shortDescription: 'Users whose payment was declined in the last two weeks, so you can recover the money before the subscription lapses.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas, ecommerce]
    object: users
    complexity: standard
    executionMode: live
    tags: [users-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: stripe, severity: blocking }
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the failed-payment list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with any of payment_failed, invoice_payment_failed, billing_failed, or charge_failed in the last 14 days.'
      prompt: |
        Create a segment called "Failed-Payment Users".

        Object: Users

        Rules (any condition matches: joined by OR):
        - Event: payment_failed occurred >= 1 time in last 14 days
        - OR Event: invoice_payment_failed occurred >= 1 time in last 14 days
        - OR Event: billing_failed occurred >= 1 time in last 14 days
        - OR Event: charge_failed occurred >= 1 time in last 14 days

        Description: Users with one or more payment failures in the last 14 days. Dunning-recovery cohort with the highest immediate-revenue ROI of any segment. Trigger an automated card-update email sequence; for high-LTV failures, escalate to manual CSM/AE outreach with a personal touch.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Users with a failed payment

Users whose payment was declined in the last two weeks, so you can recover the money before the subscription lapses.

## Before you run it

- Connect stripe

## What it does

1. **Build the failed-payment list** (`create_segment`)

   Users with any of payment_failed, invoice_payment_failed, billing_failed, or charge_failed in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
