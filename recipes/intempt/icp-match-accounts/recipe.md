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
touches:
  reads:
    - The employees, industry and country attributes on accounts
  writes:
    - A new segment, from step 1 "Build the ICP list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the ICP list
    summary: >-
      Accounts with 50 to 500 employees in SaaS, Technology, or Financial Services, based in the US, UK,
      Canada, or Australia.
    builds: segment
    description: |-
      Build a segment of accounts named "ICP Match Accounts".
      An account is in the segment only when all of these are true:
      - its employees attribute is between 50 and 500
      - its industry attribute is one of "SaaS", "Technology" or "Financial Services"
      - its country attribute is one of "US", "UK", "CA" or "AU"
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

## What this recipe touches

Reads:

- The employees, industry and country attributes on accounts

Writes:

- A new segment, from step 1 "Build the ICP list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
