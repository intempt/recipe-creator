---
frontmatter_id: customer-onboarding
slash_command: /customer-onboarding
description: Sets up a new account, gives the CSM a dated checklist, welcomes the customer with a kickoff invite, follows
  up on each onboarding milestone and emails weekly progress to go live.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Sets up each new customer account, gives the CSM a dated checklist, emails the customer a welcome with the kickoff
    invite, and emails weekly progress to go-live.
  parameters:
  - name: go_live_target
    type: duration
    label: Target go-live window after signup
    default: 30 d
    required: false
  - name: stall_window
    type: duration
    label: Days without a new milestone before a nudge email
    default: 7 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
    instruction: For each account that did {new_account}, set up its account record with the name from {new_account.account_name},
      the CSM from {csm_assignment}, and a target go-live date {go_live_target} after the {new_account} event.
  - id: s2
    builds: task
    uses:
    - s1
    - csm_assignment
    - new_account
    dependsOn:
    - s1
    instruction: 'For each account from "Set up the account record", create these tasks for its CSM from {csm_assignment},
      due the given number of days after the {new_account} event: hold the kickoff call (3 days), confirm setup is done (10
      days), confirm first value (20 days), confirm go-live (30 days).'
  - id: s3
    builds: email
    uses:
    - csm_assignment
    instruction: Write a welcome email to a new customer user whose account was just created. It thanks them, says their CSM
      from {csm_assignment} will run a kickoff call in the next 3 days and asks them to reply with times that suit them, lists
      the four onboarding milestones (kickoff, setup, first value, go-live), and links to the getting-started guide.
  - id: s4
    builds: automation
    uses:
    - s3
    - new_account
    - onboarding_milestones_completed
    - stall_window
    dependsOn:
    - s3
    instruction: Build an automation triggered when a user does {new_account}. It sends the email from "Write the welcome
      and kickoff email" to that user. Then it waits {stall_window}; if the user's account has not done {onboarding_milestones_completed}
      in that time, it sends the user one email via Blu's mailer that names the next milestone not yet reached, in the order
      kickoff, setup, first value, go-live, and offers help from their CSM.
  - id: s5
    builds: automation
    uses:
    - new_account
    - onboarding_milestones_completed
    - csm_assignment
    - go_live_target
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts that did
      {new_account} in the last 60 days and writes these figures: how many reached each {onboarding_milestones_completed.milestone}
      value (kickoff, setup, first value, go-live); the median days from {new_account} to go-live; the accounts past {go_live_target}
      without go-live, each by name with its CSM from {csm_assignment}. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Customer onboarding

Slash command: /customer-onboarding

## Step 1: Set up the account record

For each account that did new account, set up its account record with the name from account name, the CSM from csm assignment, and a target go-live date 30 d after the new account event.

## Step 2: Give the CSM a checklist

For each account from "Set up the account record", create these tasks for its CSM from csm assignment, due the given number of days after the new account event: hold the kickoff call (3 days), confirm setup is done (10 days), confirm first value (20 days), confirm go-live (30 days).

## Step 3: Write the welcome and kickoff email

Write a welcome email to a new customer user whose account was just created. It thanks them, says their CSM from csm assignment will run a kickoff call in the next 3 days and asks them to reply with times that suit them, lists the four onboarding milestones (kickoff, setup, first value, go-live), and links to the getting-started guide.

## Step 4: Send the welcome and nudge stalled onboarding

Build an automation triggered when a user does new account. It sends the email from "Write the welcome and kickoff email" to that user. Then it waits 7 d; if the user's account has not done onboarding milestones completed in that time, it sends the user one email via Blu's mailer that names the next milestone not yet reached, in the order kickoff, setup, first value, go-live, and offers help from their CSM.

## Step 5: Email weekly progress to go-live

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts that did new account in the last 60 days and writes these figures: how many reached each milestone value (kickoff, setup, first value, go-live); the median days from new account to go-live; the accounts past 30 d without go-live, each by name with its CSM from csm assignment. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
