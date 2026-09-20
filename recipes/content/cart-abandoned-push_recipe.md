---
name: cart-abandoned-push
description: |
  Use when a user mentions "re-engagement push", "cart abandoned push", "win-back notification", "push notification", or asks to create a push notification for cart recovery. Win-back lockscreen notification.
arguments: []
intempt:
  id: cart-abandoned-push
  version: 1.0.0
  slashCommand: /cart-abandoned-push
  group: Content
  title: "Cart abandonment push notification"
  shortDescription: "Writes a lockscreen push that brings shoppers back to an abandoned cart, naming the item they left behind."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [content]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [push, cart-abandoned, win-back]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_content
  procedure:
    - step: 1
      title: "Write the win-back push"
      command: create_content
      produces: content
      bindsAs: content
      description: "A push notification with your brand icon, a title and body copy, naming the abandoned item where it is known. Helpful in tone, not pushy."
      prompt: |
        Create a cart abandonment re-engagement push notification.

        Include brand icon, win-back title, and body copy. Tone: personal, helpful, not aggressive. Include the abandoned item name if available.

        Output: push notification (title + body + icon)
  outputs:
    - { name: content, type: content, cardinality: single, description: "Re-engagement push notification." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Cart abandonment push notification

Writes a lockscreen push that brings shoppers back to an abandoned cart, naming the item they left behind.

## What it does

1. **Write the win-back push** (`create_content`)

   A push notification with your brand icon, a title and body copy, naming the abandoned item where it is known. Helpful in tone, not pushy.

## What you end up with

- **content** (content): Re-engagement push notification.
