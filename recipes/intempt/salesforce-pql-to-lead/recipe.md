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
  summary: Creates a Salesforce lead as soon as product usage shows a prospect is ready, so the signal becomes a record a
    rep can work, without creating duplicates.
  parameters:
  - name: usage_threshold
    type: string
    label: Usage threshold that qualifies a user
    default: <UNKNOWN>
    required: false
  - name: failure_policy
    type: enum
    label: Failure policy when a lead is rejected
    default: skip_and_record
    required: false
    options:
    - skip_and_record
    - stop_all
  requirements:
  - slot: product_qualified_signal
    kind: segment
    meaning: Users who reached the product-qualified usage signal (usage threshold, feature reached, or seats added)
    creatable: true
    definition: users who reached {usage_threshold} on product usage
  - slot: salesforce_integration
    kind: integration
    meaning: A connected Salesforce account that can create and upsert leads
    channel: salesforce
  - slot: lead_external_id
    kind: attribute
    meaning: An external ID field on the Salesforce lead used as the upsert match key
  - slot: lead_score
    kind: attribute
    meaning: A customer score attribute owned by the project
    optional: true
  - slot: qualifying_signal
    kind: attribute
    meaning: An attribute recording which product signal qualified the user
    optional: true
  - slot: lead_source
    kind: attribute
    meaning: An attribute recording the source of the user
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - usage_threshold
    - product_qualified_signal
    instruction: Create the segment {product_qualified_signal} describing the product-qualified signal using {usage_threshold}
      (usage threshold, feature reached, or seats added). Keep the definition in the segment so sales and product can both
      review it.
  - id: s2
    builds: automation
    uses:
    - s1
    - product_qualified_signal
    - salesforce_integration
    - lead_external_id
    - lead_score
    - qualifying_signal
    - lead_source
    - failure_policy
    instruction: 'Create a workflow that enrolls members of the segment from "Agree the qualifying signal" and, for each member,
      upserts a Salesforce lead through {salesforce_integration} using {lead_external_id} as the match key. Do not use plain
      create. Map only the fields the project owns: {lead_score}, {qualifying_signal} and {lead_source}. Leave all Salesforce-owned
      fields untouched. Set the failure policy to {failure_policy} so a rejected lead is skipped and recorded without stopping
      the remaining leads.'
---

# Product qualified signal to a Salesforce lead

Slash command: /salesforce-pql-to-lead

## Step 1: Agree the qualifying signal

Create a segment describing the product-qualified signal (the usage threshold, the feature reached, the seats added) rather than encoding it inside the workflow. The definition is the thing sales and product will argue about, so it needs to live somewhere both can see it.

## Step 2: Upsert the lead, never double

Create a workflow enrolling members of the segment and creating a Salesforce lead for each. Use upsert with an external ID rather than create, because a create without a match key is a duplicate generator and the rep pays for it. Map only fields Intempt owns (the score, the signal, the source) and leave Salesforce-owned fields alone. Failure policy is skip-and-record so one rejected lead does not stop the rest. Use the result of "Agree the qualifying signal".
