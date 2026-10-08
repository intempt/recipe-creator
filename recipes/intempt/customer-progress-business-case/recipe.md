---
description: Sends each account a quarterly account of what they got out of the product, in the app and as a PDF they can hand to their own boss.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
---

# Quarterly customer progress report

Slash command: /customer-progress-business-case

## Step 1: Total up the quarter

Create an AI-derived attribute 'quarterly_progress_snapshot' on the Account object, computed at end of each quarter for all paying accounts. Aggregates: (a) usage trajectory (total events, active users, feature breadth: compared to prior quarter and to similar-cohort accounts); (b) outcomes attributed to the product (milestones reached, KPI changes if trackable); (c) ROI computed where data permits (time saved, error rate reduced, throughput increased); (d) team-impact (new users added, departments adopting); (e) noteworthy events (first time using feature X, exceeded benchmark Y). Output: structured story-ready snapshot the email and in-app surface render from.

## Step 2: Pick who should get it

Build a segment 'Quarterly progress recipients' capturing paying accounts where: (a) account is 90+ days old (needs a full quarter of data), (b) usage in the past quarter was meaningful (above noise floor: don't send 'your impact' to barely-active accounts, it backfires), (c) churn_risk_score is below 60 (don't send celebratory content to at-risk accounts: that's tone-deaf; they get the tiered-churn journey instead). Audience refreshes once per quarter at quarter-close. Use the result of "Total up the quarter".

## Step 3: Write the quarter in numbers

Generate quarterly progress email content. Subject: 'Your [Quarter] with [Product]: [headline metric]' (e.g. 'Your Q2 with Acme: 247 hours saved'). Body: hero number (top KPI from snapshot), 3-4 supporting metrics with quarter-over-quarter trend arrows, callouts to noteworthy events ('You hit your 1000th [unit] this quarter'), team-impact summary, and a soft prompt: 'Want this as a PDF to share with your team or manager?' Send-from: named CSM or success lead. Tone: celebratory but factual: no marketing-speak, all real numbers from their account. Use the result of "Total up the quarter", "Pick who should get it".

## Step 4: Show it in the app too

Configure an in-app personalization 'Your Quarter snapshot' on the admin/owner dashboard for users in the quarterly-review segment. Renders the same snapshot content as the email (hero metric, supporting metrics, trend arrows, callouts) visible for the 30 days after quarter-close. Includes an export-to-PDF action so the customer can easily share internally (the killer feature of this play, customers SHARE this content with their bosses, which is its own marketing channel). Use the result of "Total up the quarter", "Pick who should get it".

## Step 5: Send three days after close

Build a journey triggered quarterly at quarter-close for all users in the segment. Touch 1 (Day 3 after quarter end: gives time for last-day data to settle): quarterly progress email goes to the account's admin/champion. Touch 2 (Day 0 of touch 1): in-app personalization activates for 30 days. Touch 3 (Day 14, if user opened the email or interacted with in-app): light follow-up offering a CSM-led deeper review for renewal-prep, OR an advocacy ask if the metrics are strong (handoff to milestone-driven-advocacy-asks). Exit on: 60-day completion (each quarter is its own journey instance). Use the result of "Total up the quarter", "Pick who should get it", "Write the quarter in numbers", "Show it in the app too".

## Step 6: See if the report earns renewals

Compose a progress-program dashboard: send volume per quarter, email engagement rate (target: 60%+ open (these are factual personal emails, not marketing), PDF-export rate (the killer metric) exports mean the customer is sharing internally, which is a renewal leading indicator), correlation between progress-email opens and renewal rate at next renewal (the proof-of-value chart: opens typically correlate with 5-10 percentage point higher renewal rates), and AE/CSM-reported instances of the snapshot being referenced in renewal conversations. Use the result of "Total up the quarter", "Pick who should get it", "Write the quarter in numbers", "Show it in the app too", "Send three days after close".
