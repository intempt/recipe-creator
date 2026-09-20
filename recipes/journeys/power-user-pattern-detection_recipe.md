---
name: power-user-pattern-detection
description: Use when a user mentions "power user pattern detection", "manual workflow detection", "automation upgrade journey", or asks for related help. Detect users repeatedly performing manual workflows that the product can automate (5+ same task in 7 days, batch operations being done one-at-a-time, repeat exports) to surface the relevant power-feature contextually via in-app + recommendation surface, then invite to advocacy program if adopted.
arguments: []
intempt:
  id: power-user-pattern-detection
  title: "Power user pattern detection"
  version: 1.0.0
  slashCommand: /power-user-pattern-detection
  group: Journeys
  shortDescription: "Notices people doing a job by hand over and over, shows them the feature that automates it at that exact moment, and asks for a review if it lands."
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
      title: "Spot work done the hard way"
      command: create_ai_attribute
      produces: attribute
      bindsAs: manual_pattern
      description: "Checked daily for repeated manual work the product can automate: the same report run five or more times in 7 days when scheduled reports exist, three or more manual exports in 7 days when there is an API, the same task assigned again and again when templates exist, or the same dashboard filter set 10 times in 14 days when views can be saved. Each pattern is paired with the feature that replaces it and how likely that person is to adopt it."
      prompt: 'Create an AI-derived attribute ''detected_manual_patterns'' on the User object, refreshed daily. Detects repeated manual sequences that have automated counterparts in the product. Example patterns: (a) user runs same multi-step report 5+ times in 7 days (has unused ''scheduled reports'' feature), (b) user exports data manually 3+ times in 7 days (has unused API/webhook feature), (c) user assigns same task type repeatedly (has unused task templates feature), (d) user filters dashboard same way 10+ times in 14 days (has unused saved-view feature). Output: list of detected patterns with the automate-it feature name and adoption-likelihood score (based on user''s plan, skill level, prior automation adoption).'
    - step: 2
      title: "Find who could automate it"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - manual_pattern
      description: "Paying users with at least one detected pattern who have not used the matching feature, split by which feature to introduce. Anyone who has dismissed feature suggestions three times is left out, and so is anyone whose plan does not include the feature."
      prompt: Build a segment 'Manual-pattern detected' capturing paying users where detected_manual_patterns is non-empty AND the user hasn't yet used the recommended automation feature. Partitioned by feature-to-introduce. Excludes users who have dismissed feature-recommendations 3+ times (respect the no) and users with plan limits that exclude the suggested feature.
    - step: 3
      title: "Nudge them mid task"
      command: create_page_content
      produces: asset
      bindsAs: inapp_asset
      dependsOn:
      - manual_pattern
      - segment
      description: "A tooltip or card that appears while they are doing it, on the sixth manual export rather than later: how many times they have done this, a 60 second clip of the automated way, an enable now button, and a dismiss."
      prompt: 'Generate in-app nudge content per detected pattern. Format: tooltip or floating card that appears WHEN the user is mid-pattern (e.g. on their 6th manual export). Content: ''You''ve done this 6 times this week: did you know [Product] can automate this?'' + 60-second ''how it works'' GIF + ''enable now'' CTA + dismiss option. Renders at the exact moment of friction, not in a generic feature-discovery surface. The contextual timing is the magic: this is the 4x feature-adoption uplift pattern from the research.'
    - step: 4
      title: "List their power features"
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - manual_pattern
      - segment
      description: "A dashboard panel with the top three patterns and the features that replace them, ranked by how likely they are to adopt, each one a line and a link. It rotates as they adopt and stays up for 30 days after detection."
      prompt: 'Configure a recommendation surface ''Power features for your workflow'' on the user''s dashboard. Pulls: the top 3 detected_manual_patterns with their automate-it counterparts, ranked by adoption-likelihood. Each recommendation: 1-line description + ''try it'' deep link. Updates when user adopts a feature (rotates in the next-best). Renders persistently for 30 days after detection.'
    - step: 5
      title: "Ask adopters for a review"
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - manual_pattern
      - segment
      description: "Sent 14 days after someone adopts an automation: what it is saving them per week, then two options, leave a review with a direct link or refer a peer through the referral programme."
      prompt: 'Generate follow-up email content sent 14 days after a user adopts a recommended automation feature. Content: ''Congrats on automating [feature]: you''ve saved an estimated [time] per week. Mind sharing your experience?'' Two CTAs: write a review on G2/Capterra (with deep-link to the right product page), refer a peer (with referral program info). This is where power-user-detection becomes an advocacy pipeline: the user just had a positive experience, the moment is warm.'
    - step: 6
      title: "Nudge, remind, then let it go"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - manual_pattern
      - segment
      - inapp_asset
      - rec_surface
      - email_asset
      description: "The in app nudge fires live on the fifth repeat and the panel switches on. On day 3, if they did not dismiss it, an email repeats the case with a customer story. On day 14 adopters get the review ask, and everyone else is left alone: the panel stays but the pushing stops. It closes on adoption, on a dismissal, or after 30 days."
      prompt: 'Build a journey wired to manual-pattern-detected segment. Touch 1 (real-time, on the 5th+ pattern repetition mid-session): in-app contextual nudge fires. Recommendation surface activates persistently. Touch 2 (Day 3, if user didn''t dismiss): email reinforcement with the same feature pitch + a customer story of someone who automated it. Touch 3 (Day 14, IF user has adopted the feature): advocacy follow-up email asking for review/referral. Touch 4 (Day 14, IF user has NOT adopted): exit gracefully: pattern stays detected, surface stays active, but stop pushing. Exit on: feature adoption + advocacy ask sent, explicit dismiss, or 30-day timeout.'
    - step: 7
      title: "See which features stay hidden"
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
      description: "The ten manual patterns that come up most, how often the in app nudge leads to adoption, the 30 day retention of adopters against everyone else, and how many adopters go on to leave a review or refer someone."
      prompt: 'Compose a power-user detection dashboard: top 10 detected manual patterns by frequency (which features have the biggest discoverability gap (informs in-app UI redesign priorities), in-app-nudge-to-adoption rate (the headline metric) target: 15%+, baseline generic feature emails get 4-6%), 30-day retention of adopters vs. non-adopters (proves the journey''s value beyond direct adoption), and advocacy-ask conversion (% of adopters who write a review or refer: this is the unexpected revenue side-effect of feature discovery).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Power user pattern detection

