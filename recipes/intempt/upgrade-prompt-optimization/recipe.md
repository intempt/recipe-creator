---
frontmatter_id: upgrade-prompt-optimization
slash_command: /upgrade-prompt-optimization
description: Compares four places to show the upgrade prompt to free users, with timing layered in through audience targeting.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests four placements of an upgrade prompt for free users, with account-age cohorts, to find which placement and
    timing best drives subscriptions without adding prompt fatigue.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Upgrade Prompt Optimization
    required: false
  - name: schedule_days
    type: number
    label: Schedule (days)
    default: 21
    required: false
  - name: min_account_age
    type: duration
    label: Minimum account age to enter the audience
    default: 3 d
    required: false
  - name: goal_window
    type: duration
    label: Subscription goal window after exposure
    default: 14 d
    required: false
  - name: display_frequency
    type: enum
    label: Display frequency
    default: once_per_session
    required: false
    options:
    - once_per_session
    - every_page_view
    - once_per_user
  - name: nps_drop_threshold
    type: number
    label: Maximum allowed NPS drop (points, trailing 30 days)
    default: 5
    required: false
  requirements:
  - slot: upgrade_prompt_experience
    kind: event
    meaning: A customer was exposed to or clicked an in-app upgrade prompt
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked upgrade prompt element
      optional: false
    - name: experience_id
      type: string
      meaning: Identifier of the experiment experience
      optional: false
    - name: data_placement
      type: string
      meaning: Placement of the upgrade prompt
      optional: true
  - slot: goal_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experiment experience that drove the goal
      optional: false
  - slot: feedback_event
    kind: event
    meaning: A customer submitted feedback with a score
    properties:
    - name: score
      type: number
      meaning: Feedback score given by the customer
      optional: false
  - slot: free_plan_users
    kind: segment
    meaning: Users on the free plan (no subscription or plan equal to free) whose account is at least the minimum age
  - slot: account_age
    kind: attribute
    meaning: Number of days since the customer's account was created
  - slot: subscription_plan
    kind: attribute
    meaning: The customer's current subscription plan
  - slot: experiment_destination
    kind: destination
    meaning: The in-app experience surface where client experiments are published
    channel: email
  steps:
  - id: s1
    builds: experiment
    uses:
    - upgrade_prompt_experience
    - goal_event
    - feedback_event
    - free_plan_users
    - account_age
    - subscription_plan
    - experiment_destination
    - experiment_title
    - schedule_days
    - min_account_age
    - goal_window
    - display_frequency
    - nps_drop_threshold
    instruction: 'Create a client experiment titled "{experiment_title}" on the in-app experience surface {experiment_destination}.
      Audience: {free_plan_users}, filtered to users where {subscription_plan} is null or equals free, and {account_age} is
      at least {min_account_age}. Pages: any in-app page where the dashboard chrome renders. Devices: any. Display frequency:
      {display_frequency}. Run for {schedule_days} days in three sequential account-age cohorts: cohort 1 is {account_age}
      from 3 to 7 days, cohort 2 is 8 to 14 days, cohort 3 is greater than 14 days. Each cohort uses the same four placement
      variants at 25% each: Control (existing upgrade banner at top of dashboard), Variant B (inline upgrade prompt at the
      feature-limit gate, shown when a user clicks a paywalled feature), Variant C (persistent upgrade card in sidebar navigation),
      and Variant D (floating upgrade pill in the bottom-right corner). Control variant: insert before .dashboard-header a
      banner with data-variant control and data-placement top-banner containing the text ''Upgrade to Pro for unlimited features'',
      a button with id upgrade-prompt-cta and data-placement top reading ''Upgrade now'', and a dismiss button with id upgrade-prompt-dismiss
      and aria-label Dismiss showing ×. Variant B: target .feature-gate-overlay and add a block with data-variant b and data-placement
      inline-gate, heading "You''ve hit your free plan limit", text ''Upgrade to Pro to continue with unlimited access.'',
      a button with id upgrade-prompt-cta and data-placement inline reading ''Upgrade now'', and a dismiss button with id
      upgrade-prompt-dismiss reading ''Maybe later''. Variant C: append at the bottom of .sidebar-nav a card with data-variant
      c and data-placement sidebar, a lightning icon, text ''Unlock Pro features'', and a button with id upgrade-prompt-cta
      and data-placement sidebar reading ''See plans''. Variant D: append to body a fixed-position element at bottom 24px
      and right 24px with data-variant d and data-placement floating-pill, a button with id upgrade-prompt-cta and data-placement
      floating reading ''Upgrade ↗'', and a dismiss button with id upgrade-prompt-dismiss and aria-label Dismiss showing ×.
      Keep the ids upgrade-prompt-cta and upgrade-prompt-dismiss identical across all variants. Primary goal: {goal_event}
      fires when a subscription starts within {goal_window} of exposure. Secondary metrics: clicks on upgrade-prompt-cta per
      placement, clicks on upgrade-prompt-dismiss as the dismissal rate, and subscriptions started within {goal_window}. Guardrail:
      {feedback_event} score trailing 30-day trend must not drop by more than {nps_drop_threshold} points.'
