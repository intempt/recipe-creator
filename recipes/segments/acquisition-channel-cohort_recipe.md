---
name: acquisition-channel-cohort
description: |
  Use when a user mentions "acquisition channel cohort", or asks for related help. Customers acquired through a specific channel (parameterized by utm_source/medium): for channel-quality analysis.
arguments: []
intempt:
  id: acquisition-channel-cohort
  version: 1.0.0
  slashCommand: /acquisition-channel-cohort
  group: Segments
  title: 'Customers by acquisition channel'
  shortDescription: 'Customers grouped by the channel that brought them in, so you can compare how well each channel''s buyers stick around.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [ecommerce, saas]
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
      title: 'Build the channel cohort'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users matching one utm_source and utm_medium pair (for example google and cpc) who have placed at least one order. Build one cohort per channel you want to compare.'
      prompt: |
        Create a segment called "Acquisition Channel: <Channel Name>".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: utm_source = "<source>"  (e.g., "google", "facebook", "tiktok", "klaviyo", "newsletter")
        - AND Attribute: utm_medium = "<medium>"  (e.g., "cpc", "social", "email", "referral", "organic")
        - AND Event: order_created occurred >= 1 time (all time)

        Example concrete instances merchants typically build:
        - "Paid Social Acquired": utm_source IN ["facebook", "instagram", "tiktok"] AND utm_medium IN ["cpc", "paid_social", "social"]
        - "Google Paid Acquired": utm_source = "google" AND utm_medium = "cpc"
        - "Organic Search Acquired": utm_source = "google" AND utm_medium = "organic"
        - "Email/Newsletter Acquired": utm_medium = "email"
        - "Referral Acquired": utm_medium IN ["referral", "affiliate"]

        Description: Channel-specific cohorts for retention analysis and channel-quality measurement. Customers acquired through different channels behave differently: organic and referral acquisitions typically have 30-50% higher repeat purchase rates than paid-social acquisitions. Building these cohorts lets you measure channel ROI by retention (not just acquisition cost) and tune retention investment per channel.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Customers by acquisition channel

Customers grouped by the channel that brought them in, so you can compare how well each channel's buyers stick around.

## What it does

1. **Build the channel cohort** (`create_segment`)

   Users matching one utm_source and utm_medium pair (for example google and cpc) who have placed at least one order. Build one cohort per channel you want to compare.

## What you end up with

- **segment** (segment): Segment created on /segments.
