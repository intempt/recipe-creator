---
id: cart-abandoned-push
title: Cart abandonment push notification
slash_command: /cart-abandoned-push
group: Content
owner: intempt
curator: aurobind
summary: Writes a lockscreen push that brings shoppers back to an abandoned cart, naming the item they
  left behind.
description: >-
  Win-back lockscreen notification.
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
    - push
    - cart-abandoned
    - win-back
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new content asset, from step 1 "Write the win-back push"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Write the win-back push
    summary: >-
      A push notification with your brand icon, a title and body copy, naming the abandoned item where
      it is known. Helpful in tone, not pushy.
    builds: content
    description: |-
      Create a cart abandonment re-engagement push notification.
      Include brand icon, win-back title, and body copy. Tone: personal, helpful, not aggressive. Include the abandoned item name if available.
      Output: push notification (title + body + icon)
outputs:
  - key: content
    producedByStep: s1
    type: content
    description: Re-engagement push notification.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Cart abandonment push notification

Writes a lockscreen push that brings shoppers back to an abandoned cart, naming the item they left behind.

## Steps

1. **Write the win-back push** (builds content)

   A push notification with your brand icon, a title and body copy, naming the abandoned item where it is known. Helpful in tone, not pushy.

## What you end up with

- **content** (content): Re-engagement push notification.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new content asset, from step 1 "Write the win-back push"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build content.
