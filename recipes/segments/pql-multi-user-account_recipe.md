---
name: pql-multi-user-account
description: |
  Use when a user mentions "pql (multi-user account", or asks for related help. Free/trial accounts with 2+ engaged users from same company) enterprise PQL signal.
arguments: []
intempt:
  id: pql-multi-user-account
  version: 1.0.0
  slashCommand: /pql-multi-user-account
  group: Segments
  title: 'Free accounts with a team trying it'
  shortDescription: 'Free and trial accounts where two or more colleagues are both active, which converts better than one person trying it alone.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas]
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
      title: 'Build the team-trial list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts with 2 or more users, where those users started 3 or more sessions and completed at least one journey goal in the last 14 days.'
      prompt: |
        Create a segment called "PQL: Multi-User Account".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: User count >= 2
        - AND Event (across users in account): Session start occurred >= 3 times in last 14 days
        - AND Event (across users in account): Completed a journey goal occurred >= 1 time in last 14 days

        Description: Accounts where 2+ users from the same company are actively engaged in trial or free plan. The enterprise PQL signal: distinguishes team-buying behavior from individual-trial signups. Highest-converting PQL cohort: when multiple stakeholders test the product, they convert at 2-3x the rate of individual-trial PQLs.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Free accounts with a team trying it

Free and trial accounts where two or more colleagues are both active, which converts better than one person trying it alone.

## What it does

1. **Build the team-trial list** (`create_segment`)

   Accounts with 2 or more users, where those users started 3 or more sessions and completed at least one journey goal in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
