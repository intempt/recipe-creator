---
description: Shows where new users drop out across key onboarding steps to pinpoint activation bottlenecks.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Activation funnel with velocity

Slash command: /activation-funnel-with-velocity

## Step 1: Time each step to activation

Create a Funnel report called "Activation with Step Velocity".
Steps:
1. Event "User created": "Signed Up"
2. Event "Session start" within 24h of User created: "First Return"
3. Event "Completed a journey goal" where journey_id matches the setup journey: "Completed Setup"
4. Event "Completed a journey goal" where journey_id matches the core-feature journey: "Used Core Feature"
5. Event "Completed a journey goal" where journey_id matches the activation journey, with frequency: Occurred date appears 3+ times in the 7 days following step 4: "Activated (Habituated)"
Conversion window: 14 days
Breakdown: By Users.UTM source
Compare: Previous period (prior 14 days)
For each step, in addition to conversion rate, surface:
- Median time-to-convert from previous step
- 75th-percentile time-to-convert
- Stall rate: % of users at this step who have NOT advanced after 24h, after 72h, after 7 days
Annotations:
- Add benchmarks: median signup to setup-complete ≤ 24 hours is the activation gold standard.
- Flag any step where p75 time-to-convert exceeds 7 days (long tail of stalled users).
- Flag any step where the stall-rate-at-72h is above 60%.
- Highlight the step where reducing time-to-convert by 50% would have the biggest downstream activation lift.
Velocity is the activation lever: drop-off tells you where users die, velocity tells you where they're stuck.
Taxonomy notes:
- "Habituated" Step 5 requires Lovable to compute the "3+ goal completions in 7 days" rule from Completed a journey goal timestamps grouped by user.
