---
name: recently-signed-up-users
description: |
  Use when a user mentions "recently signed-up users", or asks for related help. Users who created an account in the last 30 days: onboarding cohort.
arguments: []
intempt:
  id: recently-signed-up-users
  version: 1.0.0
  slashCommand: /recently-signed-up-users
  group: Segments
  title: 'Recent signups'
  shortDescription: 'Everyone who created an account in the last month, the audience for your welcome and first-week activation emails.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas, ecommerce]
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
      title: 'Build the new signup list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users first seen in the last 30 days.'
      prompt: |
        Create a segment called "Recently Signed-Up Users".

        Object: Users

        Rules:
        - Attribute: first_seen_at is within last 30 days

        Description: Onboarding cohort. Use as the audience for first-week activation campaigns, welcome journeys, and onboarding email sequences.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Recent signups

Everyone who created an account in the last month, the audience for your welcome and first-week activation emails.

## What it does

1. **Build the new signup list** (`create_segment`)

   Users first seen in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
