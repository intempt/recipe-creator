---
name: onboarding-stalled-users
description: |
  Use when a user mentions "onboarding-stalled users", or asks for related help. Recently signed up but no activation milestone in last 14 days: activation-rescue cohort.
arguments: []
intempt:
  id: onboarding-stalled-users
  version: 1.0.0
  slashCommand: /onboarding-stalled-users
  group: Segments
  title: 'Users stuck in onboarding'
  shortDescription: 'People who signed up a few weeks ago and still drop in now and then, but have never finished setup, so you can help them over the line.'
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
      title: 'Build the stalled-onboarding list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users first seen 7 to 30 days ago who have completed no journey goal since signing up and were last active within the past 14 days.'
      prompt: |
        Create a segment called "Onboarding-Stalled Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: First seen is between 7 and 30 days ago
        - AND Event: Completed a journey goal occurred 0 times since First seen
        - AND Attribute: Days since last activity <= 14

        Description: Users who signed up 7-30 days ago, are still occasionally active, but have not completed any activation milestone. The activation-rescue cohort. Trigger guided onboarding outreach (in-app checklist, founder-style email, CSM check-in for high-value accounts).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Users stuck in onboarding

People who signed up a few weeks ago and still drop in now and then, but have never finished setup, so you can help them over the line.

## What it does

1. **Build the stalled-onboarding list** (`create_segment`)

   Users first seen 7 to 30 days ago who have completed no journey goal since signing up and were last active within the past 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
