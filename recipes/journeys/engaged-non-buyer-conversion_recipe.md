---
name: engaged-non-buyer-conversion
description: Use when a user mentions "engaged non-buyer conversion", "high-engagement-low-conversion", "stuck free user journey", or asks for related help. Free/trial users who consistently engage with the product (multiple sessions, deep feature use, opens marketing emails) but haven't converted after 30+ days get a diagnostic intervention — personalized offer + AE/human touch option + agent handoff. NOT generic upgrade nag.
arguments: []
intempt:
  id: engaged-non-buyer-conversion
  version: 1.0.0
  slashCommand: /engaged-non-buyer-conversion
  group: Journeys
  shortDescription: "Free/trial users who consistently engage with the product (multiple sessions, deep feature use, opens marketing emails) but haven't converted after 30+ days get a diagnostic intervention — personalized offer + AE/human touch option + agent handoff. NOT generic upgrade nag."
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
      title: Build Engagement-vs-Conversion AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: engagement_paradox
      description: 'Create an AI-derived attribute ''engagement_paradox_score'' on the User object. Calculates the gap between engagement intensity and conversion behavior. Inputs: sessions in last 30 days, feature breadth/depth, marketing email engagement (opens / clicks), in-product activity vs. typical-converter benchmarks. High score = the user behaves like a converter SHOULD behave, but hasn''t converted. Output: numeric 0-100. Score >= 70 = high engagement paradox (engaged but stuck — the most interesting cohort). Includes a diagnostic field naming the likely blocker (price-sensitivity / feature-gap / authority-issue / decision-paralysis / no-urgency) inferred from behavior patterns.'
      prompt: 'Create an AI-derived attribute ''engagement_paradox_score'' on the User object. Calculates the gap between engagement intensity and conversion behavior. Inputs: sessions in last 30 days, feature breadth/depth, marketing email engagement (opens / clicks), in-product activity vs. typical-converter benchmarks. High score = the user behaves like a converter SHOULD behave, but hasn''t converted. Output: numeric 0-100. Score >= 70 = high engagement paradox (engaged but stuck — the most interesting cohort). Includes a diagnostic field naming the likely blocker (price-sensitivity / feature-gap / authority-issue / decision-paralysis / no-urgency) inferred from behavior patterns.'
    - step: 2
      title: Identify Engaged Non-Buyers
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - engagement_paradox
      description: Build a segment 'Engaged non-buyers - last 60 days' capturing users where (a) account age is 30+ days AND (b) subscription_status is free or trialing AND (c) engagement_paradox_score >= 70. Excludes users in active sales conversations (don't double-orchestrate) and users who explicitly declined an upgrade in the last 90 days (respect the no).
      prompt: Build a segment 'Engaged non-buyers - last 60 days' capturing users where (a) account age is 30+ days AND (b) subscription_status is free or trialing AND (c) engagement_paradox_score >= 70. Excludes users in active sales conversations (don't double-orchestrate) and users who explicitly declined an upgrade in the last 90 days (respect the no).
    - step: 3
      title: Build Diagnostic Content
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - engagement_paradox
      - segment
      description: 'Generate diagnostic email variants per inferred blocker. Price-sensitivity blocker: ''You''re using [Product] like a paid customer — here''s a 30% retention discount for the first 3 months.'' Feature-gap blocker: ''We noticed you tried [feature X] but didn''t continue. Here''s what most users do next — and 1:1 help if you''d like.'' Authority-issue blocker: ''Need help making the case internally? Here''s a business-case template + your team''s usage summary to share with your manager.'' Decision-paralysis blocker: ''You''ve evaluated [Product] thoroughly. Want a 15-min decision-clarity call?'' No-urgency blocker: ''No rush — but if a deadline is approaching, here''s a limited-time price-lock offer.'' Send-from: success@ or matched AE.'
      prompt: 'Generate diagnostic email variants per inferred blocker. Price-sensitivity blocker: ''You''re using [Product] like a paid customer — here''s a 30% retention discount for the first 3 months.'' Feature-gap blocker: ''We noticed you tried [feature X] but didn''t continue. Here''s what most users do next — and 1:1 help if you''d like.'' Authority-issue blocker: ''Need help making the case internally? Here''s a business-case template + your team''s usage summary to share with your manager.'' Decision-paralysis blocker: ''You''ve evaluated [Product] thoroughly. Want a 15-min decision-clarity call?'' No-urgency blocker: ''No rush — but if a deadline is approaching, here''s a limited-time price-lock offer.'' Send-from: success@ or matched AE.'
    - step: 4
      title: Build Agent Diagnostic Flow
      command: create_agent
      produces: agent
      bindsAs: agent
      dependsOn:
      - engagement_paradox
      - segment
      description: 'Configure an AI agent scenario ''Engaged non-buyer diagnostic'' that engages high-engagement-paradox users via in-app chat or email reply. Scenario: surface user''s product usage warmly (''I see you''ve been using [Product] for 45 days — that''s great!''), then ask the diagnostic question (''What''s keeping you from upgrading? Cost, features, internal approval, timing, or something else?''). Branch on response: route price to retention-discount offer, feature-gap to PM-feedback queue + feature-roadmap signal, authority to business-case generation, timing to deferred-followup, other to human handoff. The agent generates qualified diagnostic signal for the AE/CSM, not raw chat.'
      prompt: 'Configure an AI agent scenario ''Engaged non-buyer diagnostic'' that engages high-engagement-paradox users via in-app chat or email reply. Scenario: surface user''s product usage warmly (''I see you''ve been using [Product] for 45 days — that''s great!''), then ask the diagnostic question (''What''s keeping you from upgrading? Cost, features, internal approval, timing, or something else?''). Branch on response: route price to retention-discount offer, feature-gap to PM-feedback queue + feature-roadmap signal, authority to business-case generation, timing to deferred-followup, other to human handoff. The agent generates qualified diagnostic signal for the AE/CSM, not raw chat.'
    - step: 5
      title: Build Conversion Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - engagement_paradox
      - segment
      - email_asset
      - agent
      description: 'Build a 3-touch diagnostic journey wired to engaged-non-buyer segment. Touch 1 (Day 0 of entry): diagnostic email matched to inferred blocker. Touch 2 (Day 3, if no engagement): in-app chat invitation to the diagnostic agent on next session. Touch 3 (Day 7, if still no conversion): personalized AE outreach task with the full engagement-paradox profile + inferred blocker + suggested approach attached. Exit on: subscription_created (won — celebrate), explicit decline / opt-out, or successful agent diagnostic (handoff to appropriate downstream — sales, support, or PM).'
      prompt: 'Build a 3-touch diagnostic journey wired to engaged-non-buyer segment. Touch 1 (Day 0 of entry): diagnostic email matched to inferred blocker. Touch 2 (Day 3, if no engagement): in-app chat invitation to the diagnostic agent on next session. Touch 3 (Day 7, if still no conversion): personalized AE outreach task with the full engagement-paradox profile + inferred blocker + suggested approach attached. Exit on: subscription_created (won — celebrate), explicit decline / opt-out, or successful agent diagnostic (handoff to appropriate downstream — sales, support, or PM).'
    - step: 6
      title: Build Engagement-Paradox Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - engagement_paradox
      - segment
      - email_asset
      - agent
      - journey
      description: 'Compose an engaged-non-buyer dashboard: paradox-cohort size over time (is this cohort growing or shrinking — product fit signal), conversion lift vs. control (cohort getting this journey vs. holdout staying on generic free-tier nurture), conversion by inferred blocker (which diagnostic angle actually converts — informs pricing/product/sales-collateral decisions), agent-diagnostic completion rate, and time-to-conversion distribution (most paradox conversions happen within 14 days of journey entry — if not, the blocker is structural).'
      prompt: 'Compose an engaged-non-buyer dashboard: paradox-cohort size over time (is this cohort growing or shrinking — product fit signal), conversion lift vs. control (cohort getting this journey vs. holdout staying on generic free-tier nurture), conversion by inferred blocker (which diagnostic angle actually converts — informs pricing/product/sales-collateral decisions), agent-diagnostic completion rate, and time-to-conversion distribution (most paradox conversions happen within 14 days of journey entry — if not, the blocker is structural).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: agent, type: agent, cardinality: single, description: "AI Agent Scenario produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Engaged Non Buyer Conversion

## Procedure

1. **Build Engagement-vs-Conversion AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'engagement_paradox_score' on the User object. Calculates the gap between engagement intensity and conversion behavior. Inputs: sessions in last 30 days, feature breadth/depth, marketing email engagement (opens / clicks), in-product activity vs. typical-converter benchmarks. High score = the user behaves like a converter SHOULD behave, but hasn't converted. Output: numeric 0-100. Score >= 70 = high engagement paradox (engaged but stuck — the most interesting cohort). Includes a diagnostic field naming the likely blocker (price-sensitivity / feature-gap / authority-issue / decision-paralysis / no-urgency) inferred from behavior patterns. → produces: attribute
2. **Identify Engaged Non-Buyers** [`create_segment`] — Build a segment 'Engaged non-buyers - last 60 days' capturing users where (a) account age is 30+ days AND (b) subscription_status is free or trialing AND (c) engagement_paradox_score >= 70. Excludes users in active sales conversations (don't double-orchestrate) and users who explicitly declined an upgrade in the last 90 days (respect the no). → produces: segment
3. **Build Diagnostic Content** [`create_email_content`] — Generate diagnostic email variants per inferred blocker. Price-sensitivity blocker: 'You're using [Product] like a paid customer — here's a 30% retention discount for the first 3 months.' Feature-gap blocker: 'We noticed you tried [feature X] but didn't continue. Here's what most users do next — and 1:1 help if you'd like.' Authority-issue blocker: 'Need help making the case internally? Here's a business-case template + your team's usage summary to share with your manager.' Decision-paralysis blocker: 'You've evaluated [Product] thoroughly. Want a 15-min decision-clarity call?' No-urgency blocker: 'No rush — but if a deadline is approaching, here's a limited-time price-lock offer.' Send-from: success@ or matched AE. → produces: asset
4. **Build Agent Diagnostic Flow** [`create_agent`] — Configure an AI agent scenario 'Engaged non-buyer diagnostic' that engages high-engagement-paradox users via in-app chat or email reply. Scenario: surface user's product usage warmly ('I see you've been using [Product] for 45 days — that's great!'), then ask the diagnostic question ('What's keeping you from upgrading? Cost, features, internal approval, timing, or something else?'). Branch on response: route price to retention-discount offer, feature-gap to PM-feedback queue + feature-roadmap signal, authority to business-case generation, timing to deferred-followup, other to human handoff. The agent generates qualified diagnostic signal for the AE/CSM, not raw chat. → produces: agent
5. **Build Conversion Journey** [`create_journey`] — Build a 3-touch diagnostic journey wired to engaged-non-buyer segment. Touch 1 (Day 0 of entry): diagnostic email matched to inferred blocker. Touch 2 (Day 3, if no engagement): in-app chat invitation to the diagnostic agent on next session. Touch 3 (Day 7, if still no conversion): personalized AE outreach task with the full engagement-paradox profile + inferred blocker + suggested approach attached. Exit on: subscription_created (won — celebrate), explicit decline / opt-out, or successful agent diagnostic (handoff to appropriate downstream — sales, support, or PM). → produces: journey
6. **Build Engagement-Paradox Dashboard** [`create_dashboard`] — Compose an engaged-non-buyer dashboard: paradox-cohort size over time (is this cohort growing or shrinking — product fit signal), conversion lift vs. control (cohort getting this journey vs. holdout staying on generic free-tier nurture), conversion by inferred blocker (which diagnostic angle actually converts — informs pricing/product/sales-collateral decisions), agent-diagnostic completion rate, and time-to-conversion distribution (most paradox conversions happen within 14 days of journey entry — if not, the blocker is structural). → produces: dashboard
