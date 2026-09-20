---
name: mid-market-accounts
description: |
  Use when a user mentions "mid-market accounts (100-1000 employees)", or asks for related help. Mid-sized companies (100-1000 employees): inside-sales / scaled-AE routing.
arguments: []
intempt:
  id: mid-market-accounts
  version: 1.0.0
  slashCommand: /mid-market-accounts
  group: Segments
  title: 'Mid-market accounts'
  shortDescription: 'Companies with 100 to 1,000 employees, so your inside sales team works from one list.'
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
      title: 'Build the mid-market list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with 100 or more employees and fewer than 1,000.'
      prompt: |
        Create a segment called "Mid-Market Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: employees >= 100
        - AND Attribute: employees < 1000

        Description: Companies with 100-1000 employees. Foundation for inside-sales / scaled-AE routing: these accounts get standardized playbooks, semi-personalized campaigns, and shorter sales cycles than enterprise. Universal B2B routing pattern.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Mid-market accounts

Companies with 100 to 1,000 employees, so your inside sales team works from one list.

## What it does

1. **Build the mid-market list** (`create_segment`)

   Accounts with 100 or more employees and fewer than 1,000.

## What you end up with

- **segment** (segment): Segment created on /segments.
