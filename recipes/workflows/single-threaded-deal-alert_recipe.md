---
name: single-threaded-deal-alert
description: Use when a user mentions "single-threaded deal", "multi-threading task", "lone champion detection", or asks for related help. Detect deals where only one contact from the buyer side is engaged — single-threaded deals lose 3x more often when the lone champion leaves or doesn't have authority. Surface them with a multi-threading task and a recommended contact list.
arguments: []
intempt:
  id: single-threaded-deal-alert
  version: 1.0.0
  slashCommand: /single-threaded-deal-alert
  group: Workflows
  shortDescription: "Create a Deal threading_depth AI attribute and a segment of open mid/late-stage deals with exactly one engaged buyer contact, then trigger a multi-threading task workflow."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [multi-threading, deal-health]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: deal_stage_changed, severity: recommended }
      - { value: meeting_completed, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Compute Threading Depth
      command: create_ai_attribute
      produces: attribute
      bindsAs: threading
      description: 'Create an AI-derived attribute ''threading_depth'' on the Deal object. Count distinct buyer-side contacts who have (a) attended a meeting on this deal, OR (b) replied to an email on this deal, OR (c) been explicitly added as a deal contact. Output: integer count. Flag as ''single-threaded'' if count = 1 and deal is in Demo / Proposal / Closing stage (early-stage single-threading is normal; late-stage is a red flag).'
      prompt: 'Create an AI-derived attribute ''threading_depth'' on the Deal object. Count distinct buyer-side contacts who have (a) attended a meeting on this deal, OR (b) replied to an email on this deal, OR (c) been explicitly added as a deal contact. Output: integer count. Flag as ''single-threaded'' if count = 1 and deal is in Demo / Proposal / Closing stage (early-stage single-threading is normal; late-stage is a red flag).'
    - step: 2
      title: Identify Single-Threaded Deals
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - threading
      description: Build a segment 'Single-threaded deals - mid+ stage' capturing open deals where threading_depth = 1 AND stage is Demo, Proposal, or Closing. Excludes deals < 14 days old (haven't had time for multi-threading naturally) and deals flagged as exec-buyer (1-person decision is genuine in some buyer profiles — e.g. founder-led SMB).
      prompt: Build a segment 'Single-threaded deals - mid+ stage' capturing open deals where threading_depth = 1 AND stage is Demo, Proposal, or Closing. Excludes deals < 14 days old (haven't had time for multi-threading naturally) and deals flagged as exec-buyer (1-person decision is genuine in some buyer profiles — e.g. founder-led SMB).
    - step: 3
      title: Build Multi-Threading Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - threading
      - segment
      description: 'Create a workflow firing daily for deals newly-flagged as single-threaded. Step sequence: (1) recompute threading_depth (fresh); (2) for genuine single-threaded mid-stage deals, fetch suggested additional contacts from account enrichment (peer roles, manager up, related team members), prioritized by likely-buying-influence; (3) create a task for the rep labeled ''Multi-thread this deal: 3 suggested contacts'' with the contact list pre-attached; (4) Slack DM to the rep with deal context. If lone champion is the decision-maker (CEO of a small co, etc.), suppress — that''s not single-threading risk.'
      prompt: 'Create a workflow firing daily for deals newly-flagged as single-threaded. Step sequence: (1) recompute threading_depth (fresh); (2) for genuine single-threaded mid-stage deals, fetch suggested additional contacts from account enrichment (peer roles, manager up, related team members), prioritized by likely-buying-influence; (3) create a task for the rep labeled ''Multi-thread this deal: 3 suggested contacts'' with the contact list pre-attached; (4) Slack DM to the rep with deal context. If lone champion is the decision-maker (CEO of a small co, etc.), suppress — that''s not single-threading risk.'
    - step: 4
      title: Build Threading Health Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - threading
      - segment
      - workflow
      description: 'Compose a threading health dashboard: % of mid+stage deals that are multi-threaded (target: 70%+; below 50% is a coaching gap), distribution of threading depth by stage, single-threaded-deal win rate vs. multi-threaded win rate (the proof-of-value chart), rep leaderboard on threading depth, and aged single-threaded deals (>30 days single-threaded = high-loss-risk pile).'
      prompt: 'Compose a threading health dashboard: % of mid+stage deals that are multi-threaded (target: 70%+; below 50% is a coaching gap), distribution of threading depth by stage, single-threaded-deal win rate vs. multi-threaded win rate (the proof-of-value chart), rep leaderboard on threading depth, and aged single-threaded deals (>30 days single-threaded = high-loss-risk pile).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Single Threaded Deal Alert

## Procedure

1. **Compute Threading Depth** [`create_ai_attribute`] — Create an AI-derived attribute 'threading_depth' on the Deal object. Count distinct buyer-side contacts who have (a) attended a meeting on this deal, OR (b) replied to an email on this deal, OR (c) been explicitly added as a deal contact. Output: integer count. Flag as 'single-threaded' if count = 1 and deal is in Demo / Proposal / Closing stage (early-stage single-threading is normal; late-stage is a red flag). → produces: attribute
2. **Identify Single-Threaded Deals** [`create_segment`] — Build a segment 'Single-threaded deals - mid+ stage' capturing open deals where threading_depth = 1 AND stage is Demo, Proposal, or Closing. Excludes deals < 14 days old (haven't had time for multi-threading naturally) and deals flagged as exec-buyer (1-person decision is genuine in some buyer profiles — e.g. founder-led SMB). → produces: segment
3. **Build Multi-Threading Workflow** [`create_workflow`] — Create a workflow firing daily for deals newly-flagged as single-threaded. Step sequence: (1) recompute threading_depth (fresh); (2) for genuine single-threaded mid-stage deals, fetch suggested additional contacts from account enrichment (peer roles, manager up, related team members), prioritized by likely-buying-influence; (3) create a task for the rep labeled 'Multi-thread this deal: 3 suggested contacts' with the contact list pre-attached; (4) Slack DM to the rep with deal context. If lone champion is the decision-maker (CEO of a small co, etc.), suppress — that's not single-threading risk. → produces: workflow
4. **Build Threading Health Dashboard** [`create_dashboard`] — Compose a threading health dashboard: % of mid+stage deals that are multi-threaded (target: 70%+; below 50% is a coaching gap), distribution of threading depth by stage, single-threaded-deal win rate vs. multi-threaded win rate (the proof-of-value chart), rep leaderboard on threading depth, and aged single-threaded deals (>30 days single-threaded = high-loss-risk pile). → produces: dashboard
