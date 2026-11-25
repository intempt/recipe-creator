---
frontmatter_id: salesforce-pql-to-lead
slash_command: /salesforce-pql-to-lead
description: Creates a Salesforce lead the moment product usage says someone is ready, so a signal the product saw becomes a record a rep can work.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Builds a product-qualified users segment and upserts each new member as a Salesforce lead, matched on an external
    ID so no lead is doubled.
  parameters:
  - name: usage_threshold
    type: number
    label: Key product actions that make a user product-qualified
    default: 20
    required: false
  - name: usage_window
    type: duration
    label: Window the key actions are counted over
    default: 14 d
    required: false
  requirements:
  - slot: key_product_action
    kind: event
    meaning: A user did the product action that signals buying readiness (a core feature used)
  - slot: plan
    kind: attribute
    meaning: The user's current plan, empty or free/trial when they are not paying
  - slot: salesforce_integration
    kind: integration
    channel: salesforce
    meaning: A connected Salesforce account that can upsert leads
  - slot: lead_external_id
    kind: attribute
    meaning: User attribute with the external ID used as the Salesforce lead upsert match key
  - slot: lead_score
    kind: attribute
    meaning: A lead score attribute owned by the project
    optional: true
  - slot: lead_source
    kind: attribute
    meaning: An attribute recording where the user came from
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - key_product_action
    - plan
    - usage_threshold
    - usage_window
    instruction: Build a new segment of users named "Product-qualified users". A user is in it when they did {key_product_action}
      {usage_threshold} or more times in the last {usage_window} and their {plan} attribute is empty, free or trial.
  - id: s2
    builds: automation
    uses:
    - s1
    - salesforce_integration
    - lead_external_id
    - lead_score
    - lead_source
    dependsOn:
    - s1
    instruction: Build an automation that starts when a user enters the segment from "Agree the qualifying signal" and upserts
      a lead in {salesforce_integration} for that user, matched on their {lead_external_id} attribute so an existing lead
      is updated, never duplicated. It writes only the user's name, email, {lead_score}, {lead_source} and the qualifying
      signal "Product-qualified users"; every other Salesforce field is left untouched. A lead Salesforce rejects is skipped
      and recorded, and the other users carry on.
---

# Product qualified signal to a Salesforce lead

Slash command: /salesforce-pql-to-lead

## Step 1: Agree the qualifying signal

Build a new segment of users named "Product-qualified users". A user is in it when they did key product action 20 or more times in the last 14 d and their plan attribute is empty, free or trial.

## Step 2: Upsert the lead, never double

Build an automation that starts when a user enters the segment from "Agree the qualifying signal" and upserts a lead in salesforce integration for that user, matched on their lead external id attribute so an existing lead is updated, never duplicated. It writes only the user's name, email, lead score, lead source and the qualifying signal "Product-qualified users"; every other Salesforce field is left untouched. A lead Salesforce rejects is skipped and recorded, and the other users carry on.
