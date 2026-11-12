---
frontmatter_id: renewal-call-summary-recipe
slash_command: /renewal-call-summary-recipe
description: Customizes AI summaries for Renewal calls, extracting usage patterns, expansion signals, churn risks, stakeholder confirmation and contract changes.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Automatically captures renewal-call insights from AI meeting summaries and builds a dashboard tracking renewal
    risk, expansion opportunities, churn precursors and renewal-call coverage by CSM owner.
  parameters:
  - name: renewal_meeting_type
    type: string
    label: Meeting type name for renewal calls
    default: Renewal
  - name: coverage_target_days
    type: number
    label: Days before renewal date by which the renewal call should happen
    default: 60
  - name: coverage_target_percent
    type: number
    label: Target percentage of upcoming renewals with a completed renewal call
    default: 100
  requirements:
  - slot: renewal_call_completed
    kind: event
    meaning: A customer completed a renewal call
    properties:
    - name: account_id
      type: string
      meaning: Account the call was held with
      optional: false
    - name: csm_owner
      type: string
      meaning: CSM owner of the account
      optional: true
  - slot: renewal_date_attribute
    kind: attribute
    meaning: The renewal date of an account
  - slot: csm_owner_attribute
    kind: attribute
    meaning: The customer success manager who owns an account
  - slot: arr_attribute
    kind: attribute
    meaning: Annual recurring revenue of an account, used to size expansion opportunity
    optional: true
  steps:
  - id: s1
    builds: event
    uses:
    - renewal_meeting_type
    instruction: Confirm that the meeting type {renewal_meeting_type} exists in the meeting taxonomy with notetaker autojoin
      enabled, and retrieve it for use in the following steps.
  - id: s2
    builds: summary
    uses:
    - s1
    - renewal_call_completed
  - id: s3
    builds: ''
---

# Renewal call summary fields

Slash command: /renewal-call-summary-recipe

## Step 1: Check the Renewal meeting type

Retrieve the Renewal meeting type from the meeting taxonomy. Confirm exists with notetaker autojoin enabled.

## Step 2: Set what renewals capture

Configure the AI summary recipe for the Renewal meeting type. Extract: (1) Usage Patterns (features the customer mentioned actively using vs. struggling with vs. never tried; (2) Expansion Signals) explicit interest in additional seats, modules, tier upgrades; budget signal for expansion (verbatim quotes); (3) Contraction Risks: explicit signals of churn intent, reduced usage, team changes affecting fit, competitor evaluation; (4) Stakeholder Confirmation: was the decision-maker present, did stakeholders confirm continued commitment, any champion changes (departures, role changes); (5) Contract Terms Discussion (pricing pushback, term length preference, payment terms, custom contractual asks; (6) Health Score Movement) sentiment shift from prior interactions; (7) Next Step: proposal needed, additional stakeholders to loop in, agreement to terms. Use the result of "Check the Renewal meeting type".

## Step 3: Track renewal risk and upside

Compose a renewal risk + expansion dashboard reading from summaries: (1) at-risk renewals (accounts with contraction signals or unresolved competitor evaluation, sorted by renewal date; (2) expansion-ready) accounts with explicit interest signals, sorted by ARR opportunity; (3) churn precursors (accounts where champion departed or stakeholders signaled disengagement; (4) renewal-call coverage) % of upcoming renewals where the call has happened (target: 100% by 60 days before renewal date); (5) win/loss patterns from past renewal-call summaries. Group by CSM owner. Use the result of "Check the Renewal meeting type", "Set what renewals capture".
