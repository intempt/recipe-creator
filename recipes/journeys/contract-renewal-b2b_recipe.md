---
name: contract-renewal-b2b
description: Use when a user mentions "B2B contract renewal", "multi-stakeholder renewal", "enterprise renewal journey", or asks for related help. For B2B accounts approaching contract end (90/60/30 days before), fire a multi-stakeholder renewal journey reaching the buyer, the user-champion, and the economic-buyer with appropriate messaging per role — renewal is a buying process, not a single email.
arguments: []
intempt:
  id: contract-renewal-b2b
  version: 1.0.0
  slashCommand: /contract-renewal-b2b
  group: Journeys
  shortDescription: "Build a segment of active enterprise/mid-market accounts renewing in 30-90 days and trigger a multi-step email journey to their contacts."
  availability: coming-soon
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
      title: Identify Upcoming B2B Renewals
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Upcoming B2B contract renewals - next 90 days' capturing accounts where contract_end_date is between 30 and 90 days from now AND account_tier is enterprise or mid-market AND subscription_status is active. Each account in the segment has multiple touched users — the journey reaches different contacts at the account with role-appropriate messaging.
      prompt: Build a segment 'Upcoming B2B contract renewals - next 90 days' capturing accounts where contract_end_date is between 30 and 90 days from now AND account_tier is enterprise or mid-market AND subscription_status is active. Each account in the segment has multiple touched users — the journey reaches different contacts at the account with role-appropriate messaging.
    - step: 2
      title: Build Renewal Health Snapshot
      command: create_ai_attribute
      produces: attribute
      bindsAs: renewal_health
      dependsOn:
      - segment
      description: 'Create an AI-derived attribute ''renewal_health_snapshot'' on the Account object, computed at renewal-window entry. Aggregates: (a) usage trajectory over past 12 months (growing / flat / declining); (b) value delivered (key outcomes, milestones reached, ROI metric if tracked); (c) stakeholder health: champion still in role and engaged? economic buyer reachable? new stakeholders identified?; (d) support ticket sentiment over past 6 months; (e) competitor mentions in any meeting summaries. Output: composite health score + structured content for the renewal emails.'
      prompt: 'Create an AI-derived attribute ''renewal_health_snapshot'' on the Account object, computed at renewal-window entry. Aggregates: (a) usage trajectory over past 12 months (growing / flat / declining); (b) value delivered (key outcomes, milestones reached, ROI metric if tracked); (c) stakeholder health: champion still in role and engaged? economic buyer reachable? new stakeholders identified?; (d) support ticket sentiment over past 6 months; (e) competitor mentions in any meeting summaries. Output: composite health score + structured content for the renewal emails.'
    - step: 3
      title: Build Multi-Stakeholder Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      - renewal_health
      description: 'Generate role-tailored renewal content. (a) User-champion (Day 90): ''Quick value-recap of the past year — what''s working and what''s next'' — focuses on product wins, usage stats, asks for help to coordinate the upcoming renewal conversation. (b) Economic buyer (Day 60): ''Your team''s renewal is up in 60 days — let''s connect on terms'' — focuses on business value, ROI, growth opportunity, available terms. (c) IT/security stakeholder if known (Day 60): ''Security/compliance update for your upcoming renewal'' — proactive on documentation, certifications, any changes. (d) Late reminder (Day 30): consolidated reminder to all stakeholders with proposed contract terms attached. Tone: business-formal, value-substantive, not marketing-chatty.'
      prompt: 'Generate role-tailored renewal content. (a) User-champion (Day 90): ''Quick value-recap of the past year — what''s working and what''s next'' — focuses on product wins, usage stats, asks for help to coordinate the upcoming renewal conversation. (b) Economic buyer (Day 60): ''Your team''s renewal is up in 60 days — let''s connect on terms'' — focuses on business value, ROI, growth opportunity, available terms. (c) IT/security stakeholder if known (Day 60): ''Security/compliance update for your upcoming renewal'' — proactive on documentation, certifications, any changes. (d) Late reminder (Day 30): consolidated reminder to all stakeholders with proposed contract terms attached. Tone: business-formal, value-substantive, not marketing-chatty.'
    - step: 4
      title: Build Multi-Stakeholder Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - renewal_health
      - asset
      description: 'Build a multi-touch multi-stakeholder journey triggered at renewal-window entry. Each touch goes to a DIFFERENT contact at the account based on their role: Touch 1 (Day 90 before contract_end): champion. Touch 2 (Day 60): economic buyer. Touch 3 (Day 60, parallel): IT/security if applicable. Touch 4 (Day 30): all stakeholders. Add a renewal-meeting-scheduled branch: if CSM/AE schedules a renewal meeting at any point, journey pauses (human-led from here). For high-risk accounts (renewal_health composite low or any churn signal), additionally create urgent CSM task at Day 90 — automation alone won''t save at-risk renewals.'
      prompt: 'Build a multi-touch multi-stakeholder journey triggered at renewal-window entry. Each touch goes to a DIFFERENT contact at the account based on their role: Touch 1 (Day 90 before contract_end): champion. Touch 2 (Day 60): economic buyer. Touch 3 (Day 60, parallel): IT/security if applicable. Touch 4 (Day 30): all stakeholders. Add a renewal-meeting-scheduled branch: if CSM/AE schedules a renewal meeting at any point, journey pauses (human-led from here). For high-risk accounts (renewal_health composite low or any churn signal), additionally create urgent CSM task at Day 90 — automation alone won''t save at-risk renewals.'
    - step: 5
      title: Build B2B Renewal Pipeline Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - renewal_health
      - asset
      - journey
      description: 'Compose a B2B renewal pipeline dashboard: renewal forecast by quarter (account count + ARR at risk), renewal health distribution (green/yellow/red), days-to-renewal pipeline (which renewals are coming up when), CSM/AE engagement rate (% of renewals where a human conversation happened — target: 100% for accounts >$50K ARR), expansion-during-renewal rate (renewals that grow vs. flat vs. shrink), and renewal-rate trend over time. The strategic view that gives leadership confidence in NRR.'
      prompt: 'Compose a B2B renewal pipeline dashboard: renewal forecast by quarter (account count + ARR at risk), renewal health distribution (green/yellow/red), days-to-renewal pipeline (which renewals are coming up when), CSM/AE engagement rate (% of renewals where a human conversation happened — target: 100% for accounts >$50K ARR), expansion-during-renewal rate (renewals that grow vs. flat vs. shrink), and renewal-rate trend over time. The strategic view that gives leadership confidence in NRR.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Contract Renewal B2B

