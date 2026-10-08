---
id: accounts-at-churn-risk
title: Accounts at churn risk
slash_command: /accounts-at-churn-risk
group: Segments
owner: intempt
curator: harish
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
  industry:
    - ai
    - b2b-saas
    - finance
    - media
  vertical: []
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
touches:
  reads:
    - The account_health, has_renewal_deal, account_lifetime_value and users_count attributes on accounts
  writes:
    - A new segment, from step 1 "Build the at-risk account list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the at-risk account list
    summary: >-
      Accounts with a health score of at risk, lifetime value above zero, at least one user, and no renewal
      deal open. Updates as account health changes.
    builds: segment
    description: |-
      Build a segment of accounts named "Accounts At Churn Risk".
      An account is in the segment only when all of these are true:
      - its account_health attribute is "at_risk"
      - its has_renewal_deal attribute is false
      - its account_lifetime_value attribute is more than 0
      - its users_count attribute is 1 or more
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

## What this recipe touches

Reads:

- The account_health, has_renewal_deal, account_lifetime_value and users_count attributes on accounts

Writes:

- A new segment, from step 1 "Build the at-risk account list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
