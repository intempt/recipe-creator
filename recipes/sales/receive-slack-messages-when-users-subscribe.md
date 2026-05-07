---
name: Receive Slack Messages When Users Subscribe
description: Get Slack notifications when new users sign up.
intempt:
  id: receive-slack-messages-when-users-subscribe
  version: 1.0.1
  slashCommand: /receive-slack-messages-when-users-subscribe
  shortDescription: Get Slack notifications when new users sign up.
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
    - receive
    - internal-notifications
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
      voice. (Tailored for: Receive Slack messages when users subscribe.)'
    produces: snippet
  - id: configure-content-templates
    describe: 'Configure reusable email content templates for common reply scenarios. (Tailored for: Receive Slack messages
      when users subscribe.)'
    produces: content
  - id: build-inbox-dashboard
    describe: 'Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy. (Tailored
      for: Receive Slack messages when users subscribe.)'
    produces: dashboard
  - id: configure-routing-agent
    describe: 'Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold.
      (Tailored for: Receive Slack messages when users subscribe.)'
    produces: agent_config
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Receive Slack Messages When Users Subscribe

Get Slack notifications when new users sign up.

## Outputs

- **snippet** (snippet): Snippet produced by this recipe.
- **content** (content): Content produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **agent_config** (agent-config): Agent Config produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections) with brand voice. (Tailored for: Receive Slack messages when users subscribe.)
2. Configure reusable email content templates for common reply scenarios. (Tailored for: Receive Slack messages when users subscribe.)
3. Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy. (Tailored for: Receive Slack messages when users subscribe.)
4. Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence threshold. (Tailored for: Receive Slack messages when users subscribe.)

## Prerequisites

- Integration: **slack** (blocking)
