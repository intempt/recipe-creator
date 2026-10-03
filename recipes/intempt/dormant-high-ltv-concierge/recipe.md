---
id: dormant-high-ltv-concierge
title: Concierge for dormant big accounts
slash_command: /dormant-high-ltv-concierge
group: Workflows
owner: intempt
summary: When one of your most valuable accounts stops showing up for a month, it briefs the CSM and asks
  them to call. Nothing is sent automatically.
description: >-
  When a high-LTV customer goes dormant (no product activity 30+ days), trigger a concierge outreach task,
  high-LTV silence is the strongest churn precursor and warrants personal CSM contact, not automated nurture.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - saas
    - ecommerce
  complexity: standard
  executionMode: live
  tags:
    - dormancy-detection
    - vip-retention
    - csm-outreach
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: session_start
      severity: blocking
touches:
  reads:
    - The session_start event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Track dormancy and value"
    - A new segment, from step 2 "Find the valuable ones gone quiet"
    - A new workflow, from step 3 "Brief the CSM and escalate"
    - A new dashboard, from step 4 "Prove the call is worth making"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track dormancy and value
    summary: >-
      Two things per account, refreshed daily: days since anyone there last started a session, and lifetime
      value, meaning what they have paid plus what their current monthly revenue is likely to become at
      the retention curve for similar accounts. The top 10% by value counts as high value.
    builds: attribute
    description: >-
      Create AI-derived attributes on the Account object: 'days_dormant' (days since last session_start
      by ANY user on the account) and 'account_ltv' (cumulative revenue paid, plus projected forward LTV
      based on current MRR × historical retention curve for similar accounts). LTV tier: top 10% of customers
      by LTV = high-LTV. Refreshed daily.
  - id: s2
    title: Find the valuable ones gone quiet
    summary: >-
      Accounts in the top 10% by value, dormant 30 days or more, with no CSM contact in the last 30 days.
      Accounts a CSM has flagged as temporarily paused, for a legal review or a team holiday, are left
      out.
    builds: segment
    description: >-
      Build a segment 'Dormant high-LTV accounts' capturing accounts where account_ltv is in the top 10%
      AND days_dormant >= 30 AND the account has not had CSM contact in last 30 days. Excludes accounts
      with a known temporary-pause status (e.g. 'paused for legal review', 'team on annual leave', these
      are flagged by CSM separately). Use the result of "Track dormancy and value".
    dependsOn:
      - s1
  - id: s3
    title: Brief the CSM and escalate
    summary: >-
      Daily, for each newly dormant account, it gathers the usage trend before they went quiet, recent
      support tickets and the last meeting summary, and writes a brief with the days dormant, the last
      activity, any decline pattern, the support topics and a suggested angle: a check in, re-onboarding,
      or an executive introduction. That becomes an urgent CSM task, a Slack message to the CSM and their
      manager, and a churn risk tag on the account. No email goes out automatically.
    builds: workflow
    description: >-
      Create a workflow firing daily for newly-dormant high-LTV accounts. Step sequence: (1) refresh account
      context: usage trajectory (was it declining before going dormant?), recent support tickets, last
      meeting summary; (2) compose a context blob for CSM with: dormancy days, last activity date, decline
      pattern if any, recent support topics, suggested outreach angle (check-in / re-onboarding offer
      / executive sponsor intro); (3) create urgent CSM task with full context attached; (4) post Slack
      DM to the named CSM + their manager (high-LTV dormancy is escalation-worthy); (5) tag account in
      CRM as 'churn-risk: dormant' for forecast visibility. Don't auto-send any email: concierge outreach
      must be personal. Use the result of "Track dormancy and value", "Find the valuable ones gone quiet".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Prove the call is worth making
    summary: >-
      How many valuable accounts are dormant, the ARR they represent, how fast CSMs respond against a
      48 hour target, how many come back within 14 days of contact, and the 90 day churn rate for accounts
      contacted inside 48 hours against those never contacted.
    builds: dashboard
    description: >-
      Compose a VIP retention dashboard: count of high-LTV dormant accounts (the at-risk pile), ARR at
      risk in this segment, CSM response time on dormancy alerts (target: <48hr), re-engagement success
      rate (dormant-account-to-active-again within 14 days of CSM outreach), and 90-day churn rate split
      by 'CSM contacted within 48hr of dormancy' vs. 'no CSM contact': typically the gap is dramatic and
      proves the workflow's value. Use the result of "Track dormancy and value", "Find the valuable ones
      gone quiet", "Brief the CSM and escalate".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Concierge for dormant big accounts

When one of your most valuable accounts stops showing up for a month, it briefs the CSM and asks them to call. Nothing is sent automatically.

## Steps

1. **Track dormancy and value** (builds attribute)

   Two things per account, refreshed daily: days since anyone there last started a session, and lifetime value, meaning what they have paid plus what their current monthly revenue is likely to become at the retention curve for similar accounts. The top 10% by value counts as high value.

2. **Find the valuable ones gone quiet** (builds segment)

   Accounts in the top 10% by value, dormant 30 days or more, with no CSM contact in the last 30 days. Accounts a CSM has flagged as temporarily paused, for a legal review or a team holiday, are left out.

3. **Brief the CSM and escalate** (builds workflow)

   Daily, for each newly dormant account, it gathers the usage trend before they went quiet, recent support tickets and the last meeting summary, and writes a brief with the days dormant, the last activity, any decline pattern, the support topics and a suggested angle: a check in, re-onboarding, or an executive introduction. That becomes an urgent CSM task, a Slack message to the CSM and their manager, and a churn risk tag on the account. No email goes out automatically.

4. **Prove the call is worth making** (builds dashboard)

   How many valuable accounts are dormant, the ARR they represent, how fast CSMs respond against a 48 hour target, how many come back within 14 days of contact, and the 90 day churn rate for accounts contacted inside 48 hours against those never contacted.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The session_start event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Track dormancy and value"
- A new segment, from step 2 "Find the valuable ones gone quiet"
- A new workflow, from step 3 "Brief the CSM and escalate"
- A new dashboard, from step 4 "Prove the call is worth making"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
