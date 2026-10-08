---
id: customer-progress-business-case
title: Quarterly customer progress report
slash_command: /customer-progress-business-case
group: Journeys
owner: intempt
curator: somya
summary: Sends each account a quarterly account of what they got out of the product, in the app and as
  a PDF they can hand to their own boss.
description: >-
  Quarterly journey: AI-generated personalized snapshot of customer's usage, outcomes, value delivered
  to email + in-app dashboard surface + optional CSM-shareable PDF. Helps customer build their internal
  case for budget, drives renewal goodwill, surfaces wins worth amplifying. The ChurnZero 'highlight customer
  progress' play.
version: 2.0.0
classification:
  product:
    - marketing
    - sales
  agent: journey-builder
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
    - ecommerce
    - finance
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - customer-success
    - value-delivered
    - renewal-prep
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new attribute, from step 1 "Total up the quarter"
    - A new segment, from step 2 "Pick who should get it"
    - A new designed email, from step 3 "Write the quarter in numbers"
    - A new website personalization, from step 4 "Show it in the app too"
    - A new journey, from step 5 "Send three days after close"
    - A new dashboard, from step 6 "See if the report earns renewals"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Total up the quarter
    summary: >-
      At quarter close, per account: usage against last quarter and against similar accounts, outcomes
      and milestones reached, ROI where the data allows, how many new users and teams came on, and anything
      notable such as a first use of a feature or a benchmark passed.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'quarterly_progress_snapshot' on the Account object, computed at
      end of each quarter for all paying accounts. Aggregates: (a) usage trajectory (total events, active
      users, feature breadth: compared to prior quarter and to similar-cohort accounts); (b) outcomes
      attributed to the product (milestones reached, KPI changes if trackable); (c) ROI computed where
      data permits (time saved, error rate reduced, throughput increased); (d) team-impact (new users
      added, departments adopting); (e) noteworthy events (first time using feature X, exceeded benchmark
      Y). Output: structured story-ready snapshot the email and in-app surface render from.
  - id: s2
    title: Pick who should get it
    summary: >-
      Paying accounts at least 90 days old, with real usage last quarter and a churn risk score under
      60. Barely active and at risk accounts are left out, because a celebration email lands badly there.
    builds: segment
    description: >-
      Build a segment 'Quarterly progress recipients' capturing paying accounts where: (a) account is
      90+ days old (needs a full quarter of data), (b) usage in the past quarter was meaningful (above
      noise floor: don't send 'your impact' to barely-active accounts, it backfires), (c) churn_risk_score
      is below 60 (don't send celebratory content to at-risk accounts: that's tone-deaf; they get the
      tiered-churn journey instead). Audience refreshes once per quarter at quarter-close. Use the result
      of "Total up the quarter".
    dependsOn:
      - s1
  - id: s3
    title: Write the quarter in numbers
    summary: >-
      The subject line carries the headline number, for example hours saved. The body leads on that figure,
      adds three or four supporting metrics with the direction of travel, calls out notable moments, sums
      up team impact, and offers the same thing as a PDF. Sent by a named CSM, celebratory but factual.
    builds: email_html
    description: >-
      Generate quarterly progress email content. Subject: 'Your [Quarter] with [Product]: [headline metric]'
      (e.g. 'Your Q2 with Acme: 247 hours saved'). Body: hero number (top KPI from snapshot), 3-4 supporting
      metrics with quarter-over-quarter trend arrows, callouts to noteworthy events ('You hit your 1000th
      [unit] this quarter'), team-impact summary, and a soft prompt: 'Want this as a PDF to share with
      your team or manager?' Send-from: named CSM or success lead. Tone: celebratory but factual: no marketing-speak,
      all real numbers from their account. Use the result of "Total up the quarter", "Pick who should
      get it".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Show it in the app too
    summary: >-
      The same snapshot on the admin dashboard for the 30 days after quarter close, with an export to
      PDF button so they can pass it around internally.
    builds: personalization
    description: >-
      Configure an in-app personalization 'Your Quarter snapshot' on the admin/owner dashboard for users
      in the quarterly-review segment. Renders the same snapshot content as the email (hero metric, supporting
      metrics, trend arrows, callouts) visible for the 30 days after quarter-close. Includes an export-to-PDF
      action so the customer can easily share internally (the killer feature of this play, customers SHARE
      this content with their bosses, which is its own marketing channel). Use the result of "Total up
      the quarter", "Pick who should get it".
    dependsOn:
      - s1
      - s2
  - id: s5
    title: Send three days after close
    summary: >-
      Runs every quarter. The email goes out three days after quarter end so late data settles, the in
      app version switches on the same day, and on day 14 anyone who engaged is offered a deeper review
      with their CSM, or an advocacy ask if the numbers are strong. Each quarter is its own run and closes
      after 60 days.
    builds: journey
    description: >-
      Build a journey triggered quarterly at quarter-close for all users in the segment. Touch 1 (Day
      3 after quarter end: gives time for last-day data to settle): quarterly progress email goes to the
      account's admin/champion. Touch 2 (Day 0 of touch 1): in-app personalization activates for 30 days.
      Touch 3 (Day 14, if user opened the email or interacted with in-app): light follow-up offering a
      CSM-led deeper review for renewal-prep, OR an advocacy ask if the metrics are strong (handoff to
      milestone-driven-advocacy-asks). Exit on: 60-day completion (each quarter is its own journey instance).
      Use the result of "Total up the quarter", "Pick who should get it", "Write the quarter in numbers",
      "Show it in the app too".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: See if the report earns renewals
    summary: >-
      Sends per quarter, open rate, how often the PDF gets exported, how renewal rates compare between
      accounts that opened it and those that did not, and where CSMs saw it cited in a renewal conversation.
    builds: dashboard
    description: >-
      Compose a progress-program dashboard: send volume per quarter, email engagement rate (target: 60%+
      open (these are factual personal emails, not marketing), PDF-export rate (the killer metric) exports
      mean the customer is sharing internally, which is a renewal leading indicator), correlation between
      progress-email opens and renewal rate at next renewal (the proof-of-value chart: opens typically
      correlate with 5-10 percentage point higher renewal rates), and AE/CSM-reported instances of the
      snapshot being referenced in renewal conversations. Use the result of "Total up the quarter", "Pick
      who should get it", "Write the quarter in numbers", "Show it in the app too", "Send three days after
      close".
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
  - key: personalization
    producedByStep: s4
    type: personalization
    description: Personalization produced by this recipe.
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

# Quarterly customer progress report

Sends each account a quarterly account of what they got out of the product, in the app and as a PDF they can hand to their own boss.

## Steps

1. **Total up the quarter** (builds attribute)

   At quarter close, per account: usage against last quarter and against similar accounts, outcomes and milestones reached, ROI where the data allows, how many new users and teams came on, and anything notable such as a first use of a feature or a benchmark passed.

2. **Pick who should get it** (builds segment)

   Paying accounts at least 90 days old, with real usage last quarter and a churn risk score under 60. Barely active and at risk accounts are left out, because a celebration email lands badly there.

3. **Write the quarter in numbers** (builds email_html)

   The subject line carries the headline number, for example hours saved. The body leads on that figure, adds three or four supporting metrics with the direction of travel, calls out notable moments, sums up team impact, and offers the same thing as a PDF. Sent by a named CSM, celebratory but factual.

4. **Show it in the app too** (builds personalization)

   The same snapshot on the admin dashboard for the 30 days after quarter close, with an export to PDF button so they can pass it around internally.

5. **Send three days after close** (builds journey)

   Runs every quarter. The email goes out three days after quarter end so late data settles, the in app version switches on the same day, and on day 14 anyone who engaged is offered a deeper review with their CSM, or an advocacy ask if the numbers are strong. Each quarter is its own run and closes after 60 days.

6. **See if the report earns renewals** (builds dashboard)

   Sends per quarter, open rate, how often the PDF gets exported, how renewal rates compare between accounts that opened it and those that did not, and where CSMs saw it cited in a renewal conversation.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new attribute, from step 1 "Total up the quarter"
- A new segment, from step 2 "Pick who should get it"
- A new designed email, from step 3 "Write the quarter in numbers"
- A new website personalization, from step 4 "Show it in the app too"
- A new journey, from step 5 "Send three days after close"
- A new dashboard, from step 6 "See if the report earns renewals"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, personalization.
