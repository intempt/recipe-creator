---
id: paths-around-power-feature
title: Paths around a key feature
slash_command: /paths-around-power-feature
group: Reports
owner: intempt
summary: Shows what leads people to your most valuable feature and what they do straight after using it.
description: >-
  Bidirectional path bracketing a high-value feature interaction: surfaces what leads to discovery and
  what users do after.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: quick
  executionMode: live
  tags:
    - path
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Look before and after a feature"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Look before and after a feature
    summary: >-
      Two paths bracketing one feature click over the last 30 days: 5 steps back inside the preceding
      30 minutes and 5 steps forward inside the following 30 minutes, split by plan, with the share of
      users for whom this was a first use.
    builds: report
    description: |-
      Create a Path report called "Paths Around a Power Feature".
      This is a TWO-PATH report (forward and backward) bracketing a configurable target feature, identified by click_on.target_id.
      Path A: Backward (what leads users to the feature):
      - Anchor event: click_on where target_id matches the target feature pattern
      - Direction: backward
      - Depth: 5 steps backward
      - Window: 30 minutes before the feature interaction
      - Loop compression: on
      Path B: Forward (what users do after using the feature):
      - Anchor event: same click_on
      - Direction: forward
      - Depth: 5 steps forward
      - Window: 30 minutes after the feature interaction
      - Loop compression: on
      Time range: Last 30 days
      Breakdown: By plan_name (resolved from each user's most-recent active subscription_created.plan_name)
      Surface for both paths:
      - The top 10 most-common precursor paths (Path A) and follow-on paths (Path B)
      - The % of users who arrived via each path (intentional discovery vs. accidental)
      - The % of users for whom this was their FIRST interaction with the feature in the trailing 90 days
      Annotations:
      - Path A: flag if the dominant precursor is "page_viewed on /help" or "click_on a tooltip" (feature is being discovered through help, not natural workflow: discoverability issue).
      - Path A: flag if the dominant precursor is from settings/admin (advanced feature only used by admins, not the broader user base).
      - Path B (flag if the dominant follow-on is session_end (users disengage after using the feature) signals confusion or completion of a single task, not workflow integration).
      - Path B: flag if the feature leads to repeated use of itself within session (sticky / habit-forming pattern).
      Use case: when prioritizing investment in a feature, knowing how users arrive at it AND what they do after reveals whether the feature is well-positioned in the product workflow or sits in isolation. The KISSmetrics product analytics literature flags this as one of the most-overlooked path use cases.
      Taxonomy notes:
      - click_on is canonical with target_id, target_text, hierarchy, path properties.
      - session_end is the canonical session-disengagement marker.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Paths around a key feature

Shows what leads people to your most valuable feature and what they do straight after using it.

## Steps

1. **Look before and after a feature** (builds report)

   Two paths bracketing one feature click over the last 30 days: 5 steps back inside the preceding 30 minutes and 5 steps forward inside the following 30 minutes, split by plan, with the share of users for whom this was a first use.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Look before and after a feature"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
