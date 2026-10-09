---
description: Flags customers who are drifting away, reaches them automatically while it is still cheap to fix, and pulls in a CSM when it is not.
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

# Churn prevention

Slash command: /churn-prevention

## Step 1: Score churn risk

Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals.

## Step 2: Split into low, medium and high

Segment users into low/medium/high churn-risk buckets. Use the result of "Score churn risk".

## Step 3: Tell the CSM about high risk

Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. Use the result of "Score churn risk", "Split into low, medium and high".

## Step 4: Write the win back emails

Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk".

## Step 5: Reach medium risk first

Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk", "Write the win back emails".

## Step 6: Compare churn by risk tier

Compose a retention report tracking churn rate by risk tier and intervention type. Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk", "Write the win back emails", "Reach medium risk first".

## Step 7: See if the saves are working

Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk", "Write the win back emails", "Reach medium risk first", "Compare churn by risk tier".
