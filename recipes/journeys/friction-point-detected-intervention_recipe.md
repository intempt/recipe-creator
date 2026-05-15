---
name: friction-point-detected-intervention
description: 'Use when a user mentions "friction point intervention", "in-product friction journey", "drop-off rescue", or asks for related help. When behavioral signals detect friction — setup abandoned, repeated failed actions, error encountered, drop-off at conversion step — fire a graduated intervention: in-app contextual help first, escalate to email tutorial, escalate to human/agent if friction persists. Catches users before they give up.'
arguments: []
intempt:
  id: friction-point-detected-intervention
  version: 1.0.0
  slashCommand: /friction-point-detected-intervention
  group: Journeys
  shortDescription: "'When behavioral signals detect friction — setup abandoned, repeated failed actions, error encountered, drop-off at conversion step — fire a graduated intervention: in-app contextual help first, escalate to email tutorial, escalate to human/agent if friction persists. Catches users before they give up.'"
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [friction-detection, in-app-rescue, graduated-escalation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: session_start, severity: blocking }
      - { value: feature_used, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_page_content
    - create_email_content
    - create_agent
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Friction Detection AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: friction_signal
      description: 'Create an AI-derived attribute ''recent_friction_signal'' on the User object, refreshed in real-time. Patterns detected: (a) repeated failed actions on the same UI element (3+ attempts at same form / button within a session); (b) abandoned setup step (started a multi-step flow, didn''t complete, didn''t return for 24+hrs); (c) error-encountered events without subsequent retry success; (d) help-content visits without subsequent action; (e) rage-click or rapid-back-button patterns. Output: structured object with friction_type, friction_location (where in product), severity (mild / moderate / severe based on time-stuck and repetition), and recommended_intervention.'
      prompt: 'Create an AI-derived attribute ''recent_friction_signal'' on the User object, refreshed in real-time. Patterns detected: (a) repeated failed actions on the same UI element (3+ attempts at same form / button within a session); (b) abandoned setup step (started a multi-step flow, didn''t complete, didn''t return for 24+hrs); (c) error-encountered events without subsequent retry success; (d) help-content visits without subsequent action; (e) rage-click or rapid-back-button patterns. Output: structured object with friction_type, friction_location (where in product), severity (mild / moderate / severe based on time-stuck and repetition), and recommended_intervention.'
    - step: 2
      title: Identify Friction-Affected Users
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - friction_signal
      description: Build a segment 'Active friction signal' capturing users with recent_friction_signal in the last 7 days where severity is moderate or severe. Real-time refresh. Excludes users already in active intervention from this journey (no double-poking). Partitions by friction_location so the journey routes contextually.
      prompt: Build a segment 'Active friction signal' capturing users with recent_friction_signal in the last 7 days where severity is moderate or severe. Real-time refresh. Excludes users already in active intervention from this journey (no double-poking). Partitions by friction_location so the journey routes contextually.
    - step: 3
      title: Build Contextual In-App Help
      command: create_page_content
      produces: asset
      bindsAs: inapp_asset
      dependsOn:
      - friction_signal
      - segment
      description: 'Generate in-app contextual help variants per friction_location. For setup-abandonment: contextual tooltip at the abandoned step with the answer to the common blocker. For repeated-failed-action: floating help bubble with ''Looks like you''re stuck — here''s what most users do'' + GIF or short video. For error-encountered: helpful error explainer rendered where the error appeared. For decision-paralysis (long dwell time on a critical step): comparison guide or recommendation card. Each renders mid-session when the friction is freshest. Tone: helpful colleague, not aggressive sales.'
      prompt: 'Generate in-app contextual help variants per friction_location. For setup-abandonment: contextual tooltip at the abandoned step with the answer to the common blocker. For repeated-failed-action: floating help bubble with ''Looks like you''re stuck — here''s what most users do'' + GIF or short video. For error-encountered: helpful error explainer rendered where the error appeared. For decision-paralysis (long dwell time on a critical step): comparison guide or recommendation card. Each renders mid-session when the friction is freshest. Tone: helpful colleague, not aggressive sales.'
    - step: 4
      title: Build Email Fallback Content
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - friction_signal
      - segment
      - inapp_asset
      description: 'Generate email fallback content sent if the user doesn''t engage with the in-app help OR has left the session before help was shown. Variants per friction_location. Format: subject directly addresses the issue (''Stuck on [specific step]? Here''s the fix.''), body is a 60-second tutorial (video link or step-by-step screenshots), with a one-click resume-where-you-left-off deep link. Tone: not generic ''we noticed you got stuck'' — specific to the exact friction.'
      prompt: 'Generate email fallback content sent if the user doesn''t engage with the in-app help OR has left the session before help was shown. Variants per friction_location. Format: subject directly addresses the issue (''Stuck on [specific step]? Here''s the fix.''), body is a 60-second tutorial (video link or step-by-step screenshots), with a one-click resume-where-you-left-off deep link. Tone: not generic ''we noticed you got stuck'' — specific to the exact friction.'
    - step: 5
      title: Build Agent Handoff Path
      command: create_agent
      produces: agent
      bindsAs: agent
      dependsOn:
      - friction_signal
      - segment
      description: 'Configure an AI agent scenario ''Friction rescue'' that engages users with severe friction signal who haven''t responded to in-app help OR email. Scenario: agent opens with awareness of the specific friction (''I see you''ve been working on [step] — happy to help walk through it''), offers to: (a) co-pilot the action with screen-share or step-by-step in chat, (b) escalate to human support if the problem is technical/account-level, (c) flag the friction as a product bug for the engineering queue. Agent NEVER pretends to be human; handoff to human is offered when agent can''t resolve in 3 turns.'
      prompt: 'Configure an AI agent scenario ''Friction rescue'' that engages users with severe friction signal who haven''t responded to in-app help OR email. Scenario: agent opens with awareness of the specific friction (''I see you''ve been working on [step] — happy to help walk through it''), offers to: (a) co-pilot the action with screen-share or step-by-step in chat, (b) escalate to human support if the problem is technical/account-level, (c) flag the friction as a product bug for the engineering queue. Agent NEVER pretends to be human; handoff to human is offered when agent can''t resolve in 3 turns.'
    - step: 6
      title: Build Graduated Rescue Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - friction_signal
      - segment
      - inapp_asset
      - email_asset
      - agent
      description: 'Build a graduated-escalation journey triggered when recent_friction_signal becomes moderate or severe. Touch 1 (mid-session, immediate): in-app contextual help renders at the friction location. Touch 2 (4 hours later, if user left without resolving): email fallback with tutorial + resume-link. Touch 3 (24 hours later, if friction signal still active OR user hasn''t returned): trigger agent scenario or, for severe-tier high-value users, create a CSM task for direct outreach. Exit on: friction_signal resolves (user completed the step — success), user explicitly dismisses help 3 times (respect — don''t pester), unsubscribe.'
      prompt: 'Build a graduated-escalation journey triggered when recent_friction_signal becomes moderate or severe. Touch 1 (mid-session, immediate): in-app contextual help renders at the friction location. Touch 2 (4 hours later, if user left without resolving): email fallback with tutorial + resume-link. Touch 3 (24 hours later, if friction signal still active OR user hasn''t returned): trigger agent scenario or, for severe-tier high-value users, create a CSM task for direct outreach. Exit on: friction_signal resolves (user completed the step — success), user explicitly dismisses help 3 times (respect — don''t pester), unsubscribe.'
    - step: 7
      title: Build Friction Intervention Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - friction_signal
      - segment
      - inapp_asset
      - email_asset
      - agent
      - journey
      description: 'Compose a friction intervention dashboard: top 10 friction locations by frequency (a product-team-priority signal — these are the UX bugs the data is telling you about), in-app-help dismiss rate (high = irrelevant help, low = useful), friction-to-resolution rate by intervention touch (which level of escalation actually resolves), severe-tier-to-churn correlation (do users stuck severely actually churn — proves the intervention''s necessity), and journey-attributed activation lift (does this play meaningfully move activation rate). The product team gets a free UX-research stream as a side effect.'
      prompt: 'Compose a friction intervention dashboard: top 10 friction locations by frequency (a product-team-priority signal — these are the UX bugs the data is telling you about), in-app-help dismiss rate (high = irrelevant help, low = useful), friction-to-resolution rate by intervention touch (which level of escalation actually resolves), severe-tier-to-churn correlation (do users stuck severely actually churn — proves the intervention''s necessity), and journey-attributed activation lift (does this play meaningfully move activation rate). The product team gets a free UX-research stream as a side effect.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: agent, type: agent, cardinality: single, description: "AI Agent Scenario produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Friction Point Detected Intervention

## Procedure

1. **Build Friction Detection AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'recent_friction_signal' on the User object, refreshed in real-time. Patterns detected: (a) repeated failed actions on the same UI element (3+ attempts at same form / button within a session); (b) abandoned setup step (started a multi-step flow, didn't complete, didn't return for 24+hrs); (c) error-encountered events without subsequent retry success; (d) help-content visits without subsequent action; (e) rage-click or rapid-back-button patterns. Output: structured object with friction_type, friction_location (where in product), severity (mild / moderate / severe based on time-stuck and repetition), and recommended_intervention. → produces: attribute
2. **Identify Friction-Affected Users** [`create_segment`] — Build a segment 'Active friction signal' capturing users with recent_friction_signal in the last 7 days where severity is moderate or severe. Real-time refresh. Excludes users already in active intervention from this journey (no double-poking). Partitions by friction_location so the journey routes contextually. → produces: segment
3. **Build Contextual In-App Help** [`create_page_content`] — Generate in-app contextual help variants per friction_location. For setup-abandonment: contextual tooltip at the abandoned step with the answer to the common blocker. For repeated-failed-action: floating help bubble with 'Looks like you're stuck — here's what most users do' + GIF or short video. For error-encountered: helpful error explainer rendered where the error appeared. For decision-paralysis (long dwell time on a critical step): comparison guide or recommendation card. Each renders mid-session when the friction is freshest. Tone: helpful colleague, not aggressive sales. → produces: asset
4. **Build Email Fallback Content** [`create_email_content`] — Generate email fallback content sent if the user doesn't engage with the in-app help OR has left the session before help was shown. Variants per friction_location. Format: subject directly addresses the issue ('Stuck on [specific step]? Here's the fix.'), body is a 60-second tutorial (video link or step-by-step screenshots), with a one-click resume-where-you-left-off deep link. Tone: not generic 'we noticed you got stuck' — specific to the exact friction. → produces: asset
5. **Build Agent Handoff Path** [`create_agent`] — Configure an AI agent scenario 'Friction rescue' that engages users with severe friction signal who haven't responded to in-app help OR email. Scenario: agent opens with awareness of the specific friction ('I see you've been working on [step] — happy to help walk through it'), offers to: (a) co-pilot the action with screen-share or step-by-step in chat, (b) escalate to human support if the problem is technical/account-level, (c) flag the friction as a product bug for the engineering queue. Agent NEVER pretends to be human; handoff to human is offered when agent can't resolve in 3 turns. → produces: agent
6. **Build Graduated Rescue Journey** [`create_journey`] — Build a graduated-escalation journey triggered when recent_friction_signal becomes moderate or severe. Touch 1 (mid-session, immediate): in-app contextual help renders at the friction location. Touch 2 (4 hours later, if user left without resolving): email fallback with tutorial + resume-link. Touch 3 (24 hours later, if friction signal still active OR user hasn't returned): trigger agent scenario or, for severe-tier high-value users, create a CSM task for direct outreach. Exit on: friction_signal resolves (user completed the step — success), user explicitly dismisses help 3 times (respect — don't pester), unsubscribe. → produces: journey
7. **Build Friction Intervention Dashboard** [`create_dashboard`] — Compose a friction intervention dashboard: top 10 friction locations by frequency (a product-team-priority signal — these are the UX bugs the data is telling you about), in-app-help dismiss rate (high = irrelevant help, low = useful), friction-to-resolution rate by intervention touch (which level of escalation actually resolves), severe-tier-to-churn correlation (do users stuck severely actually churn — proves the intervention's necessity), and journey-attributed activation lift (does this play meaningfully move activation rate). The product team gets a free UX-research stream as a side effect. → produces: dashboard
