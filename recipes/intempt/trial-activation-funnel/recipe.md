---
description: Shows how far trial users get through setup and core feature use before the trial ends, and which sources bring trials that activate.
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
  - finance
  - media
---

# Trial activation funnel

Slash command: /trial-activation-funnel

## Step 1: Track trials through setup

Create a Funnel report called "Trial Activation Funnel".
Steps:
1. Event "Subscription started" where trial_end and trial_start are populated: "Started Trial"
2. Event "Session start" by the same user within 24h of step 1: "First Return Session"
3. Event "Completed a journey goal" where journey_id matches the integration/setup journey: "Completed Setup Goal"
4. Event "Completed a journey goal" where journey_id matches the core-feature-use journey: "Used Core Feature"
5. Event "Completed a journey goal" where journey_id matches the full-activation journey AND occurred within 14 days of trial start: "Fully Activated"
Conversion window: 14 days
Breakdown: By Users.UTM source
Compare: Previous period (prior 14 days)
For each step, also surface:
- Median time-to-convert from previous step
- Per-source conversion rate at each stage
Annotations:
- Flag if the % of trials that hit Step 3 within 24 hours is below 50%: first-day setup is a strong activation predictor.
- Flag if median time from Step 1 to Step 4 exceeds 48 hours: the time-to-value benchmark for self-serve PLG.
- Flag any source where Step 5 (full activation) rate is below 15%.
- Highlight sources where Step 5 rate exceeds 35%.
Surface the single highest-leverage step to optimize: largest drop-off × largest downstream lift on Step 5.
Taxonomy notes:
- "integration_connected" and "onboarding_started" as standalone events do not exist. Setup milestones are tracked via Completed a journey goal events emitted by the relevant onboarding journey.
- Each onboarding milestone (setup, core-feature use, full activation) corresponds to a different journey_id in the project's journey configuration.
