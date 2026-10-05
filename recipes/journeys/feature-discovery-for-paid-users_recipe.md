---
name: feature-discovery-for-paid-users
description: Use when a user mentions "feature discovery paid users", "unused feature nudge", "feature adoption journey", or asks for related help. For paid users who haven't touched key features after 30+ days, fire a feature-discovery nudge journey — one feature at a time, contextually relevant to their use case — preventing retention erosion from underutilization.
arguments: []
intempt:
  id: feature-discovery-for-paid-users
  version: 1.0.0
  slashCommand: /feature-discovery-for-paid-users
  group: Journeys
  shortDescription: "Create a weekly AI-derived User attribute ranking top 3 unused plan features, then enroll 30+ day inactive paid users in a one-feature email journey."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [feature-adoption, paid-user-engagement, retention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: feature_used, severity: blocking }
      - { value: subscription_created, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Untouched-Features Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: untouched_features
      description: 'Create an AI-derived attribute ''untouched_features'' on the User object. Computed weekly. For each user, compare features-touched in last 90 days against the catalog of features available on their plan, and surface the top 3 high-value features they haven''t used. Prioritize features by: (a) historical correlation with retention among similar users, (b) features the user''s use case (inferred from segment / industry / role) suggests they should benefit from. Excludes features that the user''s plan doesn''t include. Output: ranked list of 3 untouched features with the recommended order.'
      prompt: 'Create an AI-derived attribute ''untouched_features'' on the User object. Computed weekly. For each user, compare features-touched in last 90 days against the catalog of features available on their plan, and surface the top 3 high-value features they haven''t used. Prioritize features by: (a) historical correlation with retention among similar users, (b) features the user''s use case (inferred from segment / industry / role) suggests they should benefit from. Excludes features that the user''s plan doesn''t include. Output: ranked list of 3 untouched features with the recommended order.'
    - step: 2
      title: Identify Discovery Audience
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - untouched_features
      description: Build a segment 'Feature discovery audience' capturing paid users where subscription is at least 30 days old AND untouched_features list is non-empty AND the user has had at least 2 sessions in the last 14 days (active enough to benefit from a feature nudge). Excludes users in initial onboarding (different motion) and users who already received a feature-discovery nudge in the last 30 days.
      prompt: Build a segment 'Feature discovery audience' capturing paid users where subscription is at least 30 days old AND untouched_features list is non-empty AND the user has had at least 2 sessions in the last 14 days (active enough to benefit from a feature nudge). Excludes users in initial onboarding (different motion) and users who already received a feature-discovery nudge in the last 30 days.
    - step: 3
      title: Build Discovery Email Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - untouched_features
      - segment
      description: 'Generate per-feature discovery email templates (one template that pulls the top untouched feature per recipient). Subject: ''[First name], you haven''t tried [feature] yet'' — specific feature, specific benefit. Body: brief value statement of the feature (''Users who use [feature] save an average of [time/effort metric]''), a short use-case description that matches the user''s segment, a screenshot or short GIF showing the feature in action, and a deep-link CTA into the app at the right place. Tone: helpful nudge, not ''we noticed you''re not getting your money''s worth'' (which feels accusatory).'
      prompt: 'Generate per-feature discovery email templates (one template that pulls the top untouched feature per recipient). Subject: ''[First name], you haven''t tried [feature] yet'' — specific feature, specific benefit. Body: brief value statement of the feature (''Users who use [feature] save an average of [time/effort metric]''), a short use-case description that matches the user''s segment, a screenshot or short GIF showing the feature in action, and a deep-link CTA into the app at the right place. Tone: helpful nudge, not ''we noticed you''re not getting your money''s worth'' (which feels accusatory).'
    - step: 4
      title: Build Discovery Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - untouched_features
      - segment
      - asset
      description: 'Build a 3-touch journey triggered weekly for users in the feature-discovery segment. Each touch surfaces a DIFFERENT untouched feature from the user''s list (not the same feature 3 times). Touch 1: top feature, Day 0. Touch 2: second feature, Day 14. Touch 3: third feature, Day 28. Skip a touch if the user actually started using that feature between touches (they got the message — don''t pester). Exit on: user adopts all 3 features (success), user opens cancel-flow (handoff to pre-cancellation-save), or 60-day completion.'
      prompt: 'Build a 3-touch journey triggered weekly for users in the feature-discovery segment. Each touch surfaces a DIFFERENT untouched feature from the user''s list (not the same feature 3 times). Touch 1: top feature, Day 0. Touch 2: second feature, Day 14. Touch 3: third feature, Day 28. Skip a touch if the user actually started using that feature between touches (they got the message — don''t pester). Exit on: user adopts all 3 features (success), user opens cancel-flow (handoff to pre-cancellation-save), or 60-day completion.'
    - step: 5
      title: Build Feature Adoption Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - untouched_features
      - segment
      - asset
      - journey
      description: 'Compose a feature adoption dashboard: feature-discovery email volume by feature (which features need the most nudge — could signal weak in-app discoverability), feature-adoption rate after nudge (% of recipients who use the feature within 14 days of receiving the nudge — typical: 8-15%), retention lift from adoption (compare 90-day retention of users who adopted post-nudge vs. control), and untouched-feature distribution (which features are most-commonly never-touched — informs product team where the discoverability gaps are).'
      prompt: 'Compose a feature adoption dashboard: feature-discovery email volume by feature (which features need the most nudge — could signal weak in-app discoverability), feature-adoption rate after nudge (% of recipients who use the feature within 14 days of receiving the nudge — typical: 8-15%), retention lift from adoption (compare 90-day retention of users who adopted post-nudge vs. control), and untouched-feature distribution (which features are most-commonly never-touched — informs product team where the discoverability gaps are).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Feature Discovery For Paid Users

## Procedure

1. **Build Untouched-Features Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'untouched_features' on the User object. Computed weekly. For each user, compare features-touched in last 90 days against the catalog of features available on their plan, and surface the top 3 high-value features they haven't used. Prioritize features by: (a) historical correlation with retention among similar users, (b) features the user's use case (inferred from segment / industry / role) suggests they should benefit from. Excludes features that the user's plan doesn't include. Output: ranked list of 3 untouched features with the recommended order. → produces: attribute
2. **Identify Discovery Audience** [`create_segment`] — Build a segment 'Feature discovery audience' capturing paid users where subscription is at least 30 days old AND untouched_features list is non-empty AND the user has had at least 2 sessions in the last 14 days (active enough to benefit from a feature nudge). Excludes users in initial onboarding (different motion) and users who already received a feature-discovery nudge in the last 30 days. → produces: segment
3. **Build Discovery Email Content** [`create_email_content`] — Generate per-feature discovery email templates (one template that pulls the top untouched feature per recipient). Subject: '[First name], you haven't tried [feature] yet' — specific feature, specific benefit. Body: brief value statement of the feature ('Users who use [feature] save an average of [time/effort metric]'), a short use-case description that matches the user's segment, a screenshot or short GIF showing the feature in action, and a deep-link CTA into the app at the right place. Tone: helpful nudge, not 'we noticed you're not getting your money's worth' (which feels accusatory). → produces: asset
4. **Build Discovery Journey** [`create_journey`] — Build a 3-touch journey triggered weekly for users in the feature-discovery segment. Each touch surfaces a DIFFERENT untouched feature from the user's list (not the same feature 3 times). Touch 1: top feature, Day 0. Touch 2: second feature, Day 14. Touch 3: third feature, Day 28. Skip a touch if the user actually started using that feature between touches (they got the message — don't pester). Exit on: user adopts all 3 features (success), user opens cancel-flow (handoff to pre-cancellation-save), or 60-day completion. → produces: journey
5. **Build Feature Adoption Dashboard** [`create_dashboard`] — Compose a feature adoption dashboard: feature-discovery email volume by feature (which features need the most nudge — could signal weak in-app discoverability), feature-adoption rate after nudge (% of recipients who use the feature within 14 days of receiving the nudge — typical: 8-15%), retention lift from adoption (compare 90-day retention of users who adopted post-nudge vs. control), and untouched-feature distribution (which features are most-commonly never-touched — informs product team where the discoverability gaps are). → produces: dashboard
