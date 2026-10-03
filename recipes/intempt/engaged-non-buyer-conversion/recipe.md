---
id: engaged-non-buyer-conversion
title: Engaged users who never buy
slash_command: /engaged-non-buyer-conversion
group: Journeys
owner: intempt
summary: Finds free users who behave like paying customers, works out what is actually blocking them,
  and answers that instead of nagging them to upgrade.
description: >-
  Free/trial users who consistently engage with the product (multiple sessions, deep feature use, opens
  marketing emails) but haven't converted after 30+ days get a diagnostic intervention, personalized offer
  + AE/human touch option + agent handoff. NOT generic upgrade nag.
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
    - activation
    - engaged-non-buyer
    - diagnostic-intervention
prerequisites:
  events:
    - value: user_signed_up
      severity: blocking
    - value: feature_used
      severity: blocking
steps:
  - id: s1
    title: Measure the gap
    summary: >-
      A 0 to 100 score for the distance between how much someone uses the product and the fact they have
      not paid, built from sessions in the last 30 days, how broadly and deeply they use features, and
      email engagement, all against the profile of people who do convert. It also names the likely blocker:
      price, a missing feature, no authority, indecision or no urgency.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'engagement_paradox_score' on the User object. Calculates the gap
      between engagement intensity and conversion behavior. Inputs: sessions in last 30 days, feature
      breadth/depth, marketing email engagement (opens / clicks), in-product activity vs. typical-converter
      benchmarks. High score = the user behaves like a converter SHOULD behave, but hasn't converted.
      Output: numeric 0-100. Score >= 70 = high engagement paradox (engaged but stuck: the most interesting
      cohort). Includes a diagnostic field naming the likely blocker (price-sensitivity / feature-gap
      / authority-issue / decision-paralysis / no-urgency) inferred from behavior patterns.
  - id: s2
    title: Find engaged free users
    summary: >-
      Accounts at least 30 days old, still free or trialing, scoring 70 or above. People already in a
      sales conversation are left out, and so is anyone who turned down an upgrade in the last 90 days.
    builds: segment
    description: >-
      Build a segment 'Engaged non-buyers - last 60 days' capturing users where (a) account age is 30+
      days AND (b) subscription_status is free or trialing AND (c) engagement_paradox_score >= 70. Excludes
      users in active sales conversations (don't double-orchestrate) and users who explicitly declined
      an upgrade in the last 90 days (respect the no). Use the result of "Measure the gap".
    dependsOn:
      - s1
  - id: s3
    title: Write one email per blocker
    summary: >-
      Price gets 30% off for the first three months. A missing feature gets what most users do next plus
      an offer of help. No authority gets a business case template and their own usage summary to pass
      upward. Indecision gets a 15 minute clarity call. No urgency gets a price lock. Sent by success
      or by their AE.
    builds: email_html
    description: >-
      Generate diagnostic email variants per inferred blocker. Price-sensitivity blocker: 'You're using
      [Product] like a paid customer: here's a 30% retention discount for the first 3 months.' Feature-gap
      blocker: 'We noticed you tried [feature X] but didn't continue. Here's what most users do next:
      and 1:1 help if you'd like.' Authority-issue blocker: 'Need help making the case internally? Here's
      a business-case template + your team's usage summary to share with your manager.' Decision-paralysis
      blocker: 'You've evaluated [Product] thoroughly. Want a 15-min decision-clarity call?' No-urgency
      blocker: 'No rush: but if a deadline is approaching, here's a limited-time price-lock offer.' Send-from:
      success@ or matched AE. Use the result of "Measure the gap", "Find engaged free users".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Ask what is stopping them
    summary: >-
      An AI agent opens in app or by email reply, notes how long they have been using the product, and
      asks what is holding up the upgrade: cost, features, approval, timing or something else. Each answer
      routes somewhere: a discount, the product feedback queue, a business case, a later follow up, or
      a human.
    builds: agent
    description: >-
      Configure an AI agent scenario 'Engaged non-buyer diagnostic' that engages high-engagement-paradox
      users via in-app chat or email reply. Scenario: surface user's product usage warmly ('I see you've
      been using [Product] for 45 days: that's great!'), then ask the diagnostic question ('What's keeping
      you from upgrading? Cost, features, internal approval, timing, or something else?'). Branch on response:
      route price to retention-discount offer, feature-gap to PM-feedback queue + feature-roadmap signal,
      authority to business-case generation, timing to deferred-followup, other to human handoff. The
      agent generates qualified diagnostic signal for the AE/CSM, not raw chat. Use the result of "Measure
      the gap", "Find engaged free users".
    dependsOn:
      - s1
      - s2
  - id: s5
    title: Diagnose, then bring a human in
    summary: >-
      The blocker email on day 0, an invitation to the agent on their next session if nothing happens
      by day 3, and on day 7 an AE task carrying the score, the blocker and a suggested approach. They
      leave when they subscribe, when they decline, or when the agent gets an answer and hands them on.
    builds: journey
    description: >-
      Build a 3-touch diagnostic journey wired to engaged-non-buyer segment. Touch 1 (Day 0 of entry):
      diagnostic email matched to inferred blocker. Touch 2 (Day 3, if no engagement): in-app chat invitation
      to the diagnostic agent on next session. Touch 3 (Day 7, if still no conversion): personalized AE
      outreach task with the full engagement-paradox profile + inferred blocker + suggested approach attached.
      Exit on: subscription_created (won (celebrate), explicit decline / opt-out, or successful agent
      diagnostic (handoff to appropriate downstream) sales, support, or PM). Use the result of "Measure
      the gap", "Find engaged free users", "Write one email per blocker", "Ask what is stopping them".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: See which angle converts
    summary: >-
      How the cohort grows or shrinks, conversion against a holdout left on the generic free tier nurture,
      conversion by blocker, how often the agent gets an answer, and how long conversion takes.
    builds: dashboard
    description: >-
      Compose an engaged-non-buyer dashboard: paradox-cohort size over time (is this cohort growing or
      shrinking: product fit signal), conversion lift vs. control (cohort getting this journey vs. holdout
      staying on generic free-tier nurture), conversion by inferred blocker (which diagnostic angle actually
      converts: informs pricing/product/sales-collateral decisions), agent-diagnostic completion rate,
      and time-to-conversion distribution (most paradox conversions happen within 14 days of journey entry:
      if not, the blocker is structural). Use the result of "Measure the gap", "Find engaged free users",
      "Write one email per blocker", "Ask what is stopping them", "Diagnose, then bring a human in".
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
  - key: agent
    producedByStep: s4
    type: agent
    description: AI Agent Scenario produced by this recipe.
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

# Engaged users who never buy

Finds free users who behave like paying customers, works out what is actually blocking them, and answers that instead of nagging them to upgrade.

## Steps

1. **Measure the gap** (builds attribute)

   A 0 to 100 score for the distance between how much someone uses the product and the fact they have not paid, built from sessions in the last 30 days, how broadly and deeply they use features, and email engagement, all against the profile of people who do convert. It also names the likely blocker: price, a missing feature, no authority, indecision or no urgency.

2. **Find engaged free users** (builds segment)

   Accounts at least 30 days old, still free or trialing, scoring 70 or above. People already in a sales conversation are left out, and so is anyone who turned down an upgrade in the last 90 days.

3. **Write one email per blocker** (builds email_html)

   Price gets 30% off for the first three months. A missing feature gets what most users do next plus an offer of help. No authority gets a business case template and their own usage summary to pass upward. Indecision gets a 15 minute clarity call. No urgency gets a price lock. Sent by success or by their AE.

4. **Ask what is stopping them** (builds agent)

   An AI agent opens in app or by email reply, notes how long they have been using the product, and asks what is holding up the upgrade: cost, features, approval, timing or something else. Each answer routes somewhere: a discount, the product feedback queue, a business case, a later follow up, or a human.

5. **Diagnose, then bring a human in** (builds journey)

   The blocker email on day 0, an invitation to the agent on their next session if nothing happens by day 3, and on day 7 an AE task carrying the score, the blocker and a suggested approach. They leave when they subscribe, when they decline, or when the agent gets an answer and hands them on.

6. **See which angle converts** (builds dashboard)

   How the cohort grows or shrinks, conversion against a holdout left on the generic free tier nurture, conversion by blocker, how often the agent gets an answer, and how long conversion takes.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **agent** (agent): AI Agent Scenario produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build agent, dashboard, journey.
