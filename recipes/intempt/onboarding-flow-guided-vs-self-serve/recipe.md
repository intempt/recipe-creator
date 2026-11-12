---
frontmatter_id: onboarding-flow-guided-vs-self-serve
slash_command: /onboarding-flow-guided-vs-self-serve
description: Compares a self-serve checklist, a guided wizard and a video-first walkthrough, scored on activation within 7 days.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Runs an A/B/C test of three onboarding flows (self-serve checklist, guided wizard, video-first) for new signups
    and scores which drives activation within 7 days.
  parameters:
  - name: control_traffic
    type: number
    label: Control variant traffic share (%)
    default: 34
    required: false
  - name: variant_b_traffic
    type: number
    label: Guided wizard variant traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic
    type: number
    label: Video-first variant traffic share (%)
    default: 33
    required: false
  - name: new_user_window
    type: duration
    label: New signup window for targeting
    default: 1 h
    required: false
  - name: activation_window
    type: duration
    label: Activation goal window after exposure
    default: 7 d
    required: false
  - name: test_duration
    type: duration
    label: Minimum test duration
    default: 30 d
    required: false
  - name: bounce_guardrail_increase
    type: number
    label: Maximum allowed increase in onboarding bounce rate (%)
    default: 10
    required: false
  - name: return_window
    type: duration
    label: Day-2 return window
    default: 2 d
    required: false
  requirements:
  - slot: onboarding_experiment_tool
    kind: integration
    meaning: An experimentation tool that can run client-side experiments with visual editor variants and goal tracking
    channel: email
  - slot: new_signup_segment
    kind: segment
    meaning: Users who were created within the last hour, i.e. new signups
  - slot: onboarding_page
    kind: destination
    meaning: The in-app onboarding page or post-signup landing page where the onboarding flow is shown
    channel: email
  - slot: activation_goal
    kind: event
    meaning: A customer completed the activation journey goal
  - slot: experience_exposed
    kind: event
    meaning: A user was shown an experiment experience variant
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience the user was exposed to
      optional: false
  - slot: goal_completed_in_experience
    kind: event
    meaning: A user completed a goal within an experience
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience where the goal completed
      optional: false
  - slot: ui_click
    kind: event
    meaning: A user clicked a tracked UI element
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element
      optional: false
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  - slot: session_end
    kind: event
    meaning: A user ended a session in the product
  steps:
  - id: s1
    builds: experiment
    uses:
    - onboarding_experiment_tool
    - new_signup_segment
    - onboarding_page
    - activation_goal
    - experience_exposed
    - goal_completed_in_experience
    - ui_click
    - session_start
    - session_end
    - control_traffic
    - variant_b_traffic
    - variant_c_traffic
    - new_user_window
    - activation_window
    - test_duration
    - bounce_guardrail_increase
    - return_window
    instruction: 'Create a client-side experiment titled "Onboarding Flow: Guided vs Self-Serve" in the experimentation tool.
      Targeting: the onboarding page; audience limited to {new_signup_segment} (users created within {new_user_window}); all
      devices; display once per user, sticky to the first session. Variants: Control ({control_traffic}%) keeps the self-serve
      checklist with no DOM changes; Variant B ({variant_b_traffic}%) is a guided wizard with progressive steps and contextual
      tooltips; Variant C ({variant_c_traffic}%) is a video-first onboarding with an embedded walkthrough. Primary metric:
      goal_completed_in_experience for this experience, where the goal is {activation_goal} reached within {activation_window}
      of exposure. Secondary metrics: (a) median time from experience_exposed to the first ui_click whose target_id is key
      feature click id, computed per variant as time to value; (b) session_start rate on day 2 within {return_window} of signup;
      (c) onboarding completion rate, measured as ui_click on the final onboarding step''s target_id. Guardrail: the share
      of users with a session_end and no ui_click after onboarding render must not rise more than {bounce_guardrail_increase}%
      relative to control. Run for at least {test_duration}.'
---

# Guided vs self-serve onboarding

Slash command: /onboarding-flow-guided-vs-self-serve

## Step 1: Set up the onboarding test

Create a CLIENT EXPERIMENT on /experiences titled "Onboarding Flow: Guided vs Self-Serve".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (34%): self-serve checklist (current: list of clickable steps)
- Variant B (33%): guided wizard with progressive steps and contextual tooltips
- Variant C (33%): video-first onboarding with embedded walkthrough
Targeting:
- Pages: in-app onboarding page (typically /onboarding or post-signup landing)
- Audience: new signups only: segment: User created within 1 hour
- Devices: any
- Display frequency: once (sticky to user's first session)
Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on the activation event, e.g. Completed a journey goal for the activation journey, within 7 days of exposure)
Secondary metrics:
- Median time from exposed_to_experience to first key Click on (the canonical "time to value" measurement)
- Session start day-2 (returned-after-signup rate: engagement persistence)
- Onboarding completion rate (Click on on the final step's target_id)
Guardrail: bounce-from-onboarding rate (Session end without any Click on after onboarding render) must not increase >10%
Schedule: 30 days minimum
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (self-serve checklist: no DOM changes)
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
 <div class="wizard-tooltip" role="tooltip">Hover here for tips to </div>
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
- "Time to first key Click on" is computed by Lovable from exposed_to_experience timestamp to the first downstream Click on event for the same user. Median across users = the variant's TTV.
- The "key Click on" identifier (which Click on target_id counts as activation) is project-defined; typically it's the first interaction with a core product feature.
