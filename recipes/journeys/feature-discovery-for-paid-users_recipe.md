---
name: feature-discovery-for-paid-users
description: Use when a user mentions "feature discovery paid users", "unused feature nudge", "feature adoption journey", or asks for related help. For paid users who haven't touched key features after 30+ days, fire a feature-discovery nudge journey (one feature at a time, contextually relevant to their use case) preventing retention erosion from underutilization.
arguments: []
intempt:
  id: feature-discovery-for-paid-users
  title: "Feature discovery for paid users"
  version: 1.0.0
  slashCommand: /feature-discovery-for-paid-users
  group: Journeys
  shortDescription: "Shows paying customers the features they have never opened, one at a time, picked for the way they actually use the product."
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
      title: "Find features they never use"
      command: create_ai_attribute
      produces: attribute
      bindsAs: untouched_features
      description: "Weekly, for each user: the features on their plan they have not touched in 90 days, cut to the top three by how strongly each correlates with retention for similar users and how well it fits their role and industry."
      prompt: 'Create an AI-derived attribute ''untouched_features'' on the User object. Computed weekly. For each user, compare features-touched in last 90 days against the catalog of features available on their plan, and surface the top 3 high-value features they haven''t used. Prioritize features by: (a) historical correlation with retention among similar users, (b) features the user''s use case (inferred from segment / industry / role) suggests they should benefit from. Excludes features that the user''s plan doesn''t include. Output: ranked list of 3 untouched features with the recommended order.'
    - step: 2
      title: "Pick who is worth nudging"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - untouched_features
      description: "Paid users at least 30 days in, with at least one untouched feature and two or more sessions in the last 14 days. People still onboarding are left out, and so is anyone already nudged in the last 30 days."
      prompt: Build a segment 'Feature discovery audience' capturing paid users where subscription is at least 30 days old AND untouched_features list is non-empty AND the user has had at least 2 sessions in the last 14 days (active enough to benefit from a feature nudge). Excludes users in initial onboarding (different motion) and users who already received a feature-discovery nudge in the last 30 days.
    - step: 3
      title: "Write the nudge"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - untouched_features
      - segment
      description: "The subject names the feature. The body gives what it saves, a use case that matches their segment, a screenshot or short clip, and a link straight into the right screen. A helpful nudge, not a note about getting their money's worth."
      prompt: 'Generate per-feature discovery email templates (one template that pulls the top untouched feature per recipient). Subject: ''[First name], you haven''t tried [feature] yet'': specific feature, specific benefit. Body: brief value statement of the feature (''Users who use [feature] save an average of [time/effort metric]''), a short use-case description that matches the user''s segment, a screenshot or short GIF showing the feature in action, and a deep-link CTA into the app at the right place. Tone: helpful nudge, not ''we noticed you''re not getting your money''s worth'' (which feels accusatory).'
    - step: 4
      title: "One feature every two weeks"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - untouched_features
      - segment
      - asset
      description: "Three emails on day 0, day 14 and day 28, each about a different untouched feature. If they start using one in between, that email is skipped. They leave once all three are adopted, if they open the cancel flow, or after 60 days."
      prompt: 'Build a 3-touch journey triggered weekly for users in the feature-discovery segment. Each touch surfaces a DIFFERENT untouched feature from the user''s list (not the same feature 3 times). Touch 1: top feature, Day 0. Touch 2: second feature, Day 14. Touch 3: third feature, Day 28. Skip a touch if the user actually started using that feature between touches (they got the message: don''t pester). Exit on: user adopts all 3 features (success), user opens cancel-flow (handoff to pre-cancellation-save), or 60-day completion.'
    - step: 5
      title: "See what the nudges actually change"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - untouched_features
      - segment
      - asset
      - journey
      description: "Emails per feature, how many people use the feature within 14 days of a nudge, the 90 day retention of those who adopted against a control, and which features go untouched most often."
      prompt: 'Compose a feature adoption dashboard: feature-discovery email volume by feature (which features need the most nudge: could signal weak in-app discoverability), feature-adoption rate after nudge (% of recipients who use the feature within 14 days of receiving the nudge: typical: 8-15%), retention lift from adoption (compare 90-day retention of users who adopted post-nudge vs. control), and untouched-feature distribution (which features are most-commonly never-touched: informs product team where the discoverability gaps are).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Feature discovery for paid users

Shows paying customers the features they have never opened, one at a time, picked for the way they actually use the product.

## Before you run it

- Send the `feature_used` event
- Send the `subscription_created` event

## What it does

1. **Find features they never use** (`create_ai_attribute`)

   Weekly, for each user: the features on their plan they have not touched in 90 days, cut to the top three by how strongly each correlates with retention for similar users and how well it fits their role and industry.

2. **Pick who is worth nudging** (`create_segment`)

   Paid users at least 30 days in, with at least one untouched feature and two or more sessions in the last 14 days. People still onboarding are left out, and so is anyone already nudged in the last 30 days.

3. **Write the nudge** (`create_email_content`)

   The subject names the feature. The body gives what it saves, a use case that matches their segment, a screenshot or short clip, and a link straight into the right screen. A helpful nudge, not a note about getting their money's worth.

4. **One feature every two weeks** (`create_journey`)

   Three emails on day 0, day 14 and day 28, each about a different untouched feature. If they start using one in between, that email is skipped. They leave once all three are adopted, if they open the cancel flow, or after 60 days.

5. **See what the nudges actually change** (`create_dashboard`)

   Emails per feature, how many people use the feature within 14 days of a nudge, the 90 day retention of those who adopted against a control, and which features go untouched most often.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
