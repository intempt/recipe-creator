---
name: free-to-paid-csm-kickoff
description: Use when a user mentions "free to paid CSM kickoff", "new customer onboarding workflow", "PLG to CS handoff", or asks for related help. When a user converts from free → paid (subscription_created on a previously-free user), create a CSM kickoff task with the user's full pre-conversion activity history and trigger the structured onboarding journey — every paid customer gets a real human handoff.
arguments: []
intempt:
  id: free-to-paid-csm-kickoff
  version: 1.0.0
  slashCommand: /free-to-paid-csm-kickoff
  group: Workflows
  shortDescription: 'When a user converts from free to paid (subscription_created on a previously-free user), create a CSM kickoff task with the user''s full pre-conversion activity history and trigger the structured onboarding journey: every paid customer gets a real human handoff.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [plg-to-cs, csm-handoff, onboarding]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: subscription_created, severity: blocking }
      - { value: user_signed_up, severity: recommended }
  invokesCommands:
    - create_segment
    - create_ai_attribute
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Identify Free-to-Paid Conversions
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Free-to-paid converters - last 7 days' capturing users where subscription_created fired in the last 7 days AND the user previously had subscription_status = free OR trialing (true conversion, not net-new direct-paid signup — those go through a different flow). Excludes users where the subscription is < $50 MRR (consumer-tier; doesn't get CSM motion).
      prompt: Build a segment 'Free-to-paid converters - last 7 days' capturing users where subscription_created fired in the last 7 days AND the user previously had subscription_status = free OR trialing (true conversion, not net-new direct-paid signup — those go through a different flow). Excludes users where the subscription is < $50 MRR (consumer-tier; doesn't get CSM motion).
    - step: 2
      title: Build Activity History Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: preconversion_history
      description: 'Create an AI-derived attribute ''preconversion_history'' on the User object, computed at subscription_created time. Capture: (a) days from signup to paid conversion; (b) features most-used in free period; (c) features NEVER touched (potential expansion drivers later); (d) team-member signal: how many users from the same account are also on free / paid; (e) source: how they got to signup (organic / paid / referral / outbound). This becomes the CSM''s pre-call brief.'
      prompt: 'Create an AI-derived attribute ''preconversion_history'' on the User object, computed at subscription_created time. Capture: (a) days from signup to paid conversion; (b) features most-used in free period; (c) features NEVER touched (potential expansion drivers later); (d) team-member signal: how many users from the same account are also on free / paid; (e) source: how they got to signup (organic / paid / referral / outbound). This becomes the CSM''s pre-call brief.'
    - step: 3
      title: Build CSM Kickoff Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - segment
      - preconversion_history
      description: 'Create a workflow firing on subscription_created for free-to-paid converters. Step sequence: (1) compute preconversion_history attribute; (2) assign CSM via territory + plan-tier rules (enterprise tier gets named CSM, SMB tier gets pooled CSM); (3) create CSM kickoff task with the preconversion history pre-attached, due within 5 business days; (4) trigger the structured onboarding journey (separate recipe) for the user; (5) update account lifecycle to ''new-customer''; (6) post Slack notification to the assigned CSM and a celebration message to #wins.'
      prompt: 'Create a workflow firing on subscription_created for free-to-paid converters. Step sequence: (1) compute preconversion_history attribute; (2) assign CSM via territory + plan-tier rules (enterprise tier gets named CSM, SMB tier gets pooled CSM); (3) create CSM kickoff task with the preconversion history pre-attached, due within 5 business days; (4) trigger the structured onboarding journey (separate recipe) for the user; (5) update account lifecycle to ''new-customer''; (6) post Slack notification to the assigned CSM and a celebration message to #wins.'
    - step: 4
      title: Build PLG Conversion Quality Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - preconversion_history
      - workflow
      description: 'Compose a PLG-to-CS handoff quality dashboard: free-to-paid conversion volume per week, CSM-task completion rate within 5 business days (target: 95%+), median days from signup-to-conversion (PLG funnel speed), and 90-day retention of free-to-paid converters split by ''CSM kickoff completed within 5 days'' vs. ''CSM kickoff missed'' — typically the gap is 15-25 percentage points (the proof-of-value for human CSM motion).'
      prompt: 'Compose a PLG-to-CS handoff quality dashboard: free-to-paid conversion volume per week, CSM-task completion rate within 5 business days (target: 95%+), median days from signup-to-conversion (PLG funnel speed), and 90-day retention of free-to-paid converters split by ''CSM kickoff completed within 5 days'' vs. ''CSM kickoff missed'' — typically the gap is 15-25 percentage points (the proof-of-value for human CSM motion).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Free To Paid Csm Kickoff

## Procedure

1. **Identify Free-to-Paid Conversions** [`create_segment`] — Build a segment 'Free-to-paid converters - last 7 days' capturing users where subscription_created fired in the last 7 days AND the user previously had subscription_status = free OR trialing (true conversion, not net-new direct-paid signup — those go through a different flow). Excludes users where the subscription is < $50 MRR (consumer-tier; doesn't get CSM motion). → produces: segment
2. **Build Activity History Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'preconversion_history' on the User object, computed at subscription_created time. Capture: (a) days from signup to paid conversion; (b) features most-used in free period; (c) features NEVER touched (potential expansion drivers later); (d) team-member signal: how many users from the same account are also on free / paid; (e) source: how they got to signup (organic / paid / referral / outbound). This becomes the CSM's pre-call brief. → produces: attribute
3. **Build CSM Kickoff Workflow** [`create_workflow`] — Create a workflow firing on subscription_created for free-to-paid converters. Step sequence: (1) compute preconversion_history attribute; (2) assign CSM via territory + plan-tier rules (enterprise tier gets named CSM, SMB tier gets pooled CSM); (3) create CSM kickoff task with the preconversion history pre-attached, due within 5 business days; (4) trigger the structured onboarding journey (separate recipe) for the user; (5) update account lifecycle to 'new-customer'; (6) post Slack notification to the assigned CSM and a celebration message to #wins. → produces: workflow
4. **Build PLG Conversion Quality Dashboard** [`create_dashboard`] — Compose a PLG-to-CS handoff quality dashboard: free-to-paid conversion volume per week, CSM-task completion rate within 5 business days (target: 95%+), median days from signup-to-conversion (PLG funnel speed), and 90-day retention of free-to-paid converters split by 'CSM kickoff completed within 5 days' vs. 'CSM kickoff missed' — typically the gap is 15-25 percentage points (the proof-of-value for human CSM motion). → produces: dashboard
