---
name: power-users
description: |
  Use when a user mentions "power users", or asks for related help. Highly engaged users with frequent sessions and high activity score in the last 30 days.
arguments: []
intempt:
  id: power-users
  version: 1.0.0
  slashCommand: /power-users
  group: Segments
  title: 'Power users'
  shortDescription: 'Your most active users over the last month, the people to ask for reviews, case studies, and beta feedback.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [all]
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
      title: 'Build the power-user list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with 10 or more sessions and 20 or more clicks in the last 30 days, a High engagement score, and activity in the last 7 days.'
      prompt: |
        Create a segment called "Power Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: session_start occurred >= 10 times in last 30 days
        - AND Event: click_on occurred >= 20 times in last 30 days
        - AND Attribute: engagement_score = "High"
        - AND Attribute: last_seen_at is within last 7 days

        Description: Highly engaged users: frequent sessions, high engagement, recent activity. Priority cohort for advocacy programs, beta access, and case-study outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Power users

Your most active users over the last month, the people to ask for reviews, case studies, and beta feedback.

## What it does

1. **Build the power-user list** (`create_segment`)

   Users with 10 or more sessions and 20 or more clicks in the last 30 days, a High engagement score, and activity in the last 7 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
