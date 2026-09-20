---
name: paid-users-low-engagement
description: |
  Use when a user mentions "paid users: low engagement", or asks for related help. Paying customers showing early disengagement signals. Engagement bucketed enum.
arguments: []
intempt:
  id: paid-users-low-engagement
  version: 1.0.0
  slashCommand: /paid-users-low-engagement
  group: Segments
  title: 'Paid users losing interest'
  shortDescription: 'Paying customers whose usage has dropped off in the last couple of weeks, early enough to fix before it turns into churn.'
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
      title: 'Build the low-engagement list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users on a paid plan (not free or trial) with a Low engagement score whose last activity was 7 to 21 days ago.'
      prompt: |
        Create a segment called "Paid Users: Low Engagement".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: plan_name is not in ["free", "trial"]
        - AND Attribute: days_since_last_activity is between 7 and 21
        - AND Attribute: engagement_score = "Low"

        Description: Paid customers showing early disengagement before they become full churn risk. Trigger CSM check-in or feature-rediscovery campaign.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Paid users losing interest

Paying customers whose usage has dropped off in the last couple of weeks, early enough to fix before it turns into churn.

## What it does

1. **Build the low-engagement list** (`create_segment`)

   Users on a paid plan (not free or trial) with a Low engagement score whose last activity was 7 to 21 days ago.

## What you end up with

- **segment** (segment): Segment created on /segments.
