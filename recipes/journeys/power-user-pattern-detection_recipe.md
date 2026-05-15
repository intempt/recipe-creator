---
name: power-user-pattern-detection
description: Use when a user mentions "power user pattern detection", "manual workflow detection", "automation upgrade journey", or asks for related help. Detect users repeatedly performing manual workflows that the product can automate (5+ same task in 7 days, batch operations being done one-at-a-time, repeat exports) → surface the relevant power-feature contextually via in-app + recommendation surface, then invite to advocacy program if adopted.
arguments: []
intempt:
  id: power-user-pattern-detection
  version: 1.0.0
  slashCommand: /power-user-pattern-detection
  group: Journeys
  shortDescription: "Detect users repeatedly performing manual workflows that the product can automate (5+ same task in 7 days, batch operations being done one-at-a-time, repeat exports) → surface the relevant power-feature contextually via in-app + recommendation surface, then invite to advocacy program if adopted."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [power-user-detection, feature-discovery, advocacy-pipeline]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: feature_used, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_page_content
    - create_recommendation
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Manual-Pattern AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: manual_pattern
      description: 'Create an AI-derived attribute ''detected_manual_patterns'' on the User object, refreshed daily. Detects repeated manual sequences that have automated counterparts in the product. Example patterns: (a) user runs same multi-step report 5+ times in 7 days (has unused ''scheduled reports'' feature), (b) user exports data manually 3+ times in 7 days (has unused API/webhook feature), (c) user assigns same task type repeatedly (has unused task templates feature), (d) user filters dashboard same way 10+ times in 14 days (has unused saved-view feature). Output: list of detected patterns with the automate-it feature name and adoption-likelihood score (based on user''s plan, skill level, prior automation adoption).'
      prompt: 'Create an AI-derived attribute ''detected_manual_patterns'' on the User object, refreshed daily. Detects repeated manual sequences that have automated counterparts in the product. Example patterns: (a) user runs same multi-step report 5+ times in 7 days (has unused ''scheduled reports'' feature), (b) user exports data manually 3+ times in 7 days (has unused API/webhook feature), (c) user assigns same task type repeatedly (has unused task templates feature), (d) user filters dashboard same way 10+ times in 14 days (has unused saved-view feature). Output: list of detected patterns with the automate-it feature name and adoption-likelihood score (based on user''s plan, skill level, prior automation adoption).'
    - step: 2
      title: Identify Power-User Candidates
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - manual_pattern
      description: Build a segment 'Manual-pattern detected' capturing paying users where detected_manual_patterns is non-empty AND the user hasn't yet used the recommended automation feature. Partitioned by feature-to-introduce. Excludes users who have dismissed feature-recommendations 3+ times (respect the no) and users with plan limits that exclude the suggested feature.
      prompt: Build a segment 'Manual-pattern detected' capturing paying users where detected_manual_patterns is non-empty AND the user hasn't yet used the recommended automation feature. Partitioned by feature-to-introduce. Excludes users who have dismissed feature-recommendations 3+ times (respect the no) and users with plan limits that exclude the suggested feature.
    - step: 3
      title: Build Contextual In-App Nudge
      command: create_page_content
      produces: asset
      bindsAs: inapp_asset
      dependsOn:
      - manual_pattern
      - segment
      description: 'Generate in-app nudge content per detected pattern. Format: tooltip or floating card that appears WHEN the user is mid-pattern (e.g. on their 6th manual export). Content: ''You''ve done this 6 times this week — did you know [Product] can automate this?'' + 60-second ''how it works'' GIF + ''enable now'' CTA + dismiss option. Renders at the exact moment of friction, not in a generic feature-discovery surface. The contextual timing is the magic — this is the 4x feature-adoption uplift pattern from the research.'
      prompt: 'Generate in-app nudge content per detected pattern. Format: tooltip or floating card that appears WHEN the user is mid-pattern (e.g. on their 6th manual export). Content: ''You''ve done this 6 times this week — did you know [Product] can automate this?'' + 60-second ''how it works'' GIF + ''enable now'' CTA + dismiss option. Renders at the exact moment of friction, not in a generic feature-discovery surface. The contextual timing is the magic — this is the 4x feature-adoption uplift pattern from the research.'
    - step: 4
      title: Build Power-Feature Recommendation Surface
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - manual_pattern
      - segment
      description: 'Configure a recommendation surface ''Power features for your workflow'' on the user''s dashboard. Pulls: the top 3 detected_manual_patterns with their automate-it counterparts, ranked by adoption-likelihood. Each recommendation: 1-line description + ''try it'' deep link. Updates when user adopts a feature (rotates in the next-best). Renders persistently for 30 days after detection.'
      prompt: 'Configure a recommendation surface ''Power features for your workflow'' on the user''s dashboard. Pulls: the top 3 detected_manual_patterns with their automate-it counterparts, ranked by adoption-likelihood. Each recommendation: 1-line description + ''try it'' deep link. Updates when user adopts a feature (rotates in the next-best). Renders persistently for 30 days after detection.'
    - step: 5
      title: Build Advocacy Follow-up Content
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - manual_pattern
      - segment
      description: 'Generate follow-up email content sent 14 days after a user adopts a recommended automation feature. Content: ''Congrats on automating [feature] — you''ve saved an estimated [time] per week. Mind sharing your experience?'' Two CTAs: write a review on G2/Capterra (with deep-link to the right product page), refer a peer (with referral program info). This is where power-user-detection becomes an advocacy pipeline — the user just had a positive experience, the moment is warm.'
      prompt: 'Generate follow-up email content sent 14 days after a user adopts a recommended automation feature. Content: ''Congrats on automating [feature] — you''ve saved an estimated [time] per week. Mind sharing your experience?'' Two CTAs: write a review on G2/Capterra (with deep-link to the right product page), refer a peer (with referral program info). This is where power-user-detection becomes an advocacy pipeline — the user just had a positive experience, the moment is warm.'
    - step: 6
      title: Build Power-User Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - manual_pattern
      - segment
      - inapp_asset
      - rec_surface
      - email_asset
      description: 'Build a journey wired to manual-pattern-detected segment. Touch 1 (real-time, on the 5th+ pattern repetition mid-session): in-app contextual nudge fires. Recommendation surface activates persistently. Touch 2 (Day 3, if user didn''t dismiss): email reinforcement with the same feature pitch + a customer story of someone who automated it. Touch 3 (Day 14, IF user has adopted the feature): advocacy follow-up email asking for review/referral. Touch 4 (Day 14, IF user has NOT adopted): exit gracefully — pattern stays detected, surface stays active, but stop pushing. Exit on: feature adoption + advocacy ask sent, explicit dismiss, or 30-day timeout.'
      prompt: 'Build a journey wired to manual-pattern-detected segment. Touch 1 (real-time, on the 5th+ pattern repetition mid-session): in-app contextual nudge fires. Recommendation surface activates persistently. Touch 2 (Day 3, if user didn''t dismiss): email reinforcement with the same feature pitch + a customer story of someone who automated it. Touch 3 (Day 14, IF user has adopted the feature): advocacy follow-up email asking for review/referral. Touch 4 (Day 14, IF user has NOT adopted): exit gracefully — pattern stays detected, surface stays active, but stop pushing. Exit on: feature adoption + advocacy ask sent, explicit dismiss, or 30-day timeout.'
    - step: 7
      title: Build Power-User Detection Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - manual_pattern
      - segment
      - inapp_asset
      - rec_surface
      - email_asset
      - journey
      description: 'Compose a power-user detection dashboard: top 10 detected manual patterns by frequency (which features have the biggest discoverability gap — informs in-app UI redesign priorities), in-app-nudge-to-adoption rate (the headline metric — target: 15%+, baseline generic feature emails get 4-6%), 30-day retention of adopters vs. non-adopters (proves the journey''s value beyond direct adoption), and advocacy-ask conversion (% of adopters who write a review or refer — this is the unexpected revenue side-effect of feature discovery).'
      prompt: 'Compose a power-user detection dashboard: top 10 detected manual patterns by frequency (which features have the biggest discoverability gap — informs in-app UI redesign priorities), in-app-nudge-to-adoption rate (the headline metric — target: 15%+, baseline generic feature emails get 4-6%), 30-day retention of adopters vs. non-adopters (proves the journey''s value beyond direct adoption), and advocacy-ask conversion (% of adopters who write a review or refer — this is the unexpected revenue side-effect of feature discovery).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Power User Pattern Detection

