---
name: pql-signal-to-sdr-task
description: Use when a user mentions "PQL signal to SDR task", "product-qualified lead workflow", "PQL routing", or asks for related help. When a free-tier user crosses a PQL behavioral threshold (feature use, depth, repeated sessions), create an enriched SDR task with the qualification context so the rep has everything needed for first-touch in one click.
arguments: []
intempt:
  id: pql-signal-to-sdr-task
  version: 1.0.0
  slashCommand: /pql-signal-to-sdr-task
  group: Workflows
  shortDescription: "When a free-tier user crosses a PQL behavioral threshold (feature use, depth, repeated sessions), create an enriched SDR task with the qualification context so the rep has everything needed for first-touch in one click."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [pql, sdr-routing, product-led-growth]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: feature_used, severity: blocking }
      - { value: session_start, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Compute PQL Score
      command: create_ai_attribute
      produces: attribute
      bindsAs: pql_score
      description: 'Create an AI-derived attribute ''pql_score'' on the User object. Composite signal: (a) high-value feature usage (key activation events) weighted highest; (b) usage depth (sessions in last 14 days, features touched, time-in-product); (c) account-level density (other users from same domain active). Output: numeric score 0-100. Score >= 70 = PQL. Refreshed daily and on feature_used events.'
      prompt: 'Create an AI-derived attribute ''pql_score'' on the User object. Composite signal: (a) high-value feature usage (key activation events) weighted highest; (b) usage depth (sessions in last 14 days, features touched, time-in-product); (c) account-level density (other users from same domain active). Output: numeric score 0-100. Score >= 70 = PQL. Refreshed daily and on feature_used events.'
    - step: 2
      title: Identify PQL Cohort
      command: create_segment
      produces: segment
      bindsAs: pql_segment
      dependsOn:
      - pql_score
      description: 'Build a segment ''PQL: free users score >= 70'' capturing free-tier users where pql_score crossed 70 in the last 7 days AND no active SDR task exists for this user AND no recent (last 30 days) outreach has occurred. Excludes paid users (different workflow) and users in opt-out list.'
      prompt: 'Build a segment ''PQL: free users score >= 70'' capturing free-tier users where pql_score crossed 70 in the last 7 days AND no active SDR task exists for this user AND no recent (last 30 days) outreach has occurred. Excludes paid users (different workflow) and users in opt-out list.'
    - step: 3
      title: Build PQL Task Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - pql_score
      - pql_segment
      description: 'Create a workflow firing when pql_score crosses 70. Step sequence: (1) enrich the user''s account if not already enriched (firmographics, ICP fit); (2) compute outreach context: top features used, usage frequency, account size, ICP fit tier; (3) create a high-priority SDR task with the outreach context attached, assigned via territory rules (geo / industry / account size); (4) post a brief Slack notification to the assigned SDR''s DM with the task link. If account is below ICP threshold, route to self-serve nurture journey instead of SDR queue.'
      prompt: 'Create a workflow firing when pql_score crosses 70. Step sequence: (1) enrich the user''s account if not already enriched (firmographics, ICP fit); (2) compute outreach context: top features used, usage frequency, account size, ICP fit tier; (3) create a high-priority SDR task with the outreach context attached, assigned via territory rules (geo / industry / account size); (4) post a brief Slack notification to the assigned SDR''s DM with the task link. If account is below ICP threshold, route to self-serve nurture journey instead of SDR queue.'
    - step: 4
      title: Build PQL Conversion Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - pql_score
      - pql_segment
      - workflow
      description: 'Compose a PQL conversion dashboard: PQL volume (count of free users crossing threshold per week, trend), median time from threshold-cross to first SDR touch (SLA target: <24hr), PQL-to-meeting conversion rate, PQL-to-deal conversion rate by ICP tier, and rep leaderboard (SDRs converting PQLs at the highest rates). Flag any week where >20% of PQLs are untouched after 48 hours.'
      prompt: 'Compose a PQL conversion dashboard: PQL volume (count of free users crossing threshold per week, trend), median time from threshold-cross to first SDR touch (SLA target: <24hr), PQL-to-meeting conversion rate, PQL-to-deal conversion rate by ICP tier, and rep leaderboard (SDRs converting PQLs at the highest rates). Flag any week where >20% of PQLs are untouched after 48 hours.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Pql Signal To Sdr Task

## Procedure

1. **Compute PQL Score** [`create_ai_attribute`] — Create an AI-derived attribute 'pql_score' on the User object. Composite signal: (a) high-value feature usage (key activation events) weighted highest; (b) usage depth (sessions in last 14 days, features touched, time-in-product); (c) account-level density (other users from same domain active). Output: numeric score 0-100. Score >= 70 = PQL. Refreshed daily and on feature_used events. → produces: attribute
2. **Identify PQL Cohort** [`create_segment`] — Build a segment 'PQL: free users score >= 70' capturing free-tier users where pql_score crossed 70 in the last 7 days AND no active SDR task exists for this user AND no recent (last 30 days) outreach has occurred. Excludes paid users (different workflow) and users in opt-out list. → produces: segment
3. **Build PQL Task Workflow** [`create_workflow`] — Create a workflow firing when pql_score crosses 70. Step sequence: (1) enrich the user's account if not already enriched (firmographics, ICP fit); (2) compute outreach context: top features used, usage frequency, account size, ICP fit tier; (3) create a high-priority SDR task with the outreach context attached, assigned via territory rules (geo / industry / account size); (4) post a brief Slack notification to the assigned SDR's DM with the task link. If account is below ICP threshold, route to self-serve nurture journey instead of SDR queue. → produces: workflow
4. **Build PQL Conversion Dashboard** [`create_dashboard`] — Compose a PQL conversion dashboard: PQL volume (count of free users crossing threshold per week, trend), median time from threshold-cross to first SDR touch (SLA target: <24hr), PQL-to-meeting conversion rate, PQL-to-deal conversion rate by ICP tier, and rep leaderboard (SDRs converting PQLs at the highest rates). Flag any week where >20% of PQLs are untouched after 48 hours. → produces: dashboard
