---
description: When one of your most valuable accounts stops showing up for a month, it briefs the CSM and asks them to call. Nothing is sent automatically.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
  - media
---

# Concierge for dormant big accounts

Slash command: /dormant-high-ltv-concierge

## Step 1: Track dormancy and value

Create AI-derived attributes on the Account object: 'days_dormant' (days since last Session start by ANY user on the account) and 'account_ltv' (cumulative revenue paid, plus projected forward LTV based on current MRR × historical retention curve for similar accounts). LTV tier: top 10% of customers by LTV = high-LTV. Refreshed daily.

## Step 2: Find the valuable ones gone quiet

Build a segment 'Dormant high-LTV accounts' capturing accounts where account_ltv is in the top 10% AND days_dormant >= 30 AND the account has not had CSM contact in last 30 days. Excludes accounts with a known temporary-pause status (e.g. 'paused for legal review', 'team on annual leave', these are flagged by CSM separately). Use the result of "Track dormancy and value".

## Step 3: Brief the CSM and escalate

Create a workflow firing daily for newly-dormant high-LTV accounts. Step sequence: (1) refresh account context: usage trajectory (was it declining before going dormant?), recent support tickets, last meeting summary; (2) compose a context blob for CSM with: dormancy days, last activity date, decline pattern if any, recent support topics, suggested outreach angle (check-in / re-onboarding offer / executive sponsor intro); (3) create urgent CSM task with full context attached; (4) post Slack DM to the named CSM + their manager (high-LTV dormancy is escalation-worthy); (5) tag account in CRM as 'churn-risk: dormant' for forecast visibility. Don't auto-send any email: concierge outreach must be personal. Use the result of "Track dormancy and value", "Find the valuable ones gone quiet".

## Step 4: Prove the call is worth making

Compose a VIP retention dashboard: count of high-LTV dormant accounts (the at-risk pile), ARR at risk in this segment, CSM response time on dormancy alerts (target: <48hr), re-engagement success rate (dormant-account-to-active-again within 14 days of CSM outreach), and 90-day churn rate split by 'CSM contacted within 48hr of dormancy' vs. 'no CSM contact': typically the gap is dramatic and proves the workflow's value. Use the result of "Track dormancy and value", "Find the valuable ones gone quiet", "Brief the CSM and escalate".
