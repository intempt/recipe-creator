---
id: free-to-paid-csm-kickoff
title: Free to paid CSM kickoff
slash_command: /free-to-paid-csm-kickoff
group: Workflows
owner: intempt
summary: Every upgrade from free to paid creates a CSM kickoff task carrying the customer's whole free
  period history, due inside five working days.
description: >-
  When a user converts from free to paid (subscription_created on a previously-free user), create a CSM
  kickoff task with the user's full pre-conversion activity history and trigger the structured onboarding
  journey, every paid customer gets a real human handoff.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - saas
  complexity: standard
  executionMode: live
  tags:
    - plg-to-cs
    - csm-handoff
    - onboarding
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: subscription_created
      severity: blocking
    - value: user_signed_up
      severity: recommended
steps:
  - id: s1
    title: Find genuine upgrades
    summary: >-
      People who started paying in the last 7 days and were free or trialing before, so not net new direct
      purchases. Subscriptions under $50 a month are left out, because they do not get a CSM.
    builds: segment
    description: >-
      Build a segment 'Free-to-paid converters - last 7 days' capturing users where subscription_created
      fired in the last 7 days AND the user previously had subscription_status = free OR trialing (true
      conversion, not net-new direct-paid signup, those go through a different flow). Excludes users where
      the subscription is < $50 MRR (consumer-tier; doesn't get CSM motion).
  - id: s2
    title: Write the pre call brief
    summary: >-
      Built the moment they upgrade: how many days from signup to paying, the features they leaned on
      while free, the ones they never opened, which become the expansion candidates later, how many other
      people at their account are free or paid, and how they arrived, whether organic, paid, referral
      or outbound.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'preconversion_history' on the User object, computed at subscription_created
      time. Capture: (a) days from signup to paid conversion; (b) features most-used in free period; (c)
      features NEVER touched (potential expansion drivers later); (d) team-member signal: how many users
      from the same account are also on free / paid; (e) source: how they got to signup (organic / paid
      / referral / outbound). This becomes the CSM's pre-call brief.
  - id: s3
    title: Assign a CSM and kick off
    summary: >-
      On the upgrade it builds the brief, assigns a CSM by territory and plan, named for enterprise and
      pooled for SMB, creates the kickoff task with the brief attached and due within five working days,
      starts the onboarding journey, moves the account to new customer, and posts to the CSM and to the
      wins channel.
    builds: workflow
    description: >-
      Create a workflow firing on subscription_created for free-to-paid converters. Step sequence: (1)
      compute preconversion_history attribute; (2) assign CSM via territory + plan-tier rules (enterprise
      tier gets named CSM, SMB tier gets pooled CSM); (3) create CSM kickoff task with the preconversion
      history pre-attached, due within 5 business days; (4) trigger the structured onboarding journey
      (separate recipe) for the user; (5) update account lifecycle to 'new-customer'; (6) post Slack notification
      to the assigned CSM and a celebration message to #wins. Use the result of "Find genuine upgrades",
      "Write the pre call brief".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Prove the handoff matters
    summary: >-
      Upgrades per week, how many kickoff tasks are done inside five working days against a 95% target,
      the median time from signup to paying, and 90 day retention for customers whose kickoff happened
      on time against those it did not, where the gap is usually 15 to 25 points.
    builds: dashboard
    description: >-
      Compose a PLG-to-CS handoff quality dashboard: free-to-paid conversion volume per week, CSM-task
      completion rate within 5 business days (target: 95%+), median days from signup-to-conversion (PLG
      funnel speed), and 90-day retention of free-to-paid converters split by 'CSM kickoff completed within
      5 days' vs. 'CSM kickoff missed': typically the gap is 15-25 percentage points (the proof-of-value
      for human CSM motion). Use the result of "Find genuine upgrades", "Write the pre call brief", "Assign
      a CSM and kick off".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: attribute
    producedByStep: s2
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Free to paid CSM kickoff

Every upgrade from free to paid creates a CSM kickoff task carrying the customer's whole free period history, due inside five working days.

## Steps

1. **Find genuine upgrades** (builds segment)

   People who started paying in the last 7 days and were free or trialing before, so not net new direct purchases. Subscriptions under $50 a month are left out, because they do not get a CSM.

2. **Write the pre call brief** (builds attribute)

   Built the moment they upgrade: how many days from signup to paying, the features they leaned on while free, the ones they never opened, which become the expansion candidates later, how many other people at their account are free or paid, and how they arrived, whether organic, paid, referral or outbound.

3. **Assign a CSM and kick off** (builds workflow)

   On the upgrade it builds the brief, assigns a CSM by territory and plan, named for enterprise and pooled for SMB, creates the kickoff task with the brief attached and due within five working days, starts the onboarding journey, moves the account to new customer, and posts to the CSM and to the wins channel.

4. **Prove the handoff matters** (builds dashboard)

   Upgrades per week, how many kickoff tasks are done inside five working days against a 95% target, the median time from signup to paying, and 90 day retention for customers whose kickoff happened on time against those it did not, where the gap is usually 15 to 25 points.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
