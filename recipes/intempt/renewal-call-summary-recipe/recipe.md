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
visibility: draft
rejected: Its purpose is configuring the AI summary fields of the Renewal meeting type; meeting and meeting-type setup is
  not planned on Blu.
portable:
  summary: Sets the AI summary of Renewal calls to capture usage, expansion signals, churn risks, stakeholder changes and
    contract asks.
  parameters:
  - name: renewal_meeting_type
    type: string
    label: Meeting type name for renewal calls
    default: Renewal
  requirements: []
  steps:
  - id: s1
    builds: meeting_type
    uses:
    - renewal_meeting_type
    instruction: 'For the meeting type {renewal_meeting_type}, set its AI summary to extract: features the customer uses,
      struggles with or never tried; expansion interest (seats, modules, tier) with verbatim quotes; churn or contraction
      signals and competitor evaluation; whether the decision-maker attended and any champion change; contract asks (pricing,
      term, payment); the agreed next step.'
---

# Renewal call summary fields

Slash command: /renewal-call-summary-recipe

## Step 1: Set what renewal calls capture

For the meeting type Renewal, set its AI summary to extract: features the customer uses, struggles with or never tried; expansion interest (seats, modules, tier) with verbatim quotes; churn or contraction signals and competitor evaluation; whether the decision-maker attended and any champion change; contract asks (pricing, term, payment); the agreed next step.
