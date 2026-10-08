---
description: Follows up right after someone hits the action that predicts retention, so the first win turns into a habit instead of a one off.
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
  - media
---

# Aha moment reinforcement

Slash command: /aha-moment-activation

## Step 1: Find people who just got value

Build a segment 'Recent aha-moment achievers' capturing users who completed the aha-moment event (defined per product, e.g. 'first message sent', 'first project published', 'first deal created'; configurable in the segment definition) in the last 14 days AND who haven't received the activation reinforcement yet. The aha-moment event is product-specific and should be set by Product team based on retention curve analysis.

## Step 2: Write three follow up emails

Generate 3-touch reinforcement email content. Touch 1 (24 hours after aha): celebrate the milestone, frame it as a meaningful first step, share 1-2 success stories of users who achieved similar moments. Tone: warm, motivating. Touch 2 (Day 5): point to the natural next feature that complements the aha action (cross-sell within the product, not upsell to plan). Include a brief how-to and an in-app deep link. Touch 3 (Day 10): introduce a power-user behavior: 'now that you've [done aha], here's how power users go further.' Aim: shift user from 'tried it' to 'depends on it'. Use the result of "Find people who just got value".

## Step 3: Send on days 1, 5 and 10

Build a 3-touch journey triggered when feature_first_used = aha-moment fires. Touch 1: Day 1. Touch 2: Day 5. Touch 3: Day 10. Add a branch: if the user has already done the next-step feature naturally by Day 5 (great sign), skip touch 2 and go straight to touch 3 power-user content. Exit on: subscription_created (paid conversion: celebrate and handoff to free-to-paid-csm-kickoff), unsubscribe, or 14-day timeout. Use the result of "Find people who just got value", "Write three follow up emails".

## Step 4: Track activation and retention

Compose an activation funnel dashboard: aha-moment achievement rate among new signups (the activation rate: target depends on product, but trend matters more than absolute), time-from-signup-to-aha distribution, post-aha retention curve (do aha-achievers stick around better than non-achievers?: this is the proof-of-value of focusing activation efforts), and journey engagement by touch. Compare 30-day retention of aha-achievers who went through this journey vs. aha-achievers who didn't (typical lift: 10-20% retention improvement). Use the result of "Find people who just got value", "Write three follow up emails", "Send on days 1, 5 and 10".
