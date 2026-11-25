---
frontmatter_id: hubspot-lifecycle-writeback
slash_command: /hubspot-lifecycle-writeback
description: Pushes the lifecycle stage computed from real product and billing behaviour onto the HubSpot contact, so sales and marketing read the same thing.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
visibility: draft
rejected: Its purpose is writing the computed lifecycle stage onto the HubSpot contact; HubSpot writes are not planned on
  Blu.
portable:
  summary: Computes each contact's lifecycle stage from product and billing behaviour and writes it one way to the HubSpot
    contact so sales and marketing see the same value.
  parameters:
  - name: hubspot_property_name
    type: string
    label: HubSpot contact property to update
    default: lifecycle_stage
    required: false
  requirements:
  - slot: product_usage_event
    kind: event
    meaning: A customer used the product (product activity tracked for each user)
    properties:
    - name: user_id
      type: string
      meaning: Identifier of the user who used the product
      optional: false
  - slot: billing_event
    kind: event
    meaning: A billing change occurred for a customer (subscription started, renewed, or cancelled)
    properties:
    - name: subscription_status
      type: string
      meaning: Current billing status of the subscription
      optional: false
  - slot: hubspot_contact
    kind: integration
    meaning: A connected HubSpot account where contact properties can be updated by workflow
    channel: hubspot
  steps:
  - id: s1
    builds: attribute
    uses:
    - product_usage_event
    - billing_event
    instruction: 'Build a computed attribute on users named "lifecycle_stage", refreshed daily, with exactly one of these
      values: trialing, active, at_risk, churned, from {billing_event.subscription_status} on the user''s latest {billing_event}
      and whether they did {product_usage_event} in the last 14 days.'
  - id: s2
    builds: automation
    uses:
    - s1
    - hubspot_contact
    - hubspot_property_name
    dependsOn:
    - s1
    instruction: Build an automation triggered when a user's lifecycle_stage from "Define the lifecycle honestly" changes.
      It writes the new value to the {hubspot_property_name} property of the matching contact in {hubspot_contact}, one way
      only.
---

# Write lifecycle back to HubSpot

Slash command: /hubspot-lifecycle-writeback

## Step 1: Define the lifecycle honestly

Build a computed attribute on users named "lifecycle_stage", refreshed daily, with exactly one of these values: trialing, active, at_risk, churned, from subscription status on the user's latest billing event and whether they did product usage event in the last 14 days.

## Step 2: Push it one way to HubSpot

Build an automation triggered when a user's lifecycle_stage from "Define the lifecycle honestly" changes. It writes the new value to the lifecycle_stage property of the matching contact in hubspot contact, one way only.
