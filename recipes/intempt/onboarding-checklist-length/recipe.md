---
frontmatter_id: onboarding-checklist-length
slash_command: /onboarding-checklist-length
description: Compares a 3, 5 and 7 step onboarding checklist for new signups, scored on activation within 7 days.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests 3, 5 and 7 step onboarding checklists for new signups and scores which length drives activation within 7
    days without hurting 14-day retention.
  parameters:
  - name: experimentTitle
    type: string
    label: Experiment title
    default: Onboarding Checklist Length
    required: false
  - name: controlTrafficPct
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variantBTrafficPct
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: variantCTrafficPct
    type: number
    label: Variant C traffic share (%)
    default: 33
    required: false
  - name: newUserWindow
    type: duration
    label: New signup window
    default: 24 h
    required: false
  - name: activationWindow
    type: duration
    label: Activation window after exposure
    default: 7 d
    required: false
  - name: retentionGuardrailDropPts
    type: number
    label: Max allowed 14-day retention drop (percentage points)
    default: 3
    required: false
  - name: experimentDuration
    type: duration
    label: Experiment schedule
    default: 30 d
    required: false
  - name: displayFrequency
    type: enum
    label: Display frequency
    default: once
    required: false
    options:
    - always
    - once
  requirements:
  - slot: onboarding_dashboard_page
    kind: destination
    meaning: The in-app dashboard page where the onboarding checklist component renders
    channel: email
  - slot: new_signup_segment
    kind: segment
    meaning: Users who were created within the last 24 hours
  - slot: goal_completed_in_experience
    kind: event
    meaning: A customer completed their nominated activation milestone after seeing an experiment variant
    properties:
    - name: experience_id
      type: string
      meaning: ID of the experiment the goal is attributed to
      optional: false
  - slot: checklist_step_click
    kind: event
    meaning: A customer clicked a step in the onboarding checklist
    properties:
    - name: target_id
      type: string
      meaning: Stable ID of the clicked checklist step, such as step-1
      optional: false
  - slot: activation_journey_goal
    kind: event
    meaning: A customer completed a goal in the activation journey
  - slot: session_start
    kind: event
    meaning: A customer started a session in the app
  steps:
  - id: s1
    builds: experiment
    uses:
    - onboarding_dashboard_page
    - new_signup_segment
    - goal_completed_in_experience
    - checklist_step_click
    - activation_journey_goal
    - session_start
    - experimentTitle
    - controlTrafficPct
    - variantBTrafficPct
    - variantCTrafficPct
    - newUserWindow
    - activationWindow
    - retentionGuardrailDropPts
    - experimentDuration
    - displayFrequency
    instruction: 'Create a client experiment titled "{experimentTitle}" on the experiences page. Define three variants: Control
      ({controlTrafficPct}% traffic) with a 3-step checklist (Connect data, Invite team, Create first report); Variant B ({variantBTrafficPct}%
      traffic) with a 5-step checklist, adding Set goals and Customize dashboard to the Control steps; Variant C ({variantCTrafficPct}%
      traffic) with a 7-step checklist, adding Watch tutorial and Configure notifications to Variant B''s steps. Target the
      {onboarding_dashboard_page} where the onboarding checklist renders, for devices of any type. Restrict the audience to
      {new_signup_segment} (users created within {newUserWindow}). Set display frequency to {displayFrequency} during the
      user''s first session. Primary metric: {goal_completed_in_experience} filtered to this experiment, where the goal fires
      when the user completes their nominated activation milestone within {activationWindow} of exposure. Secondary metrics:
      per-step click rate from {checklist_step_click} grouped by target_id; completion of a goal in {activation_journey_goal}
      within {activationWindow}; and {session_start} on day 2 and day 7. Guardrail: 14-day {session_start} retention must
      not drop by more than {retentionGuardrailDropPts} percentage points. Run for {experimentDuration}.'
---

# Onboarding checklist length test

Slash command: /onboarding-checklist-length

## Step 1: Set up the checklist length test

Create a CLIENT EXPERIMENT on /experiences titled "Onboarding Checklist Length".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (34%): 3 steps: Connect data, Invite team, Create first report
- Variant B (33%): 5 steps: adds Set goals, Customize dashboard
- Variant C (33%): 7 steps: adds Watch tutorial, Configure notifications
Targeting:
- Pages: in-app dashboard URL where the onboarding checklist component renders
- Audience: new signups only: segment definition: User created within 24 hours
- Devices: any
- Display frequency: always (during user's first session) or once (sticky to first visit)
Primary metric: goal_completed_in_experience where experience_id = <this> (the goal fires when the user completes their nominated activation milestone within 7 days of exposure)
Secondary metrics:
- Click on per checklist step (per-step completion rate)
- Completed a journey goal within 7 days (existing activation journey completion)
- Session start day-2 / day-7 (engagement after onboarding)
Guardrail: 14-day Session start retention must not drop >3 percentage points
Schedule: 30 days
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (3 steps)
 HTML target selector: .onboarding-checklist
 Replacement HTML:
 <div class="onboarding-checklist" data-variant="control" data-step-count="3">
 <h2>Get started in 3 steps</h2>
 <ol class="checklist-steps">
 <li class="checklist-step" id="step-1"><a href="/setup/data">Connect your data</a></li>
 <li class="checklist-step" id="step-2"><a href="/team/invite">Invite your team</a></li>
 <li class="checklist-step" id="step-3"><a href="/reports/new">Create your first report</a></li>
 </ol>
 <div class="checklist-progress" data-completed="0" data-total="3"></div>
 </div>
Variant: B (5 steps)
 Same wrapper, add 2 additional <li> entries:
 <li class="checklist-step" id="step-4"><a href="/goals/setup">Set your goals</a></li>
 <li class="checklist-step" id="step-5"><a href="/dashboard/customize">Customize your dashboard</a></li>
Variant: C (7 steps)
 Same wrapper, add 2 more:
 <li class="checklist-step" id="step-6"><a href="/tutorial">Watch the tutorial</a></li>
 <li class="checklist-step" id="step-7"><a href="/settings/notifications">Configure notifications</a></li>
User refines the step copy, icons, and ordering in the Visual Editor. Ensure each step has a stable target_id (step-1, step-2, etc.) so per-step Click on metrics roll up consistently.
Taxonomy notes:
- The "activation milestone" is project-defined: typically Completed a journey goal for the activation journey. This recipe assumes the activation journey is configured separately.
- Session start is the canonical engagement signal.
