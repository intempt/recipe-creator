---
description: Scores how well each trial is going and sends different onboarding to the ones racing ahead, the ones drifting, and the ones at risk.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Trial to paid activation

Slash command: /trial-activation

## Step 1: Score how the trial is going

Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded).

## Step 2: Split trials into three tiers

Segment trial users into risk tiers (high-engagement, moderate, at-risk) based on trial_health_score. Use the result of "Score how the trial is going".

## Step 3: Write onboarding per tier

Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. Use the result of "Score how the trial is going", "Split trials into three tiers".

## Step 4: Route each tier differently

Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. Use the result of "Score how the trial is going", "Split trials into three tiers", "Write onboarding per tier".

## Step 5: Track trial to paid

Compose a funnel report tracking trial-signup to key-event-1 to key-event-2 to paid-conversion with retention overlay. Use the result of "Score how the trial is going", "Split trials into three tiers", "Write onboarding per tier", "Route each tier differently".
