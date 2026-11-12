---
frontmatter_id: customer-onboarding
slash_command: /customer-onboarding
description: Sets up a new account, gives the CSM a dated checklist, books the kickoff, and walks the customer through to go live.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Sets up a new customer account, gives the CSM a dated onboarding checklist, books the kickoff call, emails milestone
    resources, and tracks progress to go-live.
  parameters:
  - name: go_live_target
    type: duration
    label: Target go-live window after signup
    default: 30 d
    required: false
  requirements:
  - slot: new_account
    kind: event
    meaning: A new customer account was created or signed up
    properties:
    - name: account_name
      type: string
      meaning: Name of the customer account
      optional: false
  - slot: csm_assignment
    kind: attribute
    meaning: The customer success manager assigned to an account
  - slot: account_stakeholders
    kind: attribute
    meaning: Contacts at the customer account who attend onboarding meetings
  - slot: calendar_integration
    kind: integration
    meaning: A calendar connection used to book the kickoff meeting with account stakeholders
    optional: true
    channel: google_sheets
  - slot: onboarding_milestones_completed
    kind: event
    meaning: A customer completed an onboarding milestone such as kickoff, setup, first value, or go-live
    properties:
    - name: milestone
      type: string
      meaning: Name of the onboarding milestone reached
      optional: false
  steps:
  - id: s1
    builds: account
    uses:
    - new_account
    - csm_assignment
    - go_live_target
    instruction: Configure the new account record for {new_account} with onboarding fields, a target go-live date set {go_live_target}
      after signup, and the CSM assigned from {csm_assignment}.
  - id: s2
    builds: task
    uses:
    - s1
    instruction: Create an onboarding task checklist for the CSM assigned to the account in "Set up the account record", with
      default due dates counted from signup.
  - id: s3
    builds: meeting
    uses:
    - s1
    - s2
    - account_stakeholders
    - calendar_integration
    instruction: Create a kickoff meeting calendar event for the account in "Set up the account record" with the contacts
      from {account_stakeholders} and the CSM from "Give the CSM a checklist".
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    instruction: Build an email journey for the account in "Set up the account record" that sends the customer onboarding
      milestone emails with helpful resources at each step, tied to the checklist in "Give the CSM a checklist" and the meeting
      in "Book the kickoff call".
  - id: s5
    builds: report
    uses:
    - s1
    - s2
    - s3
    - s4
    - onboarding_milestones_completed
    instruction: Create a funnel report tracking {onboarding_milestones_completed.milestone} completion for the account in
      "Set up the account record", in order kickoff, setup, first value, go-live, using the checklist, meeting, and email
      journey from prior steps.
---

# Customer onboarding

Slash command: /customer-onboarding

## Step 1: Set up the account record

Configure the new account record with onboarding fields, target go-live date, and CSM assignment.

## Step 2: Give the CSM a checklist

Create the onboarding task checklist for the assigned CSM with default due dates. Use the result of "Set up the account record".

## Step 3: Book the kickoff call

Create kickoff meeting calendar event with the account stakeholders. Use the result of "Set up the account record", "Give the CSM a checklist".

## Step 4: Email through each milestone

Build an email journey supporting the user through onboarding milestones with helpful resources at each step. Use the result of "Set up the account record", "Give the CSM a checklist", "Book the kickoff call".

## Step 5: Track progress to go live

Compose a funnel report tracking onboarding milestone completion (kickoff to setup to first-value to go-live). Use the result of "Set up the account record", "Give the CSM a checklist", "Book the kickoff call", "Email through each milestone".
