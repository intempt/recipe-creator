---
name: inbound-lead-routing
description: Use when a user mentions "inbound lead routing", "lead assignment workflow", "round-robin SDR", or asks for related help. When a new inbound lead arrives (form submission, demo request, signup), enrich + score + assign to the right rep based on territory / round-robin / named-account rules — the unglamorous workflow that prevents leads from rotting in unassigned queues.
arguments: []
intempt:
  id: inbound-lead-routing
  version: 1.0.0
  slashCommand: /inbound-lead-routing
  group: Workflows
  shortDescription: "When a new inbound lead arrives (form submission, demo request, signup), enrich + score + assign to the right rep based on territory / round-robin / named-account rules — the unglamorous workflow that prevents leads from rotting in unassigned queues."
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
    events:
      - { value: form_submitted, severity: blocking }
      - { value: user_signed_up, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Compute Lead Score
      command: create_ai_attribute
      produces: attribute
      bindsAs: lead_score
      description: 'Create an AI-derived attribute ''lead_score'' on the User object. Composite: (a) ICP fit — firmographics match (industry, employee count, geo), 0-40 points; (b) intent signal — form type (demo > content > newsletter), pricing-page views, last-week product activity, 0-30 points; (c) buyer signal — title seniority + role relevance, 0-20 points; (d) brand engagement — prior touchpoints on this account, 0-10 points. Output: 0-100 score with tier label (hot 70+, warm 40-69, cold <40).'
      prompt: 'Create an AI-derived attribute ''lead_score'' on the User object. Composite: (a) ICP fit — firmographics match (industry, employee count, geo), 0-40 points; (b) intent signal — form type (demo > content > newsletter), pricing-page views, last-week product activity, 0-30 points; (c) buyer signal — title seniority + role relevance, 0-20 points; (d) brand engagement — prior touchpoints on this account, 0-10 points. Output: 0-100 score with tier label (hot 70+, warm 40-69, cold <40).'
    - step: 2
      title: Build Lead Routing Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - lead_score
      description: 'Create a workflow firing on form_submitted OR user_signed_up (where source != self-serve-only). Step sequence: (1) enrich the account (firmographics, technographics, decision-maker contacts); (2) compute lead_score; (3) apply routing rules in priority order: (i) named-account override (if account is on target-account list, route to assigned account owner); (ii) territory match (geography, industry, segment); (iii) round-robin within territory pool (preserves balanced rep load); (4) create task assigned to the determined rep with lead context, score, and routing reason explained; (5) post Slack notification to rep; (6) IF score = cold AND no named-account match, route to self-serve nurture journey instead of human queue.'
      prompt: 'Create a workflow firing on form_submitted OR user_signed_up (where source != self-serve-only). Step sequence: (1) enrich the account (firmographics, technographics, decision-maker contacts); (2) compute lead_score; (3) apply routing rules in priority order: (i) named-account override (if account is on target-account list, route to assigned account owner); (ii) territory match (geography, industry, segment); (iii) round-robin within territory pool (preserves balanced rep load); (4) create task assigned to the determined rep with lead context, score, and routing reason explained; (5) post Slack notification to rep; (6) IF score = cold AND no named-account match, route to self-serve nurture journey instead of human queue.'
    - step: 3
      title: Build Routing Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - lead_score
      - workflow
      description: 'Compose a lead routing performance dashboard: lead volume by tier (hot/warm/cold), routing distribution by rep (round-robin balance check — variance should be <15% rep-to-rep), median time from lead-arrival to first-touch (SLA: <2hr hot, <24hr warm), tier-conversion: hot-to-meeting / warm-to-meeting / cold-to-engaged rates. Flag any rep with significantly worse first-touch SLA than peers.'
      prompt: 'Compose a lead routing performance dashboard: lead volume by tier (hot/warm/cold), routing distribution by rep (round-robin balance check — variance should be <15% rep-to-rep), median time from lead-arrival to first-touch (SLA: <2hr hot, <24hr warm), tier-conversion: hot-to-meeting / warm-to-meeting / cold-to-engaged rates. Flag any rep with significantly worse first-touch SLA than peers.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Inbound Lead Routing

## Procedure

1. **Compute Lead Score** [`create_ai_attribute`] — Create an AI-derived attribute 'lead_score' on the User object. Composite: (a) ICP fit — firmographics match (industry, employee count, geo), 0-40 points; (b) intent signal — form type (demo > content > newsletter), pricing-page views, last-week product activity, 0-30 points; (c) buyer signal — title seniority + role relevance, 0-20 points; (d) brand engagement — prior touchpoints on this account, 0-10 points. Output: 0-100 score with tier label (hot 70+, warm 40-69, cold <40). → produces: attribute
2. **Build Lead Routing Workflow** [`create_workflow`] — Create a workflow firing on form_submitted OR user_signed_up (where source != self-serve-only). Step sequence: (1) enrich the account (firmographics, technographics, decision-maker contacts); (2) compute lead_score; (3) apply routing rules in priority order: (i) named-account override (if account is on target-account list, route to assigned account owner); (ii) territory match (geography, industry, segment); (iii) round-robin within territory pool (preserves balanced rep load); (4) create task assigned to the determined rep with lead context, score, and routing reason explained; (5) post Slack notification to rep; (6) IF score = cold AND no named-account match, route to self-serve nurture journey instead of human queue. → produces: workflow
3. **Build Routing Performance Dashboard** [`create_dashboard`] — Compose a lead routing performance dashboard: lead volume by tier (hot/warm/cold), routing distribution by rep (round-robin balance check — variance should be <15% rep-to-rep), median time from lead-arrival to first-touch (SLA: <2hr hot, <24hr warm), tier-conversion: hot-to-meeting / warm-to-meeting / cold-to-engaged rates. Flag any rep with significantly worse first-touch SLA than peers. → produces: dashboard
