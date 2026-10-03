---
id: demo-requested-accounts
title: Accounts that asked for a demo
slash_command: /demo-requested-accounts
group: Segments
owner: intempt
summary: Accounts where somebody filled in your demo form in the last month and no deal is open yet, so
  an SDR can call them back the same hour.
description: >-
  Accounts where any user submitted a demo form in last 30 days: top SDR-routing priority.
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
    title: Build the demo-request list
    summary: >-
      Accounts where any user submitted a demo request form at least once in the last 30 days, and no
      deal is currently open.
    builds: segment
    description: |-
      Create a segment called "Demo-Requested Accounts".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Event (across users in account): submit_on a demo-request form occurred >= 1 time in last 30 days
      - AND Attribute: has_open_deal = false
      Description: Accounts where any user submitted a demo-request form in the last 30 days, with no existing open deal. Highest SDR-routing priority: research consistently shows 53% conversion rate for 1-hour response vs 17% after 24 hours. SLA: SDR contact within 1 hour, AE follow-up within 24 hours.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accounts that asked for a demo

Accounts where somebody filled in your demo form in the last month and no deal is open yet, so an SDR can call them back the same hour.

## Steps

1. **Build the demo-request list** (builds segment)

   Accounts where any user submitted a demo request form at least once in the last 30 days, and no deal is currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
