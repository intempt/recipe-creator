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
steps:
  - id: s1
    title: Build the new-customer list
    summary: >-
      Users who created a subscription in the last 30 days and are on a plan other than free or trial.
    builds: segment
    description: |-
      Create a segment called "New Paying Customers".
      Object: Users
      Rules (all conditions joined by AND):
      - Event: subscription_created occurred >= 1 time in last 30 days
      - AND Attribute: plan_name is not "free"
      - AND Attribute: plan_name is not "trial"
      Description: Users who converted to a paid plan in the last 30 days. The paid-onboarding cohort: distinct from recently-signed-up-users (which is account creation). The first 30 days post-paid-conversion is the highest-leverage retention window; trigger CSM kickoff, premium-feature discovery, and ROI-tracking content.
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

## Availability

Install now: every step builds something the engine supports today.