---

# Upgrade prompt test

Slash command: /upgrade-prompt-optimization

## Step 1: Set up the upgrade prompt test

Create a CLIENT EXPERIMENT on /experiences titled "Upgrade Prompt Optimization".
This recipe merges what was historically two separate experiments (placement + timing) into one. The PLACEMENT dimension is tested via client variants (different on-page locations); the TIMING dimension is layered via the experience's audience targeting (segment-based: account age + activity).
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants (placement axis):
- Control (25%): existing upgrade banner at top of dashboard
- Variant B (25%): inline upgrade prompt at the feature-limit gate (shown when user clicks a paywalled feature)
- Variant C (25%): persistent upgrade card in sidebar navigation
- Variant D (25%): floating upgrade pill in the bottom-right corner
Targeting (timing dimension applied as audience filter):
- Pages: any in-app page where the dashboard chrome renders
- Audience: free plan users only: segment definition: subscription is null OR Plan = "free", AND account_age >= 3 days
 - Run this experiment in three sequential cohorts to test timing:
 - Cohort 1: account_age 3-7 days
 - Cohort 2: account_age 8-14 days
 - Cohort 3: account_age >14 days
 - Each cohort gets the same 4 placement variants; comparing across cohorts answers the timing question.
- Devices: any
- Display frequency: once_per_session (avoid prompt fatigue within a session)
Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on Subscription started within 14 days of exposure)
Secondary metrics:
- Click on where target_id = "upgrade-prompt-cta" (per-placement click rate)
- Click on where target_id = "upgrade-prompt-dismiss" (dismissal rate: friction signal)
- Subscription started within 14 days
Guardrail: NPS feedback (Feedback submitted with score property) must not drop more than 5 points in trailing-30d trend
Schedule: 21 days
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (top banner)
 HTML target selector: .dashboard-header (insert before)
 Variant DOM (existing):
 <div class="upgrade-banner" data-variant="control" data-placement="top-banner">
 <p>Upgrade to Pro for unlimited features</p>
 <button class="upgrade-cta" id="upgrade-prompt-cta" data-placement="top">Upgrade now</button>
 <button class="dismiss" id="upgrade-prompt-dismiss" aria-label="Dismiss">×</button>
 </div>
Variant: B (inline at feature-limit gate)
 HTML target selector: .feature-gate-overlay (the modal/overlay that appears when a free user hits a feature limit)
 Variant DOM:
 <div class="upgrade-inline-prompt" data-variant="b" data-placement="inline-gate">
 <h3>You've hit your free plan limit</h3>
 <p>Upgrade to Pro to continue with unlimited access.</p>
 <button class="upgrade-cta" id="upgrade-prompt-cta" data-placement="inline">Upgrade now</button>
 <button class="dismiss" id="upgrade-prompt-dismiss">Maybe later</button>
 </div>
Variant: C (sidebar card)
 HTML target selector: .sidebar-nav (append at bottom)
 Variant DOM:
 <div class="upgrade-sidebar-card" data-variant="c" data-placement="sidebar">
 <span class="upgrade-icon">⚡</span>
 <p>Unlock Pro features</p>
 <button class="upgrade-cta" id="upgrade-prompt-cta" data-placement="sidebar">See plans</button>
 </div>
Variant: D (floating pill)
 HTML target selector: body (append fixed-position element)
 Variant DOM:
 <div class="upgrade-floating-pill" data-variant="d" data-placement="floating-pill" style="position:fixed;bottom:24px;right:24px;">
 <button class="upgrade-cta" id="upgrade-prompt-cta" data-placement="floating">Upgrade ↗</button>
 <button class="dismiss" id="upgrade-prompt-dismiss" aria-label="Dismiss">×</button>
 </div>
The Visual Editor lets the user adjust copy, colors, animation, and exact positioning per variant. Ensure target_id values "upgrade-prompt-cta" and "upgrade-prompt-dismiss" are preserved across all variants so Click on aggregation is consistent.
Taxonomy notes:
- The 4-variant design tests placement; the 3-cohort schedule tests timing. Total observations: 4 placements × 3 timings = 12 cells. Plan sample sizes accordingly: you'll want at least 500 exposures per cell, so ~6,000 free users in the experiment.
- Click on.target_id = "upgrade-prompt-cta" is shared across placements, with target_id and the data-placement attribute on the button enabling per-placement segmentation in analysis.
