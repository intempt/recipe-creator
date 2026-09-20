---
name: high-intent-icp-prospects
description: |
  Use when a user mentions "high-intent icp prospects", or asks for related help. ICP-matching accounts with active intent signals (pricing + docs visited recently).
arguments: []
intempt:
  id: high-intent-icp-prospects
  version: 1.0.0
  slashCommand: /high-intent-icp-prospects
  group: Segments
  title: 'ICP accounts showing intent'
  shortDescription: 'Accounts that fit your ideal profile and read both your pricing and your docs this week, with no deal open yet.'
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
      title: 'Build the hot ICP list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with 50 to 1,000 employees in SaaS, Technology, Fintech, or Financial Services, where users viewed both a /pricing page and a /docs page in the last 7 days, and no deal is open.'
      prompt: |
        Create a segment called "High-Intent ICP Prospects".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: employees is between 50 and 1000
        - AND Attribute: industry is one of ["SaaS", "Technology", "Fintech", "Financial Services"]
        - AND Event (via users in account): page_viewed where page_url contains "/pricing" occurred >= 1 time in last 7 days
        - AND Event (via users in account): page_viewed where page_url contains "/docs" occurred >= 1 time in last 7 days
        - AND Attribute: has_open_deal = false

        Description: ICP-matching accounts with hot buying signals this week. Highest-priority cohort for SDR outreach: pre-qualified and actively researching.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# ICP accounts showing intent

Accounts that fit your ideal profile and read both your pricing and your docs this week, with no deal open yet.

## What it does

1. **Build the hot ICP list** (`create_segment`)

   Accounts with 50 to 1,000 employees in SaaS, Technology, Fintech, or Financial Services, where users viewed both a /pricing page and a /docs page in the last 7 days, and no deal is open.

## What you end up with

- **segment** (segment): Segment created on /segments.
