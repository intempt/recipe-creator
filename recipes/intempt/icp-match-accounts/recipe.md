---
id: icp-match-accounts
title: Accounts matching your ICP
slash_command: /icp-match-accounts
group: Segments
owner: intempt
summary: Accounts that fit your ideal customer profile on size, industry, and country, as the base list
  for account-based targeting.
description: >-
  Accounts matching ideal customer profile by company size, industry, and geography.
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
    title: Build the ICP list
    summary: >-
      Accounts with 50 to 500 employees in SaaS, Technology, or Financial Services, based in the US, UK,
      Canada, or Australia.
    builds: segment
    description: |-
      Create a segment called "ICP Match Accounts".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: employees is between 50 and 500
      - AND Attribute: industry is one of ["SaaS", "Technology", "Financial Services"]
      - AND Attribute: country is one of ["US", "UK", "CA", "AU"]
      Description: Accounts matching the ideal customer profile by size, industry, and geography. Foundation segment for ABM targeting.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accounts matching your ICP

Accounts that fit your ideal customer profile on size, industry, and country, as the base list for account-based targeting.

## Steps

1. **Build the ICP list** (builds segment)

   Accounts with 50 to 500 employees in SaaS, Technology, or Financial Services, based in the US, UK, Canada, or Australia.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
