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
portable:
  summary: Computes each contact's lifecycle stage from product and billing behaviour and writes it one way to the HubSpot
    contact so sales and marketing see the same value.
  parameters:
  - name: lifecycle_stages
    type: enum
    label: Lifecycle stages to compute
    default: trialing,active,at_risk,churned
    required: false
    options:
    - trialing
    - active
    - at_risk
    - churned
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
  - slot: lifecycle_attribute
    kind: attribute
    meaning: A user attribute holding the computed lifecycle stage (trialing, active, at risk, churned)
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
    - lifecycle_attribute
    - lifecycle_stages
    instruction: Create {lifecycle_attribute} from product activity in {product_usage_event} and billing status in {billing_event},
      not from form data, assigning one of {lifecycle_stages} to each contact.
  - id: s2
    builds: automation
    uses:
    - s1
    - lifecycle_attribute
    - hubspot_contact
    - hubspot_property_name
    instruction: 'Create a one-way workflow that updates the {hubspot_property_name} property on the {hubspot_contact} contact
      whenever {lifecycle_attribute} changes, using the value computed in "Define the lifecycle honestly". Treat the lifecycle
      as owned by the CDP: HubSpot only displays it and must not write to this field.'
---

# Write lifecycle back to HubSpot

Slash command: /hubspot-lifecycle-writeback

## Step 1: Define the lifecycle honestly

Create the lifecycle attribute from product and billing reality (trialing, active, at risk, churned) rather than from whatever a form last said. This is the value worth having in two systems.

## Step 2: Push it one way to HubSpot

Create a workflow updating the HubSpot contact property when the lifecycle changes. The direction is one way on this field: Intempt owns it, HubSpot displays it. A field written from both sides needs a stated winner, and pretending otherwise is how a CRM and a CDP quietly disagree for months. Use the result of "Define the lifecycle honestly".
