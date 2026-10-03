---
id: decision-maker-prospects
title: Decision makers checking pricing
slash_command: /decision-maker-prospects
group: Segments
owner: intempt
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
steps:
  - id: s1
    title: Build the decision-maker list
    summary: >-
      Users whose title contains CEO, CTO, CFO, CMO, COO, VP, Vice President, Director, Head of, or Chief,
      who viewed a /pricing page in the last 30 days and have an email on file.
    builds: segment
    description: |-
      Create a segment called "Decision-Maker Prospects".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: title contains any of ["CEO", "CTO", "CFO", "CMO", "COO", "VP", "Vice President", "Director", "Head of", "Chief"]
      - AND Event: page_viewed where page_url contains "/pricing" occurred >= 1 time in last 30 days
      - AND Attribute: email is not empty
      Description: Senior-title users (C-level, VP, Director) who have visited pricing in the last 30 days. The economic-buyer signal: these are budget-holders actively researching. Highest priority for AE-led outreach, executive-sponsor engagement, and ROI-focused content delivery.
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

## Availability

Install now: every step builds something the engine supports today.
