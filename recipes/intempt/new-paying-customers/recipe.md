---
id: new-paying-customers
title: New paying customers
slash_command: /new-paying-customers
group: Segments
owner: intempt
summary: Customers who started paying in the last month, the window where onboarding decides whether they
  stay.
description: >-
  First 30 days post-subscription: paid-onboarding cohort distinct from generic recently-signed-up.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
touches:
  reads:
    - The subscription_created event in your project
    - The plan_name attribute on users
  writes:
    - A new segment, from step 1 "Build the new-customer list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the new-customer list
    summary: >-
      Users who created a subscription in the last 30 days and are on a plan other than free or trial.
    builds: segment
    description: |-
      Build a segment of users named "New Paying Customers".
      A user is in the segment only when all of these are true:
      - they did the subscription_created event at least once in the last 30 days
      - their plan_name attribute is not "free"
      - their plan_name attribute is not "trial"
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# New paying customers

Customers who started paying in the last month, the window where onboarding decides whether they stay.

## Steps

1. **Build the new-customer list** (builds segment)

   Users who created a subscription in the last 30 days and are on a plan other than free or trial.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The subscription_created event in your project
- The plan_name attribute on users

Writes:

- A new segment, from step 1 "Build the new-customer list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
