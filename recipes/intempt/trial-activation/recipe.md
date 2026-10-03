---
id: trial-activation
title: Trial to paid activation
slash_command: /trial-activation
group: Journeys
owner: intempt
summary: Scores how well each trial is going and sends different onboarding to the ones racing ahead,
  the ones drifting, and the ones at risk.
description: >-
  Drive trial users to paid conversion via scoring, segmentation, onboarding journey, and funnel measurement.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - trial-activation
steps:
  - id: s1
    title: Score how the trial is going
    summary: >-
      A trial health score from logins, use of the key features, team invites and data uploaded.
    builds: attribute
    description: >-
      Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature
      usage, team invites, data uploaded).
  - id: s2
    title: Split trials into three tiers
    summary: >-
      Highly engaged, moderate and at risk, off that score.
    builds: segment
    description: >-
      Segment trial users into risk tiers (high-engagement, moderate, at-risk) based on trial_health_score.
      Use the result of "Score how the trial is going".
    dependsOn:
      - s1
  - id: s3
    title: Write onboarding per tier
    summary: >-
      Content for each tier, leading with the features most likely to get that tier to its first real
      win.
    builds: email_html
    description: >-
      Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier.
      Use the result of "Score how the trial is going", "Split trials into three tiers".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Route each tier differently
    summary: >-
      One journey with a branch per tier, each running the education and conversion touches that tier
      needs.
    builds: journey
    description: >-
      Build a tiered onboarding journey routing each tier through appropriate education and conversion
      touches. Use the result of "Score how the trial is going", "Split trials into three tiers", "Write
      onboarding per tier".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Track trial to paid
    summary: >-
      A funnel from signup to the first key event, then the second, then paid conversion, with retention
      laid over it.
    builds: report
    description: >-
      Compose a funnel report tracking trial-signup to key-event-1 to key-event-2 to paid-conversion with
      retention overlay. Use the result of "Score how the trial is going", "Split trials into three tiers",
      "Write onboarding per tier", "Route each tier differently".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s3
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s4
    type: journey
    description: Journey produced by this recipe.
  - key: report
    producedByStep: s5
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Trial to paid activation

Scores how well each trial is going and sends different onboarding to the ones racing ahead, the ones drifting, and the ones at risk.

## Steps

1. **Score how the trial is going** (builds attribute)

   A trial health score from logins, use of the key features, team invites and data uploaded.

2. **Split trials into three tiers** (builds segment)

   Highly engaged, moderate and at risk, off that score.

3. **Write onboarding per tier** (builds email_html)

   Content for each tier, leading with the features most likely to get that tier to its first real win.

4. **Route each tier differently** (builds journey)

   One journey with a branch per tier, each running the education and conversion touches that tier needs.

5. **Track trial to paid** (builds report)

   A funnel from signup to the first key event, then the second, then paid conversion, with retention laid over it.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build journey, report.
