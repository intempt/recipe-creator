---
name: churn-risk-users
description: |
  Use when a user mentions "churn risk users", or asks for related help. Previously active paid users who have gone silent in the last month.
arguments: []
intempt:
  id: churn-risk-users
  version: 1.0.0
  slashCommand: /churn-risk-users
  group: Segments
  title: 'Paid users going quiet'
  shortDescription: 'Paying users who used to log in regularly and have not shown up for a month, so you can reach them before they cancel.'
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
      title: 'Build the silent paid-user list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users on a paid plan who started 5 or more sessions between 60 and 90 days ago and have started none in the last 30 days.'
      prompt: |
        Create a segment called "Churn Risk Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: session_start occurred >= 5 times between 60 and 90 days ago
        - AND Event: session_start occurred 0 times in last 30 days
        - AND Attribute: plan_name is not "free"

        Description: Previously active paid users who have gone silent. Trigger CSM outreach or save-offer journey before they churn.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Paid users going quiet

Paying users who used to log in regularly and have not shown up for a month, so you can reach them before they cancel.

## What it does

1. **Build the silent paid-user list** (`create_segment`)

   Users on a paid plan who started 5 or more sessions between 60 and 90 days ago and have started none in the last 30 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
