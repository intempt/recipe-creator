---
id: recently-won-accounts
title: Recently won accounts
slash_command: /recently-won-accounts
group: Segments
owner: intempt
summary: Accounts that became customers in the last quarter, so onboarding and implementation start from
  one current list.
description: >-
  Accounts that closed a deal in last 90 days: onboarding cohort distinct from new-paying-customers.
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
    title: Build the recently-won list
    summary: >-
      Accounts whose lifecycle changed to customer within the last 90 days, with no deal currently open.
    builds: segment
    description: |-
      Create a segment called "Recently-Won Accounts".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: lifecycle_changed_at is within last 90 days
      - AND Attribute: account_lifecycle is "customer"
      - AND Attribute: has_open_deal = false
      Description: Accounts that became customers in the last 90 days: the post-deal-close onboarding cohort. Distinct from new-paying-customers (which is plan-tier-conversion at the User level). For B2B sales motion, the deal-close moment is the kickoff for CSM onboarding, implementation milestones, and time-to-value tracking.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Recently won accounts

Accounts that became customers in the last quarter, so onboarding and implementation start from one current list.

## Steps

1. **Build the recently-won list** (builds segment)

   Accounts whose lifecycle changed to customer within the last 90 days, with no deal currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
