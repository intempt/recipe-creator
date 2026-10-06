---
id: inbound-lead-routing
title: Inbound lead routing
slash_command: /inbound-lead-routing
group: Workflows
owner: intempt
curator: trishik
summary: Enriches and scores every inbound lead, then assigns it by named account, territory or round
  robin so nothing rots in an unassigned queue.
description: >-
  When a new inbound lead arrives (form submission, demo request, signup), enrich + score + assign to
  the right rep based on territory / round-robin / named-account rules, the unglamorous workflow that
  prevents leads from rotting in unassigned queues.
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
    - sales-led
  complexity: advanced
  executionMode: live
  tags:
    - lead-routing
    - round-robin
    - territory
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: form_submitted
      severity: blocking
    - value: user_signed_up
      severity: recommended
touches:
  reads:
    - The form_submitted event in your project
    - The user_signed_up event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Score the lead out of 100"
    - A new workflow, from step 2 "Assign it to the right rep"
    - A new dashboard, from step 3 "Check the balance and the SLA"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score the lead out of 100
    summary: >-
      Up to 40 points for ICP fit on industry, headcount and geography, up to 30 for intent from the form
      type, pricing page views and product activity last week, up to 20 for seniority and how relevant
      the role is, and up to 10 for previous touches on the account. Hot is 70 and up, warm 40 to 69,
      cold below 40.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'lead_score' on the User object. Composite: (a) ICP fit (firmographics
      match (industry, employee count, geo), 0-40 points; (b) intent signal) form type (demo > content
      > newsletter), pricing-page views, last-week product activity, 0-30 points; (c) buyer signal (title
      seniority + role relevance, 0-20 points; (d) brand engagement) prior touchpoints on this account,
      0-10 points. Output: 0-100 score with tier label (hot 70+, warm 40-69, cold <40).
  - id: s2
    title: Assign it to the right rep
    summary: >-
      On a form submission or a signup that is not purely self serve, it enriches the account, scores
      the lead, then applies the routing rules in order: a named account goes to its owner, otherwise
      territory by geography, industry and segment, otherwise round robin inside that territory to keep
      loads even. It creates a task with the context, the score and the reason for the routing, and pings
      the rep in Slack. Cold leads with no named account go to self serve nurture instead of to a person.
    builds: workflow
    description: >-
      Create a workflow firing on form_submitted OR user_signed_up (where source != self-serve-only).
      Step sequence: (1) enrich the account (firmographics, technographics, decision-maker contacts);
      (2) compute lead_score; (3) apply routing rules in priority order: (i) named-account override (if
      account is on target-account list, route to assigned account owner); (ii) territory match (geography,
      industry, segment); (iii) round-robin within territory pool (preserves balanced rep load); (4) create
      task assigned to the determined rep with lead context, score, and routing reason explained; (5)
      post Slack notification to rep; (6) IF score = cold AND no named-account match, route to self-serve
      nurture journey instead of human queue. Use the result of "Score the lead out of 100".
    dependsOn:
      - s1
  - id: s3
    title: Check the balance and the SLA
    summary: >-
      Volume by tier, how evenly leads fall across reps, which should vary by less than 15%, the median
      time from arrival to first contact against two hours for hot and 24 for warm, and conversion per
      tier, with any rep well behind their peers flagged.
    builds: dashboard
    description: >-
      Compose a lead routing performance dashboard: lead volume by tier (hot/warm/cold), routing distribution
      by rep (round-robin balance check: variance should be <15% rep-to-rep), median time from lead-arrival
      to first-touch (SLA: <2hr hot, <24hr warm), tier-conversion: hot-to-meeting / warm-to-meeting /
      cold-to-engaged rates. Flag any rep with significantly worse first-touch SLA than peers. Use the
      result of "Score the lead out of 100", "Assign it to the right rep".
    dependsOn:
      - s1
      - s2
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Inbound lead routing

Enriches and scores every inbound lead, then assigns it by named account, territory or round robin so nothing rots in an unassigned queue.

## Steps

1. **Score the lead out of 100** (builds attribute)

   Up to 40 points for ICP fit on industry, headcount and geography, up to 30 for intent from the form type, pricing page views and product activity last week, up to 20 for seniority and how relevant the role is, and up to 10 for previous touches on the account. Hot is 70 and up, warm 40 to 69, cold below 40.

2. **Assign it to the right rep** (builds workflow)

   On a form submission or a signup that is not purely self serve, it enriches the account, scores the lead, then applies the routing rules in order: a named account goes to its owner, otherwise territory by geography, industry and segment, otherwise round robin inside that territory to keep loads even. It creates a task with the context, the score and the reason for the routing, and pings the rep in Slack. Cold leads with no named account go to self serve nurture instead of to a person.

3. **Check the balance and the SLA** (builds dashboard)

   Volume by tier, how evenly leads fall across reps, which should vary by less than 15%, the median time from arrival to first contact against two hours for hot and 24 for warm, and conversion per tier, with any rep well behind their peers flagged.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The form_submitted event in your project
- The user_signed_up event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Score the lead out of 100"
- A new workflow, from step 2 "Assign it to the right rep"
- A new dashboard, from step 3 "Check the balance and the SLA"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
