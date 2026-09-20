---
name: multi-stakeholder-engaged-accounts
description: |
  Use when a user mentions "multi-stakeholder engaged accounts", or asks for related help. Accounts where 3+ users have been active in last 14 days: buying-committee signal for B2B.
arguments: []
intempt:
  id: multi-stakeholder-engaged-accounts
  version: 1.0.0
  slashCommand: /multi-stakeholder-engaged-accounts
  group: Segments
  title: 'Accounts with a buying group active'
  shortDescription: 'Accounts where three or more people have been using the product in the last two weeks, usually the sign a buying group has formed.'
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
      title: 'Build the multi-stakeholder list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with 3 or more users, plus 5 or more sessions and 10 or more page views across those users in the last 14 days.'
      prompt: |
        Create a segment called "Multi-Stakeholder Engaged Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: users_count >= 3
        - AND Event (across users in account): session_start occurred >= 5 times in last 14 days
        - AND Event (across users in account): page_viewed occurred >= 10 times in last 14 days

        Description: Accounts where 3+ users have been actively engaged in the last 14 days. The buying-committee signal: Salesforce reports B2B deals now involve an average of 11 stakeholders, so multi-user engagement at the account level is one of the strongest forward-looking indicators of an active buying cycle. Foundation for AE multi-threading plays and ABM coordination.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Accounts with a buying group active

Accounts where three or more people have been using the product in the last two weeks, usually the sign a buying group has formed.

## What it does

1. **Build the multi-stakeholder list** (`create_segment`)

   Accounts with 3 or more users, plus 5 or more sessions and 10 or more page views across those users in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
