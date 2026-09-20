---
name: compliance-setup
description: |
  Use when a user mentions "marketing consent suppression", "GDPR exclusion segment", or asks for related help. Build a suppression segment from consent_granted/consent_revoked events so opted-out users are excluded from marketing journeys.
arguments: []
intempt:
  id: compliance-setup
  version: 1.0.1
  slashCommand: /compliance-setup
  group: Segments
  title: 'Marketing consent suppression list'
  shortDescription: 'A list of people who never gave marketing consent or have since opted out, so you can exclude them from every marketing send.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing, sales]
    agent: revops-automator
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [compliance-setup]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: consent_granted, severity: blocking }  # Required for suppression-segment logic
      - { value: consent_revoked, severity: blocking }  # Required for suppression-segment logic
      - { value: preference_updated, severity: recommended }  # Preference center updates
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the suppression list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with no marketing consent on record, or with an active opt-out, read from your consent_granted and consent_revoked events. Exclude this list from every marketing journey.'
      prompt: "Build a suppression segment of users without marketing consent or with active opt-outs."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Marketing consent suppression list

A list of people who never gave marketing consent or have since opted out, so you can exclude them from every marketing send.

## Before you run it

- Send the `consent_granted` event
- Send the `consent_revoked` event
- Send the `preference_updated` event

## What it does

1. **Build the suppression list** (`create_segment`)

   Users with no marketing consent on record, or with an active opt-out, read from your consent_granted and consent_revoked events. Exclude this list from every marketing journey.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
