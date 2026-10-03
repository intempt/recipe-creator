---
id: smb-accounts
title: Small business accounts
slash_command: /smb-accounts
group: Segments
owner: intempt
summary: Companies under 100 employees, the list your self-serve nurture and in-product prompts should
  run against.
description: >-
  Small businesses (under 100 employees): self-serve / low-touch routing.
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
    title: Build the SMB list
    summary: >-
      Accounts with fewer than 100 employees.
    builds: segment
    description: |-
      Create a segment called "SMB Accounts".
      Object: Accounts
      Rules:
      - Attribute: employees < 100
      Description: Small businesses with under 100 employees. Foundation for self-serve / low-touch routing: these accounts go through automated nurture flows, in-product upgrade prompts, and minimal direct sales engagement. The PLG sweet spot.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Small business accounts

Companies under 100 employees, the list your self-serve nurture and in-product prompts should run against.

## Steps

1. **Build the SMB list** (builds segment)

   Accounts with fewer than 100 employees.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
