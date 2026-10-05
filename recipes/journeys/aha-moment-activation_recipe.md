---
name: aha-moment-activation
description: Use when a user mentions "aha moment activation", "first key action reinforcement", "activation journey", or asks for related help. When a user completes their product's defined aha-moment action (the activation event that predicts retention), fire a reinforcement journey — congratulate, deepen engagement with the next-step feature, and educate around expansion to prevent post-aha dropoff.
arguments: []
intempt:
  id: aha-moment-activation
  version: 1.0.0
  slashCommand: /aha-moment-activation
  group: Journeys
  shortDescription: "Builds a 'Recent aha-moment achievers' segment from the product-defined activation event and enrols those users in a 3-touch reinforcement email journey."
  availability: coming-soon
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
      title: Identify Aha-Moment Achievers
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Recent aha-moment achievers' capturing users who completed the aha-moment event (defined per product — e.g. 'first message sent', 'first project published', 'first deal created'; configurable in the segment definition) in the last 14 days AND who haven't received the activation reinforcement yet. The aha-moment event is product-specific and should be set by Product team based on retention curve analysis.
      prompt: Build a segment 'Recent aha-moment achievers' capturing users who completed the aha-moment event (defined per product — e.g. 'first message sent', 'first project published', 'first deal created'; configurable in the segment definition) in the last 14 days AND who haven't received the activation reinforcement yet. The aha-moment event is product-specific and should be set by Product team based on retention curve analysis.
    - step: 2
      title: Build Reinforcement Email Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: 'Generate 3-touch reinforcement email content. Touch 1 (24 hours after aha): celebrate the milestone, frame it as a meaningful first step, share 1-2 success stories of users who achieved similar moments. Tone: warm, motivating. Touch 2 (Day 5): point to the natural next feature that complements the aha action (cross-sell within the product, not upsell to plan). Include a brief how-to and an in-app deep link. Touch 3 (Day 10): introduce a power-user behavior — ''now that you''ve [done aha], here''s how power users go further.'' Aim: shift user from ''tried it'' to ''depends on it''.'
      prompt: 'Generate 3-touch reinforcement email content. Touch 1 (24 hours after aha): celebrate the milestone, frame it as a meaningful first step, share 1-2 success stories of users who achieved similar moments. Tone: warm, motivating. Touch 2 (Day 5): point to the natural next feature that complements the aha action (cross-sell within the product, not upsell to plan). Include a brief how-to and an in-app deep link. Touch 3 (Day 10): introduce a power-user behavior — ''now that you''ve [done aha], here''s how power users go further.'' Aim: shift user from ''tried it'' to ''depends on it''.'
    - step: 3
      title: Build Activation Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      description: 'Build a 3-touch journey triggered when feature_first_used = aha-moment fires. Touch 1: Day 1. Touch 2: Day 5. Touch 3: Day 10. Add a branch: if the user has already done the next-step feature naturally by Day 5 (great sign), skip touch 2 and go straight to touch 3 power-user content. Exit on: subscription_created (paid conversion — celebrate and handoff to free-to-paid-csm-kickoff), unsubscribe, or 14-day timeout.'
      prompt: 'Build a 3-touch journey triggered when feature_first_used = aha-moment fires. Touch 1: Day 1. Touch 2: Day 5. Touch 3: Day 10. Add a branch: if the user has already done the next-step feature naturally by Day 5 (great sign), skip touch 2 and go straight to touch 3 power-user content. Exit on: subscription_created (paid conversion — celebrate and handoff to free-to-paid-csm-kickoff), unsubscribe, or 14-day timeout.'
    - step: 4
      title: Build Activation Funnel Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - journey
      description: 'Compose an activation funnel dashboard: aha-moment achievement rate among new signups (the activation rate — target depends on product, but trend matters more than absolute), time-from-signup-to-aha distribution, post-aha retention curve (do aha-achievers stick around better than non-achievers? — this is the proof-of-value of focusing activation efforts), and journey engagement by touch. Compare 30-day retention of aha-achievers who went through this journey vs. aha-achievers who didn''t (typical lift: 10-20% retention improvement).'
      prompt: 'Compose an activation funnel dashboard: aha-moment achievement rate among new signups (the activation rate — target depends on product, but trend matters more than absolute), time-from-signup-to-aha distribution, post-aha retention curve (do aha-achievers stick around better than non-achievers? — this is the proof-of-value of focusing activation efforts), and journey engagement by touch. Compare 30-day retention of aha-achievers who went through this journey vs. aha-achievers who didn''t (typical lift: 10-20% retention improvement).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Aha Moment Activation

## Procedure

1. **Identify Aha-Moment Achievers** [`create_segment`] — Build a segment 'Recent aha-moment achievers' capturing users who completed the aha-moment event (defined per product — e.g. 'first message sent', 'first project published', 'first deal created'; configurable in the segment definition) in the last 14 days AND who haven't received the activation reinforcement yet. The aha-moment event is product-specific and should be set by Product team based on retention curve analysis. → produces: segment
2. **Build Reinforcement Email Content** [`create_email_content`] — Generate 3-touch reinforcement email content. Touch 1 (24 hours after aha): celebrate the milestone, frame it as a meaningful first step, share 1-2 success stories of users who achieved similar moments. Tone: warm, motivating. Touch 2 (Day 5): point to the natural next feature that complements the aha action (cross-sell within the product, not upsell to plan). Include a brief how-to and an in-app deep link. Touch 3 (Day 10): introduce a power-user behavior — 'now that you've [done aha], here's how power users go further.' Aim: shift user from 'tried it' to 'depends on it'. → produces: asset
3. **Build Activation Journey** [`create_journey`] — Build a 3-touch journey triggered when feature_first_used = aha-moment fires. Touch 1: Day 1. Touch 2: Day 5. Touch 3: Day 10. Add a branch: if the user has already done the next-step feature naturally by Day 5 (great sign), skip touch 2 and go straight to touch 3 power-user content. Exit on: subscription_created (paid conversion — celebrate and handoff to free-to-paid-csm-kickoff), unsubscribe, or 14-day timeout. → produces: journey
4. **Build Activation Funnel Dashboard** [`create_dashboard`] — Compose an activation funnel dashboard: aha-moment achievement rate among new signups (the activation rate — target depends on product, but trend matters more than absolute), time-from-signup-to-aha distribution, post-aha retention curve (do aha-achievers stick around better than non-achievers? — this is the proof-of-value of focusing activation efforts), and journey engagement by touch. Compare 30-day retention of aha-achievers who went through this journey vs. aha-achievers who didn't (typical lift: 10-20% retention improvement). → produces: dashboard
