---
name: renewal-window-90-day
description: |
  Use when a user mentions "renewal window (90 days", or asks for related help. Subscriptions ending in next 90 days) foundation for renewal-flow journeys and NRR plays.
arguments: []
intempt:
  id: renewal-window-90-day
  version: 1.0.0
  slashCommand: /renewal-window-90-day
  group: Segments
  title: 'Renewals due in 90 days'
  shortDescription: 'Paid subscriptions that end within the next three months, so renewal conversations start early instead of the week before.'
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
      title: 'Build the renewal list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users on a paid plan whose subscription end date falls within the next 90 days and is still in the future.'
      prompt: |
        Create a segment called "Renewal Window: 90 Days".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: end_date is within next 90 days
        - AND Attribute: end_date is in the future
        - AND Attribute: plan_name is not "free"

        Description: Users with active paid subscriptions ending in the next 90 days. The renewal-targeting cohort: foundation for QBR-style ROI emails, renewal-conversation triggers, and NRR-driven CSM outreach. NRR is the single most important SaaS metric in 2026; this segment makes the renewal pipeline actionable.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Renewals due in 90 days

Paid subscriptions that end within the next three months, so renewal conversations start early instead of the week before.

## What it does

1. **Build the renewal list** (`create_segment`)

   Users on a paid plan whose subscription end date falls within the next 90 days and is still in the future.

## What you end up with

- **segment** (segment): Segment created on /segments.
