---
frontmatter_id: trial-activation-funnel
author:
  name: Intempt
  last_name: Technologies
  org_name: intempt
---
# Trial activation funnel

## Step 1: Track trials through setup

Create a Funnel report called "Trial Activation Funnel".
Steps:
1. Event "Subscription started" where trial_end and trial_start are populated: "Started Trial"
2. Event "Session start" by the same user within 24 hours of step 1: "First Return Session"
3. Event "Completed a journey goal" where journey_id matches the integration/setup journey: "Completed Setup Goal"
4. Event "Completed a journey goal" where journey_id matches the core-feature-use journey: "Used Core Feature"
5. Event "Completed a journey goal" where journey_id matches the full-activation journey and occurred within 14 days of trial start: "Fully Activated"
Conversion window: 14 days
Breakdown: By Users.UTM source
Compare: Previous period (prior 14 days)
For each step, also surface:
- Median time-to-convert from the previous step
- Per-source conversion rate at each stage
Annotations:
- Flag if the percent of trials that hit Step 3 within 24 hours is below 50 percent.
- Flag if median time from Step 1 to Step 4 exceeds 48 hours.
- Flag any source where Step 5 (full activation) rate is below 15 percent.
- Highlight sources where Step 5 rate exceeds 35 percent.
Taxonomy notes:
- "integration_connected" and "onboarding_started" as standalone events do not exist. Setup milestones are tracked via Completed a journey goal events emitted by the relevant onboarding journey.
- Each onboarding milestone (setup, core-feature use, full activation) corresponds to a different journey_id in the project's journey configuration.

## Step 2: Nudge trials stalled before full activation

Build a segment of users named "Stalled Trial Users". A user is in the segment only when all of these are true: they completed "Started Trial" more than 48 hours ago; they have not completed the full-activation journey goal; their trial has not yet ended. Use the result of "Track trials through setup".

## Step 3: Re-engage stalled trials before they expire

Build a journey for the users in "Stalled Trial Users". On entry, send an email naming the specific setup or core-feature step they have not completed and linking directly to it. If the user still has not reached "Used Core Feature" 48 hours after that email, create a task for the onboarding owner with the user's current funnel stage and trial end date attached. Exit the journey when the user reaches "Fully Activated" or when the trial ends. Use the result of "Track trials through setup", "Nudge trials stalled before full activation".
