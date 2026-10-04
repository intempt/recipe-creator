---
id: competitor-mention-detected-response
title: Competitor signal response
slash_command: /competitor-mention-detected-response
group: Journeys
owner: intempt
curator: somya
summary: 'Spots customers comparing you with a rival and answers within hours: a matched email, the capabilities
  they have not tried, and a briefed CSM.'
description: >-
  Behavioral signal detection, visited competitor comparison page, mentioned competitor in support conversation,
  clicked competitor-keyword email content, fires personalized competitive content + AE/CSM task with
  intel + recommendation surface highlighting differentiators. Modern B2B savvy.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: journey-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - competitive-intelligence
    - intent-response
    - differentiation
prerequisites:
  events:
    - value: page_viewed
      severity: blocking
    - value: email_clicked
      severity: recommended
touches:
  reads:
    - The page_viewed event in your project
    - The email_clicked event in your project
  writes:
    - A new attribute, from step 1 "Spot competitor interest"
    - A new segment, from step 2 "Group by what they intend"
    - A new designed email, from step 3 "Write a reply per intent"
    - A new product recommendation, from step 4 "Show what they are missing"
    - A new journey, from step 5 "Respond within four hours"
    - A new dashboard, from step 6 "See which rivals you lose to"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Spot competitor interest
    summary: >-
      A signal on the user or account when they visit a versus page, click a competitor named link, mention
      a rival in support or chat, or download a comparison. It records which competitor, how strong the
      signal is, how recent it is, and whether it reads as evaluation, dissatisfaction, curiosity or leaving.
      It stays live for 30 days after the last signal.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'recent_competitor_signal' on the User/Account object. Detects: (a)
      visited /vs/[competitor] comparison pages, (b) clicked competitor-named links in marketing emails,
      (c) mentioned competitor in support conversations or AI agent chats, (d) downloaded a competitor-comparison
      resource, (e) appeared on a competitor's review site as a reviewer (if data permits). Output: structured
      object with competitor_name, signal_type, signal_strength, recency, and inferred_intent (evaluation
      / dissatisfaction / curious-comparison / leaving). Stays active for 30 days after last competitor
      signal.
  - id: s2
    title: Group by what they intend
    summary: >-
      Existing customers and late stage prospects with a medium or strong signal in the last 14 days,
      split by intent so each gets a different response. Brand new prospects are left out, because for
      them competitive intel belongs in the AE's sales process.
    builds: segment
    description: >-
      Build a segment 'Active competitor signal' capturing users/accounts with recent_competitor_signal
      in the last 14 days where signal_strength is medium or high. Partitioned by inferred_intent so the
      journey branches accordingly. Excludes brand-new prospects (different motion, for prospects, competitive
      intel goes into the AE's sales process). This segment is specifically EXISTING CUSTOMERS or LATE-STAGE
      prospects where competitor signal is a save/competitive-defend moment. Use the result of "Spot competitor
      interest".
    dependsOn:
      - s1
  - id: s3
    title: Write a reply per intent
    summary: >-
      Evaluation gets an honest comparison aimed at their use case. Dissatisfaction gets a direct note
      from their CSM asking what is not working, with no product pitch. Curiosity gets the reason most
      teams pick you plus a case study. Leaving gets an executive sponsor offering a business review.
      Strong signals come from the named CSM or AE, weak ones from marketing.
    builds: email_html
    description: >-
      Generate competitive content variants per inferred_intent. Evaluation intent (existing customer
      comparing (concerning but not yet leaving): 'Helpful comparison: [Product] vs [Competitor] from
      your team's perspective') honest comparison + specific advantages relevant to their use case. Dissatisfaction
      intent (existing customer with friction signals + competitor signal (leaving risk): 'Want to talk?
      [CSM name] would like to understand what's not working') direct outreach offer, no defensive product
      pitch. Curious-comparison intent (neutral exploration): 'Most teams who compare us to [Competitor]
      choose [Product] for [specific differentiator]: here's why' + customer case study. Leaving intent
      (strong signals + cancel-page visit + competitor signal): exec-sponsor outreach offering executive-business-review
      meeting + retention discussion. Send-from: matched CSM or AE for high-signal cases; marketing@ for
      low-signal exploration. Use the result of "Spot competitor interest", "Group by what they intend".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Show what they are missing
    summary: >-
      An in app surface listing the capabilities their peers use for high value work that this account
      has never tried. It runs for 30 days and answers why stay with something concrete.
    builds: recommendation
    description: >-
      Configure a recommendation surface 'Capabilities you're not using yet' that activates when a user
      has a competitor signal. Pulls: differentiator features of [Product] that the user/account hasn't
      tried but their cohort uses for high-value outcomes. The surface answers the implicit question 'why
      stay?' with concrete unused capability: much more convincing than feature-comparison docs. Renders
      in-app for 30 days. Use the result of "Spot competitor interest", "Group by what they intend".
    dependsOn:
      - s1
      - s2
  - id: s5
    title: Respond within four hours
    summary: >-
      The matched email goes out within four hours of the signal and the in app surface switches on the
      same day. On day 2 a strong signal raises a CSM or AE task carrying the competitor name, the intent,
      talking points and the account's usage. On day 7, high ARR accounts still showing intent get an
      executive sponsor offer. They leave on a clear retention signal, on churn, or after 30 quiet days.
    builds: journey
    description: >-
      Build a journey wired to competitor-signal segment, branched by inferred_intent. Touch 1 (within
      4 hours of signal: speed matters): intent-matched email. Touch 2 (Day 0 of touch 1): differentiator-recommendation
      surface activates in-app for 30 days. Touch 3 (Day 2, for high-signal-strength accounts): CSM/AE
      task with full competitor intel attached (competitor name, signal type, inferred intent, suggested
      talking points, customer's current usage profile). Touch 4 (Day 7, if account is still showing competitive
      intent + hasn't engaged with CSM): executive-sponsor outreach offer for high-ARR accounts. Exit
      on: explicit positive renewal/retention signal (saved), churned (loss: feed into win-loss analysis),
      or 30-day timeout with no further competitor signal (signal cooled). Use the result of "Spot competitor
      interest", "Group by what they intend", "Write a reply per intent", "Show what they are missing".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: See which rivals you lose to
    summary: >-
      Signal volume per competitor, how often you save an account from each one, the split of intents,
      and the ARR sitting under competitive pressure.
    builds: dashboard
    description: >-
      Compose a competitive defense dashboard: competitor signal volume per competitor (which competitors
      are hottest in your current customer base: strategic competitive intel for leadership), per-competitor
      save rate (which competitors you actually save customers from vs. lose to), inferred-intent distribution
      (evaluation vs. leaving: leading indicator of churn from competitive pressure), and ARR-weighted
      at-risk pile from competitor signals. Feeds the product-marketing competitive-positioning function
      with real data, not assumptions. Use the result of "Spot competitor interest", "Group by what they
      intend", "Write a reply per intent", "Show what they are missing", "Respond within four hours".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
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
    producedByStep: s3
    type: asset
    description: Asset produced by this recipe.
  - key: recommendation
    producedByStep: s4
    type: recommendation
    description: Recommendation Surface produced by this recipe.
  - key: journey
    producedByStep: s5
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s6
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Competitor signal response

Spots customers comparing you with a rival and answers within hours: a matched email, the capabilities they have not tried, and a briefed CSM.

## Steps

1. **Spot competitor interest** (builds attribute)

   A signal on the user or account when they visit a versus page, click a competitor named link, mention a rival in support or chat, or download a comparison. It records which competitor, how strong the signal is, how recent it is, and whether it reads as evaluation, dissatisfaction, curiosity or leaving. It stays live for 30 days after the last signal.

2. **Group by what they intend** (builds segment)

   Existing customers and late stage prospects with a medium or strong signal in the last 14 days, split by intent so each gets a different response. Brand new prospects are left out, because for them competitive intel belongs in the AE's sales process.

3. **Write a reply per intent** (builds email_html)

   Evaluation gets an honest comparison aimed at their use case. Dissatisfaction gets a direct note from their CSM asking what is not working, with no product pitch. Curiosity gets the reason most teams pick you plus a case study. Leaving gets an executive sponsor offering a business review. Strong signals come from the named CSM or AE, weak ones from marketing.

4. **Show what they are missing** (builds recommendation)

   An in app surface listing the capabilities their peers use for high value work that this account has never tried. It runs for 30 days and answers why stay with something concrete.

5. **Respond within four hours** (builds journey)

   The matched email goes out within four hours of the signal and the in app surface switches on the same day. On day 2 a strong signal raises a CSM or AE task carrying the competitor name, the intent, talking points and the account's usage. On day 7, high ARR accounts still showing intent get an executive sponsor offer. They leave on a clear retention signal, on churn, or after 30 quiet days.

6. **See which rivals you lose to** (builds dashboard)

   Signal volume per competitor, how often you save an account from each one, the split of intents, and the ARR sitting under competitive pressure.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The page_viewed event in your project
- The email_clicked event in your project

Writes:

- A new attribute, from step 1 "Spot competitor interest"
- A new segment, from step 2 "Group by what they intend"
- A new designed email, from step 3 "Write a reply per intent"
- A new product recommendation, from step 4 "Show what they are missing"
- A new journey, from step 5 "Respond within four hours"
- A new dashboard, from step 6 "See which rivals you lose to"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, recommendation.
