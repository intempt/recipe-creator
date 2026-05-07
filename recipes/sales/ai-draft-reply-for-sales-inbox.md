---
name: Ai Draft Reply For Sales Inbox
description: Generate a contextualised AI draft reply for sales emails using account and deal context.
intempt:
  id: ai-draft-reply-for-sales-inbox
  version: 1.0.1
  slashCommand: /ai-draft-reply-for-sales-inbox
  shortDescription: Generate a contextualised AI draft reply for sales emails using account and deal context.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    - design
    agent: outreach-rep
    mode:
    - b2b
    complexity: standard
    executionMode: live
    tags:
    - ai
    - inbox-and-reply-automation
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
    describe: 'Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand
      voice. (Tailored for: AI draft reply for sales inbox.)'
    produces: snippet
  - id: configure-content-templates
    describe: 'Configure reusable email content templates for common reply scenarios. (Tailored for: AI draft reply for sales
      inbox.)'
    produces: content
  - id: build-inbox-dashboard
    describe: 'Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy. (Tailored
      for: AI draft reply for sales inbox.)'
    produces: dashboard
  - id: configure-routing-agent
    describe: 'Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold.
      (Tailored for: AI draft reply for sales inbox.)'
    produces: agent_config
---

# Ai Draft Reply For Sales Inbox

Generate a contextualised AI draft reply for sales emails using account and deal context.

## Outputs

- **snippet** (snippet): Snippet produced by this recipe.
- **content** (content): Content produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **agent_config** (agent-config): Agent Config produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand voice. (Tailored for: AI draft reply for sales inbox.)
2. Configure reusable email content templates for common reply scenarios. (Tailored for: AI draft reply for sales inbox.)
3. Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy. (Tailored for: AI draft reply for sales inbox.)
4. Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold. (Tailored for: AI draft reply for sales inbox.)
