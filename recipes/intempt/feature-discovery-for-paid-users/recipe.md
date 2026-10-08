---
description: Shows paying customers the features they have never opened, one at a time, picked for the way they actually use the product.
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

# Feature discovery for paid users

Slash command: /feature-discovery-for-paid-users

## Step 1: Find features they never use

Create an AI-derived attribute 'untouched_features' on the User object. Computed weekly. For each user, compare features-touched in last 90 days against the catalog of features available on their plan, and surface the top 3 high-value features they haven't used. Prioritize features by: (a) historical correlation with retention among similar users, (b) features the user's use case (inferred from segment / industry / role) suggests they should benefit from. Excludes features that the user's plan doesn't include. Output: ranked list of 3 untouched features with the recommended order.

## Step 2: Pick who is worth nudging

Build a segment 'Feature discovery audience' capturing paid users where subscription is at least 30 days old AND untouched_features list is non-empty AND the user has had at least 2 sessions in the last 14 days (active enough to benefit from a feature nudge). Excludes users in initial onboarding (different motion) and users who already received a feature-discovery nudge in the last 30 days. Use the result of "Find features they never use".

## Step 3: Write the nudge

Generate per-feature discovery email templates (one template that pulls the top untouched feature per recipient). Subject: '[First name], you haven't tried [feature] yet': specific feature, specific benefit. Body: brief value statement of the feature ('Users who use [feature] save an average of [time/effort metric]'), a short use-case description that matches the user's segment, a screenshot or short GIF showing the feature in action, and a deep-link CTA into the app at the right place. Tone: helpful nudge, not 'we noticed you're not getting your money's worth' (which feels accusatory). Use the result of "Find features they never use", "Pick who is worth nudging".

## Step 4: One feature every two weeks

Build a 3-touch journey triggered weekly for users in the feature-discovery segment. Each touch surfaces a DIFFERENT untouched feature from the user's list (not the same feature 3 times). Touch 1: top feature, Day 0. Touch 2: second feature, Day 14. Touch 3: third feature, Day 28. Skip a touch if the user actually started using that feature between touches (they got the message: don't pester). Exit on: user adopts all 3 features (success), user opens cancel-flow (handoff to pre-cancellation-save), or 60-day completion. Use the result of "Find features they never use", "Pick who is worth nudging", "Write the nudge".

## Step 5: See what the nudges actually change

Compose a feature adoption dashboard: feature-discovery email volume by feature (which features need the most nudge: could signal weak in-app discoverability), feature-adoption rate after nudge (% of recipients who use the feature within 14 days of receiving the nudge: typical: 8-15%), retention lift from adoption (compare 90-day retention of users who adopted post-nudge vs. control), and untouched-feature distribution (which features are most-commonly never-touched: informs product team where the discoverability gaps are). Use the result of "Find features they never use", "Pick who is worth nudging", "Write the nudge", "One feature every two weeks".
