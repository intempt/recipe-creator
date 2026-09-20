---
name: enterprise-accounts
description: |
  Use when a user mentions "enterprise accounts (1000+ employees)", or asks for related help. Large companies (1000+ employees): AE white-glove sales-motion routing.
arguments: []
intempt:
  id: enterprise-accounts
  version: 1.0.0
  slashCommand: /enterprise-accounts
  group: Segments
  title: 'Enterprise accounts'
  shortDescription: 'Companies with 1,000 or more employees, so your enterprise sellers work from one list.'
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
  prerequisites:
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the enterprise list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with 1,000 or more employees. Updates as company size data changes.'
      prompt: |
        Create a segment called "Enterprise Accounts".

        Object: Accounts

        Rules:
        - Attribute: employees >= 1000

        Description: Companies with 1000+ employees. Foundation for enterprise sales-motion routing: these accounts get AE white-glove engagement: dedicated account plans, executive-sponsor outreach, and quarterly business reviews. Universal B2B routing pattern.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Enterprise accounts

Companies with 1,000 or more employees, so your enterprise sellers work from one list.

## What it does

1. **Build the enterprise list** (`create_segment`)

   Accounts with 1,000 or more employees. Updates as company size data changes.

## What you end up with

- **segment** (segment): Segment created on /segments.
