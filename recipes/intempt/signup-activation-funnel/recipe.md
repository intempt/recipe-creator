---
description: Shows how many new signups come back, use the core feature and activate within two weeks, and which signup source produces the best ones.
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

# Signup to activation

Slash command: /signup-activation-funnel

## Step 1: Follow signups to activation

Create a Funnel report called "Signup to Activation".
Steps:
1. Event "user_created": "Signed Up"
2. Event "session_start" within 24 hours of user_created: "Returned After Signup" (proxy for engagement after creation)
3. Event "goal_completed_in_journey" where journey_id matches the onboarding/activation journey: "Used Core Feature"
4. Event "goal_completed_in_journey" where journey_id matches the activation journey AND occurred_at - signup_at <= 14 days: "Activated"
Conversion window: 14 days
Breakdown: By Users.utm_source (signup source: top 6 channels: organic, paid_search, paid_social, content, referral, direct)
Compare: Previous period (prior 14 days)
For each step, also surface:
- Median and 75th-percentile time-to-convert from previous step
- Per-source conversion rate at each stage
Annotations:
- Add benchmark: activation rate (Step 4 / Step 1) of 30% is typical PLG SaaS.
- Flag any source with activation rate <15% (poor lead quality or onboarding mismatch).
- Flag any step where median time-to-convert exceeds 24 hours for "Returned After Signup" or 7 days for "Used Core Feature".
- Highlight sources with activation rate >40%.
Identify which signup source produces the highest-activating users at sufficient volume.
Taxonomy notes:
- user_created and goal_completed_in_journey are canonical. goal_completed_in_journey carries journey_id, occurred_at, user_id.
- "signup_completed", "onboarding_started" as standalone events do not exist; the activation journey itself emits goal_completed_in_journey when the user hits the activation goal.
- Users.utm_source is the canonical first-touch source attribute.
