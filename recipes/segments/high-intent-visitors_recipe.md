---
name: high-intent-visitors
description: |
  Use when a user mentions "high-intent visitors", or asks for related help. Non-customers who viewed both pricing and documentation in the last 14 days: strong buying signals.
arguments: []
intempt:
  id: high-intent-visitors
  version: 1.0.0
  slashCommand: /high-intent-visitors
  group: Segments
  title: 'High-intent visitors'
  shortDescription: 'Free and unregistered users who read both your pricing and your docs in the last two weeks, the clearest sign somebody is close to buying.'
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
      title: 'Build the high-intent list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users with no plan or the free plan who viewed both a /pricing page and a /docs page in the last 14 days.'
      prompt: |
        Create a segment called "High-Intent Visitors".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: page_viewed where page_url contains "/pricing" occurred >= 1 time in last 14 days
        - AND Event: page_viewed where page_url contains "/docs" occurred >= 1 time in last 14 days
        - AND Attribute: plan_name is empty OR plan_name = "free"

        Description: Non-customers (or free-plan users) showing strong buying signals across pricing and docs. Prioritize for sales outreach or in-app upgrade prompt.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# High-intent visitors

Free and unregistered users who read both your pricing and your docs in the last two weeks, the clearest sign somebody is close to buying.

## What it does

1. **Build the high-intent list** (`create_segment`)

   Users with no plan or the free plan who viewed both a /pricing page and a /docs page in the last 14 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
