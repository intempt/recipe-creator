---
description: For B2B accounts approaching contract end, run a renewal journey at 90, 60, and 30 days to the enrolled profile.
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
  - finance
---

# B2B contract renewal

Slash command: /contract-renewal-b2b

## Step 1: Find renewals inside 90 days

Build a segment 'Upcoming B2B contract renewals - next 90 days' capturing accounts where contract_end_date is between 30 and 90 days from now AND account_tier is enterprise or mid-market AND subscription_status is active. Each account in the segment has multiple touched users, the journey reaches different contacts at the account with role-appropriate messaging.

## Step 2: Read the renewal health

Create an AI-derived attribute 'renewal_health_snapshot' on the Account object, computed at renewal-window entry. Aggregates: (a) usage trajectory over past 12 months (growing / flat / declining); (b) value delivered (key outcomes, milestones reached, ROI metric if tracked); (c) stakeholder health: champion still in role and engaged? economic buyer reachable? new stakeholders identified?; (d) support ticket sentiment over past 6 months; (e) competitor mentions in any meeting summaries. Output: composite health score + structured content for the renewal emails. Use the result of "Find renewals inside 90 days".

## Step 3: Write one email per role

This step builds a designed marketing email (HTML).
Generate role-tailored renewal content. (a) User-champion (Day 90): 'Quick value-recap of the past year (what's working and what's next') focuses on product wins, usage stats, asks for help to coordinate the upcoming renewal conversation. (b) Economic buyer (Day 60): 'Your team's renewal is up in 60 days (let's connect on terms') focuses on business value, ROI, growth opportunity, available terms. (c) IT/security stakeholder if known (Day 60): 'Security/compliance update for your upcoming renewal': proactive on documentation, certifications, any changes. (d) Late reminder (Day 30): consolidated reminder to all stakeholders with proposed contract terms attached. Tone: business-formal, value-substantive, not marketing-chatty. Use the result of "Find renewals inside 90 days", "Read the renewal health".

## Step 4: Reach each stakeholder in turn

Build a multi-touch multi-stakeholder journey triggered at renewal-window entry. Each touch goes to a DIFFERENT contact at the account based on their role: Touch 1 (Day 90 before contract_end): champion. Touch 2 (Day 60): economic buyer. Touch 3 (Day 60, parallel): IT/security if applicable. Touch 4 (Day 30): all stakeholders. Add a renewal-meeting-scheduled branch: if CSM/AE schedules a renewal meeting at any point, journey pauses (human-led from here). For high-risk accounts (renewal_health composite low or any churn signal), additionally create urgent CSM task at Day 90: automation alone won't save at-risk renewals. Use the result of "Find renewals inside 90 days", "Read the renewal health", "Write one email per role".

## Step 5: Forecast the renewal book

Compose a B2B renewal pipeline dashboard: renewal forecast by quarter (account count + ARR at risk), renewal health distribution (green/yellow/red), days-to-renewal pipeline (which renewals are coming up when), CSM/AE engagement rate (% of renewals where a human conversation happened: target: 100% for accounts >$50K ARR), expansion-during-renewal rate (renewals that grow vs. flat vs. shrink), and renewal-rate trend over time. The strategic view that gives leadership confidence in NRR. Use the result of "Find renewals inside 90 days", "Read the renewal health", "Write one email per role", "Reach each stakeholder in turn".
