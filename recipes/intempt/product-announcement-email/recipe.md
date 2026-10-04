---
id: product-announcement-email
title: Product launch announcement email
slash_command: /product-announcement-email
group: Content
owner: intempt
curator: aurobind
summary: Writes a launch-day email in your brand colors and fonts, with the product hero image and a subject
  line written for opens and clicks.
description: >-
  Launch-day email with hero.
version: 2.0.0
classification:
  product:
    - content
  agent: creative-assistant
  mode:
    - all
  complexity: quick
  executionMode: oneshot
  tags:
    - email
    - announcement
    - product-launch
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new content asset, from step 1 "Write the announcement email"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Write the announcement email
    summary: >-
      A ready-to-send email using your brand colors, fonts and logo, with a product hero block and a subject
      line written for open and click rate.
    builds: content
    description: |-
      Create a product announcement email.
      Apply the project's brand tokens (colors, fonts, logo). Include a product hero block with the featured product image. Write an announcement subject line and body copy optimized for open rate and click-through.
      Output: ready-to-send email template
outputs:
  - key: content
    producedByStep: s1
    type: content
    description: Product announcement email.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product launch announcement email

Writes a launch-day email in your brand colors and fonts, with the product hero image and a subject line written for opens and clicks.

## Steps

1. **Write the announcement email** (builds content)

   A ready-to-send email using your brand colors, fonts and logo, with a product hero block and a subject line written for open and click rate.

## What you end up with

- **content** (content): Product announcement email.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new content asset, from step 1 "Write the announcement email"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build content.
