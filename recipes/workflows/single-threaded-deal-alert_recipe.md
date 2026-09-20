---
name: single-threaded-deal-alert
description: Use when a user mentions "single-threaded deal", "multi-threading task", "lone champion detection", or asks for related help. Detect deals where only one contact from the buyer side is engaged, single-threaded deals lose 3x more often when the lone champion leaves or doesn't have authority. Surface them with a multi-threading task and a recommended contact list.
arguments: []
intempt:
  id: single-threaded-deal-alert
  title: "Single threaded deal alert"
  version: 1.0.0
  slashCommand: /single-threaded-deal-alert
  group: Workflows
  shortDescription: "Finds late stage deals where only one person on the buyer's side is engaged and gives the rep three other names to bring in."
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
    integrations:
      - { value: slack, severity: recommended }
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
      title: "Count who is actually engaged"
      command: create_ai_attribute
      produces: attribute
      bindsAs: threading
      description: "The number of people on the buyer's side who have attended a meeting on this deal, replied to an email on it, or been added as a contact. One person at demo, proposal or closing stage is flagged. One person early on is normal."
      prompt: 'Create an AI-derived attribute ''threading_depth'' on the Deal object. Count distinct buyer-side contacts who have (a) attended a meeting on this deal, OR (b) replied to an email on this deal, OR (c) been explicitly added as a deal contact. Output: integer count. Flag as ''single-threaded'' if count = 1 and deal is in Demo / Proposal / Closing stage (early-stage single-threading is normal; late-stage is a red flag).'
    - step: 2
      title: "Find the risky ones"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - threading
      description: "Open deals with a single engaged contact at demo, proposal or closing. Deals under 14 days old are left out, because multi threading takes time, and so are deals marked as a genuine single buyer, such as a founder led small business."
      prompt: Build a segment 'Single-threaded deals - mid+ stage' capturing open deals where threading_depth = 1 AND stage is Demo, Proposal, or Closing. Excludes deals < 14 days old (haven't had time for multi-threading naturally) and deals flagged as exec-buyer (1-person decision is genuine in some buyer profiles, e.g. founder-led SMB).
    - step: 3
      title: "Give the rep three names"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - threading
      - segment
      description: "Daily, for newly flagged deals, it recounts the contacts, pulls suggested additions from enrichment, peers, the manager above and related team members, ranked by likely influence on the decision, creates a task with that list attached, and messages the rep. If the lone contact is the decision maker, it stays quiet."
      prompt: 'Create a workflow firing daily for deals newly-flagged as single-threaded. Step sequence: (1) recompute threading_depth (fresh); (2) for genuine single-threaded mid-stage deals, fetch suggested additional contacts from account enrichment (peer roles, manager up, related team members), prioritized by likely-buying-influence; (3) create a task for the rep labeled ''Multi-thread this deal: 3 suggested contacts'' with the contact list pre-attached; (4) Slack DM to the rep with deal context. If lone champion is the decision-maker (CEO of a small co, etc.), suppress: that''s not single-threading risk.'
    - step: 4
      title: "See what threading is worth"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - threading
      - segment
      - workflow
      description: "The share of mid and late stage deals with more than one contact against a 70% target, where under 50% is a coaching gap, the depth by stage, the win rate of single threaded deals against multi threaded ones, a rep leaderboard, and the deals single threaded for over 30 days."
      prompt: 'Compose a threading health dashboard: % of mid+stage deals that are multi-threaded (target: 70%+; below 50% is a coaching gap), distribution of threading depth by stage, single-threaded-deal win rate vs. multi-threaded win rate (the proof-of-value chart), rep leaderboard on threading depth, and aged single-threaded deals (>30 days single-threaded = high-loss-risk pile).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Single threaded deal alert

Finds late stage deals where only one person on the buyer's side is engaged and gives the rep three other names to bring in.

## Before you run it

- Connect slack
- Send the `deal_stage_changed` event
- Send the `meeting_completed` event

## What it does

1. **Count who is actually engaged** (`create_ai_attribute`)

   The number of people on the buyer's side who have attended a meeting on this deal, replied to an email on it, or been added as a contact. One person at demo, proposal or closing stage is flagged. One person early on is normal.

2. **Find the risky ones** (`create_segment`)

   Open deals with a single engaged contact at demo, proposal or closing. Deals under 14 days old are left out, because multi threading takes time, and so are deals marked as a genuine single buyer, such as a founder led small business.

3. **Give the rep three names** (`create_workflow`)

   Daily, for newly flagged deals, it recounts the contacts, pulls suggested additions from enrichment, peers, the manager above and related team members, ranked by likely influence on the decision, creates a task with that list attached, and messages the rep. If the lone contact is the decision maker, it stays quiet.

4. **See what threading is worth** (`create_dashboard`)

   The share of mid and late stage deals with more than one contact against a 70% target, where under 50% is a coaching gap, the depth by stage, the win rate of single threaded deals against multi threaded ones, a rep leaderboard, and the deals single threaded for over 30 days.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
