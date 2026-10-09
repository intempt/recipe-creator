---
name: free-to-paid-csm-kickoff
description: Use when a user mentions "free to paid CSM kickoff", "new customer onboarding workflow", "PLG to CS handoff", or asks for related help. When a user converts from free to paid (Subscription started on a previously-free user), create a CSM kickoff task with the user's full pre-conversion activity history and trigger the structured onboarding journey, every paid customer gets a real human handoff.
arguments: []
intempt:
  id: free-to-paid-csm-kickoff
  title: "Free to paid CSM kickoff"
  version: 1.0.0
  slashCommand: /free-to-paid-csm-kickoff
  group: Workflows
  shortDescription: "Every upgrade from free to paid creates a CSM kickoff task carrying the customer's whole free period history, due inside five working days."
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
      title: "Find genuine upgrades"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "People who started paying in the last 7 days and were free or trialing before, so not net new direct purchases. Subscriptions under $50 a month are left out, because they do not get a CSM."
      prompt: Build a segment 'Free-to-paid converters - last 7 days' capturing users where Subscription started fired in the last 7 days AND the user previously had subscription status = free OR trialing (true conversion, not net-new direct-paid signup, those go through a different flow). Excludes users where the subscription is < $50 MRR (consumer-tier; doesn't get CSM motion).
    - step: 2
      title: "Write the pre call brief"
      command: create_ai_attribute
      produces: attribute
      bindsAs: preconversion_history
      description: "Built the moment they upgrade: how many days from signup to paying, the features they leaned on while free, the ones they never opened, which become the expansion candidates later, how many other people at their account are free or paid, and how they arrived, whether organic, paid, referral or outbound."
      prompt: 'Create an AI-derived attribute ''preconversion history'' on the User object, computed when the subscription starts. Capture: (a) days from signup to paid conversion; (b) features most-used in free period; (c) features NEVER touched (potential expansion drivers later); (d) team-member signal: how many users from the same account are also on free / paid; (e) source: how they got to signup (organic / paid / referral / outbound). This becomes the CSM''s pre-call brief.'
    - step: 3
      title: "Assign a CSM and kick off"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - segment
      - preconversion_history
      description: "On the upgrade it builds the brief, assigns a CSM by territory and plan, named for enterprise and pooled for SMB, creates the kickoff task with the brief attached and due within five working days, starts the onboarding journey, moves the account to new customer, and posts to the CSM and to the wins channel."
      prompt: 'Create a workflow firing on Subscription started for free-to-paid converters. Step sequence: (1) compute the preconversion history attribute; (2) assign CSM via territory + plan-tier rules (enterprise tier gets named CSM, SMB tier gets pooled CSM); (3) create CSM kickoff task with the preconversion history pre-attached, due within 5 business days; (4) trigger the structured onboarding journey (separate recipe) for the user; (5) update account lifecycle to ''new-customer''; (6) post Slack notification to the assigned CSM and a celebration message to #wins.'
    - step: 4
      title: "Prove the handoff matters"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - preconversion_history
      - workflow
      description: "Upgrades per week, how many kickoff tasks are done inside five working days against a 95% target, the median time from signup to paying, and 90 day retention for customers whose kickoff happened on time against those it did not, where the gap is usually 15 to 25 points."
      prompt: 'Compose a PLG-to-CS handoff quality dashboard: free-to-paid conversion volume per week, CSM-task completion rate within 5 business days (target: 95%+), median days from signup-to-conversion (PLG funnel speed), and 90-day retention of free-to-paid converters split by ''CSM kickoff completed within 5 days'' vs. ''CSM kickoff missed'': typically the gap is 15-25 percentage points (the proof-of-value for human CSM motion).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Free to paid CSM kickoff

Every upgrade from free to paid creates a CSM kickoff task carrying the customer's whole free period history, due inside five working days.

## Before you run it

- Connect slack
- Send the `subscription_created` event
- Send the `user_signed_up` event

## What it does

1. **Find genuine upgrades** (`create_segment`)

   People who started paying in the last 7 days and were free or trialing before, so not net new direct purchases. Subscriptions under $50 a month are left out, because they do not get a CSM.

2. **Write the pre call brief** (`create_ai_attribute`)

   Built the moment they upgrade: how many days from signup to paying, the features they leaned on while free, the ones they never opened, which become the expansion candidates later, how many other people at their account are free or paid, and how they arrived, whether organic, paid, referral or outbound.

3. **Assign a CSM and kick off** (`create_workflow`)

   On the upgrade it builds the brief, assigns a CSM by territory and plan, named for enterprise and pooled for SMB, creates the kickoff task with the brief attached and due within five working days, starts the onboarding journey, moves the account to new customer, and posts to the CSM and to the wins channel.

4. **Prove the handoff matters** (`create_dashboard`)

   Upgrades per week, how many kickoff tasks are done inside five working days against a 95% target, the median time from signup to paying, and 90 day retention for customers whose kickoff happened on time against those it did not, where the gap is usually 15 to 25 points.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
