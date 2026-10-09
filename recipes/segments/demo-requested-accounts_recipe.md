---
name: demo-requested-accounts
description: |
  Use when a user mentions "demo-requested accounts", or asks for related help. Accounts where any user submitted a demo form in last 30 days: top SDR-routing priority.
arguments: []
intempt:
  id: demo-requested-accounts
  version: 1.0.0
  slashCommand: /demo-requested-accounts
  group: Segments
  title: 'Accounts that asked for a demo'
  shortDescription: 'Accounts where somebody filled in your demo form in the last month and no deal is open yet, so an SDR can call them back the same hour.'
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
      title: 'Build the demo-request list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts where any user submitted a demo request form at least once in the last 30 days, and no deal is currently open.'
      prompt: |
        Create a segment called "Demo-Requested Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Event (across users in account): Submit on a demo-request form occurred >= 1 time in last 30 days
        - AND Attribute: Has an open deal = false

        Description: Accounts where any user submitted a demo-request form in the last 30 days, with no existing open deal. Highest SDR-routing priority: research consistently shows 53% conversion rate for 1-hour response vs 17% after 24 hours. SLA: SDR contact within 1 hour, AE follow-up within 24 hours.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Accounts that asked for a demo

Accounts where somebody filled in your demo form in the last month and no deal is open yet, so an SDR can call them back the same hour.

## What it does

1. **Build the demo-request list** (`create_segment`)

   Accounts where any user submitted a demo request form at least once in the last 30 days, and no deal is currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.
