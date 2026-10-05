---
name: next-best-action-orchestration
description: Use when a user mentions "next best action orchestration", "AI decisioning journey", "per-user adaptive journey", or asks for related help. AI-decisioning journey where the next step is selected per-user from a candidate set (content / offer / feature-nudge / human-touch / recommendation surface) based on a live AI attribute — replaces fixed cadences with adaptive paths that match each user's signal at decision time.
arguments: []
intempt:
  id: next-best-action-orchestration
  version: 1.0.0
  slashCommand: /next-best-action-orchestration
  group: Journeys
  shortDescription: "Produce a daily-refreshed next_best_action user attribute and use it to branch a journey across educate/offer/feature/recommendation/handoff paths."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas, b2b]
    complexity: advanced
    executionMode: live
    tags: [ai-decisioning, next-best-action, adaptive-journey]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: feature_used, severity: recommended }
      - { value: session_start, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_page_content
    - create_recommendation
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Next-Best-Action AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: nba_attribute
      description: 'Create an AI-derived attribute ''next_best_action'' on the User object, refreshed daily and on every significant behavioral event. Inputs: current lifecycle stage, engagement velocity (sessions trend), feature usage breadth, recent intent signals (pricing visit, feature first-click, support touch), and prior message engagement. Outputs: a structured object with (a) recommended_action one of [educate / nurture / offer / surface-feature / surface-recommendations / handoff-to-agent / wait]; (b) recommended_channel [email / sms / in_app / push / slack-internal]; (c) recommended_content_theme; (d) confidence (0-100); (e) expected_uplift_signal. The attribute is the decisioning brain — the journey routes from it at each gate.'
      prompt: 'Create an AI-derived attribute ''next_best_action'' on the User object, refreshed daily and on every significant behavioral event. Inputs: current lifecycle stage, engagement velocity (sessions trend), feature usage breadth, recent intent signals (pricing visit, feature first-click, support touch), and prior message engagement. Outputs: a structured object with (a) recommended_action one of [educate / nurture / offer / surface-feature / surface-recommendations / handoff-to-agent / wait]; (b) recommended_channel [email / sms / in_app / push / slack-internal]; (c) recommended_content_theme; (d) confidence (0-100); (e) expected_uplift_signal. The attribute is the decisioning brain — the journey routes from it at each gate.'
    - step: 2
      title: Identify NBA-Ready Cohort
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - nba_attribute
      description: Build a segment 'NBA-orchestrated users' capturing active users where next_best_action.confidence >= 50 AND user is not currently in another high-priority journey (no double-orchestration). Refreshed continuously — as users' NBA changes, they move between sub-cohorts of this parent segment.
      prompt: Build a segment 'NBA-orchestrated users' capturing active users where next_best_action.confidence >= 50 AND user is not currently in another high-priority journey (no double-orchestration). Refreshed continuously — as users' NBA changes, they move between sub-cohorts of this parent segment.
    - step: 3
      title: Author Branch Content
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - nba_attribute
      - segment
      description: 'Generate email content variants per recommended_action: (a) educate variant — short value tip matched to the user''s stage; (b) nurture variant — case study/customer story relevant to user''s segment; (c) offer variant — personalized incentive (discount / trial extension / credit) matched to plan and tenure; (d) surface-feature variant — feature spotlight with deep-link to the in-app destination. Each variant pulls dynamic content blocks based on the user''s full profile, not just first name.'
      prompt: 'Generate email content variants per recommended_action: (a) educate variant — short value tip matched to the user''s stage; (b) nurture variant — case study/customer story relevant to user''s segment; (c) offer variant — personalized incentive (discount / trial extension / credit) matched to plan and tenure; (d) surface-feature variant — feature spotlight with deep-link to the in-app destination. Each variant pulls dynamic content blocks based on the user''s full profile, not just first name.'
    - step: 4
      title: Author In-App Branch Content
      command: create_page_content
      produces: asset
      bindsAs: inapp_asset
      dependsOn:
      - nba_attribute
      - segment
      - email_asset
      description: 'Generate in-app message variants for the surface-feature and surface-recommendations branches. Surface-feature: contextual tooltip pointing to the feature, with a 1-line value prop and ''try it'' CTA, rendered in the relevant in-app location. Surface-recommendations: a personalized recommendation card pulling from the user''s product affinity. In-app fires only during active sessions, never outside the app (avoids interruption fatigue).'
      prompt: 'Generate in-app message variants for the surface-feature and surface-recommendations branches. Surface-feature: contextual tooltip pointing to the feature, with a 1-line value prop and ''try it'' CTA, rendered in the relevant in-app location. Surface-recommendations: a personalized recommendation card pulling from the user''s product affinity. In-app fires only during active sessions, never outside the app (avoids interruption fatigue).'
    - step: 5
      title: Build Branch Recommendation Surface
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - nba_attribute
      - segment
      description: 'Configure a recommendation surface ''NBA-driven product/content recs'' that activates when next_best_action.recommended_action = surface-recommendations. Sources: the user''s prior interaction history + similar-user purchase/usage patterns + currently-trending items in their segment. Render in: in-app sidebar + email content block + page personalization slot. Refresh weekly.'
      prompt: 'Configure a recommendation surface ''NBA-driven product/content recs'' that activates when next_best_action.recommended_action = surface-recommendations. Sources: the user''s prior interaction history + similar-user purchase/usage patterns + currently-trending items in their segment. Render in: in-app sidebar + email content block + page personalization slot. Refresh weekly.'
    - step: 6
      title: Build NBA-Routed Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - nba_attribute
      - segment
      - email_asset
      - inapp_asset
      - rec_surface
      description: 'Build an adaptive journey wired to the NBA segment. At each gate (signup+7d, +14d, +30d, +60d, ongoing weekly), the journey reads next_best_action attribute and routes the user down the matching branch: educate → email variant a; nurture → email variant b; offer → email variant c with discount; surface-feature → in-app tooltip + email variant d; surface-recommendations → activate recommendation surface + email digest with recs; handoff-to-agent → trigger agent conversation; wait → skip touch, recompute next gate. Each branch''s outcome (clicked / engaged / converted / ignored) feeds back into the next NBA computation so the decisioning learns. Exit on: conversion event (deal_created / subscription_created / activation_milestone — depending on lifecycle), unsubscribe, or sustained no-engagement (NBA returns wait 3 gates in a row → suppress).'
      prompt: 'Build an adaptive journey wired to the NBA segment. At each gate (signup+7d, +14d, +30d, +60d, ongoing weekly), the journey reads next_best_action attribute and routes the user down the matching branch: educate → email variant a; nurture → email variant b; offer → email variant c with discount; surface-feature → in-app tooltip + email variant d; surface-recommendations → activate recommendation surface + email digest with recs; handoff-to-agent → trigger agent conversation; wait → skip touch, recompute next gate. Each branch''s outcome (clicked / engaged / converted / ignored) feeds back into the next NBA computation so the decisioning learns. Exit on: conversion event (deal_created / subscription_created / activation_milestone — depending on lifecycle), unsubscribe, or sustained no-engagement (NBA returns wait 3 gates in a row → suppress).'
    - step: 7
      title: Build NBA Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - nba_attribute
      - segment
      - email_asset
      - inapp_asset
      - rec_surface
      - journey
      description: 'Compose an NBA orchestration dashboard: distribution of recommended_action across users (which actions does the model favor — sanity check on model balance), per-branch engagement rates (which actions actually convert), confidence-vs-conversion correlation (does higher-confidence routing actually predict higher conversion — model-quality signal), uplift vs control (a 5-10% holdout that gets fixed cadence — the proof-of-value chart), and per-segment NBA quality (model may serve some segments better than others — informs retraining priorities).'
      prompt: 'Compose an NBA orchestration dashboard: distribution of recommended_action across users (which actions does the model favor — sanity check on model balance), per-branch engagement rates (which actions actually convert), confidence-vs-conversion correlation (does higher-confidence routing actually predict higher conversion — model-quality signal), uplift vs control (a 5-10% holdout that gets fixed cadence — the proof-of-value chart), and per-segment NBA quality (model may serve some segments better than others — informs retraining priorities).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Next Best Action Orchestration

## Procedure

1. **Build Next-Best-Action AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'next_best_action' on the User object, refreshed daily and on every significant behavioral event. Inputs: current lifecycle stage, engagement velocity (sessions trend), feature usage breadth, recent intent signals (pricing visit, feature first-click, support touch), and prior message engagement. Outputs: a structured object with (a) recommended_action one of [educate / nurture / offer / surface-feature / surface-recommendations / handoff-to-agent / wait]; (b) recommended_channel [email / sms / in_app / push / slack-internal]; (c) recommended_content_theme; (d) confidence (0-100); (e) expected_uplift_signal. The attribute is the decisioning brain — the journey routes from it at each gate. → produces: attribute
2. **Identify NBA-Ready Cohort** [`create_segment`] — Build a segment 'NBA-orchestrated users' capturing active users where next_best_action.confidence >= 50 AND user is not currently in another high-priority journey (no double-orchestration). Refreshed continuously — as users' NBA changes, they move between sub-cohorts of this parent segment. → produces: segment
3. **Author Branch Content** [`create_email_content`] — Generate email content variants per recommended_action: (a) educate variant — short value tip matched to the user's stage; (b) nurture variant — case study/customer story relevant to user's segment; (c) offer variant — personalized incentive (discount / trial extension / credit) matched to plan and tenure; (d) surface-feature variant — feature spotlight with deep-link to the in-app destination. Each variant pulls dynamic content blocks based on the user's full profile, not just first name. → produces: asset
4. **Author In-App Branch Content** [`create_page_content`] — Generate in-app message variants for the surface-feature and surface-recommendations branches. Surface-feature: contextual tooltip pointing to the feature, with a 1-line value prop and 'try it' CTA, rendered in the relevant in-app location. Surface-recommendations: a personalized recommendation card pulling from the user's product affinity. In-app fires only during active sessions, never outside the app (avoids interruption fatigue). → produces: asset
5. **Build Branch Recommendation Surface** [`create_recommendation`] — Configure a recommendation surface 'NBA-driven product/content recs' that activates when next_best_action.recommended_action = surface-recommendations. Sources: the user's prior interaction history + similar-user purchase/usage patterns + currently-trending items in their segment. Render in: in-app sidebar + email content block + page personalization slot. Refresh weekly. → produces: recommendation
6. **Build NBA-Routed Journey** [`create_journey`] — Build an adaptive journey wired to the NBA segment. At each gate (signup+7d, +14d, +30d, +60d, ongoing weekly), the journey reads next_best_action attribute and routes the user down the matching branch: educate → email variant a; nurture → email variant b; offer → email variant c with discount; surface-feature → in-app tooltip + email variant d; surface-recommendations → activate recommendation surface + email digest with recs; handoff-to-agent → trigger agent conversation; wait → skip touch, recompute next gate. Each branch's outcome (clicked / engaged / converted / ignored) feeds back into the next NBA computation so the decisioning learns. Exit on: conversion event (deal_created / subscription_created / activation_milestone — depending on lifecycle), unsubscribe, or sustained no-engagement (NBA returns wait 3 gates in a row → suppress). → produces: journey
7. **Build NBA Performance Dashboard** [`create_dashboard`] — Compose an NBA orchestration dashboard: distribution of recommended_action across users (which actions does the model favor — sanity check on model balance), per-branch engagement rates (which actions actually convert), confidence-vs-conversion correlation (does higher-confidence routing actually predict higher conversion — model-quality signal), uplift vs control (a 5-10% holdout that gets fixed cadence — the proof-of-value chart), and per-segment NBA quality (model may serve some segments better than others — informs retraining priorities). → produces: dashboard
