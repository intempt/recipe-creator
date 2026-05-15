---
name: customer-progress-business-case
description: 'Use when a user mentions "customer progress business case", "highlight customer progress", "your impact journey", or asks for related help. Quarterly journey: AI-generated personalized snapshot of customer''s usage, outcomes, value delivered → email + in-app dashboard surface + optional CSM-shareable PDF. Helps customer build their internal case for budget, drives renewal goodwill, surfaces wins worth amplifying. The ChurnZero ''highlight customer progress'' play.'
arguments: []
intempt:
  id: customer-progress-business-case
  version: 1.0.0
  slashCommand: /customer-progress-business-case
  group: Journeys
  shortDescription: "'Quarterly journey: AI-generated personalized snapshot of customer''s usage, outcomes, value delivered → email + in-app dashboard surface + optional CSM-shareable PDF. Helps customer build their internal case for budget, drives renewal goodwill, surfaces wins worth amplifying. The ChurnZero ''highlight customer progress'' play.'"
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing, sales]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [customer-success, value-delivered, renewal-prep]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_personalization
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Quarterly Progress Snapshot AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: progress_snapshot
      description: 'Create an AI-derived attribute ''quarterly_progress_snapshot'' on the Account object, computed at end of each quarter for all paying accounts. Aggregates: (a) usage trajectory (total events, active users, feature breadth — compared to prior quarter and to similar-cohort accounts); (b) outcomes attributed to the product (milestones reached, KPI changes if trackable); (c) ROI computed where data permits (time saved, error rate reduced, throughput increased); (d) team-impact (new users added, departments adopting); (e) noteworthy events (first time using feature X, exceeded benchmark Y). Output: structured story-ready snapshot the email and in-app surface render from.'
      prompt: 'Create an AI-derived attribute ''quarterly_progress_snapshot'' on the Account object, computed at end of each quarter for all paying accounts. Aggregates: (a) usage trajectory (total events, active users, feature breadth — compared to prior quarter and to similar-cohort accounts); (b) outcomes attributed to the product (milestones reached, KPI changes if trackable); (c) ROI computed where data permits (time saved, error rate reduced, throughput increased); (d) team-impact (new users added, departments adopting); (e) noteworthy events (first time using feature X, exceeded benchmark Y). Output: structured story-ready snapshot the email and in-app surface render from.'
    - step: 2
      title: Identify Quarterly-Review Audience
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - progress_snapshot
      description: 'Build a segment ''Quarterly progress recipients'' capturing paying accounts where: (a) account is 90+ days old (needs a full quarter of data), (b) usage in the past quarter was meaningful (above noise floor — don''t send ''your impact'' to barely-active accounts, it backfires), (c) churn_risk_score is below 60 (don''t send celebratory content to at-risk accounts — that''s tone-deaf; they get the tiered-churn journey instead). Audience refreshes once per quarter at quarter-close.'
      prompt: 'Build a segment ''Quarterly progress recipients'' capturing paying accounts where: (a) account is 90+ days old (needs a full quarter of data), (b) usage in the past quarter was meaningful (above noise floor — don''t send ''your impact'' to barely-active accounts, it backfires), (c) churn_risk_score is below 60 (don''t send celebratory content to at-risk accounts — that''s tone-deaf; they get the tiered-churn journey instead). Audience refreshes once per quarter at quarter-close.'
    - step: 3
      title: Build Progress Email Content
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - progress_snapshot
      - segment
      description: 'Generate quarterly progress email content. Subject: ''Your [Quarter] with [Product]: [headline metric]'' (e.g. ''Your Q2 with Acme: 247 hours saved''). Body: hero number (top KPI from snapshot), 3-4 supporting metrics with quarter-over-quarter trend arrows, callouts to noteworthy events (''You hit your 1000th [unit] this quarter''), team-impact summary, and a soft prompt: ''Want this as a PDF to share with your team or manager?'' Send-from: named CSM or success lead. Tone: celebratory but factual — no marketing-speak, all real numbers from their account.'
      prompt: 'Generate quarterly progress email content. Subject: ''Your [Quarter] with [Product]: [headline metric]'' (e.g. ''Your Q2 with Acme: 247 hours saved''). Body: hero number (top KPI from snapshot), 3-4 supporting metrics with quarter-over-quarter trend arrows, callouts to noteworthy events (''You hit your 1000th [unit] this quarter''), team-impact summary, and a soft prompt: ''Want this as a PDF to share with your team or manager?'' Send-from: named CSM or success lead. Tone: celebratory but factual — no marketing-speak, all real numbers from their account.'
    - step: 4
      title: Build Progress Personalization
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn:
      - progress_snapshot
      - segment
      description: Configure an in-app personalization 'Your Quarter snapshot' on the admin/owner dashboard for users in the quarterly-review segment. Renders the same snapshot content as the email — hero metric, supporting metrics, trend arrows, callouts — visible for the 30 days after quarter-close. Includes an export-to-PDF action so the customer can easily share internally (the killer feature of this play — customers SHARE this content with their bosses, which is its own marketing channel).
      prompt: Configure an in-app personalization 'Your Quarter snapshot' on the admin/owner dashboard for users in the quarterly-review segment. Renders the same snapshot content as the email — hero metric, supporting metrics, trend arrows, callouts — visible for the 30 days after quarter-close. Includes an export-to-PDF action so the customer can easily share internally (the killer feature of this play — customers SHARE this content with their bosses, which is its own marketing channel).
    - step: 5
      title: Build Progress Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - progress_snapshot
      - segment
      - email_asset
      - personalization
      description: 'Build a journey triggered quarterly at quarter-close for all users in the segment. Touch 1 (Day 3 after quarter end — gives time for last-day data to settle): quarterly progress email goes to the account''s admin/champion. Touch 2 (Day 0 of touch 1): in-app personalization activates for 30 days. Touch 3 (Day 14, if user opened the email or interacted with in-app): light follow-up offering a CSM-led deeper review for renewal-prep, OR an advocacy ask if the metrics are strong (handoff to milestone-driven-advocacy-asks). Exit on: 60-day completion (each quarter is its own journey instance).'
      prompt: 'Build a journey triggered quarterly at quarter-close for all users in the segment. Touch 1 (Day 3 after quarter end — gives time for last-day data to settle): quarterly progress email goes to the account''s admin/champion. Touch 2 (Day 0 of touch 1): in-app personalization activates for 30 days. Touch 3 (Day 14, if user opened the email or interacted with in-app): light follow-up offering a CSM-led deeper review for renewal-prep, OR an advocacy ask if the metrics are strong (handoff to milestone-driven-advocacy-asks). Exit on: 60-day completion (each quarter is its own journey instance).'
    - step: 6
      title: Build Progress Program Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - progress_snapshot
      - segment
      - email_asset
      - personalization
      - journey
      description: 'Compose a progress-program dashboard: send volume per quarter, email engagement rate (target: 60%+ open — these are factual personal emails, not marketing), PDF-export rate (the killer metric — exports mean the customer is sharing internally, which is a renewal leading indicator), correlation between progress-email opens and renewal rate at next renewal (the proof-of-value chart — opens typically correlate with 5-10 percentage point higher renewal rates), and AE/CSM-reported instances of the snapshot being referenced in renewal conversations.'
      prompt: 'Compose a progress-program dashboard: send volume per quarter, email engagement rate (target: 60%+ open — these are factual personal emails, not marketing), PDF-export rate (the killer metric — exports mean the customer is sharing internally, which is a renewal leading indicator), correlation between progress-email opens and renewal rate at next renewal (the proof-of-value chart — opens typically correlate with 5-10 percentage point higher renewal rates), and AE/CSM-reported instances of the snapshot being referenced in renewal conversations.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: personalization, type: personalization, cardinality: single, description: "Personalization produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Customer Progress Business Case

