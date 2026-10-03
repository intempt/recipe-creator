---
id: renewal-window-90-day
title: Renewals due in 90 days
slash_command: /renewal-window-90-day
group: Segments
owner: intempt
summary: Paid subscriptions that end within the next three months, so renewal conversations start early
  instead of the week before.
description: >-
  Subscriptions ending in next 90 days) foundation for renewal-flow journeys and NRR plays.
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
    title: Build the renewal list
    summary: >-
      Users on a paid plan whose subscription end date falls within the next 90 days and is still in the
      future.
    builds: segment
    description: |-
      Create a segment called "Renewal Window: 90 Days".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: end_date is within next 90 days
      - AND Attribute: end_date is in the future
      - AND Attribute: plan_name is not "free"
      Description: Users with active paid subscriptions ending in the next 90 days. The renewal-targeting cohort: foundation for QBR-style ROI emails, renewal-conversation triggers, and NRR-driven CSM outreach. NRR is the single most important SaaS metric in 2026; this segment makes the renewal pipeline actionable.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Renewals due in 90 days

Paid subscriptions that end within the next three months, so renewal conversations start early instead of the week before.

## Steps

1. **Build the renewal list** (builds segment)

   Users on a paid plan whose subscription end date falls within the next 90 days and is still in the future.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
