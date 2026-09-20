---
name: next-best-action-orchestration
description: Use when a user mentions "next best action orchestration", "AI decisioning journey", "per-user adaptive journey", or asks for related help. AI-decisioning journey where the next step is selected per-user from a candidate set (content / offer / feature-nudge / human-touch / recommendation surface) based on a live AI attribute, replaces fixed cadences with adaptive paths that match each user's signal at decision time.
arguments: []
intempt:
  id: next-best-action-orchestration
  title: "Next best action orchestration"
  version: 1.0.0
  slashCommand: /next-best-action-orchestration
  group: Journeys
  shortDescription: "Picks each person's next step from their live signal instead of a fixed cadence: teach, nurture, offer, nudge a feature, recommend, hand off, or wait."
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
    integrations:
      - { value: slack, severity: recommended }
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
      title: "Decide the next step per user"
      command: create_ai_attribute
      produces: attribute
      bindsAs: nba_attribute
      description: "Refreshed daily and on every meaningful event, from lifecycle stage, whether sessions are trending up or down, how many features they use, recent intent such as a pricing visit or a support touch, and how they responded to past messages. It returns the action to take, the channel, the content theme, a confidence score, and the uplift it expects."
      prompt: 'Create an AI-derived attribute ''next_best_action'' on the User object, refreshed daily and on every significant behavioral event. Inputs: current lifecycle stage, engagement velocity (sessions trend), feature usage breadth, recent intent signals (pricing visit, feature first-click, support touch), and prior message engagement. Outputs: a structured object with (a) recommended_action one of [educate / nurture / offer / surface-feature / surface-recommendations / handoff-to-agent / wait]; (b) recommended_channel [email / sms / in_app / push / slack-internal]; (c) recommended_content_theme; (d) confidence (0-100); (e) expected_uplift_signal. The attribute is the decisioning brain: the journey routes from it at each gate.'
    - step: 2
      title: "Only route confident calls"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - nba_attribute
      description: "Active users whose confidence is 50 or above and who are not already in another high priority journey. It refreshes continuously, so people move between branches as their signal changes."
      prompt: Build a segment 'NBA-orchestrated users' capturing active users where next_best_action.confidence >= 50 AND user is not currently in another high-priority journey (no double-orchestration). Refreshed continuously, as users' NBA changes, they move between sub-cohorts of this parent segment.
    - step: 3
      title: "Write an email per action"
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - nba_attribute
      - segment
      description: "A short value tip for teaching, a customer story for nurture, a personal incentive such as a discount, trial extension or credit for an offer, and a feature spotlight with a deep link. Each pulls content blocks from the whole profile, not just a first name."
      prompt: 'Generate email content variants per recommended_action: (a) educate variant (short value tip matched to the user''s stage; (b) nurture variant) case study/customer story relevant to user''s segment; (c) offer variant (personalized incentive (discount / trial extension / credit) matched to plan and tenure; (d) surface-feature variant) feature spotlight with deep-link to the in-app destination. Each variant pulls dynamic content blocks based on the user''s full profile, not just first name.'
    - step: 4
      title: "Write the in app versions"
      command: create_page_content
      produces: asset
      bindsAs: inapp_asset
      dependsOn:
      - nba_attribute
      - segment
      - email_asset
      description: "A tooltip pointing at the feature with a one line reason and a try it button, and a recommendation card built from what they tend to use. These only appear during an active session."
      prompt: 'Generate in-app message variants for the surface-feature and surface-recommendations branches. Surface-feature: contextual tooltip pointing to the feature, with a 1-line value prop and ''try it'' CTA, rendered in the relevant in-app location. Surface-recommendations: a personalized recommendation card pulling from the user''s product affinity. In-app fires only during active sessions, never outside the app (avoids interruption fatigue).'
    - step: 5
      title: "Build the recommendation set"
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - nba_attribute
      - segment
      description: "Fed by their own history, what similar users buy and use, and what is trending in their segment. It shows in the app sidebar, inside emails and in a page slot, and refreshes weekly."
      prompt: 'Configure a recommendation surface ''NBA-driven product/content recs'' that activates when next_best_action.recommended_action = surface-recommendations. Sources: the user''s prior interaction history + similar-user purchase/usage patterns + currently-trending items in their segment. Render in: in-app sidebar + email content block + page personalization slot. Refresh weekly.'
    - step: 6
      title: "Re-read the signal at each gate"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - nba_attribute
      - segment
      - email_asset
      - inapp_asset
      - rec_surface
      description: "At day 7, 14, 30 and 60 after signup and weekly after that, the journey reads the recommendation and takes that branch: teach, nurture, offer, nudge a feature, surface recommendations, hand to an agent, or wait and recompute. What happens next feeds back into the decision. They leave on conversion, on unsubscribe, or after three waits in a row."
      prompt: 'Build an adaptive journey wired to the NBA segment. At each gate (signup+7d, +14d, +30d, +60d, ongoing weekly), the journey reads next_best_action attribute and routes the user down the matching branch: educate to email variant a; nurture to email variant b; offer to email variant c with discount; surface-feature to in-app tooltip + email variant d; surface-recommendations to activate recommendation surface + email digest with recs; handoff-to-agent to trigger agent conversation; wait to skip touch, recompute next gate. Each branch''s outcome (clicked / engaged / converted / ignored) feeds back into the next NBA computation so the decisioning learns. Exit on: conversion event (deal_created / subscription_created / activation_milestone: depending on lifecycle), unsubscribe, or sustained no-engagement (NBA returns wait 3 gates in a row to suppress).'
    - step: 7
      title: "Check the model against a control"
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
      description: "Which actions the model picks and how often, engagement per branch, whether higher confidence really does mean higher conversion, the lift against a 5 to 10% holdout left on a fixed cadence, and which segments it serves worst."
      prompt: 'Compose an NBA orchestration dashboard: distribution of recommended_action across users (which actions does the model favor: sanity check on model balance), per-branch engagement rates (which actions actually convert), confidence-vs-conversion correlation (does higher-confidence routing actually predict higher conversion (model-quality signal), uplift vs control (a 5-10% holdout that gets fixed cadence) the proof-of-value chart), and per-segment NBA quality (model may serve some segments better than others: informs retraining priorities).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Next best action orchestration

