---
name: expansion-candidates
description: |
  Use when a user mentions "expansion candidates: near plan limit", or asks for related help. Users approaching their plan limit who are ready for an upgrade conversation.
arguments: []
intempt:
  id: expansion-candidates
  version: 1.0.0
  slashCommand: /expansion-candidates
  group: Segments
  title: 'Users close to their plan limit'
  shortDescription: 'Users who have used up most of their plan allowance, so you can start the upgrade conversation before they hit the ceiling.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas]
    object: users
    complexity: standard
    executionMode: live
    tags: [users-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the near-limit list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users on any plan other than enterprise whose usage is at 80 percent or more of their limit.'
      prompt: |
        Create a segment called "Expansion Candidates".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: plan_name is not "enterprise"
        - AND Attribute: usage_pct >= 80

        Description: Users approaching plan limits: prime upgrade candidates. Trigger in-app upgrade prompt or AE outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Users close to their plan limit

Users who have used up most of their plan allowance, so you can start the upgrade conversation before they hit the ceiling.

## What it does

1. **Build the near-limit list** (`create_segment`)

   Users on any plan other than enterprise whose usage is at 80 percent or more of their limit.

## What you end up with

- **segment** (segment): Segment created on /segments.
