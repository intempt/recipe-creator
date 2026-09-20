---
name: inbox-setup
description: |
  Use when a user mentions "inbox & conversation management", or asks for related help. Multi-channel inbox configuration with AI drafts, snippet library, routing, dashboard.
arguments: []
intempt:
  id: inbox-setup
  version: 1.0.1
  slashCommand: /inbox-setup
  group: Agents
  title: "Shared inbox with AI drafts"
  shortDescription: "Sets up the shared inbox: reusable replies for the questions you get most, rules that send each message to the right owner, and a view of how fast you respond."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, design]
    agent: outreach-rep
    mode: [all]
    complexity: standard
    executionMode: live
    tags: [inbox-setup]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_snippet
    - create_dashboard
    - create_agent
  procedure:
    - step: 1
      title: "Build the snippet library"
      command: create_snippet
      produces: asset
      bindsAs: snippet
      description: "Reusable replies grouped by pricing, support, scheduling, follow-up and objections, written in your brand voice."
      prompt: "Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand voice."
    - step: 2
      title: "Add reply templates"
      command: create_snippet
      produces: asset
      bindsAs: asset
      dependsOn: [snippet]
      description: "Longer reusable email templates for the reply scenarios that come up most often."
      prompt: "Configure reusable email content templates for common reply scenarios."
    - step: 3
      title: "Track inbox performance"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [snippet, asset]
      description: "Message volume, response time, how often the AI draft gets accepted, and how accurately messages are routed."
      prompt: "Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy."
    - step: 4
      title: "Set the routing rules"
      command: create_agent
      produces: agent
      bindsAs: agent
      dependsOn: [snippet, asset, dashboard]
      description: "Messages go to the account owner first and round-robin when there is no owner, and are only handled automatically above a confidence threshold."
      prompt: "Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold."
  outputs:
    - { name: asset, type: asset, cardinality: single, description: "Snippet produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
    - { name: agent, type: agent, cardinality: single, description: "Agent produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Shared inbox with AI drafts

Sets up the shared inbox: reusable replies for the questions you get most, rules that send each message to the right owner, and a view of how fast you respond.

## What it does

1. **Build the snippet library** (`create_snippet`)

   Reusable replies grouped by pricing, support, scheduling, follow-up and objections, written in your brand voice.

2. **Add reply templates** (`create_snippet`)

   Longer reusable email templates for the reply scenarios that come up most often.

3. **Track inbox performance** (`create_dashboard`)

   Message volume, response time, how often the AI draft gets accepted, and how accurately messages are routed.

4. **Set the routing rules** (`create_agent`)

   Messages go to the account owner first and round-robin when there is no owner, and are only handled automatically above a confidence threshold.

## What you end up with

- **asset** (asset): Snippet produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **agent** (agent): Agent produced by this recipe.
