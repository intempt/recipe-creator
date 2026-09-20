---
name: net-new-prospects
description: |
  Use when a user mentions "net-new prospects", or asks for related help. Recently identified accounts with minimal engagement: SDR first-touch foundation.
arguments: []
intempt:
  id: net-new-prospects
  version: 1.0.0
  slashCommand: /net-new-prospects
  group: Segments
  title: 'Net-new prospect accounts'
  shortDescription: 'Accounts created in the last week that have barely done anything yet, so SDRs know who to contact first.'
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
      title: 'Build the net-new account list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts created in the last 7 days, with 5 or fewer events, lifecycle set to prospect, and no open deal. Updates as new accounts arrive.'
      prompt: |
        Create a segment called "Net-New Prospects".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: created_at is within last 7 days
        - AND Attribute: total_events <= 5
        - AND Attribute: account_lifecycle = "prospect"
        - AND Attribute: has_open_deal = false

        Description: Accounts identified in the last 7 days with minimal engagement so far. Foundation for SDR first-touch sequences: these are the freshest entries to your TAL or your inbound feed, deserving immediate qualification within ICP-fit and intent-strength frameworks.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Net-new prospect accounts

Accounts created in the last week that have barely done anything yet, so SDRs know who to contact first.

## What it does

1. **Build the net-new account list** (`create_segment`)

   Accounts created in the last 7 days, with 5 or fewer events, lifecycle set to prospect, and no open deal. Updates as new accounts arrive.

## What you end up with

- **segment** (segment): Segment created on /segments.
