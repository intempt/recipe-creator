---
name: engaged-free-users
description: |
  Use when a user mentions "engaged free users", or asks for related help. Free-plan users with high engagement: prime upgrade-targeting cohort.
arguments: []
intempt:
  id: engaged-free-users
  version: 1.0.0
  slashCommand: /engaged-free-users
  group: Segments
  title: 'Engaged free users'
  shortDescription: 'Free-plan users who are in the product often and recently, so upgrade prompts reach the people already getting value.'
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
      title: 'Build the engaged free list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users on the free plan with a High engagement score, active in the last 7 days, and 5 or more sessions in the last 14 days.'
      prompt: |
        Create a segment called "Engaged Free Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: Plan = "free"
        - AND Attribute: Engagement score = "High"
        - AND Attribute: Days since last activity <= 7
        - AND Event: Session start occurred >= 5 times in last 14 days

        Description: Free users showing strong engagement and recent activity. Prime cohort for upgrade prompts, premium-feature trials, and account-expansion outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Engaged free users

Free-plan users who are in the product often and recently, so upgrade prompts reach the people already getting value.

## What it does

1. **Build the engaged free list** (`create_segment`)

   Users on the free plan with a High engagement score, active in the last 7 days, and 5 or more sessions in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
