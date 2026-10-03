---
id: active-research-surge-accounts
title: Accounts researching pricing now
slash_command: /active-research-surge-accounts
group: Segments
owner: intempt
summary: Accounts whose people hit your pricing page three or more times in the past week and have no
  deal open yet, so an AE can reach out while they are still looking.
description: >-
  Accounts with 3+ pricing-page visits in last 7 days: active buying-cycle signal.
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
    title: Build the pricing-surge list
    summary: >-
      Accounts where users viewed a page whose URL contains /pricing 3 or more times in the last 7 days,
      and no deal is currently open.
    builds: segment
    description: |-
      Create a segment called "Active Research Surge Accounts".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Event (across users in account): page_viewed where page_url contains "/pricing" occurred >= 3 times in last 7 days
      - AND Attribute: has_open_deal = false
      Description: Accounts where users have visited the pricing page 3+ times in the last 7 days: the active-research-surge signal. Sharper than single-visit indicators; multi-visit pricing review within a tight window is one of the strongest predictors of an in-flight buying decision. Trigger AE personalized outreach within 24 hours.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accounts researching pricing now

Accounts whose people hit your pricing page three or more times in the past week and have no deal open yet, so an AE can reach out while they are still looking.

## Steps

1. **Build the pricing-surge list** (builds segment)

   Accounts where users viewed a page whose URL contains /pricing 3 or more times in the last 7 days, and no deal is currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
