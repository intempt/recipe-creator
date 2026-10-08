---
id: next-best-action-orchestration
title: Next best action orchestration
slash_command: /next-best-action-orchestration
group: Journeys
owner: intempt
curator: somya
summary: >-
  A rules-based journey that routes each person to a next step from a candidate set using attributes and
  segment membership at branch points.
description: >-
  Build a journey with triggers, conditions, branches, and waits. Branch on attributes or segment membership
  to send email, show a page, surface a recommendation, or wait before the next step, then track outcomes in
  dashboards.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - saas
    - b2b
  industry:
    - ai
    - b2b-saas
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - ai-decisioning
    - next-best-action
    - adaptive-journey
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: feature_used
      severity: recommended
    - value: session_start
      severity: recommended
touches:
  reads:
    - The feature_used event in your project
    - The session_start event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Decide the next step per user"
    - A new segment, from step 2 "Only route confident calls"
    - A new designed email, from step 3 "Write an email per action"
    - A new landing page, from step 4 "Write the in app versions"
    - A new product recommendation, from step 5 "Build the recommendation set"
    - A new journey, from step 6 "Re-read the signal at each gate"
    - A new dashboard, from step 7 "Check the model against a control"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Decide the next step per user
    summary: >-
      Refreshed daily and on every meaningful event, from lifecycle stage, whether sessions are trending
      up or down, how many features they use, recent intent such as a pricing visit or a support touch,
      and how they responded to past messages. It returns the action to take, the channel, the content
      theme, a confidence score, and the uplift it expects.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'next_best_action' on the User object, refreshed daily and on every
      significant behavioral event. Inputs: current lifecycle stage, engagement velocity (sessions trend),
      feature usage breadth, recent intent signals (pricing visit, feature first-click, support touch),
      and prior message engagement. Outputs: a structured object with (a) recommended_action one of [educate
      / nurture / offer / surface-feature / surface-recommendations / handoff-to-agent / wait]; (b) recommended_channel
      [email / sms / in_app / push / slack-internal]; (c) recommended_content_theme; (d) confidence (0-100);
      (e) expected_uplift_signal. The attribute is the decisioning brain: the journey routes from it at
      each gate.
  - id: s2
    title: Only route confident calls
    summary: >-
      Active users whose confidence is 50 or above and who are not already in another high priority journey.
      It refreshes continuously, so people move between branches as their signal changes.
    builds: segment
    description: >-
      Build a segment 'NBA-orchestrated users' capturing active users where next_best_action.confidence
      >= 50 AND user is not currently in another high-priority journey (no double-orchestration). Refreshed
      continuously, as users' NBA changes, they move between sub-cohorts of this parent segment. Use the
      result of "Decide the next step per user".
    dependsOn:
      - s1
  - id: s3
    title: Write an email per action
    summary: >-
      A short value tip for teaching, a customer story for nurture, a personal incentive such as a discount,
      trial extension or credit for an offer, and a feature spotlight with a deep link. Each pulls content
      blocks from the whole profile, not just a first name.
    builds: email_html
    description: >-
      Generate email content variants per recommended_action: (a) educate variant (short value tip matched
      to the user's stage; (b) nurture variant) case study/customer story relevant to user's segment;
      (c) offer variant (personalized incentive (discount / trial extension / credit) matched to plan
      and tenure; (d) surface-feature variant) feature spotlight with deep-link to the in-app destination.
      Each variant pulls dynamic content blocks based on the user's full profile, not just first name.
      Use the result of "Decide the next step per user", "Only route confident calls".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Write the in app versions
    summary: >-
      A tooltip pointing at the feature with a one line reason and a try it button, and a recommendation
      card built from what they tend to use. These only appear during an active session.
    builds: page
    description: >-
      Generate in-app message variants for the surface-feature and surface-recommendations branches. Surface-feature:
      contextual tooltip pointing to the feature, with a 1-line value prop and 'try it' CTA, rendered
      in the relevant in-app location. Surface-recommendations: a personalized recommendation card pulling
      from the user's product affinity. In-app fires only during active sessions, never outside the app
      (avoids interruption fatigue). Use the result of "Decide the next step per user", "Only route confident
      calls", "Write an email per action".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Build the recommendation set
    summary: >-
      Fed by their own history, what similar users buy and use, and what is trending in their segment.
      It shows in the app sidebar, inside emails and in a page slot, and refreshes weekly.
    builds: recommendation
    description: >-
      Configure a recommendation surface 'NBA-driven product/content recs' that activates when next_best_action.recommended_action
      = surface-recommendations. Sources: the user's prior interaction history + similar-user purchase/usage
      patterns + currently-trending items in their segment. Render in: in-app sidebar + email content
      block + page personalization slot. Refresh weekly. Use the result of "Decide the next step per user",
      "Only route confident calls".
    dependsOn:
      - s1
      - s2
  - id: s6
    title: Re-read the signal at each gate
    summary: >-
      At day 7, 14, 30 and 60 after signup and weekly after that, the journey reads the recommendation
      and takes that branch: teach, nurture, offer, nudge a feature, surface recommendations, hand to
      an agent, or wait and recompute. What happens next feeds back into the decision. They leave on conversion,
      on unsubscribe, or after three waits in a row.
    builds: journey
    description: >-
      Build an adaptive journey wired to the NBA segment. At each gate (signup+7d, +14d, +30d, +60d, ongoing
      weekly), the journey reads next_best_action attribute and routes the user down the matching branch:
      educate to email variant a; nurture to email variant b; offer to email variant c with discount;
      surface-feature to in-app tooltip + email variant d; surface-recommendations to activate recommendation
      surface + email digest with recs; handoff-to-agent to trigger agent conversation; wait to skip touch,
      recompute next gate. Each branch's outcome (clicked / engaged / converted / ignored) feeds back
      into the next NBA computation so the decisioning learns. Exit on: conversion event (deal_created
      / subscription_created / activation_milestone: depending on lifecycle), unsubscribe, or sustained
      no-engagement (NBA returns wait 3 gates in a row to suppress). Use the result of "Decide the next
      step per user", "Only route confident calls", "Write an email per action", "Write the in app versions",
      "Build the recommendation set".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
  - id: s7
    title: Check the model against a control
    summary: >-
      Which actions the model picks and how often, engagement per branch, whether higher confidence really
      does mean higher conversion, the lift against a 5 to 10% holdout left on a fixed cadence, and which
      segments it serves worst.
    builds: dashboard
    description: >-
      Compose an NBA orchestration dashboard: distribution of recommended_action across users (which actions
      does the model favor: sanity check on model balance), per-branch engagement rates (which actions
      actually convert), confidence-vs-conversion correlation (does higher-confidence routing actually
      predict higher conversion (model-quality signal), uplift vs control (a 5-10% holdout that gets fixed
      cadence) the proof-of-value chart), and per-segment NBA quality (model may serve some segments better
      than others: informs retraining priorities). Use the result of "Decide the next step per user",
      "Only route confident calls", "Write an email per action", "Write the in app versions", "Build the
      recommendation set", "Re-read the signal at each gate".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
      - s6
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s4
    type: asset
    description: Asset produced by this recipe.
  - key: recommendation
    producedByStep: s5
    type: recommendation
    description: Recommendation Surface produced by this recipe.
  - key: journey
    producedByStep: s6
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s7
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Next best action orchestration

A rules-based journey that routes each person to a next step from a candidate set using attributes and segment membership at branch points.

## Steps

1. **Decide the next step per user** (builds attribute)

   Refreshed daily and on every meaningful event, from lifecycle stage, whether sessions are trending up or down, how many features they use, recent intent such as a pricing visit or a support touch, and how they responded to past messages. It returns the action to take, the channel, the content theme, a confidence score, and the uplift it expects.

2. **Only route confident calls** (builds segment)

   Active users whose confidence is 50 or above and who are not already in another high priority journey. It refreshes continuously, so people move between branches as their signal changes.

3. **Write an email per action** (builds email_html)

   A short value tip for teaching, a customer story for nurture, a personal incentive such as a discount, trial extension or credit for an offer, and a feature spotlight with a deep link. Each pulls content blocks from the whole profile, not just a first name.

4. **Write the in app versions** (builds page)

   A tooltip pointing at the feature with a one line reason and a try it button, and a recommendation card built from what they tend to use. These only appear during an active session.

5. **Build the recommendation set** (builds recommendation)

   Fed by their own history, what similar users buy and use, and what is trending in their segment. It shows in the app sidebar, inside emails and in a page slot, and refreshes weekly.

6. **Re-read the signal at each gate** (builds journey)

   At day 7, 14, 30 and 60 after signup and weekly after that, the journey reads the recommendation and takes that branch: teach, nurture, offer, nudge a feature, surface recommendations, hand to an agent, or wait and recompute. What happens next feeds back into the decision. They leave on conversion, on unsubscribe, or after three waits in a row.

7. **Check the model against a control** (builds dashboard)

   Which actions the model picks and how often, engagement per branch, whether higher confidence really does mean higher conversion, the lift against a 5 to 10% holdout left on a fixed cadence, and which segments it serves worst.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The feature_used event in your project
- The session_start event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Decide the next step per user"
- A new segment, from step 2 "Only route confident calls"
- A new designed email, from step 3 "Write an email per action"
- A new landing page, from step 4 "Write the in app versions"
- A new product recommendation, from step 5 "Build the recommendation set"
- A new journey, from step 6 "Re-read the signal at each gate"
- A new dashboard, from step 7 "Check the model against a control"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, page, recommendation.
