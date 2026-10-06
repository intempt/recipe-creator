---
id: acquisition-channel-cohort
title: Customers by acquisition channel
slash_command: /acquisition-channel-cohort
group: Segments
owner: intempt
curator: harish
summary: Customers grouped by the channel that brought them in, so you can compare how well each channel's
  buyers stick around.
description: >-
  Customers acquired through a specific channel (parameterized by utm_source/medium): for channel-quality
  analysis.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - ecommerce
    - saas
  industry:
    - ai
    - b2b-saas
    - ecommerce
  vertical: []
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
inputs:
  - input: Channel
    what_the_installer_supplies: One utm_source and utm_medium pair, for example facebook and cpc
    if_missing: google and cpc are used. To compare channels, install once per pair and change the segment
      name and both values.
touches:
  reads:
    - The order_created event in your project
    - The utm_source and utm_medium attributes on users
    - The channel you supply when you run it
  writes:
    - A new segment, from step 1 "Build the channel cohort"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the channel cohort
    summary: >-
      Users matching one utm_source and utm_medium pair (for example google and cpc) who have placed at
      least one order. Build one cohort per channel you want to compare.
    builds: segment
    description: |-
      Build a segment of users named "Google Paid Acquired".
      A user is in the segment only when all of these are true:
      - their utm_source attribute is "google"
      - their utm_medium attribute is "cpc"
      - they did the order_created event at least once, at any time
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Customers by acquisition channel

Customers grouped by the channel that brought them in, so you can compare how well each channel's buyers stick around.

## Steps

1. **Build the channel cohort** (builds segment)

   Users matching one utm_source and utm_medium pair (for example google and cpc) who have placed at least one order. Build one cohort per channel you want to compare.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The order_created event in your project
- The utm_source and utm_medium attributes on users
- The channel you supply when you run it

Writes:

- A new segment, from step 1 "Build the channel cohort"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Channel | One utm_source and utm_medium pair, for example facebook and cpc | google and cpc are used. To compare channels, install once per pair and change the segment name and both values. |

## Availability

Install now: every step builds something the engine supports today.
