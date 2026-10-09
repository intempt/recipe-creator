---
name: at-risk-vips
description: |
  Use when a user mentions "at-risk vips", or asks for related help. High-lifetime-value customers showing recency decay: Klaviyo's Needs Attention cohort. Distinct from generic churn risk.
arguments: []
intempt:
  id: at-risk-vips
  version: 1.0.0
  slashCommand: /at-risk-vips
  group: Segments
  title: 'At-risk VIP customers'
  shortDescription: 'Your biggest spenders who have gone quiet for about six weeks, so you can reach out personally before they drift away for good.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [ecommerce]
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
      title: 'Build the at-risk VIP list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Customers with lifetime value of 1,000 or more and 2 or more orders, whose last activity was 45 to 90 days ago and who have not ordered in 45 days.'
      prompt: |
        Create a segment called "At-Risk VIPs".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: Lifetime value >= 1000
        - AND Attribute: Days since last activity is between 45 and 90
        - AND Event: Placed order occurred >= 2 times (all time)
        - AND Event: Placed order occurred 0 times in last 45 days

        Description: High-LTV customers who are going quiet: the Klaviyo "Needs Attention" RFM cohort. Most expensive cohort to lose; strongest ROI for personalized win-back outreach (CSM-style email from a real person, not a discount blast).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# At-risk VIP customers

Your biggest spenders who have gone quiet for about six weeks, so you can reach out personally before they drift away for good.

## What it does

1. **Build the at-risk VIP list** (`create_segment`)

   Customers with lifetime value of 1,000 or more and 2 or more orders, whose last activity was 45 to 90 days ago and who have not ordered in 45 days.

## What you end up with

- **segment** (segment): Segment created on /segments.
