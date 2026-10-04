---
id: predictive-churn-tiered-intervention
title: Tiered churn intervention
slash_command: /predictive-churn-tiered-intervention
group: Journeys
owner: intempt
curator: somya
summary: 'Scores churn risk daily and treats each band differently: content at low risk, in app help at
  medium, a CSM at high, a founder''s email at critical.'
description: >-
  Predictive churn-risk AI attribute with nuanced scores routes users to one of four intervention tiers,
  low gets nurture content, medium gets personalized in-app + email, high gets CSM task + recommendation
  surface, critical gets agent handoff + exec-sponsor task, the CleverTap-style differentiated churn rescue.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - churn-prevention
    - tiered-intervention
    - predictive
prerequisites:
  events:
    - value: session_start
      severity: blocking
    - value: feature_used
      severity: recommended
touches:
  reads:
    - The session_start event in your project
    - The feature_used event in your project
  writes:
    - A new attribute, from step 1 "Score churn risk daily"
    - A new segment, from step 2 "Take everyone above 30"
    - A new designed email, from step 3 "Write an email per band"
    - A new landing page, from step 4 "Catch them when they log in"
    - A new product recommendation, from step 5 "Recommend what keeps people"
    - A new journey, from step 6 "Treat each band differently"
    - A new dashboard, from step 7 "See if the bands hold up"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score churn risk daily
    summary: >-
      A 0 to 100 score from how sessions are trending over 30, 14 and 7 days, features falling out of
      use, the direction of support sentiment, billing signals, what similar accounts did, and account
      level usage for B2B. Banded low 0 to 29, medium 30 to 59, high 60 to 79 and critical 80 to 100,
      and recomputed on any significant event so a sudden drop is caught quickly.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'churn_risk_score' on the User object, refreshed daily. Inputs: engagement
      velocity (sessions trend over 30/14/7 days), feature usage decay, support sentiment trajectory,
      billing-status signals, peer-cohort churn patterns, account-level usage (for B2B). Output: numeric
      0-100 with tier label (low (0-29) / medium (30-59) / high (60-79) / critical (80-100). NOT binary
      at-risk-or-not) the nuance is the point: medium and high get different treatments. Refresh on every
      significant behavioral event so a sudden engagement drop is caught fast.
  - id: s2
    title: Take everyone above 30
    summary: >-
      All paying users scoring 30 or more, held in bands by that score. The first 14 days are excluded
      because early signals are unreliable, and so is anyone already in a save flow.
    builds: segment
    description: >-
      Build a parent segment 'Churn risk - paying users' capturing all paying users with churn_risk_score
      >= 30. Implicitly partitioned by tier through the attribute. Excludes users in the first 14 days
      (early signals aren't reliable yet) and users already in active save flows (no double-intervention).
      Use the result of "Score churn risk daily".
    dependsOn:
      - s1
  - id: s3
    title: Write an email per band
    summary: >-
      Medium gets helpful content about the features that keep people like them, plus a link back to where
      they left off. High gets a direct offer of help from their CSM and a 15 minute walkthrough. Critical
      gets a personal letter from the founder with a calendar link. Sent from success, from the named
      CSM, and from the founder respectively.
    builds: email_html
    description: >-
      Generate per-tier email content. Medium tier: educational content matched to underutilized features
      that drive retention in their cohort + personalized 'pick up where you left off' deep-link. Tone:
      helpful, not alarmed. High tier: urgent value reinforcement, CSM availability signal, specific use-case
      help offer ('Want a 15-min walkthrough on [feature]?'). Critical tier: founder/CEO personal letter
      ('I noticed your account hasn't been used much: anything we can do?'), with direct calendar link
      and concrete asks. Send-from: success@ for medium, named CSM for high, founder/CEO for critical.
      Use the result of "Score churn risk daily", "Take everyone above 30".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Catch them when they log in
    summary: >-
      High risk users see a banner pointing at the path most people in their position succeed with. Critical
      users get a full screen note from their CSM or the founder offering a call. Only when the signal
      is strong, never to everyone.
    builds: page
    description: >-
      Generate in-app messages for high-tier users when they DO log in (rare and precious moments). Format:
      contextual banner referencing their most-likely-success-path ('Most users in your segment succeed
      by trying [feature] (want a 60-second walkthrough?'). For critical-tier users on rare logins: a
      personal-touch interrupt) full-screen modal from the CSM or founder offering a 1:1 call. Never blanket:
      only when AI signal is strong. Use the result of "Score churn risk daily", "Take everyone above
      30", "Write an email per band".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Recommend what keeps people
    summary: >-
      For high and critical users, the features their cohort uses successfully and they have never tried,
      ranked by how strongly each one correlates with staying. It shows on the dashboard, inside emails
      and in page slots.
    builds: recommendation
    description: >-
      Configure a recommendation surface specifically for high+critical tier users: surfaces underutilized
      features that THIS user's cohort uses successfully but THIS user has not adopted (the 'features-that-stick-users'
      pattern). Renders in-app on dashboard, in email content blocks, and on personalization slots when
      the user does visit. The recommendation logic prioritizes features with high retention-correlation
      in this user's segment. Use the result of "Score churn risk daily", "Take everyone above 30".
    dependsOn:
      - s1
      - s2
  - id: s6
    title: Treat each band differently
    summary: >-
      Bands are read at entry and again weekly. Low gets one light email on day 7. Medium gets a tip on
      day 0, in app help at the next login, and recommendations on day 7. High gets a CSM email on day
      0, an urgent banner at the next session, and a same day CSM task. Critical gets all of it inside
      four hours: the founder's email, an agent offering a call, a CSM task and an executive sponsor task.
      People who improve drop out, people who worsen move up a band. They leave once the score stays under
      30 for 14 days, on cancellation, or on unsubscribe.
    builds: journey
    description: >-
      Build a tiered journey wired to the churn-risk segment. Branch on churn_risk tier at entry AND re-evaluate
      weekly: LOW tier (light-touch nurture email at Day 7 (no urgency, just value content). MEDIUM tier)
      Touch 1 email Day 0 (helpful tip), Touch 2 in-app at next login (deep-link to retention feature),
      Touch 3 email Day 7 with recommendation surface highlighting cohort-success features. HIGH tier:
      Touch 1 email Day 0 from CSM with offer of help, in-app urgent banner on next session, CSM task
      created same-day. CRITICAL tier: within 4 hours: founder/CEO personal email + agent handoff offering
      1:1 call + urgent CSM task + executive-sponsor task. Tier RECOMPUTED weekly: users de-escalate (engagement
      returned) exit gracefully; users escalate get tier-appropriate next-touch. Exit on: churn_risk drops
      below 30 for 14+ days (recovered: log retention_win), subscription_canceled (handoff to post-cancel-winback),
      or unsubscribe. Use the result of "Score churn risk daily", "Take everyone above 30", "Write an
      email per band", "Catch them when they log in", "Recommend what keeps people".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
  - id: s7
    title: See if the bands hold up
    summary: >-
      How users spread across the bands each week, the save rate in each one, how fast a human reaches
      critical users against a four hour target, the ARR saved per band, which way accounts are migrating,
      and predicted against actual churn at 30, 60 and 90 days.
    builds: dashboard
    description: >-
      Compose a tiered churn intervention dashboard: distribution of users across tiers (low/medium/high/critical)
      per week (leading indicator of book-of-business health, tier-level save rate (% of users in each
      tier who exit risk vs. churn) proves tiered strategy works), critical-tier CSM response SLA (target:
      <4hr for human-touch start), ARR-weighted save value by tier, and tier-migration tracking (high
      to medium = success, medium to high = early warning). Compare model accuracy: predicted churn vs.
      actual churn at 30/60/90 days. Use the result of "Score churn risk daily", "Take everyone above
      30", "Write an email per band", "Catch them when they log in", "Recommend what keeps people", "Treat
      each band differently".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
      - s6
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
    producedByStep: s4
    type: asset
    description: Asset produced by this recipe.
  - key: recommendation
    producedByStep: s5
    type: recommendation
    description: Recommendation Surface produced by this recipe.
  - key: journey
    producedByStep: s6
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s7
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Tiered churn intervention

Scores churn risk daily and treats each band differently: content at low risk, in app help at medium, a CSM at high, a founder's email at critical.

## Steps

1. **Score churn risk daily** (builds attribute)

   A 0 to 100 score from how sessions are trending over 30, 14 and 7 days, features falling out of use, the direction of support sentiment, billing signals, what similar accounts did, and account level usage for B2B. Banded low 0 to 29, medium 30 to 59, high 60 to 79 and critical 80 to 100, and recomputed on any significant event so a sudden drop is caught quickly.

2. **Take everyone above 30** (builds segment)

   All paying users scoring 30 or more, held in bands by that score. The first 14 days are excluded because early signals are unreliable, and so is anyone already in a save flow.

3. **Write an email per band** (builds email_html)

   Medium gets helpful content about the features that keep people like them, plus a link back to where they left off. High gets a direct offer of help from their CSM and a 15 minute walkthrough. Critical gets a personal letter from the founder with a calendar link. Sent from success, from the named CSM, and from the founder respectively.

4. **Catch them when they log in** (builds page)

   High risk users see a banner pointing at the path most people in their position succeed with. Critical users get a full screen note from their CSM or the founder offering a call. Only when the signal is strong, never to everyone.

5. **Recommend what keeps people** (builds recommendation)

   For high and critical users, the features their cohort uses successfully and they have never tried, ranked by how strongly each one correlates with staying. It shows on the dashboard, inside emails and in page slots.

6. **Treat each band differently** (builds journey)

   Bands are read at entry and again weekly. Low gets one light email on day 7. Medium gets a tip on day 0, in app help at the next login, and recommendations on day 7. High gets a CSM email on day 0, an urgent banner at the next session, and a same day CSM task. Critical gets all of it inside four hours: the founder's email, an agent offering a call, a CSM task and an executive sponsor task. People who improve drop out, people who worsen move up a band. They leave once the score stays under 30 for 14 days, on cancellation, or on unsubscribe.

7. **See if the bands hold up** (builds dashboard)

   How users spread across the bands each week, the save rate in each one, how fast a human reaches critical users against a four hour target, the ARR saved per band, which way accounts are migrating, and predicted against actual churn at 30, 60 and 90 days.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The session_start event in your project
- The feature_used event in your project

Writes:

- A new attribute, from step 1 "Score churn risk daily"
- A new segment, from step 2 "Take everyone above 30"
- A new designed email, from step 3 "Write an email per band"
- A new landing page, from step 4 "Catch them when they log in"
- A new product recommendation, from step 5 "Recommend what keeps people"
- A new journey, from step 6 "Treat each band differently"
- A new dashboard, from step 7 "See if the bands hold up"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, page, recommendation.
