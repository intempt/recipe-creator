---
id: onboarding-checklist-length
title: Onboarding checklist length test
slash_command: /onboarding-checklist-length
group: Experiments
owner: intempt
summary: Compares a 3, 5 and 7 step onboarding checklist for new signups, scored on activation within
  7 days.
description: >-
  Test whether shorter or longer in-app onboarding checklists improve 7-day activation. Client experiment.
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - saas
  complexity: standard
  executionMode: live
  tags:
    - experiment
    - client
  experimentType: a-b
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new A/B experiment, from step 1 "Set up the checklist length test"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Set up the checklist length test
    summary: >-
      Shows new signups one of three checklists: three steps (connect data, invite team, first report),
      five steps, or seven steps. The winner is the length with the most users hitting your activation
      milestone within 7 days of seeing it.
    builds: experiment
    description: |-
      Create a CLIENT EXPERIMENT on /experiences titled "Onboarding Checklist Length".
      ═══ PATH 1: Top-level configuration ═══
      Experience type: client_experiment
      Variants:
      - Control (34%): 3 steps: Connect data, Invite team, Create first report
      - Variant B (33%): 5 steps: adds Set goals, Customize dashboard
      - Variant C (33%): 7 steps: adds Watch tutorial, Configure notifications
      Targeting:
      - Pages: in-app dashboard URL where the onboarding checklist component renders
      - Audience: new signups only: segment definition: user_created within 24 hours
      - Devices: any
      - Display frequency: always (during user's first session) or once (sticky to first visit)
      Primary metric: goal_completed_in_experience where experience_id = <this> (the goal fires when the user completes their nominated activation milestone within 7 days of exposure)
      Secondary metrics:
      - click_on per checklist step (per-step completion rate)
      - goal_completed_in_journey within 7 days (existing activation journey completion)
      - session_start day-2 / day-7 (engagement after onboarding)
      Guardrail: 14-day session_start retention must not drop >3 percentage points
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
      User refines the step copy, icons, and ordering in the Visual Editor. Ensure each step has a stable target_id (step-1, step-2, etc.) so per-step click_on metrics roll up consistently.
      Taxonomy notes:
      - The "activation milestone" is project-defined: typically goal_completed_in_journey for the activation journey. This recipe assumes the activation journey is configured separately.
      - session_start is the canonical engagement signal.
outputs:
  - key: experiment
    producedByStep: s1
    type: experiment
    description: Website experiment created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Onboarding checklist length test

Compares a 3, 5 and 7 step onboarding checklist for new signups, scored on activation within 7 days.

## Steps

1. **Set up the checklist length test** (builds experiment)

   Shows new signups one of three checklists: three steps (connect data, invite team, first report), five steps, or seven steps. The winner is the length with the most users hitting your activation milestone within 7 days of seeing it.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new A/B experiment, from step 1 "Set up the checklist length test"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build experiment.
