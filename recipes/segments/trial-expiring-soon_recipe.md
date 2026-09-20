---
name: trial-expiring-soon
description: |
  Use when a user mentions "trial expiring soon", or asks for related help. Trial users approaching expiry who haven't converted to paid.
arguments: []
intempt:
  id: trial-expiring-soon
  version: 1.0.0
  slashCommand: /trial-expiring-soon
  group: Segments
  title: 'Trials expiring this week'
  shortDescription: 'Trial users whose trial runs out within a week and who have not paid yet, your last chance to convert them.'
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
      title: 'Build the expiring-trial list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users on the trial plan whose end date falls within the next 7 days and who have not created a subscription in the last 14 days.'
      prompt: |
        Create a segment called "Trial Expiring Soon".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: plan_name = "trial"
        - AND Attribute: end_date is within next 7 days
        - AND Event: subscription_created has not occurred in last 14 days

        Description: Trial users approaching expiry without paid conversion. Trigger a final-push email or in-app upgrade prompt.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Trials expiring this week

Trial users whose trial runs out within a week and who have not paid yet, your last chance to convert them.

## What it does

1. **Build the expiring-trial list** (`create_segment`)

   Users on the trial plan whose end date falls within the next 7 days and who have not created a subscription in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
