---
frontmatter_id: hubspot-pql-to-deal
slash_command: /hubspot-pql-to-deal
description: Update a HubSpot property, add a contact to a list, or create a HubSpot task when product usage signals readiness, so HubSpot reflects product evidence.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
visibility: draft
rejected: Its purpose is creating and updating HubSpot deals from product signals; HubSpot writes are not planned on Blu.
portable:
  summary: When product usage shows an account is ready to buy, the recipe updates its HubSpot deal, adds the contact to a
    list, or creates a task, so HubSpot reflects product evidence.
  parameters:
  - name: signal_score
    type: number
    label: Product signal score written to the deal
    required: true
  - name: signal_source
    type: string
    label: Source value written to the deal
    default: Intempt
    required: false
  requirements:
  - slot: product_qualified_usage
    kind: event
    meaning: A customer used the product in a way that shows readiness to buy
    properties:
    - name: signal
      type: string
      meaning: The product usage signal that triggered the event
      optional: false
    - name: account_id
      type: string
      meaning: Identifier of the account that performed the usage
      optional: false
  - slot: hubspot_account
    kind: integration
    meaning: A connected HubSpot account where deals, contacts, lists and tasks are managed
    channel: hubspot
  steps:
  - id: s1
    builds: segment
    uses:
    - product_qualified_usage
    instruction: Build a new segment of accounts named "Ready to Buy Accounts" with every account whose users did {product_qualified_usage}
      in the last 30 days.
  - id: s2
    builds: automation
    uses:
    - s1
    - hubspot_account
    - product_qualified_usage
    - signal_source
    - signal_score
    dependsOn:
    - s1
    instruction: Build an automation triggered when an account enters the segment from "Define what ready to buy means". It
      creates a deal in {hubspot_account} for that account, matched on {product_qualified_usage.account_id} so a second signal
      updates the existing deal, setting only source to {signal_source}, signal to {product_qualified_usage.signal} and score
      to {signal_score}.
---

# Product qualified signal to a HubSpot deal

Slash command: /hubspot-pql-to-deal

## Step 1: Define what ready to buy means

Build a new segment of accounts named "Ready to Buy Accounts" with every account whose users did product qualified usage in the last 30 days.

## Step 2: Open the deal, leave the rest

Build an automation triggered when an account enters the segment from "Define what ready to buy means". It creates a deal in hubspot account for that account, matched on account id so a second signal updates the existing deal, setting only source to Intempt, signal to signal and score to the product signal score written to the deal.
