---
name: onboarding-flow-guided-vs-self-serve
description: |
  Use when a user mentions "onboarding flow — guided vs self-serve", or asks for related help. Test whether a guided wizard or self-serve checklist or video-first onboarding produces faster time-to-value. Client experiment.
arguments: []
intempt:
  id: onboarding-flow-guided-vs-self-serve
  version: 1.0.0
  slashCommand: /experiment-recipe
  group: Experiments
  shortDescription: "Create an A/B client experiment testing guided wizard, self-serve checklist, and video-first onboarding flows for time-to-value."
  availability: coming-soon
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
        Create a CLIENT EXPERIMENT on /experiences titled "Onboarding Flow — Guided vs Self-Serve".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (34%): self-serve checklist (current — list of clickable steps)
        - Variant B (33%): guided wizard with progressive steps and contextual tooltips
        - Variant C (33%): video-first onboarding with embedded walkthrough

        Targeting:
        - Pages: in-app onboarding page (typically /onboarding or post-signup landing)
        - Audience: new signups only — segment: user_created within 1 hour
        - Devices: any
        - Display frequency: once (sticky to user's first session)

        Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on the activation event, e.g. goal_completed_in_journey for the activation journey, within 7 days of exposure)
        Secondary metrics:
        - Median time from exposed_to_experience to first key click_on (the canonical "time to value" measurement)
        - session_start day-2 (returned-after-signup rate — engagement persistence)
        - Onboarding completion rate (click_on on the final step's target_id)

        Guardrail: bounce-from-onboarding rate (session_end without any click_on after onboarding render) must not increase >10%

        Schedule: 30 days minimum

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (self-serve checklist — no DOM changes)
          Existing onboarding checklist remains in place.

        Variant: B (guided wizard)
          HTML target selector: .onboarding-container (replace contents)
          Replacement HTML:
          <div class="onboarding-wizard" data-variant="b">
            <div class="wizard-progress">
              <div class="wizard-step active" data-step="1">1. Welcome</div>
              <div class="wizard-step" data-step="2">2. Connect data</div>
              <div class="wizard-step" data-step="3">3. Invite team</div>
              <div class="wizard-step" data-step="4">4. Create report</div>
            </div>
            <main class="wizard-content">
              <h2 class="wizard-step-title">Welcome to [Product]</h2>
              <p class="wizard-step-body">Let's get you set up in 4 quick steps.</p>
              <div class="wizard-tooltip" role="tooltip">Hover here for tips →</div>
              <div class="wizard-actions">
                <button class="wizard-prev" disabled>Back</button>
                <button class="wizard-next" id="wizard-next-1">Continue</button>
              </div>
            </main>
          </div>

        Variant: C (video-first)
          HTML target selector: .onboarding-container (replace contents)
          Replacement HTML:
          <div class="onboarding-video" data-variant="c">
            <div class="video-hero">
              <video controls autoplay muted poster="/onboarding-poster.jpg">
                <source src="/onboarding-walkthrough.mp4" type="video/mp4" />
              </video>
            </div>
            <div class="video-secondary-actions">
              <h3>Or jump straight in</h3>
              <button class="quickstart-cta" id="quickstart-cta">Skip and start exploring</button>
            </div>
          </div>

        The user supplies their actual onboarding copy, video file, and styling in the Visual Editor.

        Taxonomy notes:
        - "Time to first key click_on" is computed by Lovable from exposed_to_experience timestamp to the first downstream click_on event for the same user. Median across users = the variant's TTV.
        - The "key click_on" identifier (which click_on target_id counts as activation) is project-defined; typically it's the first interaction with a core product feature.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---

# Onboarding Flow — Guided vs Self-Serve

## Procedure

1. **Configure Website Experiment** [`create_experiment`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: experiment

   ```text
   Create a CLIENT EXPERIMENT on /experiences titled "Onboarding Flow — Guided vs Self-Serve".

   ═══ PATH 1: Top-level configuration ═══

   Experience type: client_experiment

   Variants:
   - Control (34%): self-serve checklist (current — list of clickable steps)
   - Variant B (33%): guided wizard with progressive steps and contextual tooltips
   - Variant C (33%): video-first onboarding with embedded walkthrough

   Targeting:
   - Pages: in-app onboarding page (typically /onboarding or post-signup landing)
   - Audience: new signups only — segment: user_created within 1 hour
   - Devices: any
   - Display frequency: once (sticky to user's first session)

   Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on the activation event, e.g. goal_completed_in_journey for the activation journey, within 7 days of exposure)
   Secondary metrics:
   - Median time from exposed_to_experience to first key click_on (the canonical "time to value" measurement)
   - session_start day-2 (returned-after-signup rate — engagement persistence)
   - Onboarding completion rate (click_on on the final step's target_id)

   Guardrail: bounce-from-onboarding rate (session_end without any click_on after onboarding render) must not increase >10%

   Schedule: 30 days minimum

   ═══ PATH 2: Variant HTML content (Visual Editor) ═══

   Variant: Control (self-serve checklist — no DOM changes)
     Existing onboarding checklist remains in place.

   Variant: B (guided wizard)
     HTML target selector: .onboarding-container (replace contents)
     Replacement HTML:
     <div class="onboarding-wizard" data-variant="b">
       <div class="wizard-progress">
         <div class="wizard-step active" data-step="1">1. Welcome</div>
         <div class="wizard-step" data-step="2">2. Connect data</div>
         <div class="wizard-step" data-step="3">3. Invite team</div>
         <div class="wizard-step" data-step="4">4. Create report</div>
       </div>
       <main class="wizard-content">
         <h2 class="wizard-step-title">Welcome to [Product]</h2>
         <p class="wizard-step-body">Let's get you set up in 4 quick steps.</p>
         <div class="wizard-tooltip" role="tooltip">Hover here for tips →</div>
         <div class="wizard-actions">
           <button class="wizard-prev" disabled>Back</button>
           <button class="wizard-next" id="wizard-next-1">Continue</button>
         </div>
       </main>
     </div>

   Variant: C (video-first)
     HTML target selector: .onboarding-container (replace contents)
     Replacement HTML:
     <div class="onboarding-video" data-variant="c">
       <div class="video-hero">
         <video controls autoplay muted poster="/onboarding-poster.jpg">
           <source src="/onboarding-walkthrough.mp4" type="video/mp4" />
         </video>
       </div>
       <div class="video-secondary-actions">
         <h3>Or jump straight in</h3>
         <button class="quickstart-cta" id="quickstart-cta">Skip and start exploring</button>
       </div>
     </div>

   The user supplies their actual onboarding copy, video file, and styling in the Visual Editor.

   Taxonomy notes:
   - "Time to first key click_on" is computed by Lovable from exposed_to_experience timestamp to the first downstream click_on event for the same user. Median across users = the variant's TTV.
   - The "key click_on" identifier (which click_on target_id counts as activation) is project-defined; typically it's the first interaction with a core product feature.
   ```
