---
name: Inbox Setup
description: Multi-channel inbox configuration with AI drafts, snippet library, routing, dashboard.
intempt:
  id: inbox-setup
  version: 1.0.1
  slashCommand: /inbox-setup
  shortDescription: Multi-channel inbox configuration with AI drafts, snippet library, routing, dashboard.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    - design
    agent: outreach-rep
    mode:
    - all
    complexity: standard
    executionMode: live
    tags:
    - inbox-setup
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: snippet
    type: snippet
    description: Snippet produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: agent_config
    type: agent-config
    description: Agent Config produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: configure-snippets
    describe: Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand
      voice.
    produces: snippet
  - id: configure-content-templates
    describe: Configure reusable email content templates for common reply scenarios.
    produces: content
  - id: build-inbox-dashboard
    describe: Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy.
    produces: dashboard
  - id: configure-routing-agent
    describe: 'Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold.'
    produces: agent_config
---

# Inbox Setup

Multi-channel inbox configuration with AI drafts, snippet library, routing, dashboard.

## Outputs

- **snippet** (snippet): Snippet produced by this recipe.
- **content** (content): Content produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **agent_config** (agent-config): Agent Config produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand voice.
2. Configure reusable email content templates for common reply scenarios.
3. Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy.
4. Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold.
