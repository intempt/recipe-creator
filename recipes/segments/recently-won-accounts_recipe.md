---
name: recently-won-accounts
description: |
  Use when a user mentions "recently-won accounts", or asks for related help. Accounts that closed a deal in last 90 days: onboarding cohort distinct from new-paying-customers.
arguments: []
intempt:
  id: recently-won-accounts
  version: 1.0.0
  slashCommand: /recently-won-accounts
  group: Segments
  title: 'Recently won accounts'
  shortDescription: 'Accounts that became customers in the last quarter, so onboarding and implementation start from one current list.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [b2b, saas]
    object: accounts
    complexity: standard
    executionMode: live
    tags: [accounts-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the recently-won list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Accounts whose lifecycle changed to customer within the last 90 days, with no deal currently open.'
      prompt: |
        Create a segment called "Recently-Won Accounts".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: lifecycle_changed_at is within last 90 days
        - AND Attribute: account_lifecycle is "customer"
        - AND Attribute: has_open_deal = false

        Description: Accounts that became customers in the last 90 days: the post-deal-close onboarding cohort. Distinct from new-paying-customers (which is plan-tier-conversion at the User level). For B2B sales motion, the deal-close moment is the kickoff for CSM onboarding, implementation milestones, and time-to-value tracking.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Recently won accounts

Accounts that became customers in the last quarter, so onboarding and implementation start from one current list.

## What it does

1. **Build the recently-won list** (`create_segment`)

   Accounts whose lifecycle changed to customer within the last 90 days, with no deal currently open.

## What you end up with

- **segment** (segment): Segment created on /segments.
