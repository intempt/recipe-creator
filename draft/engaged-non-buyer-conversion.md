---
description: Identifies highly engaged free users who have not converted, sending targeted email check-ins and routing replies using sentiment analysis.
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
---

# Engaged users who never buy

Slash command: /engaged-non-buyer-conversion

## Step 1: Measure the gap

Create an AI-derived attribute 'engagement_paradox_score' on the User object. Calculates the gap between engagement intensity and conversion behavior. Inputs: sessions in last 30 days, feature breadth/depth, marketing email engagement (opens / clicks), in-product activity vs. typical-converter benchmarks. High score = the user behaves like a converter SHOULD behave, but hasn't converted. Output: numeric 0-100. Score >= 70 = high engagement paradox (engaged but stuck: the most interesting cohort). Includes a diagnostic field naming the likely blocker (price-sensitivity / feature-gap / authority-issue / decision-paralysis / no-urgency) inferred from behavior patterns.

## Step 2: Find engaged free users

Build a segment 'Engaged non-buyers - last 60 days' capturing users where (a) account age is 30+ days AND (b) subscription_status is free or trialing AND (c) engagement_paradox_score >= 70. Excludes users in active sales conversations (don't double-orchestrate) and users who explicitly declined an upgrade in the last 90 days (respect the no). Use the result of "Measure the gap".

## Step 3: Write one email per blocker

Generate diagnostic email variants per inferred blocker. Price-sensitivity blocker: 'You're using [Product] like a paid customer: here's a 30% retention discount for the first 3 months.' Feature-gap blocker: 'We noticed you tried [feature X] but didn't continue. Here's what most users do next: and 1:1 help if you'd like.' Authority-issue blocker: 'Need help making the case internally? Here's a business-case template + your team's usage summary to share with your manager.' Decision-paralysis blocker: 'You've evaluated [Product] thoroughly. Want a 15-min decision-clarity call?' No-urgency blocker: 'No rush: but if a deadline is approaching, here's a limited-time price-lock offer.' Send-from: success@ or matched AE. Use the result of "Measure the gap", "Find engaged free users".

## Step 4: Ask what is stopping them

Configure an AI agent scenario 'Engaged non-buyer diagnostic' that engages high-engagement-paradox users via in-app chat or email reply. Scenario: surface user's product usage warmly ('I see you've been using [Product] for 45 days: that's great!'), then ask the diagnostic question ('What's keeping you from upgrading? Cost, features, internal approval, timing, or something else?'). Branch on response: route price to retention-discount offer, feature-gap to PM-feedback queue + feature-roadmap signal, authority to business-case generation, timing to deferred-followup, other to human handoff. The agent generates qualified diagnostic signal for the AE/CSM, not raw chat. Use the result of "Measure the gap", "Find engaged free users".

## Step 5: Diagnose, then bring a human in

Build a 3-touch diagnostic journey wired to engaged-non-buyer segment. Touch 1 (Day 0 of entry): diagnostic email matched to inferred blocker. Touch 2 (Day 3, if no engagement): in-app chat invitation to the diagnostic agent on next session. Touch 3 (Day 7, if still no conversion): personalized AE outreach task with the full engagement-paradox profile + inferred blocker + suggested approach attached. Exit on: Subscription started (won (celebrate), explicit decline / opt-out, or successful agent diagnostic (handoff to appropriate downstream) sales, support, or PM). Use the result of "Measure the gap", "Find engaged free users", "Write one email per blocker", "Ask what is stopping them".

## Step 6: See which angle converts

Compose an engaged-non-buyer dashboard: paradox-cohort size over time (is this cohort growing or shrinking: product fit signal), conversion lift vs. control (cohort getting this journey vs. holdout staying on generic free-tier nurture), conversion by inferred blocker (which diagnostic angle actually converts: informs pricing/product/sales-collateral decisions), agent-diagnostic completion rate, and time-to-conversion distribution (most paradox conversions happen within 14 days of journey entry: if not, the blocker is structural). Use the result of "Measure the gap", "Find engaged free users", "Write one email per blocker", "Ask what is stopping them", "Diagnose, then bring a human in".
