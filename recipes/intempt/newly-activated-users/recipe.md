---
frontmatter_id: newly-activated-users
slash_command: /newly-activated-users
description: Paying users who hit their activation milestone in the last week, while they are warm enough to say yes to more.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Builds a segment of paying users who completed the activation journey in the last week, so they can be targeted
    while engaged enough to upgrade or expand.
  parameters:
  - name: activation_window
    type: duration
    label: Lookback window for activation event
    default: 7 d
  - name: activation_journey_id
    type: string
    label: Activation journey ID chosen for this run
    required: true
  - name: excluded_plan
    type: string
    label: Plan value that marks a non-paying user
    default: free
  requirements:
  - slot: journey_completed_event
    kind: event
    meaning: A customer completed a journey goal
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey that was completed
      optional: false
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a user is on
  steps:
  - id: s1
    builds: segment
    uses:
    - journey_completed_event
    - plan_attribute
    - activation_window
    - activation_journey_id
    - excluded_plan
    instruction: Build a new segment named "Newly Activated Users" containing users who did {journey_completed_event} at least
      once in the last {activation_window} with {journey_completed_event.journey_id} equal to {activation_journey_id}, and
      whose {plan_attribute} has a value and is not {excluded_plan}.
---

# Newly activated users

Slash command: /newly-activated-users

## Step 1: Build the newly-activated list

Build a new segment named "Newly Activated Users" containing users who did journey completed event at least once in the last 7 d with journey id equal to the activation journey ID chosen for this run, and whose plan attribute has a value and is not free.
