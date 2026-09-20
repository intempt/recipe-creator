---
name: accounts-at-churn-risk
description: |
  Use when a user mentions "accounts at churn risk", or asks for related help. Active accounts showing health deterioration: CSM intervention needed.
arguments: []
intempt:
  id: accounts-at-churn-risk
  version: 1.0.1
  slashCommand: /accounts-at-churn-risk
  group: Segments
  title: 'Accounts at churn risk'
  shortDescription: 'Paying accounts the health score has flagged as at risk, with no renewal deal in flight, so your CSMs can step in before they leave.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [b2b, saas]
    object: accounts
    complexity: standard
    executionMode: live
    tags: [accounts-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the at-risk account list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with a health score of at risk, lifetime value above zero, at least one user, and no renewal deal open. Updates as account health changes.'
      prompt: |
        Create a segment called "Accounts At Churn Risk".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: account_health = "at_risk"
        - AND Attribute: has_renewal_deal = false
        - AND Attribute: account_lifetime_value > 0
        - AND Attribute: users_count >= 1

        Description: Active accounts flagged at-risk by the platform's health-scoring with positive lifetime value (proven paid customer) and no active renewal deal in flight. CSM intervention priority: these are recoverable churn risks where someone has paid before and isn't currently in renewal motion.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Accounts at churn risk

Paying accounts the health score has flagged as at risk, with no renewal deal in flight, so your CSMs can step in before they leave.

## What it does

1. **Build the at-risk account list** (`create_segment`)

   Accounts with a health score of at risk, lifetime value above zero, at least one user, and no renewal deal open. Updates as account health changes.

## What you end up with

- **segment** (segment): Segment created on /segments.
