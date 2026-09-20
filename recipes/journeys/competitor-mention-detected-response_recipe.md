---
name: competitor-mention-detected-response
description: Use when a user mentions "competitor mention detected", "competitive intent response", "competitor signal journey", or asks for related help. Behavioral signal detection — visited competitor comparison page, mentioned competitor in support conversation, clicked competitor-keyword email content — fires personalized competitive content + AE/CSM task with intel + recommendation surface highlighting differentiators. Modern B2B savvy.
arguments: []
intempt:
  id: competitor-mention-detected-response
  version: 1.0.0
  slashCommand: /competitor-mention-detected-response
  group: Journeys
  shortDescription: 'Behavioral signal detection (visited competitor comparison page, mentioned competitor in support conversation, clicked competitor-keyword email content) fires personalized competitive content + AE/CSM task with intel + recommendation surface highlighting differentiators. Modern B2B savvy.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [competitive-intelligence, intent-response, differentiation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: page_viewed, severity: blocking }
      - { value: email_clicked, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_recommendation
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Competitor-Signal AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: competitor_signal
      description: 'Create an AI-derived attribute ''recent_competitor_signal'' on the User/Account object. Detects: (a) visited /vs/[competitor] comparison pages, (b) clicked competitor-named links in marketing emails, (c) mentioned competitor in support conversations or AI agent chats, (d) downloaded a competitor-comparison resource, (e) appeared on a competitor''s review site as a reviewer (if data permits). Output: structured object with competitor_name, signal_type, signal_strength, recency, and inferred_intent (evaluation / dissatisfaction / curious-comparison / leaving). Stays active for 30 days after last competitor signal.'
      prompt: 'Create an AI-derived attribute ''recent_competitor_signal'' on the User/Account object. Detects: (a) visited /vs/[competitor] comparison pages, (b) clicked competitor-named links in marketing emails, (c) mentioned competitor in support conversations or AI agent chats, (d) downloaded a competitor-comparison resource, (e) appeared on a competitor''s review site as a reviewer (if data permits). Output: structured object with competitor_name, signal_type, signal_strength, recency, and inferred_intent (evaluation / dissatisfaction / curious-comparison / leaving). Stays active for 30 days after last competitor signal.'
    - step: 2
      title: Identify Competitive-Intent Audience
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - competitor_signal
      description: Build a segment 'Active competitor signal' capturing users/accounts with recent_competitor_signal in the last 14 days where signal_strength is medium or high. Partitioned by inferred_intent so the journey branches accordingly. Excludes brand-new prospects (different motion — for prospects, competitive intel goes into the AE's sales process). This segment is specifically EXISTING CUSTOMERS or LATE-STAGE prospects where competitor signal is a save/competitive-defend moment.
      prompt: Build a segment 'Active competitor signal' capturing users/accounts with recent_competitor_signal in the last 14 days where signal_strength is medium or high. Partitioned by inferred_intent so the journey branches accordingly. Excludes brand-new prospects (different motion — for prospects, competitive intel goes into the AE's sales process). This segment is specifically EXISTING CUSTOMERS or LATE-STAGE prospects where competitor signal is a save/competitive-defend moment.
    - step: 3
      title: Build Competitive Content
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - competitor_signal
      - segment
      description: 'Generate competitive content variants per inferred_intent. Evaluation intent (existing customer comparing — concerning but not yet leaving): ''Helpful comparison: [Product] vs [Competitor] from your team''s perspective'' — honest comparison + specific advantages relevant to their use case. Dissatisfaction intent (existing customer with friction signals + competitor signal — leaving risk): ''Want to talk? [CSM name] would like to understand what''s not working'' — direct outreach offer, no defensive product pitch. Curious-comparison intent (neutral exploration): ''Most teams who compare us to [Competitor] choose [Product] for [specific differentiator] — here''s why'' + customer case study. Leaving intent (strong signals + cancel-page visit + competitor signal): exec-sponsor outreach offering executive-business-review meeting + retention discussion. Send-from: matched CSM or AE for high-signal cases; marketing@ for low-signal exploration.'
      prompt: 'Generate competitive content variants per inferred_intent. Evaluation intent (existing customer comparing — concerning but not yet leaving): ''Helpful comparison: [Product] vs [Competitor] from your team''s perspective'' — honest comparison + specific advantages relevant to their use case. Dissatisfaction intent (existing customer with friction signals + competitor signal — leaving risk): ''Want to talk? [CSM name] would like to understand what''s not working'' — direct outreach offer, no defensive product pitch. Curious-comparison intent (neutral exploration): ''Most teams who compare us to [Competitor] choose [Product] for [specific differentiator] — here''s why'' + customer case study. Leaving intent (strong signals + cancel-page visit + competitor signal): exec-sponsor outreach offering executive-business-review meeting + retention discussion. Send-from: matched CSM or AE for high-signal cases; marketing@ for low-signal exploration.'
    - step: 4
      title: Build Differentiator Recommendation Surface
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - competitor_signal
      - segment
      description: 'Configure a recommendation surface ''Capabilities you''re not using yet'' that activates when a user has a competitor signal. Pulls: differentiator features of [Product] that the user/account hasn''t tried but their cohort uses for high-value outcomes. The surface answers the implicit question ''why stay?'' with concrete unused capability — much more convincing than feature-comparison docs. Renders in-app for 30 days.'
      prompt: 'Configure a recommendation surface ''Capabilities you''re not using yet'' that activates when a user has a competitor signal. Pulls: differentiator features of [Product] that the user/account hasn''t tried but their cohort uses for high-value outcomes. The surface answers the implicit question ''why stay?'' with concrete unused capability — much more convincing than feature-comparison docs. Renders in-app for 30 days.'
    - step: 5
      title: Build Competitive Defense Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - competitor_signal
      - segment
      - email_asset
      - rec_surface
      description: 'Build a journey wired to competitor-signal segment, branched by inferred_intent. Touch 1 (within 4 hours of signal — speed matters): intent-matched email. Touch 2 (Day 0 of touch 1): differentiator-recommendation surface activates in-app for 30 days. Touch 3 (Day 2, for high-signal-strength accounts): CSM/AE task with full competitor intel attached (competitor name, signal type, inferred intent, suggested talking points, customer''s current usage profile). Touch 4 (Day 7, if account is still showing competitive intent + hasn''t engaged with CSM): executive-sponsor outreach offer for high-ARR accounts. Exit on: explicit positive renewal/retention signal (saved), churned (loss — feed into win-loss analysis), or 30-day timeout with no further competitor signal (signal cooled).'
      prompt: 'Build a journey wired to competitor-signal segment, branched by inferred_intent. Touch 1 (within 4 hours of signal — speed matters): intent-matched email. Touch 2 (Day 0 of touch 1): differentiator-recommendation surface activates in-app for 30 days. Touch 3 (Day 2, for high-signal-strength accounts): CSM/AE task with full competitor intel attached (competitor name, signal type, inferred intent, suggested talking points, customer''s current usage profile). Touch 4 (Day 7, if account is still showing competitive intent + hasn''t engaged with CSM): executive-sponsor outreach offer for high-ARR accounts. Exit on: explicit positive renewal/retention signal (saved), churned (loss — feed into win-loss analysis), or 30-day timeout with no further competitor signal (signal cooled).'
    - step: 6
      title: Build Competitive Defense Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - competitor_signal
      - segment
      - email_asset
      - rec_surface
      - journey
      description: 'Compose a competitive defense dashboard: competitor signal volume per competitor (which competitors are hottest in your current customer base — strategic competitive intel for leadership), per-competitor save rate (which competitors you actually save customers from vs. lose to), inferred-intent distribution (evaluation vs. leaving — leading indicator of churn from competitive pressure), and ARR-weighted at-risk pile from competitor signals. Feeds the product-marketing competitive-positioning function with real data, not assumptions.'
      prompt: 'Compose a competitive defense dashboard: competitor signal volume per competitor (which competitors are hottest in your current customer base — strategic competitive intel for leadership), per-competitor save rate (which competitors you actually save customers from vs. lose to), inferred-intent distribution (evaluation vs. leaving — leading indicator of churn from competitive pressure), and ARR-weighted at-risk pile from competitor signals. Feeds the product-marketing competitive-positioning function with real data, not assumptions.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Competitor Mention Detected Response

## Procedure

1. **Build Competitor-Signal AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'recent_competitor_signal' on the User/Account object. Detects: (a) visited /vs/[competitor] comparison pages, (b) clicked competitor-named links in marketing emails, (c) mentioned competitor in support conversations or AI agent chats, (d) downloaded a competitor-comparison resource, (e) appeared on a competitor's review site as a reviewer (if data permits). Output: structured object with competitor_name, signal_type, signal_strength, recency, and inferred_intent (evaluation / dissatisfaction / curious-comparison / leaving). Stays active for 30 days after last competitor signal. → produces: attribute
2. **Identify Competitive-Intent Audience** [`create_segment`] — Build a segment 'Active competitor signal' capturing users/accounts with recent_competitor_signal in the last 14 days where signal_strength is medium or high. Partitioned by inferred_intent so the journey branches accordingly. Excludes brand-new prospects (different motion — for prospects, competitive intel goes into the AE's sales process). This segment is specifically EXISTING CUSTOMERS or LATE-STAGE prospects where competitor signal is a save/competitive-defend moment. → produces: segment
3. **Build Competitive Content** [`create_email_content`] — Generate competitive content variants per inferred_intent. Evaluation intent (existing customer comparing — concerning but not yet leaving): 'Helpful comparison: [Product] vs [Competitor] from your team's perspective' — honest comparison + specific advantages relevant to their use case. Dissatisfaction intent (existing customer with friction signals + competitor signal — leaving risk): 'Want to talk? [CSM name] would like to understand what's not working' — direct outreach offer, no defensive product pitch. Curious-comparison intent (neutral exploration): 'Most teams who compare us to [Competitor] choose [Product] for [specific differentiator] — here's why' + customer case study. Leaving intent (strong signals + cancel-page visit + competitor signal): exec-sponsor outreach offering executive-business-review meeting + retention discussion. Send-from: matched CSM or AE for high-signal cases; marketing@ for low-signal exploration. → produces: asset
4. **Build Differentiator Recommendation Surface** [`create_recommendation`] — Configure a recommendation surface 'Capabilities you're not using yet' that activates when a user has a competitor signal. Pulls: differentiator features of [Product] that the user/account hasn't tried but their cohort uses for high-value outcomes. The surface answers the implicit question 'why stay?' with concrete unused capability — much more convincing than feature-comparison docs. Renders in-app for 30 days. → produces: recommendation
5. **Build Competitive Defense Journey** [`create_journey`] — Build a journey wired to competitor-signal segment, branched by inferred_intent. Touch 1 (within 4 hours of signal — speed matters): intent-matched email. Touch 2 (Day 0 of touch 1): differentiator-recommendation surface activates in-app for 30 days. Touch 3 (Day 2, for high-signal-strength accounts): CSM/AE task with full competitor intel attached (competitor name, signal type, inferred intent, suggested talking points, customer's current usage profile). Touch 4 (Day 7, if account is still showing competitive intent + hasn't engaged with CSM): executive-sponsor outreach offer for high-ARR accounts. Exit on: explicit positive renewal/retention signal (saved), churned (loss — feed into win-loss analysis), or 30-day timeout with no further competitor signal (signal cooled). → produces: journey
6. **Build Competitive Defense Dashboard** [`create_dashboard`] — Compose a competitive defense dashboard: competitor signal volume per competitor (which competitors are hottest in your current customer base — strategic competitive intel for leadership), per-competitor save rate (which competitors you actually save customers from vs. lose to), inferred-intent distribution (evaluation vs. leaving — leading indicator of churn from competitive pressure), and ARR-weighted at-risk pile from competitor signals. Feeds the product-marketing competitive-positioning function with real data, not assumptions. → produces: dashboard
