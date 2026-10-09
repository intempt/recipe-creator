---
name: aha-moment-activation
description: Use when a user mentions "aha moment activation", "first key action reinforcement", "activation journey", or asks for related help. When a user completes their product's defined aha-moment action (the activation event that predicts retention), fire a reinforcement journey, congratulate, deepen engagement with the next-step feature, and educate around expansion to prevent post-aha dropoff.
arguments: []
intempt:
  id: aha-moment-activation
  title: "Aha moment reinforcement"
  version: 1.0.0
  slashCommand: /aha-moment-activation
  group: Journeys
  shortDescription: "Follows up right after someone hits the action that predicts retention, so the first win turns into a habit instead of a one off."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [activation, aha-moment, early-engagement]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: feature_first_used, severity: blocking }
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Find people who just got value"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Anyone who completed your activation event in the last 14 days and has not been through this follow up yet. Your product team picks that event off the retention curve, for example first message sent or first project published."
      prompt: Build a segment 'Recent aha-moment achievers' capturing users who completed the aha-moment event (defined per product, e.g. 'first message sent', 'first project published', 'first deal created'; configurable in the segment definition) in the last 14 days AND who haven't received the activation reinforcement yet. The aha-moment event is product-specific and should be set by Product team based on retention curve analysis.
    - step: 2
      title: "Write three follow up emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: "One that congratulates them and shows what others did after the same milestone, one that points to the natural next feature with a how to and a deep link, and one that shows how power users go further."
      prompt: 'Generate 3-touch reinforcement email content. Touch 1 (24 hours after aha): celebrate the milestone, frame it as a meaningful first step, share 1-2 success stories of users who achieved similar moments. Tone: warm, motivating. Touch 2 (Day 5): point to the natural next feature that complements the aha action (cross-sell within the product, not upsell to plan). Include a brief how-to and an in-app deep link. Touch 3 (Day 10): introduce a power-user behavior: ''now that you''ve [done aha], here''s how power users go further.'' Aim: shift user from ''tried it'' to ''depends on it''.'
    - step: 3
      title: "Send on days 1, 5 and 10"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      description: "Starts when the activation event fires, with emails on day 1, day 5 and day 10. If they find the next feature on their own by day 5, the middle email is skipped and they go straight to the power user one. They leave if they start paying, unsubscribe, or after 14 days."
      prompt: 'Build a 3-touch journey triggered when the aha-moment event (first feature used) fires. Touch 1: Day 1. Touch 2: Day 5. Touch 3: Day 10. Add a branch: if the user has already done the next-step feature naturally by Day 5 (great sign), skip touch 2 and go straight to touch 3 power-user content. Exit on: Subscription started (paid conversion: celebrate and handoff to free-to-paid-csm-kickoff), unsubscribe, or 14-day timeout.'
    - step: 4
      title: "Track activation and retention"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - journey
      description: "What share of signups reach the activation event, how long it takes them, and how their 30 day retention compares with people who never got there or never went through this follow up."
      prompt: 'Compose an activation funnel dashboard: aha-moment achievement rate among new signups (the activation rate: target depends on product, but trend matters more than absolute), time-from-signup-to-aha distribution, post-aha retention curve (do aha-achievers stick around better than non-achievers?: this is the proof-of-value of focusing activation efforts), and journey engagement by touch. Compare 30-day retention of aha-achievers who went through this journey vs. aha-achievers who didn''t (typical lift: 10-20% retention improvement).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Aha moment reinforcement

Follows up right after someone hits the action that predicts retention, so the first win turns into a habit instead of a one off.

## Before you run it

- Send the `feature_first_used` event

## What it does

1. **Find people who just got value** (`create_segment`)

   Anyone who completed your activation event in the last 14 days and has not been through this follow up yet. Your product team picks that event off the retention curve, for example first message sent or first project published.

2. **Write three follow up emails** (`create_email_content`)

   One that congratulates them and shows what others did after the same milestone, one that points to the natural next feature with a how to and a deep link, and one that shows how power users go further.

3. **Send on days 1, 5 and 10** (`create_journey`)

   Starts when the activation event fires, with emails on day 1, day 5 and day 10. If they find the next feature on their own by day 5, the middle email is skipped and they go straight to the power user one. They leave if they start paying, unsubscribe, or after 14 days.

4. **Track activation and retention** (`create_dashboard`)

   What share of signups reach the activation event, how long it takes them, and how their 30 day retention compares with people who never got there or never went through this follow up.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
