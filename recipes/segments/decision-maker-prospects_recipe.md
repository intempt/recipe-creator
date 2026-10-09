---
name: decision-maker-prospects
description: |
  Use when a user mentions "decision-maker prospects", or asks for related help. Senior-title users (C-level, VP, Director) showing intent: priority routing for AE outreach.
arguments: []
intempt:
  id: decision-maker-prospects
  version: 1.0.0
  slashCommand: /decision-maker-prospects
  group: Segments
  title: 'Decision makers checking pricing'
  shortDescription: 'Senior people who looked at your pricing in the last month, so AEs can talk to whoever actually holds the budget.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [b2b, saas]
    object: users
    complexity: standard
    executionMode: live
    tags: [users-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: 'Build the decision-maker list'
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Users whose title contains CEO, CTO, CFO, CMO, COO, VP, Vice President, Director, Head of, or Chief, who viewed a /pricing page in the last 30 days and have an email on file.'
      prompt: |
        Create a segment called "Decision-Maker Prospects".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: Job title contains any of ["CEO", "CTO", "CFO", "CMO", "COO", "VP", "Vice President", "Director", "Head of", "Chief"]
        - AND Event: View page where Page URL contains "/pricing" occurred >= 1 time in last 30 days
        - AND Attribute: email is not empty

        Description: Senior-title users (C-level, VP, Director) who have visited pricing in the last 30 days. The economic-buyer signal: these are budget-holders actively researching. Highest priority for AE-led outreach, executive-sponsor engagement, and ROI-focused content delivery.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Decision makers checking pricing

Senior people who looked at your pricing in the last month, so AEs can talk to whoever actually holds the budget.

## What it does

1. **Build the decision-maker list** (`create_segment`)

   Users whose title contains CEO, CTO, CFO, CMO, COO, VP, Vice President, Director, Head of, or Chief, who viewed a /pricing page in the last 30 days and have an email on file.

## What you end up with

- **segment** (segment): Segment created on /segments.
