---
name: single-threaded-accounts
description: |
  Use when a user mentions "single-threaded accounts", or asks for related help. Multi-user companies where only 1 user is engaged: multi-threading risk for enterprise SaaS.
arguments: []
intempt:
  id: single-threaded-accounts
  version: 1.0.0
  slashCommand: /single-threaded-accounts
  group: Segments
  title: 'Single-threaded open deals'
  shortDescription: 'Open deals at larger companies where only one person is engaged, so an AE can bring more stakeholders in before it stalls.'
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
      title: 'Build the single-threaded list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with more than 50 employees, exactly 1 engaged user, and a deal currently open.'
      prompt: |
        Create a segment called "Single-Threaded Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: employees > 50
        - AND Attribute: users_count = 1
        - AND Attribute: has_open_deal = true

        Description: Multi-user-sized companies (50+ employees) where only one user is engaged with our product, AND there's an active deal. Critical multi-threading risk: single-threaded enterprise deals lose at 2-3x the rate of multi-threaded deals. Trigger AE plays to identify and engage 2-3 additional stakeholders before deal close.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Single-threaded open deals

Open deals at larger companies where only one person is engaged, so an AE can bring more stakeholders in before it stalls.

## What it does

1. **Build the single-threaded list** (`create_segment`)

   Accounts with more than 50 employees, exactly 1 engaged user, and a deal currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.
