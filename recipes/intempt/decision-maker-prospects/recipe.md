---
id: decision-maker-prospects
title: Decision makers checking pricing
slash_command: /decision-maker-prospects
group: Segments
owner: intempt
curator: harish
summary: Senior people who looked at your pricing in the last month, so AEs can talk to whoever actually
  holds the budget.
description: >-
  Senior-title users (C-level, VP, Director) showing intent: priority routing for AE outreach.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - b2b
    - saas
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
touches:
  reads:
    - The page_viewed event in your project
    - The page_url property on those events
    - The title and email attributes on users
  writes:
    - A new segment, from step 1 "Build the decision-maker list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the decision-maker list
    summary: >-
      Users whose title contains CEO, CTO, CFO, CMO, COO, VP, Vice President, Director, Head of, or Chief,
      who viewed a /pricing page in the last 30 days and have an email on file.
    builds: segment
    description: |-
      Build a segment of users named "Decision-Maker Prospects".
      A user is in the segment only when all of these are true:
      - their title attribute contains any of "CEO", "CTO", "CFO", "CMO", "COO", "VP", "Vice President", "Director", "Head of" or "Chief"
      - they did the page_viewed event with a page_url that contains "/pricing" at least once in the last 30 days
      - their email attribute is not empty
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Decision makers checking pricing

Senior people who looked at your pricing in the last month, so AEs can talk to whoever actually holds the budget.

## Steps

1. **Build the decision-maker list** (builds segment)

   Users whose title contains CEO, CTO, CFO, CMO, COO, VP, Vice President, Director, Head of, or Chief, who viewed a /pricing page in the last 30 days and have an email on file.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The page_viewed event in your project
- The page_url property on those events
- The title and email attributes on users

Writes:

- A new segment, from step 1 "Build the decision-maker list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
