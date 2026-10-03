---
id: product-launch-site
title: Product launch microsite
slash_command: /product-launch-site
group: Content
owner: intempt
summary: Builds a small launch site (hero, feature pages, call to action, footer) in your brand styling,
  ready to publish in one click.
description: >-
  One or more pages, deploy in a click.
version: 2.0.0
classification:
  product:
    - content
  agent: creative-assistant
  mode:
    - all
  complexity: standard
  executionMode: oneshot
  tags:
    - site
    - landing-page
    - product-launch
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new content asset, from step 1 "Build the launch microsite"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the launch microsite
    summary: >-
      A multi-page site with a hero, feature and benefit pages, a call to action and a footer, using your
      brand styling and deployable in one click.
    builds: content
    description: |-
      Create a product launch microsite.
      Build a multi-page site with: hero section, feature/benefit pages, call-to-action, and footer. Apply project brand tokens. Deploy-ready in one click.
      Output: multi-page microsite
outputs:
  - key: content
    producedByStep: s1
    type: content
    description: Product launch microsite.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product launch microsite

Builds a small launch site (hero, feature pages, call to action, footer) in your brand styling, ready to publish in one click.

## Steps

1. **Build the launch microsite** (builds content)

   A multi-page site with a hero, feature and benefit pages, a call to action and a footer, using your brand styling and deployable in one click.

## What you end up with

- **content** (content): Product launch microsite.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new content asset, from step 1 "Build the launch microsite"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build content.
