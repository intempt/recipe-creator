---
id: multi-stakeholder-engaged-accounts
title: Accounts with a buying group active
slash_command: /multi-stakeholder-engaged-accounts
group: Segments
owner: intempt
summary: Accounts where three or more people have been using the product in the last two weeks, usually
  the sign a buying group has formed.
description: >-
  Accounts where 3+ users have been active in last 14 days: buying-committee signal for B2B.
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
    - The session_start and page_viewed events in your project
    - The users_count attribute on accounts
  writes:
    - A new segment, from step 1 "Build the multi-stakeholder list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the multi-stakeholder list
    summary: >-
      Accounts with 3 or more users, plus 5 or more sessions and 10 or more page views across those users
      in the last 14 days.
    builds: segment
    description: |-
      Build a segment of accounts named "Multi-Stakeholder Engaged Accounts".
      An account is in the segment only when all of these are true:
      - its users_count attribute is 3 or more
      - the users in the account together did the session_start event 5 or more times in the last 14 days
      - the users in the account together did the page_viewed event 10 or more times in the last 14 days
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accounts with a buying group active

Accounts where three or more people have been using the product in the last two weeks, usually the sign a buying group has formed.

## Steps

1. **Build the multi-stakeholder list** (builds segment)

   Accounts with 3 or more users, plus 5 or more sessions and 10 or more page views across those users in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The session_start and page_viewed events in your project
- The users_count attribute on accounts

Writes:

- A new segment, from step 1 "Build the multi-stakeholder list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
