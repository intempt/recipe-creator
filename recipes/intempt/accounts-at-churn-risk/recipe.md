---
id: accounts-at-churn-risk
title: Accounts at churn risk
slash_command: /accounts-at-churn-risk
group: Segments
owner: intempt
summary: Paying accounts the health score has flagged as at risk, with no renewal deal in flight, so your
  CSMs can step in before they leave.
description: >-
  Active accounts showing health deterioration: CSM intervention needed.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - b2b
    - saas
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
steps:
  - id: s1
    title: Build the at-risk account list
    summary: >-
      Accounts with a health score of at risk, lifetime value above zero, at least one user, and no renewal
      deal open. Updates as account health changes.
    builds: segment
    description: |-
      Create a segment called "Accounts At Churn Risk".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: account_health = "at_risk"
      - AND Attribute: has_renewal_deal = false
      - AND Attribute: account_lifetime_value > 0
      - AND Attribute: users_count >= 1
      Description: Active accounts flagged at-risk by the platform's health-scoring with positive lifetime value (proven paid customer) and no active renewal deal in flight. CSM intervention priority: these are recoverable churn risks where someone has paid before and isn't currently in renewal motion.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accounts at churn risk

Paying accounts the health score has flagged as at risk, with no renewal deal in flight, so your CSMs can step in before they leave.

## Steps

1. **Build the at-risk account list** (builds segment)

   Accounts with a health score of at risk, lifetime value above zero, at least one user, and no renewal deal open. Updates as account health changes.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
