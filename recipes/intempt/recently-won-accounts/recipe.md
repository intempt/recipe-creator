---
id: recently-won-accounts
title: Recently won accounts
slash_command: /recently-won-accounts
group: Segments
owner: intempt
curator: harish
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
  industry:
    - ai
    - b2b-saas
  vertical: []
  object: accounts
  complexity: standard
  executionMode: live
  tags:
    - accounts-segment
touches:
  reads:
    - The lifecycle_changed_at, account_lifecycle and has_open_deal attributes on accounts
  writes:
    - A new segment, from step 1 "Build the recently-won list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the recently-won list
    summary: >-
      Accounts whose lifecycle changed to customer within the last 90 days, with no deal currently open.
    builds: segment
    description: |-
      Build a segment of accounts named "Recently-Won Accounts".
      An account is in the segment only when all of these are true:
      - its lifecycle_changed_at attribute is within the last 90 days
      - its account_lifecycle attribute is "customer"
      - its has_open_deal attribute is false
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

## What this recipe touches

Reads:

- The lifecycle_changed_at, account_lifecycle and has_open_deal attributes on accounts

Writes:

- A new segment, from step 1 "Build the recently-won list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
