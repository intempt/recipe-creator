---
id: inbox-setup
title: Shared inbox with AI drafts
slash_command: /inbox-setup
group: Agents
owner: intempt
summary: 'Sets up the shared inbox: reusable replies for the questions you get most, rules that send each
  message to the right owner, and a view of how fast you respond.'
description: >-
  Multi-channel inbox configuration with AI drafts, snippet library, routing, dashboard.
version: 2.0.0
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
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new content snippet, from step 1 "Build the snippet library"
    - A new content snippet, from step 2 "Add reply templates"
    - A new dashboard, from step 3 "Track inbox performance"
    - A new custom agent, from step 4 "Set the routing rules"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the snippet library
    summary: >-
      Reusable replies grouped by pricing, support, scheduling, follow-up and objections, written in your
      brand voice.
    builds: snippet
    description: >-
      Configure snippet library across categories (Pricing, Support, Scheduling, Follow-up, Objections)
      with brand voice.
  - id: s2
    title: Add reply templates
    summary: >-
      Longer reusable email templates for the reply scenarios that come up most often.
    builds: snippet
    description: >-
      Configure reusable email content templates for common reply scenarios. Use the result of "Build
      the snippet library".
    dependsOn:
      - s1
  - id: s3
    title: Track inbox performance
    summary: >-
      Message volume, response time, how often the AI draft gets accepted, and how accurately messages
      are routed.
    builds: dashboard
    description: >-
      Compose a dashboard tracking inbox volume, response time, AI-draft acceptance rate, routing accuracy.
      Use the result of "Build the snippet library", "Add reply templates".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Set the routing rules
    summary: >-
      Messages go to the account owner first and round-robin when there is no owner, and are only handled
      automatically above a confidence threshold.
    builds: agent
    description: >-
      Configure the routing agent with rules: account-owner-first, round-robin fallback, AI-confidence
      threshold. Use the result of "Build the snippet library", "Add reply templates", "Track inbox performance".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: asset
    producedByStep: s2
    type: asset
    description: Snippet produced by this recipe.
  - key: asset_2
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
  - key: agent
    producedByStep: s4
    type: agent
    description: Agent produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Shared inbox with AI drafts

Sets up the shared inbox: reusable replies for the questions you get most, rules that send each message to the right owner, and a view of how fast you respond.

## Steps

1. **Build the snippet library** (builds snippet)

   Reusable replies grouped by pricing, support, scheduling, follow-up and objections, written in your brand voice.

2. **Add reply templates** (builds snippet)

   Longer reusable email templates for the reply scenarios that come up most often.

3. **Track inbox performance** (builds dashboard)

   Message volume, response time, how often the AI draft gets accepted, and how accurately messages are routed.

4. **Set the routing rules** (builds agent)

   Messages go to the account owner first and round-robin when there is no owner, and are only handled automatically above a confidence threshold.

## What you end up with

- **asset** (asset): Snippet produced by this recipe.
- **asset_2** (asset): Asset produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **agent** (agent): Agent produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new content snippet, from step 1 "Build the snippet library"
- A new content snippet, from step 2 "Add reply templates"
- A new dashboard, from step 3 "Track inbox performance"
- A new custom agent, from step 4 "Set the routing rules"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build agent, dashboard, snippet.
