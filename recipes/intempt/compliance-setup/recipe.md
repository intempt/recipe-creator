---
id: compliance-setup
title: Marketing consent suppression list
slash_command: /compliance-setup
group: Segments
owner: intempt
curator: harish
summary: A list of people who never gave marketing consent or have since opted out, so you can exclude
  them from every marketing send.
description: >-
  Build a suppression segment from consent_granted/consent_revoked events so opted-out users are excluded
  from marketing journeys.
version: 2.0.0
classification:
  product:
    - marketing
    - sales
  agent: revops-automator
  mode:
    - all
  industry:
    - ai
    - b2b-saas
    - ecommerce
    - finance
  vertical: []
  complexity: standard
  executionMode: oneshot
  tags:
    - compliance-setup
prerequisites:
  events:
    - value: consent_granted
      severity: blocking
    - value: consent_revoked
      severity: blocking
    - value: preference_updated
      severity: recommended
touches:
  reads:
    - The consent_granted and consent_revoked events in your project
  writes:
    - A new segment, from step 1 "Build the suppression list"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the suppression list
    summary: >-
      Users with no marketing consent on record, or with an active opt-out, read from your consent_granted
      and consent_revoked events. Exclude this list from every marketing journey.
    builds: segment
    description: |-
      Build a segment of users named "Marketing Consent Suppression List".
      A user is in the segment when any of these is true:
      - they have never done the consent_granted event
      - they did the consent_revoked event after their most recent consent_granted event
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Marketing consent suppression list

A list of people who never gave marketing consent or have since opted out, so you can exclude them from every marketing send.

## Steps

1. **Build the suppression list** (builds segment)

   Users with no marketing consent on record, or with an active opt-out, read from your consent_granted and consent_revoked events. Exclude this list from every marketing journey.

## What you end up with

- **segment** (segment): Segment produced by this recipe.

## What this recipe touches

Reads:

- The consent_granted and consent_revoked events in your project

Writes:

- A new segment, from step 1 "Build the suppression list"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Install now: every step builds something the engine supports today.
