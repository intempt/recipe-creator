---
description: A rules-based journey that routes each person to a next step from a candidate set using attributes and segment membership at branch points.
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

# Next best action orchestration

Slash command: /next-best-action-orchestration

## Step 1: Decide the next step per user

Create an AI-derived attribute 'next_best_action' on the User object, refreshed daily and on every significant behavioral event. Inputs: current lifecycle stage, engagement velocity (sessions trend), feature usage breadth, recent intent signals (pricing visit, feature first-click, support touch), and prior message engagement. Outputs: a structured object with (a) recommended_action one of [educate / nurture / offer / surface-feature / surface-recommendations / handoff-to-agent / wait]; (b) recommended_channel [email / sms / in_app / push / slack-internal]; (c) recommended_content_theme; (d) confidence (0-100); (e) expected_uplift_signal. The attribute is the decisioning brain: the journey routes from it at each gate.

## Step 2: Only route confident calls

Build a segment 'NBA-orchestrated users' capturing active users where next_best_action.confidence >= 50 AND user is not currently in another high-priority journey (no double-orchestration). Refreshed continuously, as users' NBA changes, they move between sub-cohorts of this parent segment. Use the result of "Decide the next step per user".

## Step 3: Write an email per action

Generate email content variants per recommended_action: (a) educate variant (short value tip matched to the user's stage; (b) nurture variant) case study/customer story relevant to user's segment; (c) offer variant (personalized incentive (discount / trial extension / credit) matched to plan and tenure; (d) surface-feature variant) feature spotlight with deep-link to the in-app destination. Each variant pulls dynamic content blocks based on the user's full profile, not just first name. Use the result of "Decide the next step per user", "Only route confident calls".

## Step 4: Write the in app versions

This step builds a page.
Generate in-app message variants for the surface-feature and surface-recommendations branches. Surface-feature: contextual tooltip pointing to the feature, with a 1-line value prop and 'try it' CTA, rendered in the relevant in-app location. Surface-recommendations: a personalized recommendation card pulling from the user's product affinity. In-app fires only during active sessions, never outside the app (avoids interruption fatigue). Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action".

## Step 5: Build the recommendation set

Configure a recommendation surface 'NBA-driven product/content recs' that activates when next_best_action.recommended_action = surface-recommendations. Sources: the user's prior interaction history + similar-user purchase/usage patterns + currently-trending items in their segment. Render in: in-app sidebar + email content block + page personalization slot. Refresh weekly. Use the result of "Decide the next step per user", "Only route confident calls".

## Step 6: Re-read the signal at each gate

Build an adaptive journey wired to the NBA segment. At each gate (signup+7d, +14d, +30d, +60d, ongoing weekly), the journey reads next_best_action attribute and routes the user down the matching branch: educate to email variant a; nurture to email variant b; offer to email variant c with discount; surface-feature to in-app tooltip + email variant d; surface-recommendations to activate recommendation surface + email digest with recs; handoff-to-agent to trigger agent conversation; wait to skip touch, recompute next gate. Each branch's outcome (clicked / engaged / converted / ignored) feeds back into the next NBA computation so the decisioning learns. Exit on: conversion event (deal_created / subscription_created / activation_milestone: depending on lifecycle), unsubscribe, or sustained no-engagement (NBA returns wait 3 gates in a row to suppress). Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action", "Write the in app versions", "Build the recommendation set".

## Step 7: Check the model against a control

Compose an NBA orchestration dashboard: distribution of recommended_action across users (which actions does the model favor: sanity check on model balance), per-branch engagement rates (which actions actually convert), confidence-vs-conversion correlation (does higher-confidence routing actually predict higher conversion (model-quality signal), uplift vs control (a 5-10% holdout that gets fixed cadence) the proof-of-value chart), and per-segment NBA quality (model may serve some segments better than others: informs retraining priorities). Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action", "Write the in app versions", "Build the recommendation set", "Re-read the signal at each gate".