## Procedure

1. **Build Quarterly Progress Snapshot AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'quarterly_progress_snapshot' on the Account object, computed at end of each quarter for all paying accounts. Aggregates: (a) usage trajectory (total events, active users, feature breadth — compared to prior quarter and to similar-cohort accounts); (b) outcomes attributed to the product (milestones reached, KPI changes if trackable); (c) ROI computed where data permits (time saved, error rate reduced, throughput increased); (d) team-impact (new users added, departments adopting); (e) noteworthy events (first time using feature X, exceeded benchmark Y). Output: structured story-ready snapshot the email and in-app surface render from. → produces: attribute
2. **Identify Quarterly-Review Audience** [`create_segment`] — Build a segment 'Quarterly progress recipients' capturing paying accounts where: (a) account is 90+ days old (needs a full quarter of data), (b) usage in the past quarter was meaningful (above noise floor — don't send 'your impact' to barely-active accounts, it backfires), (c) churn_risk_score is below 60 (don't send celebratory content to at-risk accounts — that's tone-deaf; they get the tiered-churn journey instead). Audience refreshes once per quarter at quarter-close. → produces: segment
3. **Build Progress Email Content** [`create_email_content`] — Generate quarterly progress email content. Subject: 'Your [Quarter] with [Product]: [headline metric]' (e.g. 'Your Q2 with Acme: 247 hours saved'). Body: hero number (top KPI from snapshot), 3-4 supporting metrics with quarter-over-quarter trend arrows, callouts to noteworthy events ('You hit your 1000th [unit] this quarter'), team-impact summary, and a soft prompt: 'Want this as a PDF to share with your team or manager?' Send-from: named CSM or success lead. Tone: celebratory but factual — no marketing-speak, all real numbers from their account. → produces: asset
4. **Build Progress Personalization** [`create_personalization`] — Configure an in-app personalization 'Your Quarter snapshot' on the admin/owner dashboard for users in the quarterly-review segment. Renders the same snapshot content as the email — hero metric, supporting metrics, trend arrows, callouts — visible for the 30 days after quarter-close. Includes an export-to-PDF action so the customer can easily share internally (the killer feature of this play — customers SHARE this content with their bosses, which is its own marketing channel). → produces: personalization
5. **Build Progress Journey** [`create_journey`] — Build a journey triggered quarterly at quarter-close for all users in the segment. Touch 1 (Day 3 after quarter end — gives time for last-day data to settle): quarterly progress email goes to the account's admin/champion. Touch 2 (Day 0 of touch 1): in-app personalization activates for 30 days. Touch 3 (Day 14, if user opened the email or interacted with in-app): light follow-up offering a CSM-led deeper review for renewal-prep, OR an advocacy ask if the metrics are strong (handoff to milestone-driven-advocacy-asks). Exit on: 60-day completion (each quarter is its own journey instance). → produces: journey
6. **Build Progress Program Dashboard** [`create_dashboard`] — Compose a progress-program dashboard: send volume per quarter, email engagement rate (target: 60%+ open — these are factual personal emails, not marketing), PDF-export rate (the killer metric — exports mean the customer is sharing internally, which is a renewal leading indicator), correlation between progress-email opens and renewal rate at next renewal (the proof-of-value chart — opens typically correlate with 5-10 percentage point higher renewal rates), and AE/CSM-reported instances of the snapshot being referenced in renewal conversations. → produces: dashboard
