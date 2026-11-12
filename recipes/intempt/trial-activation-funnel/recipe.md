---
frontmatter_id: trial-activation-funnel
slash_command: /trial-activation-funnel
description: Shows how far trial users get through setup and core feature use before the trial ends, and which sources bring trials that activate.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: placeholder
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 14 d
    required: false
  - name: comparisonWindow
    type: duration
    label: Comparison period (prior period length)
    default: 14 d
    required: false
  - name: firstReturnWindow
    type: duration
    label: Window for first return session after trial start
    default: 24 h
    required: false
  - name: setupWindow
    type: duration
    label: Window for reaching setup goal after trial start
    default: 24 h
    required: false
  - name: fullActivationWindow
    type: duration
    label: Window for full activation after trial start
    default: 14 d
    required: false
  - name: setupRateThreshold
    type: number
    label: Flag if share of trials reaching setup within window is below (%)
    default: 50
    required: false
  - name: timeToValueThreshold
    type: duration
    label: Flag if median time from trial start to core feature exceeds
    default: 48 h
    required: false
  - name: lowActivationThreshold
    type: number
    label: Flag any source whose full activation rate is below (%)
    default: 15
    required: false
  - name: highActivationThreshold
    type: number
    label: Highlight sources whose full activation rate exceeds (%)
    default: 35
    required: false
  requirements:
  - slot: trial_started_event
    kind: event
    meaning: A customer started a subscription trial
    properties:
    - name: trial_start
      type: date
      meaning: When the trial started
      optional: false
    - name: trial_end
      type: date
      meaning: When the trial ends
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: journey_goal_event
    kind: event
    meaning: A user completed a journey goal in an onboarding journey
    properties:
    - name: journey_id
      type: text
      meaning: Identifier of the onboarding journey that emitted the goal
      optional: false
  - slot: setup_journey
    kind: knowledge
    meaning: The onboarding journey id for integration and setup milestone
  - slot: core_feature_journey
    kind: knowledge
    meaning: The onboarding journey id for core feature use milestone
  - slot: full_activation_journey
    kind: knowledge
    meaning: The onboarding journey id for full activation milestone
  - slot: utm_source_attribute
    kind: attribute
    meaning: The UTM source of the user's acquisition
  steps:
  - id: s1
    builds: report
    uses:
    - trial_started_event
    - session_start_event
    - journey_goal_event
    - setup_journey
    - core_feature_journey
    - full_activation_journey
    - utm_source_attribute
    - conversionWindow
    - comparisonWindow
    - firstReturnWindow
    - setupWindow
    - fullActivationWindow
    - setupRateThreshold
    - timeToValueThreshold
    - lowActivationThreshold
    - highActivationThreshold
    instruction: 'Create a funnel report named "Trial Activation Funnel" that tracks trial users through setup and core feature
      use. Steps: 1) {trial_started_event} where trial_start and trial_end are populated, labeled "Started Trial". 2) {session_start_event}
      by the same user within {firstReturnWindow} of step 1, labeled "First Return Session". 3) {journey_goal_event} where
      journey_id matches {setup_journey} and occurs within {setupWindow} of trial start, labeled "Completed Setup Goal". 4)
      {journey_goal_event} where journey_id matches {core_feature_journey}, labeled "Used Core Feature". 5) {journey_goal_event}
      where journey_id matches {full_activation_journey} and occurs within {fullActivationWindow} of trial start, labeled
      "Fully Activated". Set conversion window to {conversionWindow}. Break down by {utm_source_attribute}. Compare against
      the previous period of {comparisonWindow}. For each step, show the median time to convert from the previous step and
      the per-source conversion rate at each stage. Annotations: flag if the share of trials reaching Step 3 within {setupWindow}
      is below {setupRateThreshold}%; flag if the median time from Step 1 to Step 4 exceeds {timeToValueThreshold}; flag any
      source whose Step 5 rate is below {lowActivationThreshold}%; highlight sources whose Step 5 rate exceeds {highActivationThreshold}%.
      Surface the single highest-leverage step to optimize, defined as the largest drop-off multiplied by the largest downstream
      lift on Step 5.'
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
