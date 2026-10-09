---
name: accounts-no-open-deal
description: |
  Use when a user mentions "accounts with no open deal", or asks for related help. Healthy customer accounts with no current open deal: whitespace expansion opportunity.
arguments: []
intempt:
  id: accounts-no-open-deal
  version: 1.0.0
  slashCommand: /accounts-no-open-deal
  group: Segments
  title: 'Healthy accounts with no open deal'
  shortDescription: 'Healthy customer accounts nobody is currently selling into, so AEs can see where the expansion room is.'
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
      title: 'Build the whitespace list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts marked healthy, with no open deal, 3 or more users, and 5 or more sessions across those users in the last 30 days.'
      prompt: |
        Create a segment called "Accounts With No Open Deal".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: Has an open deal = false
        - AND Attribute: Account health = "healthy"
        - AND Attribute: User count >= 3
        - AND Event: Session start (across users in account) occurred >= 5 times in last 30 days

        Description: Healthy active accounts with no open deal: ready for expansion conversation. Trigger AE whitespace task or executive outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Healthy accounts with no open deal

Healthy customer accounts nobody is currently selling into, so AEs can see where the expansion room is.

## What it does

1. **Build the whitespace list** (`create_segment`)

   Accounts marked healthy, with no open deal, 3 or more users, and 5 or more sessions across those users in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
