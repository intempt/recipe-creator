---
id: enterprise-domain-signup-to-ae-task
title: Enterprise signup to AE task
slash_command: /enterprise-domain-signup-to-ae-task
group: Workflows
owner: intempt
curator: trishik
summary: Spots when a self serve signup comes from a large company, enriches it, and puts it in front
  of an AE instead of leaving it in the free funnel.
description: >-
  When a self-serve signup comes from an enterprise-tier domain (Fortune 500, target-account list, or
  domain matching ICP), immediately create an AE task with full account enrichment, don't let an enterprise
  lead languish in the standard free-tier funnel.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
  vertical:
    - plg
    - sales-led
  complexity: advanced
  executionMode: live
  tags:
    - enterprise-lead
    - domain-detection
    - ae-routing
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: user_signed_up
      severity: blocking
touches:
  reads:
    - The user_signed_up event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Work out the account tier"
    - A new segment, from step 2 "Find enterprise signups with no AE"
    - A new workflow, from step 3 "Hand it to the right AE"
    - A new dashboard, from step 4 "Watch the response time"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Work out the account tier
    summary: >-
      From the email domain at signup: enterprise, mid market, SMB or consumer. It checks the target account
      list, headcount where enrichment has it, with 1000 and up enterprise and 100 to 1000 mid market,
      whether the company is publicly listed, and whether the industry matches your ICP. Gmail and the
      like are treated as consumer.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'account_tier' on the Account object. Computed at signup from email
      domain. Output: enterprise / mid-market / smb / consumer (generic email). Logic: cross-reference
      against (a) target-account list, (b) employee-count enrichment if available (1000+ = enterprise,
      100-1000 = mid-market), (c) public-company indicator, (d) ICP industry match. Generic email domains
      (gmail, outlook) to tier: consumer (likely not a buyer).
  - id: s2
    title: Find enterprise signups with no AE
    summary: >-
      Enterprise tier accounts created in the last 30 days that still have nobody assigned, used both
      to audit the workflow and to look back at how enterprise leads convert.
    builds: segment
    description: >-
      Build a segment 'Enterprise signups - last 30 days' capturing accounts where account_tier = enterprise
      AND the account was created in last 30 days AND no AE has been assigned. Used for both the workflow
      audit and post-hoc analysis of enterprise-lead conversion. Use the result of "Work out the account
      tier".
    dependsOn:
      - s1
  - id: s3
    title: Hand it to the right AE
    summary: >-
      On signup it works out the tier, and for enterprise or mid market it enriches firmographics, decision
      makers and tech stack, checks whether the account is already in the CRM or on the target list, creates
      a high priority AE task assigned by territory and named account rules, keeps any existing owner,
      posts to the enterprise alerts channel with the context, and takes the user out of self serve nurture,
      because this is a sales led motion.
    builds: workflow
    description: >-
      Create a workflow firing on user_signed_up. Step sequence: (1) compute account_tier from the email
      domain; (2) if tier = enterprise or mid-market: immediately enrich (firmographics, decision-makers,
      tech stack); (3) check whether the account is already in the CRM or part of target-account list;
      (4) create an enterprise-tier AE task with priority HIGH, assigned by territory + named-account
      rules (preserving any pre-assigned account owner); (5) post a high-visibility Slack alert to #enterprise-alerts
      with account context, decision-maker contacts, and current product activity; (6) suppress this user
      from the standard self-serve nurture journey (different motion for enterprise: sales-led, not marketing-led).
      Use the result of "Work out the account tier", "Find enterprise signups with no AE".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Watch the response time
    summary: >-
      Enterprise signups per week, AE response time against a two hour target in business hours, how many
      turn into meetings and into deals, which usually takes over 60 days, the pipeline sourced this way,
      and the tier mix across all signups.
    builds: dashboard
    description: >-
      Compose an enterprise-lead dashboard: enterprise signup volume per week, AE response time (target:
      <2hr business hours), enterprise-signup-to-meeting conversion, enterprise-signup-to-deal conversion
      (typically takes 60+ days), enterprise pipeline value sourced this way (separate from outbound),
      and account-tier mix (enterprise / mid-market / smb / consumer) of all signups so leadership can
      see ICP attraction trends. Use the result of "Work out the account tier", "Find enterprise signups
      with no AE", "Hand it to the right AE".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
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

# Enterprise signup to AE task

Spots when a self serve signup comes from a large company, enriches it, and puts it in front of an AE instead of leaving it in the free funnel.

## Steps

1. **Work out the account tier** (builds attribute)

   From the email domain at signup: enterprise, mid market, SMB or consumer. It checks the target account list, headcount where enrichment has it, with 1000 and up enterprise and 100 to 1000 mid market, whether the company is publicly listed, and whether the industry matches your ICP. Gmail and the like are treated as consumer.

2. **Find enterprise signups with no AE** (builds segment)

   Enterprise tier accounts created in the last 30 days that still have nobody assigned, used both to audit the workflow and to look back at how enterprise leads convert.

3. **Hand it to the right AE** (builds workflow)

   On signup it works out the tier, and for enterprise or mid market it enriches firmographics, decision makers and tech stack, checks whether the account is already in the CRM or on the target list, creates a high priority AE task assigned by territory and named account rules, keeps any existing owner, posts to the enterprise alerts channel with the context, and takes the user out of self serve nurture, because this is a sales led motion.

4. **Watch the response time** (builds dashboard)

   Enterprise signups per week, AE response time against a two hour target in business hours, how many turn into meetings and into deals, which usually takes over 60 days, the pipeline sourced this way, and the tier mix across all signups.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The user_signed_up event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Work out the account tier"
- A new segment, from step 2 "Find enterprise signups with no AE"
- A new workflow, from step 3 "Hand it to the right AE"
- A new dashboard, from step 4 "Watch the response time"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
