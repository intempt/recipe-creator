---
name: newly-activated-users
description: |
  Use when a user mentions "newly activated users", or asks for related help. Users who completed activation in the last 7 days: warm and ready to expand.
arguments: []
intempt:
  id: newly-activated-users
  version: 1.0.0
  slashCommand: /newly-activated-users
  group: Segments
  title: 'Newly activated users'
  shortDescription: 'Paying users who hit their activation milestone in the last week, while they are warm enough to say yes to more.'
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
      title: 'Build the newly-activated list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users on a paid plan who completed the activation journey goal at least once in the last 7 days.'
      prompt: |
        Create a segment called "Newly Activated Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: Completed a journey goal where journey_id = <activation journey id> occurred >= 1 time in last 7 days
        - AND Attribute: Plan is not "free"

        Description: Users who hit the activation milestone in the last 7 days. Warm cohort for expansion outreach, feature-discovery campaigns, and upgrade prompts.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Newly activated users

Paying users who hit their activation milestone in the last week, while they are warm enough to say yes to more.

## What it does

1. **Build the newly-activated list** (`create_segment`)

   Users on a paid plan who completed the activation journey goal at least once in the last 7 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
