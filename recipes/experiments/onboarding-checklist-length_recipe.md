---
name: onboarding-checklist-length
description: |
  Use when a user mentions "onboarding checklist length test", or asks for related help. Test whether shorter or longer in-app onboarding checklists improve 7-day activation. Client experiment.
arguments: []
intempt:
  id: onboarding-checklist-length
  version: 1.0.0
  slashCommand: /experiment-recipe
  group: Experiments
  shortDescription: "Test whether shorter or longer in-app onboarding checklists improve 7-day activation. Client experiment."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [experiment, client]
    experimentType: a-b
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_experiment
  procedure:
    - step: 1
      title: "Configure Website Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: "Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2)."
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Onboarding Checklist Length".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (34%): 3 steps — Connect data, Invite team, Create first report
        - Variant B (33%): 5 steps — adds Set goals, Customize dashboard
        - Variant C (33%): 7 steps — adds Watch tutorial, Configure notifications

        Targeting:
        - Pages: in-app dashboard URL where the onboarding checklist component renders
        - Audience: new signups only — segment definition: user_created within 24 hours
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
        - The "activation milestone" is project-defined — typically goal_completed_in_journey for the activation journey. This recipe assumes the activation journey is configured separately.
        - session_start is the canonical engagement signal.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---

# Onboarding Checklist Length Test

## Procedure

1. **Configure Website Experiment** [`create_experiment`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: experiment

   ```text
   Create a CLIENT EXPERIMENT on /experiences titled "Onboarding Checklist Length".

   ═══ PATH 1: Top-level configuration ═══

   Experience type: client_experiment

   Variants:
   - Control (34%): 3 steps — Connect data, Invite team, Create first report
   - Variant B (33%): 5 steps — adds Set goals, Customize dashboard
   - Variant C (33%): 7 steps — adds Watch tutorial, Configure notifications

   Targeting:
   - Pages: in-app dashboard URL where the onboarding checklist component renders
   - Audience: new signups only — segment definition: user_created within 24 hours
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
   - The "activation milestone" is project-defined — typically goal_completed_in_journey for the activation journey. This recipe assumes the activation journey is configured separately.
   - session_start is the canonical engagement signal.
   ```
