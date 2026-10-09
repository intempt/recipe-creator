---
name: competitor-mention-detected-response
description: Use when a user mentions "competitor mention detected", "competitive intent response", "competitor signal journey", or asks for related help. Behavioral signal detection, visited competitor comparison page, mentioned competitor in support conversation, clicked competitor-keyword email content, fires personalized competitive content + AE/CSM task with intel + recommendation surface highlighting differentiators. Modern B2B savvy.
arguments: []
intempt:
  id: competitor-mention-detected-response
  title: "Competitor signal response"
  version: 1.0.0
  slashCommand: /competitor-mention-detected-response
  group: Journeys
  shortDescription: "Spots customers comparing you with a rival and answers within hours: a matched email, the capabilities they have not tried, and a briefed CSM."
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
      title: "Spot competitor interest"
      command: create_ai_attribute
      produces: attribute
      bindsAs: competitor_signal
      description: "A signal on the user or account when they visit a versus page, click a competitor named link, mention a rival in support or chat, or download a comparison. It records which competitor, how strong the signal is, how recent it is, and whether it reads as evaluation, dissatisfaction, curiosity or leaving. It stays live for 30 days after the last signal."
      prompt: 'Create an AI-derived attribute ''Recent competitor signal'' on the User/Account object. Detects: (a) visited /vs/[competitor] comparison pages, (b) clicked competitor-named links in marketing emails, (c) mentioned competitor in support conversations or AI agent chats, (d) downloaded a competitor-comparison resource, (e) appeared on a competitor''s review site as a reviewer (if data permits). Output: structured object with competitor name, signal type, signal strength, recency, and inferred intent (evaluation / dissatisfaction / curious-comparison / leaving). Stays active for 30 days after last competitor signal.'
    - step: 2
      title: "Group by what they intend"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - competitor_signal
      description: "Existing customers and late stage prospects with a medium or strong signal in the last 14 days, split by intent so each gets a different response. Brand new prospects are left out, because for them competitive intel belongs in the AE's sales process."
      prompt: Build a segment 'Active competitor signal' capturing users/accounts with a recent competitor signal in the last 14 days where signal strength is medium or high. Partitioned by inferred intent so the journey branches accordingly. Excludes brand-new prospects (different motion, for prospects, competitive intel goes into the AE's sales process). This segment is specifically EXISTING CUSTOMERS or LATE-STAGE prospects where competitor signal is a save/competitive-defend moment.
    - step: 3
      title: "Write a reply per intent"
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - competitor_signal
      - segment
      description: "Evaluation gets an honest comparison aimed at their use case. Dissatisfaction gets a direct note from their CSM asking what is not working, with no product pitch. Curiosity gets the reason most teams pick you plus a case study. Leaving gets an executive sponsor offering a business review. Strong signals come from the named CSM or AE, weak ones from marketing."
      prompt: 'Generate competitive content variants per inferred intent. Evaluation intent (existing customer comparing (concerning but not yet leaving): ''Helpful comparison: [Product] vs [Competitor] from your team''s perspective'') honest comparison + specific advantages relevant to their use case. Dissatisfaction intent (existing customer with friction signals + competitor signal (leaving risk): ''Want to talk? [CSM name] would like to understand what''s not working'') direct outreach offer, no defensive product pitch. Curious-comparison intent (neutral exploration): ''Most teams who compare us to [Competitor] choose [Product] for [specific differentiator]: here''s why'' + customer case study. Leaving intent (strong signals + cancel-page visit + competitor signal): exec-sponsor outreach offering executive-business-review meeting + retention discussion. Send-from: matched CSM or AE for high-signal cases; marketing@ for low-signal exploration.'
    - step: 4
      title: "Show what they are missing"
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - competitor_signal
      - segment
      description: "An in app surface listing the capabilities their peers use for high value work that this account has never tried. It runs for 30 days and answers why stay with something concrete."
      prompt: 'Configure a recommendation surface ''Capabilities you''re not using yet'' that activates when a user has a competitor signal. Pulls: differentiator features of [Product] that the user/account hasn''t tried but their cohort uses for high-value outcomes. The surface answers the implicit question ''why stay?'' with concrete unused capability: much more convincing than feature-comparison docs. Renders in-app for 30 days.'
    - step: 5
      title: "Respond within four hours"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - competitor_signal
      - segment
      - email_asset
      - rec_surface
      description: "The matched email goes out within four hours of the signal and the in app surface switches on the same day. On day 2 a strong signal raises a CSM or AE task carrying the competitor name, the intent, talking points and the account's usage. On day 7, high ARR accounts still showing intent get an executive sponsor offer. They leave on a clear retention signal, on churn, or after 30 quiet days."
      prompt: 'Build a journey wired to competitor-signal segment, branched by inferred intent. Touch 1 (within 4 hours of signal: speed matters): intent-matched email. Touch 2 (Day 0 of touch 1): differentiator-recommendation surface activates in-app for 30 days. Touch 3 (Day 2, for high-signal-strength accounts): CSM/AE task with full competitor intel attached (competitor name, signal type, inferred intent, suggested talking points, customer''s current usage profile). Touch 4 (Day 7, if account is still showing competitive intent + hasn''t engaged with CSM): executive-sponsor outreach offer for high-ARR accounts. Exit on: explicit positive renewal/retention signal (saved), churned (loss: feed into win-loss analysis), or 30-day timeout with no further competitor signal (signal cooled).'
    - step: 6
      title: "See which rivals you lose to"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - competitor_signal
      - segment
      - email_asset
      - rec_surface
      - journey
      description: "Signal volume per competitor, how often you save an account from each one, the split of intents, and the ARR sitting under competitive pressure."
      prompt: 'Compose a competitive defense dashboard: competitor signal volume per competitor (which competitors are hottest in your current customer base: strategic competitive intel for leadership), per-competitor save rate (which competitors you actually save customers from vs. lose to), inferred-intent distribution (evaluation vs. leaving: leading indicator of churn from competitive pressure), and ARR-weighted at-risk pile from competitor signals. Feeds the product-marketing competitive-positioning function with real data, not assumptions.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Competitor signal response

Spots customers comparing you with a rival and answers within hours: a matched email, the capabilities they have not tried, and a briefed CSM.

## Before you run it

- Send the `page_viewed` event
- Send the `email_clicked` event

## What it does

1. **Spot competitor interest** (`create_ai_attribute`)

   A signal on the user or account when they visit a versus page, click a competitor named link, mention a rival in support or chat, or download a comparison. It records which competitor, how strong the signal is, how recent it is, and whether it reads as evaluation, dissatisfaction, curiosity or leaving. It stays live for 30 days after the last signal.

2. **Group by what they intend** (`create_segment`)

   Existing customers and late stage prospects with a medium or strong signal in the last 14 days, split by intent so each gets a different response. Brand new prospects are left out, because for them competitive intel belongs in the AE's sales process.

3. **Write a reply per intent** (`create_email_content`)

   Evaluation gets an honest comparison aimed at their use case. Dissatisfaction gets a direct note from their CSM asking what is not working, with no product pitch. Curiosity gets the reason most teams pick you plus a case study. Leaving gets an executive sponsor offering a business review. Strong signals come from the named CSM or AE, weak ones from marketing.

4. **Show what they are missing** (`create_recommendation`)

   An in app surface listing the capabilities their peers use for high value work that this account has never tried. It runs for 30 days and answers why stay with something concrete.

5. **Respond within four hours** (`create_journey`)

   The matched email goes out within four hours of the signal and the in app surface switches on the same day. On day 2 a strong signal raises a CSM or AE task carrying the competitor name, the intent, talking points and the account's usage. On day 7, high ARR accounts still showing intent get an executive sponsor offer. They leave on a clear retention signal, on churn, or after 30 quiet days.

6. **See which rivals you lose to** (`create_dashboard`)

   Signal volume per competitor, how often you save an account from each one, the split of intents, and the ARR sitting under competitive pressure.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
