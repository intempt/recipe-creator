---
name: new-paying-customers
description: |
  Use when a user mentions "new paying customers", or asks for related help. First 30 days post-subscription: paid-onboarding cohort distinct from generic recently-signed-up.
arguments: []
intempt:
  id: new-paying-customers
  version: 1.0.0
  slashCommand: /new-paying-customers
  group: Segments
  title: 'New paying customers'
  shortDescription: 'Customers who started paying in the last month, the window where onboarding decides whether they stay.'
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
      title: 'Build the new-customer list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users who created a subscription in the last 30 days and are on a plan other than free or trial.'
      prompt: |
        Create a segment called "New Paying Customers".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: Subscription started occurred >= 1 time in last 30 days
        - AND Attribute: Plan is not "free"
        - AND Attribute: Plan is not "trial"

        Description: Users who converted to a paid plan in the last 30 days. The paid-onboarding cohort: distinct from recently-signed-up-users (which is account creation). The first 30 days post-paid-conversion is the highest-leverage retention window; trigger CSM kickoff, premium-feature discovery, and ROI-tracking content.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# New paying customers

Customers who started paying in the last month, the window where onboarding decides whether they stay.

## What it does

1. **Build the new-customer list** (`create_segment`)

   Users who created a subscription in the last 30 days and are on a plan other than free or trial.

## What you end up with

- **segment** (segment): Segment created on /segments.
