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
  shortDescription: "Multi-channel inbox configuration with AI drafts, snippet library, routing, dashboard."
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
      title: "Configure Snippets"
      command: create_snippet
      produces: asset
      bindsAs: snippet
      description: "Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand voice."
      prompt: "Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand voice."
    - step: 2
      title: "Configure Snippets"
      command: create_snippet
      produces: asset
      bindsAs: asset
      dependsOn: [snippet]
      description: "Configure reusable email content templates for common reply scenarios."
      prompt: "Configure reusable email content templates for common reply scenarios."
    - step: 3
      title: "Build Inbox Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [snippet, asset]
      description: "Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy."
      prompt: "Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy."
    - step: 4
      title: "Configure Routing Agent"
      command: create_agent
      produces: agent
      bindsAs: agent
      dependsOn: [snippet, asset, dashboard]
      description: "Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold."
      prompt: "Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold."
  outputs:
    - { name: asset, type: asset, cardinality: single, description: "Snippet produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
    - { name: agent, type: agent, cardinality: single, description: "Agent produced by this recipe." }
---

# Inbox & Conversation Management

## Procedure

1. **Configure Snippets** [`create_snippet`] — Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand voice. → produces: asset
2. **Configure Snippets** [`create_snippet`] — Configure reusable email content templates for common reply scenarios. → produces: asset
3. **Build Inbox Dashboard** [`create_dashboard`] — Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy. → produces: dashboard
4. **Configure Routing Agent** [`create_agent`] — Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold. → produces: agent