Picks each person's next step from their live signal instead of a fixed cadence: teach, nurture, offer, nudge a feature, recommend, hand off, or wait.

## Before you run it

- Connect slack
- Send the `feature_used` event
- Send the `session_start` event

## What it does

1. **Decide the next step per user** (`create_ai_attribute`)

   Refreshed daily and on every meaningful event, from lifecycle stage, whether sessions are trending up or down, how many features they use, recent intent such as a pricing visit or a support touch, and how they responded to past messages. It returns the action to take, the channel, the content theme, a confidence score, and the uplift it expects.

2. **Only route confident calls** (`create_segment`)

   Active users whose confidence is 50 or above and who are not already in another high priority journey. It refreshes continuously, so people move between branches as their signal changes.

3. **Write an email per action** (`create_email_content`)

   A short value tip for teaching, a customer story for nurture, a personal incentive such as a discount, trial extension or credit for an offer, and a feature spotlight with a deep link. Each pulls content blocks from the whole profile, not just a first name.

4. **Write the in app versions** (`create_page_content`)

   A tooltip pointing at the feature with a one line reason and a try it button, and a recommendation card built from what they tend to use. These only appear during an active session.

5. **Build the recommendation set** (`create_recommendation`)

   Fed by their own history, what similar users buy and use, and what is trending in their segment. It shows in the app sidebar, inside emails and in a page slot, and refreshes weekly.

6. **Re-read the signal at each gate** (`create_journey`)

   At day 7, 14, 30 and 60 after signup and weekly after that, the journey reads the recommendation and takes that branch: teach, nurture, offer, nudge a feature, surface recommendations, hand to an agent, or wait and recompute. What happens next feeds back into the decision. They leave on conversion, on unsubscribe, or after three waits in a row.

7. **Check the model against a control** (`create_dashboard`)

   Which actions the model picks and how often, engagement per branch, whether higher confidence really does mean higher conversion, the lift against a 5 to 10% holdout left on a fixed cadence, and which segments it serves worst.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
