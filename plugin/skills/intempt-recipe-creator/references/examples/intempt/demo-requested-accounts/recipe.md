---
id: demo-requested-accounts
title: Accounts that asked for a demo
slash_command: /demo-requested-accounts
group: Segments
owner: intempt
curator: harish
summary: >-
  People who submitted a demo form in the last 30 days, so an SDR can follow up the same hour.
description: >-
  People whose own demo form submission happened in the last 30 days: top SDR-routing priority.
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
inputs:
  - input: Demo request form
    what_the_installer_supplies: The form people fill in to request a demo
    if_missing: The step is marked vague and waits until one is chosen.
touches:
  reads:
    - The submit_on event in your project
    - The has_open_deal attribute on accounts
    - The demo request form you supply when you run it
  writes:
    - A new segment, from step 1 "Build the demo-request list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the demo-request list
    summary: >-
      Accounts where any user submitted a demo request form at least once in the last 30 days, and no
      deal is currently open.
    builds: segment
    description: |-
      Build a segment of accounts named "Demo-Requested Accounts".
      An account is in the segment only when all of these are true:
      - the users in the account together did the submit_on event on the demo request form chosen for this run at least once in the last 30 days
      - its has_open_deal attribute is false
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accounts that asked for a demo

People who submitted a demo form in the last 30 days, so an SDR can follow up the same hour.

## Steps

1. **Build the demo-request list** (builds segment)

   Accounts where any user submitted a demo request form at least once in the last 30 days, and no deal is currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.

## What this recipe touches

Reads:

- The submit_on event in your project
- The has_open_deal attribute on accounts
- The demo request form you supply when you run it

Writes:

- A new segment, from step 1 "Build the demo-request list"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Demo request form | The form people fill in to request a demo | The step is marked vague and waits until one is chosen. |

## Availability

Install now: every step builds something the engine supports today.
