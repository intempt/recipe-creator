---
name: icp-match-accounts
description: |
  Use when a user mentions "icp match accounts", or asks for related help. Accounts matching ideal customer profile by company size, industry, and geography.
arguments: []
intempt:
  id: icp-match-accounts
  version: 1.0.0
  slashCommand: /icp-match-accounts
  group: Segments
  title: 'Accounts matching your ICP'
  shortDescription: 'Accounts that fit your ideal customer profile on size, industry, and country, as the base list for account-based targeting.'
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
      title: 'Build the ICP list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with 50 to 500 employees in SaaS, Technology, or Financial Services, based in the US, UK, Canada, or Australia.'
      prompt: |
        Create a segment called "ICP Match Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: employees is between 50 and 500
        - AND Attribute: industry is one of ["SaaS", "Technology", "Financial Services"]
        - AND Attribute: country is one of ["US", "UK", "CA", "AU"]

        Description: Accounts matching the ideal customer profile by size, industry, and geography. Foundation segment for ABM targeting.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Accounts matching your ICP

Accounts that fit your ideal customer profile on size, industry, and country, as the base list for account-based targeting.

## What it does

1. **Build the ICP list** (`create_segment`)

   Accounts with 50 to 500 employees in SaaS, Technology, or Financial Services, based in the US, UK, Canada, or Australia.

## What you end up with

- **segment** (segment): Segment created on /segments.
