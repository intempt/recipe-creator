---
id: acquisition-channel-cohort
title: Customers by acquisition channel
slash_command: /acquisition-channel-cohort
group: Segments
owner: intempt
summary: Customers grouped by the channel that brought them in, so you can compare how well each channel's
  buyers stick around.
description: >-
  Customers acquired through a specific channel (parameterized by utm_source/medium): for channel-quality
  analysis.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - ecommerce
    - saas
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
steps:
  - id: s1
    title: Build the channel cohort
    summary: >-
      Users matching one utm_source and utm_medium pair (for example google and cpc) who have placed at
      least one order. Build one cohort per channel you want to compare.
    builds: segment
    description: |-
      Create a segment called "Acquisition Channel: <Channel Name>".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: utm_source = "<source>" (e.g., "google", "facebook", "tiktok", "klaviyo", "newsletter")
      - AND Attribute: utm_medium = "<medium>" (e.g., "cpc", "social", "email", "referral", "organic")
      - AND Event: order_created occurred >= 1 time (all time)
      Example concrete instances merchants typically build:
      - "Paid Social Acquired": utm_source IN ["facebook", "instagram", "tiktok"] AND utm_medium IN ["cpc", "paid_social", "social"]
      - "Google Paid Acquired": utm_source = "google" AND utm_medium = "cpc"
      - "Organic Search Acquired": utm_source = "google" AND utm_medium = "organic"
      - "Email/Newsletter Acquired": utm_medium = "email"
      - "Referral Acquired": utm_medium IN ["referral", "affiliate"]
      Description: Channel-specific cohorts for retention analysis and channel-quality measurement. Customers acquired through different channels behave differently: organic and referral acquisitions typically have 30-50% higher repeat purchase rates than paid-social acquisitions. Building these cohorts lets you measure channel ROI by retention (not just acquisition cost) and tune retention investment per channel.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Customers by acquisition channel

Customers grouped by the channel that brought them in, so you can compare how well each channel's buyers stick around.

## Steps

1. **Build the channel cohort** (builds segment)

   Users matching one utm_source and utm_medium pair (for example google and cpc) who have placed at least one order. Build one cohort per channel you want to compare.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
