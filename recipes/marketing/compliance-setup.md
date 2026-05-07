---
name: Compliance Setup
description: GDPR/CAN-SPAM audit, consent capture, exclusion segmentation.
intempt:
  id: compliance-setup
  version: 1.0.1
  slashCommand: /compliance-setup
  shortDescription: GDPR/CAN-SPAM audit, consent capture, exclusion segmentation.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    - sales
    agent: revops-automator
    mode:
    - all
    complexity: standard
    executionMode: oneshot
    tags:
    - compliance-setup
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: event_mapping
    type: event-mapping
    description: Event Mapping produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: define-consent-events
    describe: Define consent_granted, consent_revoked, and preference_updated events with required attributes.
    produces: event_mapping
---

# Compliance Setup

GDPR/CAN-SPAM audit, consent capture, exclusion segmentation.

## Outputs

- **event_mapping** (event-mapping): Event Mapping produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Define consent_granted, consent_revoked, and preference_updated events with required attributes.
