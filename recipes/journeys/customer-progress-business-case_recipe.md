---
name: customer-progress-business-case
description: 'Use when a user mentions "customer progress business case", "highlight customer progress", "your impact journey", or asks for related help. Quarterly journey: AI-generated personalized snapshot of customer''s usage, outcomes, value delivered to email + in-app dashboard surface + optional CSM-shareable PDF. Helps customer build their internal case for budget, drives renewal goodwill, surfaces wins worth amplifying. The ChurnZero ''highlight customer progress'' play.'
arguments: []
intempt:
  id: customer-progress-business-case
  title: "Quarterly customer progress report"
  version: 1.0.0
  slashCommand: /customer-progress-business-case
  group: Journeys
  shortDescription: "Sends each account a quarterly account of what they got out of the product, in the app and as a PDF they can hand to their own boss."
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
      title: "Total up the quarter"
      command: create_ai_attribute
      produces: attribute
      bindsAs: progress_snapshot
      description: "At quarter close, per account: usage against last quarter and against similar accounts, outcomes and milestones reached, ROI where the data allows, how many new users and teams came on, and anything notable such as a first use of a feature or a benchmark passed."
      prompt: 'Create an AI-derived attribute ''Quarterly progress snapshot'' on the Account object, computed at end of each quarter for all paying accounts. Aggregates: (a) usage trajectory (total events, active users, feature breadth: compared to prior quarter and to similar-cohort accounts); (b) outcomes attributed to the product (milestones reached, KPI changes if trackable); (c) ROI computed where data permits (time saved, error rate reduced, throughput increased); (d) team-impact (new users added, departments adopting); (e) noteworthy events (first time using feature X, exceeded benchmark Y). Output: structured story-ready snapshot the email and in-app surface render from.'
    - step: 2
      title: "Pick who should get it"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - progress_snapshot
      description: "Paying accounts at least 90 days old, with real usage last quarter and a churn risk score under 60. Barely active and at risk accounts are left out, because a celebration email lands badly there."
      prompt: 'Build a segment ''Quarterly progress recipients'' capturing paying accounts where: (a) account is 90+ days old (needs a full quarter of data), (b) usage in the past quarter was meaningful (above noise floor: don''t send ''your impact'' to barely-active accounts, it backfires), (c) the churn risk score is below 60 (don''t send celebratory content to at-risk accounts: that''s tone-deaf; they get the tiered-churn journey instead). Audience refreshes once per quarter at quarter-close.'
    - step: 3
      title: "Write the quarter in numbers"
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - progress_snapshot
      - segment
      description: "The subject line carries the headline number, for example hours saved. The body leads on that figure, adds three or four supporting metrics with the direction of travel, calls out notable moments, sums up team impact, and offers the same thing as a PDF. Sent by a named CSM, celebratory but factual."
      prompt: 'Generate quarterly progress email content. Subject: ''Your [Quarter] with [Product]: [headline metric]'' (e.g. ''Your Q2 with Acme: 247 hours saved''). Body: hero number (top KPI from snapshot), 3-4 supporting metrics with quarter-over-quarter trend arrows, callouts to noteworthy events (''You hit your 1000th [unit] this quarter''), team-impact summary, and a soft prompt: ''Want this as a PDF to share with your team or manager?'' Send-from: named CSM or success lead. Tone: celebratory but factual: no marketing-speak, all real numbers from their account.'
    - step: 4
      title: "Show it in the app too"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn:
      - progress_snapshot
      - segment
      description: "The same snapshot on the admin dashboard for the 30 days after quarter close, with an export to PDF button so they can pass it around internally."
      prompt: Configure an in-app personalization 'Your Quarter snapshot' on the admin/owner dashboard for users in the quarterly-review segment. Renders the same snapshot content as the email (hero metric, supporting metrics, trend arrows, callouts) visible for the 30 days after quarter-close. Includes an export-to-PDF action so the customer can easily share internally (the killer feature of this play, customers SHARE this content with their bosses, which is its own marketing channel).
    - step: 5
      title: "Send three days after close"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - progress_snapshot
      - segment
      - email_asset
      - personalization
      description: "Runs every quarter. The email goes out three days after quarter end so late data settles, the in app version switches on the same day, and on day 14 anyone who engaged is offered a deeper review with their CSM, or an advocacy ask if the numbers are strong. Each quarter is its own run and closes after 60 days."
      prompt: 'Build a journey triggered quarterly at quarter-close for all users in the segment. Touch 1 (Day 3 after quarter end: gives time for last-day data to settle): quarterly progress email goes to the account''s admin/champion. Touch 2 (Day 0 of touch 1): in-app personalization activates for 30 days. Touch 3 (Day 14, if user opened the email or interacted with in-app): light follow-up offering a CSM-led deeper review for renewal-prep, OR an advocacy ask if the metrics are strong (handoff to milestone-driven-advocacy-asks). Exit on: 60-day completion (each quarter is its own journey instance).'
    - step: 6
      title: "See if the report earns renewals"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - progress_snapshot
      - segment
      - email_asset
      - personalization
      - journey
      description: "Sends per quarter, open rate, how often the PDF gets exported, how renewal rates compare between accounts that opened it and those that did not, and where CSMs saw it cited in a renewal conversation."
      prompt: 'Compose a progress-program dashboard: send volume per quarter, email engagement rate (target: 60%+ open (these are factual personal emails, not marketing), PDF-export rate (the killer metric) exports mean the customer is sharing internally, which is a renewal leading indicator), correlation between progress-email opens and renewal rate at next renewal (the proof-of-value chart: opens typically correlate with 5-10 percentage point higher renewal rates), and AE/CSM-reported instances of the snapshot being referenced in renewal conversations.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: personalization, type: personalization, cardinality: single, description: "Personalization produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Quarterly customer progress report

Sends each account a quarterly account of what they got out of the product, in the app and as a PDF they can hand to their own boss.

## What it does

1. **Total up the quarter** (`create_ai_attribute`)

   At quarter close, per account: usage against last quarter and against similar accounts, outcomes and milestones reached, ROI where the data allows, how many new users and teams came on, and anything notable such as a first use of a feature or a benchmark passed.

2. **Pick who should get it** (`create_segment`)

   Paying accounts at least 90 days old, with real usage last quarter and a churn risk score under 60. Barely active and at risk accounts are left out, because a celebration email lands badly there.

3. **Write the quarter in numbers** (`create_email_content`)

   The subject line carries the headline number, for example hours saved. The body leads on that figure, adds three or four supporting metrics with the direction of travel, calls out notable moments, sums up team impact, and offers the same thing as a PDF. Sent by a named CSM, celebratory but factual.

4. **Show it in the app too** (`create_personalization`)

   The same snapshot on the admin dashboard for the 30 days after quarter close, with an export to PDF button so they can pass it around internally.

5. **Send three days after close** (`create_journey`)

   Runs every quarter. The email goes out three days after quarter end so late data settles, the in app version switches on the same day, and on day 14 anyone who engaged is offered a deeper review with their CSM, or an advocacy ask if the numbers are strong. Each quarter is its own run and closes after 60 days.

6. **See if the report earns renewals** (`create_dashboard`)

   Sends per quarter, open rate, how often the PDF gets exported, how renewal rates compare between accounts that opened it and those that did not, and where CSMs saw it cited in a renewal conversation.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
