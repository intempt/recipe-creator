---
name: Email Sms Campaign Performance Dashboard
description: 'Lifecycle marketer view: campaign-level leaderboard with sends, opens, clicks, conversions, revenue per send
  — the canonical Klaviyo-style view.'
intempt:
  id: email-sms-campaign-performance-dashboard
  version: 1.0.0
  slashCommand: /email-sms-campaign-performance-dashboard
  shortDescription: 'Lifecycle marketer view: campaign-level leaderboard with sends, opens, clicks, conversions, revenue per
    send — the canonical Klaviyo-style view.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - dashboard
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: dashboard
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
  steps:
  - id: build-dashboard
    describe: Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes
      per the spec below.
    produces: dashboard
---

# Email Sms Campaign Performance Dashboard

Lifecycle marketer view: campaign-level leaderboard with sends, opens, clicks, conversions, revenue per send — the canonical Klaviyo-style view.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
