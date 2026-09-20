---
name: contract-renewal-b2b
description: Use when a user mentions "B2B contract renewal", "multi-stakeholder renewal", "enterprise renewal journey", or asks for related help. For B2B accounts approaching contract end (90/60/30 days before), fire a multi-stakeholder renewal journey reaching the buyer, the user-champion, and the economic-buyer with appropriate messaging per role, renewal is a buying process, not a single email.
arguments: []
intempt:
  id: contract-renewal-b2b
  title: "B2B contract renewal"
  version: 1.0.0
  slashCommand: /contract-renewal-b2b
  group: Journeys
  shortDescription: "Works a renewal like a buying process: the champion at 90 days, the budget holder at 60, everyone at 30, with a health read behind each message."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [b2b-renewal, multi-stakeholder, enterprise]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_ai_attribute
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Find renewals inside 90 days"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Active enterprise and mid market accounts whose contract ends between 30 and 90 days from now. Each one has several contacts, and the journey reaches them by role."
      prompt: Build a segment 'Upcoming B2B contract renewals - next 90 days' capturing accounts where contract_end_date is between 30 and 90 days from now AND account_tier is enterprise or mid-market AND subscription_status is active. Each account in the segment has multiple touched users, the journey reaches different contacts at the account with role-appropriate messaging.
    - step: 2
      title: "Read the renewal health"
      command: create_ai_attribute
      produces: attribute
      bindsAs: renewal_health
      dependsOn:
      - segment
      description: "Taken when the account enters the renewal window: whether usage grew, flattened or fell over 12 months, what outcomes and ROI you can show, whether the champion is still in role and the budget holder is reachable, the tone of six months of support tickets, and any competitor mentions in meeting notes."
      prompt: 'Create an AI-derived attribute ''renewal_health_snapshot'' on the Account object, computed at renewal-window entry. Aggregates: (a) usage trajectory over past 12 months (growing / flat / declining); (b) value delivered (key outcomes, milestones reached, ROI metric if tracked); (c) stakeholder health: champion still in role and engaged? economic buyer reachable? new stakeholders identified?; (d) support ticket sentiment over past 6 months; (e) competitor mentions in any meeting summaries. Output: composite health score + structured content for the renewal emails.'
    - step: 3
      title: "Write one email per role"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      - renewal_health
      description: "The champion gets a value recap of the year and a request to help line up the renewal conversation. The budget holder gets business value, ROI and terms. Security or IT gets documentation and certification updates. At 30 days everyone gets a consolidated reminder with the proposed terms attached. Business formal, not marketing chat."
      prompt: 'Generate role-tailored renewal content. (a) User-champion (Day 90): ''Quick value-recap of the past year (what''s working and what''s next'') focuses on product wins, usage stats, asks for help to coordinate the upcoming renewal conversation. (b) Economic buyer (Day 60): ''Your team''s renewal is up in 60 days (let''s connect on terms'') focuses on business value, ROI, growth opportunity, available terms. (c) IT/security stakeholder if known (Day 60): ''Security/compliance update for your upcoming renewal'': proactive on documentation, certifications, any changes. (d) Late reminder (Day 30): consolidated reminder to all stakeholders with proposed contract terms attached. Tone: business-formal, value-substantive, not marketing-chatty.'
    - step: 4
      title: "Reach each stakeholder in turn"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - renewal_health
      - asset
      description: "Champion at 90 days, budget holder at 60, security at 60 in parallel, and all of them at 30. The moment a CSM or AE books a renewal meeting the journey pauses and the human takes over. Accounts with weak health or any churn signal also get an urgent CSM task at day 90."
      prompt: 'Build a multi-touch multi-stakeholder journey triggered at renewal-window entry. Each touch goes to a DIFFERENT contact at the account based on their role: Touch 1 (Day 90 before contract_end): champion. Touch 2 (Day 60): economic buyer. Touch 3 (Day 60, parallel): IT/security if applicable. Touch 4 (Day 30): all stakeholders. Add a renewal-meeting-scheduled branch: if CSM/AE schedules a renewal meeting at any point, journey pauses (human-led from here). For high-risk accounts (renewal_health composite low or any churn signal), additionally create urgent CSM task at Day 90: automation alone won''t save at-risk renewals.'
    - step: 5
      title: "Forecast the renewal book"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - renewal_health
      - asset
      - journey
      description: "Renewals and ARR by quarter, the health split, what falls due when, how many renewals involved a human conversation, how many grew rather than held flat or shrank, and the renewal rate over time."
      prompt: 'Compose a B2B renewal pipeline dashboard: renewal forecast by quarter (account count + ARR at risk), renewal health distribution (green/yellow/red), days-to-renewal pipeline (which renewals are coming up when), CSM/AE engagement rate (% of renewals where a human conversation happened: target: 100% for accounts >$50K ARR), expansion-during-renewal rate (renewals that grow vs. flat vs. shrink), and renewal-rate trend over time. The strategic view that gives leadership confidence in NRR.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# B2B contract renewal

Works a renewal like a buying process: the champion at 90 days, the budget holder at 60, everyone at 30, with a health read behind each message.

## What it does

1. **Find renewals inside 90 days** (`create_segment`)

   Active enterprise and mid market accounts whose contract ends between 30 and 90 days from now. Each one has several contacts, and the journey reaches them by role.

2. **Read the renewal health** (`create_ai_attribute`)

   Taken when the account enters the renewal window: whether usage grew, flattened or fell over 12 months, what outcomes and ROI you can show, whether the champion is still in role and the budget holder is reachable, the tone of six months of support tickets, and any competitor mentions in meeting notes.

3. **Write one email per role** (`create_email_content`)

   The champion gets a value recap of the year and a request to help line up the renewal conversation. The budget holder gets business value, ROI and terms. Security or IT gets documentation and certification updates. At 30 days everyone gets a consolidated reminder with the proposed terms attached. Business formal, not marketing chat.

4. **Reach each stakeholder in turn** (`create_journey`)

   Champion at 90 days, budget holder at 60, security at 60 in parallel, and all of them at 30. The moment a CSM or AE books a renewal meeting the journey pauses and the human takes over. Accounts with weak health or any churn signal also get an urgent CSM task at day 90.

5. **Forecast the renewal book** (`create_dashboard`)

   Renewals and ARR by quarter, the health split, what falls due when, how many renewals involved a human conversation, how many grew rather than held flat or shrank, and the renewal rate over time.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