## Procedure

1. **Identify Upcoming B2B Renewals** [`create_segment`] — Build a segment 'Upcoming B2B contract renewals - next 90 days' capturing accounts where contract_end_date is between 30 and 90 days from now AND account_tier is enterprise or mid-market AND subscription_status is active. Each account in the segment has multiple touched users — the journey reaches different contacts at the account with role-appropriate messaging. → produces: segment
2. **Build Renewal Health Snapshot** [`create_ai_attribute`] — Create an AI-derived attribute 'renewal_health_snapshot' on the Account object, computed at renewal-window entry. Aggregates: (a) usage trajectory over past 12 months (growing / flat / declining); (b) value delivered (key outcomes, milestones reached, ROI metric if tracked); (c) stakeholder health: champion still in role and engaged? economic buyer reachable? new stakeholders identified?; (d) support ticket sentiment over past 6 months; (e) competitor mentions in any meeting summaries. Output: composite health score + structured content for the renewal emails. → produces: attribute
3. **Build Multi-Stakeholder Content** [`create_email_content`] — Generate role-tailored renewal content. (a) User-champion (Day 90): 'Quick value-recap of the past year — what's working and what's next' — focuses on product wins, usage stats, asks for help to coordinate the upcoming renewal conversation. (b) Economic buyer (Day 60): 'Your team's renewal is up in 60 days — let's connect on terms' — focuses on business value, ROI, growth opportunity, available terms. (c) IT/security stakeholder if known (Day 60): 'Security/compliance update for your upcoming renewal' — proactive on documentation, certifications, any changes. (d) Late reminder (Day 30): consolidated reminder to all stakeholders with proposed contract terms attached. Tone: business-formal, value-substantive, not marketing-chatty. → produces: asset
4. **Build Multi-Stakeholder Journey** [`create_journey`] — Build a multi-touch multi-stakeholder journey triggered at renewal-window entry. Each touch goes to a DIFFERENT contact at the account based on their role: Touch 1 (Day 90 before contract_end): champion. Touch 2 (Day 60): economic buyer. Touch 3 (Day 60, parallel): IT/security if applicable. Touch 4 (Day 30): all stakeholders. Add a renewal-meeting-scheduled branch: if CSM/AE schedules a renewal meeting at any point, journey pauses (human-led from here). For high-risk accounts (renewal_health composite low or any churn signal), additionally create urgent CSM task at Day 90 — automation alone won't save at-risk renewals. → produces: journey
5. **Build B2B Renewal Pipeline Dashboard** [`create_dashboard`] — Compose a B2B renewal pipeline dashboard: renewal forecast by quarter (account count + ARR at risk), renewal health distribution (green/yellow/red), days-to-renewal pipeline (which renewals are coming up when), CSM/AE engagement rate (% of renewals where a human conversation happened — target: 100% for accounts >$50K ARR), expansion-during-renewal rate (renewals that grow vs. flat vs. shrink), and renewal-rate trend over time. The strategic view that gives leadership confidence in NRR. → produces: dashboard
