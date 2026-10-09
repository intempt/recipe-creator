---
description: 'Scores churn risk daily and routes each band to email, SMS, push, or Slack: nurture content at low risk, personalized messages at medium, and CSM or founder outreach at high and critical.'
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
  - media
---

# Tiered churn intervention

Slash command: /predictive-churn-tiered-intervention

## Step 1: Score churn risk daily

Create an AI-derived attribute 'churn_risk_score' on the User object, refreshed daily. Inputs: engagement velocity (sessions trend over 30/14/7 days), feature usage decay, support sentiment trajectory, billing-status signals, peer-cohort churn patterns, account-level usage (for B2B). Output: numeric 0-100 with tier label (low (0-29) / medium (30-59) / high (60-79) / critical (80-100). NOT binary at-risk-or-not) the nuance is the point: medium and high get different treatments. Refresh on every significant behavioral event so a sudden engagement drop is caught fast.

## Step 2: Take everyone above 30

Build a parent segment 'Churn risk - paying users' capturing all paying users with churn_risk_score >= 30. Implicitly partitioned by tier through the attribute. Excludes users in the first 14 days (early signals aren't reliable yet) and users already in active save flows (no double-intervention). Use the result of "Score churn risk daily".

## Step 3: Write an email per band

Generate per-tier email content. Medium tier: educational content matched to underutilized features that drive retention in their cohort + personalized 'pick up where you left off' deep-link. Tone: helpful, not alarmed. High tier: urgent value reinforcement, CSM availability signal, specific use-case help offer ('Want a 15-min walkthrough on [feature]?'). Critical tier: founder/CEO personal letter ('I noticed your account hasn't been used much: anything we can do?'), with direct calendar link and concrete asks. Send-from: success@ for medium, named CSM for high, founder/CEO for critical. Use the result of "Score churn risk daily", "Take everyone above 30".

## Step 4: Catch them when they log in

This step builds a page.
Generate in-app messages for high-tier users when they DO log in (rare and precious moments). Format: contextual banner referencing their most-likely-success-path ('Most users in your segment succeed by trying [feature] (want a 60-second walkthrough?'). For critical-tier users on rare logins: a personal-touch interrupt) full-screen modal from the CSM or founder offering a 1:1 call. Never blanket: only when AI signal is strong. Use the result of "Score churn risk daily", "Take everyone above 30", "Write an email per band".

## Step 5: Recommend what keeps people

Configure a recommendation surface specifically for high+critical tier users: surfaces underutilized features that THIS user's cohort uses successfully but THIS user has not adopted (the 'features-that-stick-users' pattern). Renders in-app on dashboard, in email content blocks, and on personalization slots when the user does visit. The recommendation logic prioritizes features with high retention-correlation in this user's segment. Use the result of "Score churn risk daily", "Take everyone above 30".

## Step 6: Treat each band differently

Build a tiered journey wired to the churn-risk segment. Branch on churn_risk tier at entry AND re-evaluate weekly: LOW tier (light-touch nurture email at Day 7 (no urgency, just value content). MEDIUM tier) Touch 1 email Day 0 (helpful tip), Touch 2 in-app at next login (deep-link to retention feature), Touch 3 email Day 7 with recommendation surface highlighting cohort-success features. HIGH tier: Touch 1 email Day 0 from CSM with offer of help, in-app urgent banner on next session, CSM task created same-day. CRITICAL tier: within 4 hours: founder/CEO personal email + agent handoff offering 1:1 call + urgent CSM task + executive-sponsor task. Tier RECOMPUTED weekly: users de-escalate (engagement returned) exit gracefully; users escalate get tier-appropriate next-touch. Exit on: churn_risk drops below 30 for 14+ days (recovered: log retention_win), subscription_canceled (handoff to post-cancel-winback), or unsubscribe. Use the result of "Score churn risk daily", "Take everyone above 30", "Write an email per band", "Catch them when they log in", "Recommend what keeps people".

## Step 7: See if the bands hold up

Compose a tiered churn intervention dashboard: distribution of users across tiers (low/medium/high/critical) per week (leading indicator of book-of-business health, tier-level save rate (% of users in each tier who exit risk vs. churn) proves tiered strategy works), critical-tier CSM response SLA (target: <4hr for human-touch start), ARR-weighted save value by tier, and tier-migration tracking (high to medium = success, medium to high = early warning). Compare model accuracy: predicted churn vs. actual churn at 30/60/90 days. Use the result of "Score churn risk daily", "Take everyone above 30", "Write an email per band", "Catch them when they log in", "Recommend what keeps people", "Treat each band differently".
