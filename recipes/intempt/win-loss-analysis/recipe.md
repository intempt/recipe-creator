---
id: win-loss-analysis
title: Win/loss patterns from closed deals
slash_command: /win-loss-analysis
group: Dashboards
owner: intempt
curator: sid
summary: Reads your closed deals to show which competitors, objections and decision criteria separate
  the ones you win from the ones you lose.
description: >-
  Patterns across won vs lost deals: competitive intelligence, objection themes, battlecard.
version: 2.0.0
classification:
  product:
    - sales
    - analytics
  agent: meeting-notetaker
  mode:
    - b2b
  complexity: standard
  executionMode: oneshot
  tags:
    - win-loss-analysis
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Compare won and lost deals"
    - A new landing page, from step 2 "Write the battlecard"
    - A new dashboard, from step 3 "Track the patterns over time"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Compare won and lost deals
    summary: >-
      Closed-won and closed-lost deals read side by side for competitor mentions, objection themes and
      the decision criteria buyers stated.
    builds: report
    description: >-
      Analyze closed deals (won and lost) to extract patterns: competitive mentions, objection themes,
      decision criteria.
  - id: s2
    title: Write the battlecard
    summary: >-
      A one-page battlecard with competitive positioning, the objections that come up most, and the responses
      that work.
    builds: page
    description: >-
      Generate a battlecard content asset summarizing competitive positioning, common objections, and
      counter-messaging. Use the result of "Compare won and lost deals".
    dependsOn:
      - s1
  - id: s3
    title: Track the patterns over time
    summary: >-
      Win and loss rates split by competitor, objection type and deal size.
    builds: dashboard
    description: >-
      Compose a dashboard surfacing win/loss patterns by competitor, objection type, and deal size. Use
      the result of "Compare won and lost deals", "Write the battlecard".
    dependsOn:
      - s1
      - s2
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Win/loss patterns from closed deals

Reads your closed deals to show which competitors, objections and decision criteria separate the ones you win from the ones you lose.

## Steps

1. **Compare won and lost deals** (builds report)

   Closed-won and closed-lost deals read side by side for competitor mentions, objection themes and the decision criteria buyers stated.

2. **Write the battlecard** (builds page)

   A one-page battlecard with competitive positioning, the objections that come up most, and the responses that work.

3. **Track the patterns over time** (builds dashboard)

   Win and loss rates split by competitor, objection type and deal size.

## What you end up with

- **report** (report): Report produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Compare won and lost deals"
- A new landing page, from step 2 "Write the battlecard"
- A new dashboard, from step 3 "Track the patterns over time"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, page, report.