Notices people doing a job by hand over and over, shows them the feature that automates it at that exact moment, and asks for a review if it lands.

## Before you run it

- Send the `feature_used` event

## What it does

1. **Spot work done the hard way** (`create_ai_attribute`)

   Checked daily for repeated manual work the product can automate: the same report run five or more times in 7 days when scheduled reports exist, three or more manual exports in 7 days when there is an API, the same task assigned again and again when templates exist, or the same dashboard filter set 10 times in 14 days when views can be saved. Each pattern is paired with the feature that replaces it and how likely that person is to adopt it.

2. **Find who could automate it** (`create_segment`)

   Paying users with at least one detected pattern who have not used the matching feature, split by which feature to introduce. Anyone who has dismissed feature suggestions three times is left out, and so is anyone whose plan does not include the feature.

3. **Nudge them mid task** (`create_page_content`)

   A tooltip or card that appears while they are doing it, on the sixth manual export rather than later: how many times they have done this, a 60 second clip of the automated way, an enable now button, and a dismiss.

4. **List their power features** (`create_recommendation`)

   A dashboard panel with the top three patterns and the features that replace them, ranked by how likely they are to adopt, each one a line and a link. It rotates as they adopt and stays up for 30 days after detection.

5. **Ask adopters for a review** (`create_email_content`)

   Sent 14 days after someone adopts an automation: what it is saving them per week, then two options, leave a review with a direct link or refer a peer through the referral programme.

6. **Nudge, remind, then let it go** (`create_journey`)

   The in app nudge fires live on the fifth repeat and the panel switches on. On day 3, if they did not dismiss it, an email repeats the case with a customer story. On day 14 adopters get the review ask, and everyone else is left alone: the panel stays but the pushing stops. It closes on adoption, on a dismissal, or after 30 days.

7. **See which features stay hidden** (`create_dashboard`)

   The ten manual patterns that come up most, how often the in app nudge leads to adoption, the 30 day retention of adopters against everyone else, and how many adopters go on to leave a review or refer someone.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
