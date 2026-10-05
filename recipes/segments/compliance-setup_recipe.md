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
  shortDescription: "Create a suppression segment of users whose latest consent_revoked event supersedes consent_granted, for exclusion from marketing journeys."
  availability: available
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
      title: "Build Suppression Segment"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Build a suppression segment of users without marketing consent or with active opt-outs."
      prompt: "Build a suppression segment of users without marketing consent or with active opt-outs."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
---

# Compliance & Privacy Setup

## Procedure

1. **Build Suppression Segment** [`create_segment`] — Build a suppression segment of users without marketing consent or with active opt-outs. → produces: segment
