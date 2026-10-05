---
name: usage-spike-expansion-play
description: 'Use when a user mentions "usage spike expansion", "expansion signal journey", "customer expansion play", or asks for related help. When existing paying customers cross usage thresholds — fast user-growth on the account, feature-depth expansion, multi-team usage — fire a multi-stakeholder expansion journey: champion gets ''you''re scaling'' content, economic buyer gets upgrade-options content, recommendation surface highlights expansion features.'
arguments: []
intempt:
  id: usage-spike-expansion-play
  version: 1.0.0
  slashCommand: /usage-spike-expansion-play
  group: Journeys
  shortDescription: "Create an Account expansion_signal_score AI attribute from usage growth, feature depth, multi-team adoption, cap proximity, and integrations, then trigger a multi-stakeholder journey with segment, email, and recommendation steps."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [expansion, multi-stakeholder, usage-driven]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: feature_used, severity: blocking }
      - { value: user_signed_up, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_recommendation
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Account Expansion-Signal Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: expansion_signal
      description: 'Create an AI-derived attribute ''expansion_signal_score'' on the Account object. Inputs: (a) active-user growth rate (new users added from domain in last 30 days vs. trailing 90-day baseline); (b) feature-depth expansion (count of distinct features used per active user trending up); (c) multi-team adoption (users from different functions / departments based on email domain or profile data); (d) usage-cap proximity (seats / API calls / events / storage); (e) integration-attach (new integrations connected — signals deeper commitment). Output: 0-100 score with composite reasoning string explaining which signals are firing.'
      prompt: 'Create an AI-derived attribute ''expansion_signal_score'' on the Account object. Inputs: (a) active-user growth rate (new users added from domain in last 30 days vs. trailing 90-day baseline); (b) feature-depth expansion (count of distinct features used per active user trending up); (c) multi-team adoption (users from different functions / departments based on email domain or profile data); (d) usage-cap proximity (seats / API calls / events / storage); (e) integration-attach (new integrations connected — signals deeper commitment). Output: 0-100 score with composite reasoning string explaining which signals are firing.'
    - step: 2
      title: Identify Expansion-Ready Accounts
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - expansion_signal
      description: Build a segment 'Expansion-ready customer accounts' capturing existing paying accounts where expansion_signal_score >= 70 in the last 14 days AND no active expansion deal already in flight (don't double-orchestrate against AE work). Partitioned by primary signal type so the journey can branch on the dominant signal (user-growth-driven vs. feature-depth-driven vs. usage-cap-driven).
      prompt: Build a segment 'Expansion-ready customer accounts' capturing existing paying accounts where expansion_signal_score >= 70 in the last 14 days AND no active expansion deal already in flight (don't double-orchestrate against AE work). Partitioned by primary signal type so the journey can branch on the dominant signal (user-growth-driven vs. feature-depth-driven vs. usage-cap-driven).
    - step: 3
      title: Build Champion-Targeted Content
      command: create_email_content
      produces: asset
      bindsAs: champion_asset
      dependsOn:
      - expansion_signal
      - segment
      description: 'Generate email content for the user-champion at the account (the most-active user, usually). Variants by signal type: user-growth — ''Your team is growing on [Product] — here''s how power-using teams stay organized at this scale.'' Feature-depth — ''You''re using [Product] deeper than 85% of similar accounts — here''s what''s next.'' Usage-cap — ''Your team is approaching the [resource] limit. Here are options.'' Tone: peer-to-peer enablement, not sales pitch. The champion should feel proud, not pitched.'
      prompt: 'Generate email content for the user-champion at the account (the most-active user, usually). Variants by signal type: user-growth — ''Your team is growing on [Product] — here''s how power-using teams stay organized at this scale.'' Feature-depth — ''You''re using [Product] deeper than 85% of similar accounts — here''s what''s next.'' Usage-cap — ''Your team is approaching the [resource] limit. Here are options.'' Tone: peer-to-peer enablement, not sales pitch. The champion should feel proud, not pitched.'
    - step: 4
      title: Build Economic-Buyer Content
      command: create_email_content
      produces: asset
      bindsAs: buyer_asset
      dependsOn:
      - expansion_signal
      - segment
      - champion_asset
      description: 'Generate email content for the economic buyer at the account (often someone NOT actively using the product day-to-day — admin / manager / finance owner). Variants by signal type: user-growth — ''Your team''s usage of [Product] grew [N%] this quarter — here''s a business-case summary of value delivered.'' Feature-depth — ''Your team is in the top 15% of [Product] users by depth — let''s discuss expansion options.'' Usage-cap — ''Cost-comparison: upgrade vs. current overage costs.'' Includes ROI snapshot. Tone: business-formal, value-substantive. Reply-to: assigned AE.'
      prompt: 'Generate email content for the economic buyer at the account (often someone NOT actively using the product day-to-day — admin / manager / finance owner). Variants by signal type: user-growth — ''Your team''s usage of [Product] grew [N%] this quarter — here''s a business-case summary of value delivered.'' Feature-depth — ''Your team is in the top 15% of [Product] users by depth — let''s discuss expansion options.'' Usage-cap — ''Cost-comparison: upgrade vs. current overage costs.'' Includes ROI snapshot. Tone: business-formal, value-substantive. Reply-to: assigned AE.'
    - step: 5
      title: Build Expansion Recommendation Surface
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - expansion_signal
      - segment
      description: 'Configure a recommendation surface ''Expansion features'' that activates when the account is in the expansion segment. Renders in-app on the admin dashboard and in the email touches. Pulls: features available on higher-tier plans that the account would benefit from based on current usage patterns (e.g., ''Teams using [current features] often graduate to [advanced features] — here''s what they unlock''). Includes upgrade-comparison surface for plan-decision-makers.'
      prompt: 'Configure a recommendation surface ''Expansion features'' that activates when the account is in the expansion segment. Renders in-app on the admin dashboard and in the email touches. Pulls: features available on higher-tier plans that the account would benefit from based on current usage patterns (e.g., ''Teams using [current features] often graduate to [advanced features] — here''s what they unlock''). Includes upgrade-comparison surface for plan-decision-makers.'
    - step: 6
      title: Build Expansion Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - expansion_signal
      - segment
      - champion_asset
      - buyer_asset
      - rec_surface
      description: 'Build a multi-stakeholder journey triggered when an account enters expansion-ready segment. Touch 1 (Day 0): champion email — ''you''re growing fast / using deeply / hitting limits'' content. Touch 2 (Day 3): in-app upgrade-comparison surface activates for admin users at the account on next session. Touch 3 (Day 7): economic-buyer email with ROI summary and AE meeting CTA. Touch 4 (Day 14): if no AE meeting booked, create AE task with the full account context attached (signals, decision-makers, recommended package). Recommendation surface stays active for 60 days. Exit on: meeting_scheduled (handoff to AE), upgrade_completed (success — celebrate), deal_created (AE-owned from here), or expansion_signal drops below 50 for 30 days (false signal — exit gracefully).'
      prompt: 'Build a multi-stakeholder journey triggered when an account enters expansion-ready segment. Touch 1 (Day 0): champion email — ''you''re growing fast / using deeply / hitting limits'' content. Touch 2 (Day 3): in-app upgrade-comparison surface activates for admin users at the account on next session. Touch 3 (Day 7): economic-buyer email with ROI summary and AE meeting CTA. Touch 4 (Day 14): if no AE meeting booked, create AE task with the full account context attached (signals, decision-makers, recommended package). Recommendation surface stays active for 60 days. Exit on: meeting_scheduled (handoff to AE), upgrade_completed (success — celebrate), deal_created (AE-owned from here), or expansion_signal drops below 50 for 30 days (false signal — exit gracefully).'
    - step: 7
      title: Build Expansion Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - expansion_signal
      - segment
      - champion_asset
      - buyer_asset
      - rec_surface
      - journey
      description: 'Compose an expansion performance dashboard: expansion-signal volume per week by signal type (which signals fire most — informs which expansion levers the product naturally creates), expansion-signal-to-meeting conversion, expansion-signal-to-deal-created conversion, ARR uplift from journey-attributed expansion (cohort-attributed vs. control), and signal-type effectiveness (does user-growth signal convert better than feature-depth — informs product/marketing focus). NRR contribution from this play.'
      prompt: 'Compose an expansion performance dashboard: expansion-signal volume per week by signal type (which signals fire most — informs which expansion levers the product naturally creates), expansion-signal-to-meeting conversion, expansion-signal-to-deal-created conversion, ARR uplift from journey-attributed expansion (cohort-attributed vs. control), and signal-type effectiveness (does user-growth signal convert better than feature-depth — informs product/marketing focus). NRR contribution from this play.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Usage Spike Expansion Play

## Procedure

1. **Build Account Expansion-Signal Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'expansion_signal_score' on the Account object. Inputs: (a) active-user growth rate (new users added from domain in last 30 days vs. trailing 90-day baseline); (b) feature-depth expansion (count of distinct features used per active user trending up); (c) multi-team adoption (users from different functions / departments based on email domain or profile data); (d) usage-cap proximity (seats / API calls / events / storage); (e) integration-attach (new integrations connected — signals deeper commitment). Output: 0-100 score with composite reasoning string explaining which signals are firing. → produces: attribute
2. **Identify Expansion-Ready Accounts** [`create_segment`] — Build a segment 'Expansion-ready customer accounts' capturing existing paying accounts where expansion_signal_score >= 70 in the last 14 days AND no active expansion deal already in flight (don't double-orchestrate against AE work). Partitioned by primary signal type so the journey can branch on the dominant signal (user-growth-driven vs. feature-depth-driven vs. usage-cap-driven). → produces: segment
3. **Build Champion-Targeted Content** [`create_email_content`] — Generate email content for the user-champion at the account (the most-active user, usually). Variants by signal type: user-growth — 'Your team is growing on [Product] — here's how power-using teams stay organized at this scale.' Feature-depth — 'You're using [Product] deeper than 85% of similar accounts — here's what's next.' Usage-cap — 'Your team is approaching the [resource] limit. Here are options.' Tone: peer-to-peer enablement, not sales pitch. The champion should feel proud, not pitched. → produces: asset
4. **Build Economic-Buyer Content** [`create_email_content`] — Generate email content for the economic buyer at the account (often someone NOT actively using the product day-to-day — admin / manager / finance owner). Variants by signal type: user-growth — 'Your team's usage of [Product] grew [N%] this quarter — here's a business-case summary of value delivered.' Feature-depth — 'Your team is in the top 15% of [Product] users by depth — let's discuss expansion options.' Usage-cap — 'Cost-comparison: upgrade vs. current overage costs.' Includes ROI snapshot. Tone: business-formal, value-substantive. Reply-to: assigned AE. → produces: asset
5. **Build Expansion Recommendation Surface** [`create_recommendation`] — Configure a recommendation surface 'Expansion features' that activates when the account is in the expansion segment. Renders in-app on the admin dashboard and in the email touches. Pulls: features available on higher-tier plans that the account would benefit from based on current usage patterns (e.g., 'Teams using [current features] often graduate to [advanced features] — here's what they unlock'). Includes upgrade-comparison surface for plan-decision-makers. → produces: recommendation
6. **Build Expansion Journey** [`create_journey`] — Build a multi-stakeholder journey triggered when an account enters expansion-ready segment. Touch 1 (Day 0): champion email — 'you're growing fast / using deeply / hitting limits' content. Touch 2 (Day 3): in-app upgrade-comparison surface activates for admin users at the account on next session. Touch 3 (Day 7): economic-buyer email with ROI summary and AE meeting CTA. Touch 4 (Day 14): if no AE meeting booked, create AE task with the full account context attached (signals, decision-makers, recommended package). Recommendation surface stays active for 60 days. Exit on: meeting_scheduled (handoff to AE), upgrade_completed (success — celebrate), deal_created (AE-owned from here), or expansion_signal drops below 50 for 30 days (false signal — exit gracefully). → produces: journey
7. **Build Expansion Performance Dashboard** [`create_dashboard`] — Compose an expansion performance dashboard: expansion-signal volume per week by signal type (which signals fire most — informs which expansion levers the product naturally creates), expansion-signal-to-meeting conversion, expansion-signal-to-deal-created conversion, ARR uplift from journey-attributed expansion (cohort-attributed vs. control), and signal-type effectiveness (does user-growth signal convert better than feature-depth — informs product/marketing focus). NRR contribution from this play. → produces: dashboard
