---
name: high-intent-anonymous-visitors
description: |
  Use when a user mentions "high-intent anonymous visitors", or asks for related help. Unidentified visitors with strong engagement signals: ad retargeting cohort.
arguments: []
intempt:
  id: high-intent-anonymous-visitors
  version: 1.0.0
  slashCommand: /high-intent-anonymous-visitors
  group: Segments
  title: 'High-intent anonymous visitors'
  shortDescription: 'Visitors you cannot email yet who keep coming back, so you can retarget them with ads or try to capture an address.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas, b2b, ecommerce]
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
      title: 'Build the anonymous visitor list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Visitors with no email on file, 5 or more events in total, and 3 or more page views across 2 or more sessions in the last 7 days.'
      prompt: |
        Create a segment called "High-Intent Anonymous Visitors".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: Total events >= 5
        - AND Attribute: email is empty
        - AND Event: View page occurred >= 3 times in last 7 days
        - AND Event: Session start occurred >= 2 times in last 7 days

        Description: Unidentified visitors with multiple sessions and substantial activity. Ad-retargeting cohort: also a candidate for an email-capture popup or content offer.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# High-intent anonymous visitors

Visitors you cannot email yet who keep coming back, so you can retarget them with ads or try to capture an address.

## What it does

1. **Build the anonymous visitor list** (`create_segment`)

   Visitors with no email on file, 5 or more events in total, and 3 or more page views across 2 or more sessions in the last 7 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
