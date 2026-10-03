---
id: recently-signed-up-users
title: Recent signups
slash_command: /recently-signed-up-users
group: Segments
owner: intempt
summary: Everyone who created an account in the last month, the audience for your welcome and first-week
  activation emails.
description: >-
  Users who created an account in the last 30 days: onboarding cohort.
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
steps:
  - id: s1
    title: Build the new signup list
    summary: >-
      Users first seen in the last 30 days.
    builds: segment
    description: |-
      Create a segment called "Recently Signed-Up Users".
      Object: Users
      Rules:
      - Attribute: first_seen_at is within last 30 days
      Description: Onboarding cohort. Use as the audience for first-week activation campaigns, welcome journeys, and onboarding email sequences.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Recent signups

Everyone who created an account in the last month, the audience for your welcome and first-week activation emails.

## Steps

1. **Build the new signup list** (builds segment)

   Users first seen in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
