---
frontmatter_id: onboarding-checklist-length
slash_command: /onboarding-checklist-length
description: Tests 3, 5 and 7 step onboarding checklists for new signups and scores which length drives activation within
  7 days without hurting 14-day retention.
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
    label: How new a user must be
    default: 24 h
    required: false
  - name: activationWindow
    type: duration
    label: Activation window after exposure
    default: 7 d
    required: false
  - name: retentionGuardrailDropPts
    type: number
    label: Max drop in 14-day return rate (points)
    default: 3
    required: false
  - name: experimentDuration
    type: duration
    label: Test duration
    default: 30 d
    required: false
  - name: dashboardPagePath
    type: string
    label: In-app page where the checklist shows
    default: /dashboard
    required: false
  requirements:
  - slot: activation_event
    kind: event
    meaning: A user reached the product's activation milestone
  - slot: checklist_step_click
    kind: event
    meaning: A user clicked a step in the onboarding checklist
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked checklist step
      optional: false
  - slot: session_start
    kind: event
    meaning: A user started a session in the app
  steps:
  - id: s1
    builds: experiment
    uses:
    - activation_event
    - checklist_step_click
    - session_start
    - experimentTitle
    - controlTrafficPct
    - variantBTrafficPct
    - variantCTrafficPct
    - newUserWindow
    - activationWindow
    - retentionGuardrailDropPts
    - experimentDuration
    - dashboardPagePath
    instruction: 'Create a client-side experiment named "{experimentTitle}" on the in-app page {dashboardPagePath}, all devices,
      for users created in the last {newUserWindow}, shown once in their first session. Variants: Control ({controlTrafficPct}%)
      shows a 3-step checklist: Connect data, Invite team, Create first report; Variant B ({variantBTrafficPct}%) shows 5
      steps, adding Set goals and Customize your home page; Variant C ({variantCTrafficPct}%) shows 7 steps, adding Watch
      tutorial and Configure notifications. Primary metric: users who did {activation_event} within {activationWindow} of
      exposure. Secondary metrics: {checklist_step_click} per {checklist_step_click.target_id}; users who did {session_start}
      on day 2 and on day 7 after exposure. Guardrail: the share of users who did {session_start} 14 days after exposure must
      not drop more than {retentionGuardrailDropPts} percentage points below Control. Run for {experimentDuration}.'
---

# Onboarding checklist length test

Slash command: /onboarding-checklist-length

## Step 1: Set up the checklist length test

Create a client-side experiment named "Onboarding Checklist Length" on the in-app page /dashboard, all devices, for users created in the last 24 h, shown once in their first session. Variants: Control (34%) shows a 3-step checklist: Connect data, Invite team, Create first report; Variant B (33%) shows 5 steps, adding Set goals and Customize your home page; Variant C (33%) shows 7 steps, adding Watch tutorial and Configure notifications. Primary metric: users who did activation event within 7 d of exposure. Secondary metrics: checklist step click per target id; users who did session start on day 2 and on day 7 after exposure. Guardrail: the share of users who did session start 14 days after exposure must not drop more than 3 percentage points below Control. Run for 30 d.
