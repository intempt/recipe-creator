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
  - slot: ready_to_buy_accounts
    kind: segment
    meaning: Accounts whose product usage shows they are ready to buy
    creatable: true
    definition: accounts that did {product_qualified_usage} with the usage that means ready to buy, agreed once and reused
  - slot: hubspot_account
    kind: integration
    meaning: A connected HubSpot account where deals, contacts, lists and tasks are managed
    channel: hubspot
  steps:
  - id: s1
    builds: segment
    uses:
    - product_qualified_usage
    instruction: 'Create the segment {ready_to_buy_accounts} describing the product-qualified account: the usage that means
      someone is ready to buy, agreed once and reused. Base it on {product_qualified_usage}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - ready_to_buy_accounts
    - hubspot_account
    - product_qualified_usage
    - signal_source
    - signal_score
    instruction: 'Create a workflow that creates a HubSpot deal in {hubspot_account} for each account in the "Define what
      ready to buy means" segment, matched on the account identifier {product_qualified_usage.account_id} so a second signal
      updates the existing deal instead of opening a duplicate. Set only the fields the product signal owns: source to {signal_source},
      the triggering signal to {product_qualified_usage.signal}, and the score to {signal_score}. Leave deal stage and amount
      unchanged for the sales rep.'
---

# Product qualified signal to a HubSpot deal

Slash command: /hubspot-pql-to-deal

## Step 1: Define what ready to buy means

Create the segment describing the product-qualified account: the usage that means someone is ready to buy, agreed once and reused.

## Step 2: Open the deal, leave the rest

Create a workflow that creates a HubSpot deal for each qualifying account, matched on a key so a second signal updates the deal instead of opening a duplicate. Set only the fields Intempt owns (source, the signal that triggered it, the score) and leave stage and amount to the rep. Use the result of "Define what ready to buy means".
