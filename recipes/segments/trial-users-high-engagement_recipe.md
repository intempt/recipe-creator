---
name: trial-users-high-engagement
description: |
  Use when a user mentions "trial users: high engagement", or asks for related help. Trial users with strong usage signals who are likely to convert. Engagement bucketed enum.
arguments: []
intempt:
  id: trial-users-high-engagement
  version: 1.0.0
  slashCommand: /trial-users-high-engagement
  group: Segments
  title: 'Trials most likely to convert'
  shortDescription: 'Trial users who are using the product heavily with two weeks left to run, the ones worth a sales call.'
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
      title: 'Build the strong-trial list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users on the trial plan with a High engagement score, an end date within the next 14 days, and 3 or more journey goals completed in the last 14 days.'
      prompt: |
        Create a segment called "Trial Users: High Engagement".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: Plan = "trial"
        - AND Attribute: Subscription end date is within next 14 days
        - AND Attribute: Engagement score = "High"
        - AND Event: Completed a journey goal occurred >= 3 times in last 14 days

        Description: Trial users with strong usage signals: most likely to convert. Trigger high-touch sales outreach or premium-feature unlock.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Trials most likely to convert

Trial users who are using the product heavily with two weeks left to run, the ones worth a sales call.

## What it does

1. **Build the strong-trial list** (`create_segment`)

   Users on the trial plan with a High engagement score, an end date within the next 14 days, and 3 or more journey goals completed in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
