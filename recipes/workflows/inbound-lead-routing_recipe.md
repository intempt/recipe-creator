---
name: inbound-lead-routing
description: Use when a user mentions "inbound lead routing", "lead assignment workflow", "round-robin SDR", or asks for related help. When a new inbound lead arrives (form submission, demo request, signup), enrich + score + assign to the right rep based on territory / round-robin / named-account rules, the unglamorous workflow that prevents leads from rotting in unassigned queues.
arguments: []
intempt:
  id: inbound-lead-routing
  title: "Inbound lead routing"
  version: 1.0.0
  slashCommand: /inbound-lead-routing
  group: Workflows
  shortDescription: "Enriches and scores every inbound lead, then assigns it by named account, territory or round robin so nothing rots in an unassigned queue."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [lead-routing, round-robin, territory]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: form_submitted, severity: blocking }
      - { value: user_signed_up, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Score the lead out of 100"
      command: create_ai_attribute
      produces: attribute
      bindsAs: lead_score
      description: "Up to 40 points for ICP fit on industry, headcount and geography, up to 30 for intent from the form type, pricing page views and product activity last week, up to 20 for seniority and how relevant the role is, and up to 10 for previous touches on the account. Hot is 70 and up, warm 40 to 69, cold below 40."
      prompt: 'Create an AI-derived attribute ''lead score'' on the User object. Composite: (a) ICP fit (firmographics match (industry, employee count, geo), 0-40 points; (b) intent signal) form type (demo > content > newsletter), pricing-page views, last-week product activity, 0-30 points; (c) buyer signal (title seniority + role relevance, 0-20 points; (d) brand engagement) prior touchpoints on this account, 0-10 points. Output: 0-100 score with tier label (hot 70+, warm 40-69, cold <40).'
    - step: 2
      title: "Assign it to the right rep"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - lead_score
      description: "On a form submission or a signup that is not purely self serve, it enriches the account, scores the lead, then applies the routing rules in order: a named account goes to its owner, otherwise territory by geography, industry and segment, otherwise round robin inside that territory to keep loads even. It creates a task with the context, the score and the reason for the routing, and pings the rep in Slack. Cold leads with no named account go to self serve nurture instead of to a person."
      prompt: 'Create a workflow firing on Form submitted OR User signed up (where source != self-serve-only). Step sequence: (1) enrich the account (firmographics, technographics, decision-maker contacts); (2) compute the lead score; (3) apply routing rules in priority order: (i) named-account override (if account is on target-account list, route to assigned account owner); (ii) territory match (geography, industry, segment); (iii) round-robin within territory pool (preserves balanced rep load); (4) create task assigned to the determined rep with lead context, score, and routing reason explained; (5) post Slack notification to rep; (6) IF score = cold AND no named-account match, route to self-serve nurture journey instead of human queue.'
    - step: 3
      title: "Check the balance and the SLA"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - lead_score
      - workflow
      description: "Volume by tier, how evenly leads fall across reps, which should vary by less than 15%, the median time from arrival to first contact against two hours for hot and 24 for warm, and conversion per tier, with any rep well behind their peers flagged."
      prompt: 'Compose a lead routing performance dashboard: lead volume by tier (hot/warm/cold), routing distribution by rep (round-robin balance check: variance should be <15% rep-to-rep), median time from lead-arrival to first-touch (SLA: <2hr hot, <24hr warm), tier-conversion: hot-to-meeting / warm-to-meeting / cold-to-engaged rates. Flag any rep with significantly worse first-touch SLA than peers.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Inbound lead routing

Enriches and scores every inbound lead, then assigns it by named account, territory or round robin so nothing rots in an unassigned queue.

## Before you run it

- Connect slack
- Send the `form_submitted` event
- Send the `user_signed_up` event

## What it does

1. **Score the lead out of 100** (`create_ai_attribute`)

   Up to 40 points for ICP fit on industry, headcount and geography, up to 30 for intent from the form type, pricing page views and product activity last week, up to 20 for seniority and how relevant the role is, and up to 10 for previous touches on the account. Hot is 70 and up, warm 40 to 69, cold below 40.

2. **Assign it to the right rep** (`create_workflow`)

   On a form submission or a signup that is not purely self serve, it enriches the account, scores the lead, then applies the routing rules in order: a named account goes to its owner, otherwise territory by geography, industry and segment, otherwise round robin inside that territory to keep loads even. It creates a task with the context, the score and the reason for the routing, and pings the rep in Slack. Cold leads with no named account go to self serve nurture instead of to a person.

3. **Check the balance and the SLA** (`create_dashboard`)

   Volume by tier, how evenly leads fall across reps, which should vary by less than 15%, the median time from arrival to first contact against two hours for hot and 24 for warm, and conversion per tier, with any rep well behind their peers flagged.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
