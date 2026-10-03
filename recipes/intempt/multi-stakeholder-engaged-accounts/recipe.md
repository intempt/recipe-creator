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
steps:
  - id: s1
    title: Build the multi-stakeholder list
    summary: >-
      Accounts with 3 or more users, plus 5 or more sessions and 10 or more page views across those users
      in the last 14 days.
    builds: segment
    description: |-
      Create a segment called "Multi-Stakeholder Engaged Accounts".
      Object: Accounts
      Rules (all conditions joined by AND):
      - Attribute: users_count >= 3
      - AND Event (across users in account): session_start occurred >= 5 times in last 14 days
      - AND Event (across users in account): page_viewed occurred >= 10 times in last 14 days
      Description: Accounts where 3+ users have been actively engaged in the last 14 days. The buying-committee signal: Salesforce reports B2B deals now involve an average of 11 stakeholders, so multi-user engagement at the account level is one of the strongest forward-looking indicators of an active buying cycle. Foundation for AE multi-threading plays and ABM coordination.
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

## Availability

Install now: every step builds something the engine supports today.
