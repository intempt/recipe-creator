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
  shortDescription: "Generate one iOS lockscreen-style win-back push notification copy block for cart recovery."
  availability: available
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
      title: "Compose re-engagement push"
      command: create_content
      produces: content
      bindsAs: content
      description: "Generate a win-back push notification with brand icon, title, and body for cart abandonment recovery."
      prompt: |
        Create a cart abandonment re-engagement push notification.

        Include brand icon, win-back title, and body copy. Tone: personal, helpful, not aggressive. Include the abandoned item name if available.

        Output: push notification (title + body + icon)
  outputs:
    - { name: content, type: content, cardinality: single, description: "Re-engagement push notification." }
---

# Cart Abandoned Push

## Procedure

1. **Compose re-engagement push** [`create_content`] — Generate win-back push notification. → produces: content

## Notes

- Routes to: /content-builder?type=push&recipe=push/push-cart-abandoned
- iOS lockscreen format with brand icon.
