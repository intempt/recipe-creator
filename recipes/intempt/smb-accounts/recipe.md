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
touches:
  reads:
    - The employees attribute on accounts
  writes:
    - A new segment, from step 1 "Build the SMB list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the SMB list
    summary: >-
      Accounts with fewer than 100 employees.
    builds: segment
    description: |-
      Build a segment of accounts named "SMB Accounts".
      An account is in the segment only when all of these are true:
      - its employees attribute is less than 100
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

## What this recipe touches

Reads:

- The employees attribute on accounts

Writes:

- A new segment, from step 1 "Build the SMB list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
