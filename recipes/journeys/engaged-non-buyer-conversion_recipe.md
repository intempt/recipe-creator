---
name: engaged-non-buyer-conversion
description: Use when a user mentions "engaged non-buyer conversion", "high-engagement-low-conversion", "stuck free user journey", or asks for related help. Free/trial users who consistently engage with the product (multiple sessions, deep feature use, opens marketing emails) but haven't converted after 30+ days get a diagnostic intervention, personalized offer + AE/human touch option + agent handoff. NOT generic upgrade nag.
arguments: []
intempt:
  id: engaged-non-buyer-conversion
  title: "Engaged users who never buy"
  version: 1.0.0
  slashCommand: /engaged-non-buyer-conversion
  group: Journeys
  shortDescription: "Finds free users who behave like paying customers, works out what is actually blocking them, and answers that instead of nagging them to upgrade."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [activation, engaged-non-buyer, diagnostic-intervention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: user_signed_up, severity: blocking }
      - { value: feature_used, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_agent
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Measure the gap"
      command: create_ai_attribute
      produces: attribute
      bindsAs: engagement_paradox
      description: "A 0 to 100 score for the distance between how much someone uses the product and the fact they have not paid, built from sessions in the last 30 days, how broadly and deeply they use features, and email engagement, all against the profile of people who do convert. It also names the likely blocker: price, a missing feature, no authority, indecision or no urgency."
      prompt: 'Create an AI-derived attribute ''engagement_paradox_score'' on the User object. Calculates the gap between engagement intensity and conversion behavior. Inputs: sessions in last 30 days, feature breadth/depth, marketing email engagement (opens / clicks), in-product activity vs. typical-converter benchmarks. High score = the user behaves like a converter SHOULD behave, but hasn''t converted. Output: numeric 0-100. Score >= 70 = high engagement paradox (engaged but stuck: the most interesting cohort). Includes a diagnostic field naming the likely blocker (price-sensitivity / feature-gap / authority-issue / decision-paralysis / no-urgency) inferred from behavior patterns.'
    - step: 2
      title: "Find engaged free users"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - engagement_paradox
      description: "Accounts at least 30 days old, still free or trialing, scoring 70 or above. People already in a sales conversation are left out, and so is anyone who turned down an upgrade in the last 90 days."
      prompt: Build a segment 'Engaged non-buyers - last 60 days' capturing users where (a) account age is 30+ days AND (b) subscription_status is free or trialing AND (c) engagement_paradox_score >= 70. Excludes users in active sales conversations (don't double-orchestrate) and users who explicitly declined an upgrade in the last 90 days (respect the no).
    - step: 3
      title: "Write one email per blocker"
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - engagement_paradox
      - segment
      description: "Price gets 30% off for the first three months. A missing feature gets what most users do next plus an offer of help. No authority gets a business case template and their own usage summary to pass upward. Indecision gets a 15 minute clarity call. No urgency gets a price lock. Sent by success or by their AE."
      prompt: 'Generate diagnostic email variants per inferred blocker. Price-sensitivity blocker: ''You''re using [Product] like a paid customer: here''s a 30% retention discount for the first 3 months.'' Feature-gap blocker: ''We noticed you tried [feature X] but didn''t continue. Here''s what most users do next: and 1:1 help if you''d like.'' Authority-issue blocker: ''Need help making the case internally? Here''s a business-case template + your team''s usage summary to share with your manager.'' Decision-paralysis blocker: ''You''ve evaluated [Product] thoroughly. Want a 15-min decision-clarity call?'' No-urgency blocker: ''No rush: but if a deadline is approaching, here''s a limited-time price-lock offer.'' Send-from: success@ or matched AE.'
    - step: 4
      title: "Ask what is stopping them"
      command: create_agent
      produces: agent
      bindsAs: agent
      dependsOn:
      - engagement_paradox
      - segment
      description: "An AI agent opens in app or by email reply, notes how long they have been using the product, and asks what is holding up the upgrade: cost, features, approval, timing or something else. Each answer routes somewhere: a discount, the product feedback queue, a business case, a later follow up, or a human."
      prompt: 'Configure an AI agent scenario ''Engaged non-buyer diagnostic'' that engages high-engagement-paradox users via in-app chat or email reply. Scenario: surface user''s product usage warmly (''I see you''ve been using [Product] for 45 days: that''s great!''), then ask the diagnostic question (''What''s keeping you from upgrading? Cost, features, internal approval, timing, or something else?''). Branch on response: route price to retention-discount offer, feature-gap to PM-feedback queue + feature-roadmap signal, authority to business-case generation, timing to deferred-followup, other to human handoff. The agent generates qualified diagnostic signal for the AE/CSM, not raw chat.'
    - step: 5
      title: "Diagnose, then bring a human in"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - engagement_paradox
      - segment
      - email_asset
      - agent
      description: "The blocker email on day 0, an invitation to the agent on their next session if nothing happens by day 3, and on day 7 an AE task carrying the score, the blocker and a suggested approach. They leave when they subscribe, when they decline, or when the agent gets an answer and hands them on."
      prompt: 'Build a 3-touch diagnostic journey wired to engaged-non-buyer segment. Touch 1 (Day 0 of entry): diagnostic email matched to inferred blocker. Touch 2 (Day 3, if no engagement): in-app chat invitation to the diagnostic agent on next session. Touch 3 (Day 7, if still no conversion): personalized AE outreach task with the full engagement-paradox profile + inferred blocker + suggested approach attached. Exit on: subscription_created (won (celebrate), explicit decline / opt-out, or successful agent diagnostic (handoff to appropriate downstream) sales, support, or PM).'
    - step: 6
      title: "See which angle converts"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - engagement_paradox
      - segment
      - email_asset
      - agent
      - journey
      description: "How the cohort grows or shrinks, conversion against a holdout left on the generic free tier nurture, conversion by blocker, how often the agent gets an answer, and how long conversion takes."
      prompt: 'Compose an engaged-non-buyer dashboard: paradox-cohort size over time (is this cohort growing or shrinking: product fit signal), conversion lift vs. control (cohort getting this journey vs. holdout staying on generic free-tier nurture), conversion by inferred blocker (which diagnostic angle actually converts: informs pricing/product/sales-collateral decisions), agent-diagnostic completion rate, and time-to-conversion distribution (most paradox conversions happen within 14 days of journey entry: if not, the blocker is structural).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: agent, type: agent, cardinality: single, description: "AI Agent Scenario produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Engaged users who never buy

Finds free users who behave like paying customers, works out what is actually blocking them, and answers that instead of nagging them to upgrade.

## Before you run it

- Send the `user_signed_up` event
- Send the `feature_used` event

## What it does

1. **Measure the gap** (`create_ai_attribute`)

   A 0 to 100 score for the distance between how much someone uses the product and the fact they have not paid, built from sessions in the last 30 days, how broadly and deeply they use features, and email engagement, all against the profile of people who do convert. It also names the likely blocker: price, a missing feature, no authority, indecision or no urgency.

2. **Find engaged free users** (`create_segment`)

   Accounts at least 30 days old, still free or trialing, scoring 70 or above. People already in a sales conversation are left out, and so is anyone who turned down an upgrade in the last 90 days.

3. **Write one email per blocker** (`create_email_content`)

   Price gets 30% off for the first three months. A missing feature gets what most users do next plus an offer of help. No authority gets a business case template and their own usage summary to pass upward. Indecision gets a 15 minute clarity call. No urgency gets a price lock. Sent by success or by their AE.

4. **Ask what is stopping them** (`create_agent`)

   An AI agent opens in app or by email reply, notes how long they have been using the product, and asks what is holding up the upgrade: cost, features, approval, timing or something else. Each answer routes somewhere: a discount, the product feedback queue, a business case, a later follow up, or a human.

5. **Diagnose, then bring a human in** (`create_journey`)

   The blocker email on day 0, an invitation to the agent on their next session if nothing happens by day 3, and on day 7 an AE task carrying the score, the blocker and a suggested approach. They leave when they subscribe, when they decline, or when the agent gets an answer and hands them on.

6. **See which angle converts** (`create_dashboard`)

   How the cohort grows or shrinks, conversion against a holdout left on the generic free tier nurture, conversion by blocker, how often the agent gets an answer, and how long conversion takes.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **agent** (agent): AI Agent Scenario produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
