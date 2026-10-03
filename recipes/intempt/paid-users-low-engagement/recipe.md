---
id: paid-users-low-engagement
title: Paid users losing interest
slash_command: /paid-users-low-engagement
group: Segments
owner: intempt
summary: Paying customers whose usage has dropped off in the last couple of weeks, early enough to fix
  before it turns into churn.
description: >-
  Paying customers showing early disengagement signals. Engagement bucketed enum.
version: 2.0.0
classification:
  product:
    - segments
  agent: segment-architect
  mode:
    - saas
  object: users
  complexity: standard
  executionMode: live
  tags:
    - users-segment
steps:
  - id: s1
    title: Build the low-engagement list
    summary: >-
      Users on a paid plan (not free or trial) with a Low engagement score whose last activity was 7 to
      21 days ago.
    builds: segment
    description: |-
      Create a segment called "Paid Users: Low Engagement".
      Object: Users
      Rules (all conditions joined by AND):
      - Attribute: plan_name is not in ["free", "trial"]
      - AND Attribute: days_since_last_activity is between 7 and 21
      - AND Attribute: engagement_score = "Low"
      Description: Paid customers showing early disengagement before they become full churn risk. Trigger CSM check-in or feature-rediscovery campaign.
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment created on /segments.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Paid users losing interest

Paying customers whose usage has dropped off in the last couple of weeks, early enough to fix before it turns into churn.

## Steps

1. **Build the low-engagement list** (builds segment)

   Users on a paid plan (not free or trial) with a Low engagement score whose last activity was 7 to 21 days ago.

## What you end up with

- **segment** (segment): Segment created on /segments.

## Availability

Install now: every step builds something the engine supports today.
