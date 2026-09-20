---
name: pql-signal-to-sdr-task
description: Use when a user mentions "PQL signal to SDR task", "product-qualified lead workflow", "PQL routing", or asks for related help. When a free-tier user crosses a PQL behavioral threshold (feature use, depth, repeated sessions), create an enriched SDR task with the qualification context so the rep has everything needed for first-touch in one click.
arguments: []
intempt:
  id: pql-signal-to-sdr-task
  title: "Product qualified lead to SDR task"
  version: 1.0.0
  slashCommand: /pql-signal-to-sdr-task
  group: Workflows
  shortDescription: "When a free user's behaviour says they are ready for a conversation, it creates an SDR task carrying everything needed for the first touch."
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
    integrations:
      - { value: slack, severity: recommended }
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
      title: "Score free users on behaviour"
      command: create_ai_attribute
      produces: attribute
      bindsAs: pql_score
      description: "A 0 to 100 score weighting the high value activation events most heavily, then depth, meaning sessions in the last 14 days, features touched and time in the product, then how many other people from the same domain are active. 70 and above counts as qualified, refreshed daily and whenever a feature is used."
      prompt: 'Create an AI-derived attribute ''pql_score'' on the User object. Composite signal: (a) high-value feature usage (key activation events) weighted highest; (b) usage depth (sessions in last 14 days, features touched, time-in-product); (c) account-level density (other users from same domain active). Output: numeric score 0-100. Score >= 70 = PQL. Refreshed daily and on feature_used events.'
    - step: 2
      title: "Find free users crossing 70"
      command: create_segment
      produces: segment
      bindsAs: pql_segment
      dependsOn:
      - pql_score
      description: "Free tier users who crossed 70 in the last 7 days with no SDR task open and no outreach in the last 30 days. Paying users and anyone who has opted out are left out."
      prompt: 'Build a segment ''PQL: free users score >= 70'' capturing free-tier users where pql_score crossed 70 in the last 7 days AND no active SDR task exists for this user AND no recent (last 30 days) outreach has occurred. Excludes paid users (different workflow) and users in opt-out list.'
    - step: 3
      title: "Give the SDR the context"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - pql_score
      - pql_segment
      description: "On crossing 70 it enriches the account if needed, gathers the top features used, how often they are in, the company size and the ICP tier, creates a high priority SDR task with that attached, assigns it by territory, then messages the SDR in Slack. Accounts below your ICP threshold go to self serve nurture instead."
      prompt: 'Create a workflow firing when pql_score crosses 70. Step sequence: (1) enrich the user''s account if not already enriched (firmographics, ICP fit); (2) compute outreach context: top features used, usage frequency, account size, ICP fit tier; (3) create a high-priority SDR task with the outreach context attached, assigned via territory rules (geo / industry / account size); (4) post a brief Slack notification to the assigned SDR''s DM with the task link. If account is below ICP threshold, route to self-serve nurture journey instead of SDR queue.'
    - step: 4
      title: "Hold the 24 hour first touch"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - pql_score
      - pql_segment
      - workflow
      description: "How many users cross the threshold each week and the trend, the median time to first contact against a 24 hour target, conversion to meetings and to deals by ICP tier, and a rep leaderboard, with any week where more than 20% go untouched for 48 hours flagged."
      prompt: 'Compose a PQL conversion dashboard: PQL volume (count of free users crossing threshold per week, trend), median time from threshold-cross to first SDR touch (SLA target: <24hr), PQL-to-meeting conversion rate, PQL-to-deal conversion rate by ICP tier, and rep leaderboard (SDRs converting PQLs at the highest rates). Flag any week where >20% of PQLs are untouched after 48 hours.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product qualified lead to SDR task

When a free user's behaviour says they are ready for a conversation, it creates an SDR task carrying everything needed for the first touch.

## Before you run it

- Connect slack
- Send the `feature_used` event
- Send the `session_start` event

## What it does

1. **Score free users on behaviour** (`create_ai_attribute`)

   A 0 to 100 score weighting the high value activation events most heavily, then depth, meaning sessions in the last 14 days, features touched and time in the product, then how many other people from the same domain are active. 70 and above counts as qualified, refreshed daily and whenever a feature is used.

2. **Find free users crossing 70** (`create_segment`)

   Free tier users who crossed 70 in the last 7 days with no SDR task open and no outreach in the last 30 days. Paying users and anyone who has opted out are left out.

3. **Give the SDR the context** (`create_workflow`)

   On crossing 70 it enriches the account if needed, gathers the top features used, how often they are in, the company size and the ICP tier, creates a high priority SDR task with that attached, assigns it by territory, then messages the SDR in Slack. Accounts below your ICP threshold go to self serve nurture instead.

4. **Hold the 24 hour first touch** (`create_dashboard`)

   How many users cross the threshold each week and the trend, the median time to first contact against a 24 hour target, conversion to meetings and to deals by ICP tier, and a rep leaderboard, with any week where more than 20% go untouched for 48 hours flagged.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