## Procedure

1. **Build Manual-Pattern AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'detected_manual_patterns' on the User object, refreshed daily. Detects repeated manual sequences that have automated counterparts in the product. Example patterns: (a) user runs same multi-step report 5+ times in 7 days (has unused 'scheduled reports' feature), (b) user exports data manually 3+ times in 7 days (has unused API/webhook feature), (c) user assigns same task type repeatedly (has unused task templates feature), (d) user filters dashboard same way 10+ times in 14 days (has unused saved-view feature). Output: list of detected patterns with the automate-it feature name and adoption-likelihood score (based on user's plan, skill level, prior automation adoption). → produces: attribute
2. **Identify Power-User Candidates** [`create_segment`] — Build a segment 'Manual-pattern detected' capturing paying users where detected_manual_patterns is non-empty AND the user hasn't yet used the recommended automation feature. Partitioned by feature-to-introduce. Excludes users who have dismissed feature-recommendations 3+ times (respect the no) and users with plan limits that exclude the suggested feature. → produces: segment
3. **Build Contextual In-App Nudge** [`create_page_content`] — Generate in-app nudge content per detected pattern. Format: tooltip or floating card that appears WHEN the user is mid-pattern (e.g. on their 6th manual export). Content: 'You've done this 6 times this week — did you know [Product] can automate this?' + 60-second 'how it works' GIF + 'enable now' CTA + dismiss option. Renders at the exact moment of friction, not in a generic feature-discovery surface. The contextual timing is the magic — this is the 4x feature-adoption uplift pattern from the research. → produces: asset
4. **Build Power-Feature Recommendation Surface** [`create_recommendation`] — Configure a recommendation surface 'Power features for your workflow' on the user's dashboard. Pulls: the top 3 detected_manual_patterns with their automate-it counterparts, ranked by adoption-likelihood. Each recommendation: 1-line description + 'try it' deep link. Updates when user adopts a feature (rotates in the next-best). Renders persistently for 30 days after detection. → produces: recommendation
5. **Build Advocacy Follow-up Content** [`create_email_content`] — Generate follow-up email content sent 14 days after a user adopts a recommended automation feature. Content: 'Congrats on automating [feature] — you've saved an estimated [time] per week. Mind sharing your experience?' Two CTAs: write a review on G2/Capterra (with deep-link to the right product page), refer a peer (with referral program info). This is where power-user-detection becomes an advocacy pipeline — the user just had a positive experience, the moment is warm. → produces: asset
6. **Build Power-User Journey** [`create_journey`] — Build a journey wired to manual-pattern-detected segment. Touch 1 (real-time, on the 5th+ pattern repetition mid-session): in-app contextual nudge fires. Recommendation surface activates persistently. Touch 2 (Day 3, if user didn't dismiss): email reinforcement with the same feature pitch + a customer story of someone who automated it. Touch 3 (Day 14, IF user has adopted the feature): advocacy follow-up email asking for review/referral. Touch 4 (Day 14, IF user has NOT adopted): exit gracefully — pattern stays detected, surface stays active, but stop pushing. Exit on: feature adoption + advocacy ask sent, explicit dismiss, or 30-day timeout. → produces: journey
7. **Build Power-User Detection Dashboard** [`create_dashboard`] — Compose a power-user detection dashboard: top 10 detected manual patterns by frequency (which features have the biggest discoverability gap — informs in-app UI redesign priorities), in-app-nudge-to-adoption rate (the headline metric — target: 15%+, baseline generic feature emails get 4-6%), 30-day retention of adopters vs. non-adopters (proves the journey's value beyond direct adoption), and advocacy-ask conversion (% of adopters who write a review or refer — this is the unexpected revenue side-effect of feature discovery). → produces: dashboard
