---
name: shopify-churn-risk-discount
description: Use when a user mentions "churn risk discount", "win back discount shopify", "discount lapsing customers", or asks for related help. Apply a Shopify discount to customers a churn signal has flagged, before they lapse rather than after.
arguments: []
intempt:
  id: shopify-churn-risk-discount
  version: 1.0.0
  slashCommand: /shopify-churn-risk-discount
  group: Workflows
  shortDescription: "Apply a Shopify discount to customers a churn signal has flagged, before they lapse rather than after."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: revops-automator
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [shopify, discount, retention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
  procedure:
    - step: 1
      title: Find Who Is Slipping
      command: create_segment
      produces: segment
      bindsAs: at_risk
      description: 'Create a segment of customers whose purchase cadence has broken — a gap materially longer than their own established rhythm, not a fixed number of days that treats a monthly buyer and an annual one the same.'
      prompt: 'Create a segment of customers whose purchase cadence has broken — a gap materially longer than their own established rhythm, not a fixed number of days that treats a monthly buyer and an annual one the same.'
    - step: 2
      title: Apply The Discount
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - at_risk
      description: 'Create a workflow applying the discount code to each member. The step states the blast radius before it runs, because a discount applied to the wrong segment is money already gone by the time anyone notices. Shopify rejections come back verbatim: an expired code and an already-applied code call for different fixes.'
      prompt: 'Create a workflow applying the discount code to each member. The step states the blast radius before it runs, because a discount applied to the wrong segment is money already gone by the time anyone notices. Shopify rejections come back verbatim: an expired code and an already-applied code call for different fixes.'
---
