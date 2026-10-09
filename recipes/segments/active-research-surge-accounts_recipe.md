---
name: active-research-surge-accounts
description: |
  Use when a user mentions "active research surge accounts", or asks for related help. Accounts with 3+ pricing-page visits in last 7 days: active buying-cycle signal.
arguments: []
intempt:
  id: active-research-surge-accounts
  version: 1.0.0
  slashCommand: /active-research-surge-accounts
  group: Segments
  title: 'Accounts researching pricing now'
  shortDescription: 'Accounts whose people hit your pricing page three or more times in the past week and have no deal open yet, so an AE can reach out while they are still looking.'
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
      title: 'Build the pricing-surge list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts where users viewed a page whose URL contains /pricing 3 or more times in the last 7 days, and no deal is currently open.'
      prompt: |
        Create a segment called "Active Research Surge Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Event (across users in account): View page where Page URL contains "/pricing" occurred >= 3 times in last 7 days
        - AND Attribute: Has an open deal = false

        Description: Accounts where users have visited the pricing page 3+ times in the last 7 days: the active-research-surge signal. Sharper than single-visit indicators; multi-visit pricing review within a tight window is one of the strongest predictors of an in-flight buying decision. Trigger AE personalized outreach within 24 hours.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Accounts researching pricing now

Accounts whose people hit your pricing page three or more times in the past week and have no deal open yet, so an AE can reach out while they are still looking.

## What it does

1. **Build the pricing-surge list** (`create_segment`)

   Accounts where users viewed a page whose URL contains /pricing 3 or more times in the last 7 days, and no deal is currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.
