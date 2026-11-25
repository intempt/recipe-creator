---
frontmatter_id: revenue-operations-dashboard
slash_command: /revenue-operations-dashboard
description: Emails RevOps a monthly digest of where the go-to-market machine leaks over a trailing 90 days, by source and
  stage rather than by rep, so you can move spend and fix process.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails RevOps a monthly digest of win rate, sales cycle, lead-to-won conversion and lost deals by source and stage
    over a trailing 90 days, plus subscription churn.
  parameters:
  - name: trailingWindow
    type: duration
    label: Trailing window the figures cover
    default: 90 d
    required: false
  - name: mqlStage
    type: string
    label: Lead stage value that marks an MQL
    default: MQL
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A deal was closed as won
    properties:
    - name: utm_source
      type: string
      meaning: Source the deal came from
      optional: false
  - slot: deal_lost_event
    kind: event
    meaning: A deal was closed as lost
    properties:
    - name: utm_source
      type: string
      meaning: Source the deal came from
      optional: false
    - name: stage_at_loss
      type: string
      meaning: Stage the deal was in when lost
      optional: false
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal moved from one sales stage to another
    properties:
    - name: stage
      type: string
      meaning: The new stage
      optional: false
  - slot: lead_stage_changed_event
    kind: event
    meaning: A lead moved to a new qualification stage such as MQL or SQL
    properties:
    - name: stage
      type: string
      meaning: The new stage
      optional: false
    - name: utm_source
      type: string
      meaning: Source the lead came from
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_won_event
    - deal_lost_event
    - deal_stage_changed_event
    - lead_stage_changed_event
    - subscription_started_event
    - subscription_canceled_event
    - trailingWindow
    - mqlStage
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes deals
      and leads and writes these figures: win rate, {deal_won_event} divided by {deal_won_event} plus {deal_lost_event}, in
      the last {trailingWindow} against the {trailingWindow} before, in total and per utm_source; the median days from a deal''s
      first {deal_stage_changed_event} to its {deal_won_event}, for deals won in the last {trailingWindow}; the share of leads
      that did {lead_stage_changed_event} with {lead_stage_changed_event.stage} equal to {mqlStage} between 90 and 180 days
      ago who later did {deal_won_event}, per {lead_stage_changed_event.utm_source}; won and lost deal counts per utm_source,
      with lost deals split by {deal_lost_event.stage_at_loss}; {subscription_started_event} and {subscription_canceled_event}
      counts in the last {trailingWindow}. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# GTM health and revenue leakage

Slash command: /revenue-operations-dashboard

## Step 1: Email the monthly GTM health digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes deals and leads and writes these figures: win rate, deal won event divided by deal won event plus deal lost event, in the last 90 d against the 90 d before, in total and per utm_source; the median days from a deal's first deal stage changed event to its deal won event, for deals won in the last 90 d; the share of leads that did lead stage changed event with stage equal to MQL between 90 and 180 days ago who later did deal won event, per utm source; won and lost deal counts per utm_source, with lost deals split by stage at loss; subscription started event and subscription canceled event counts in the last 90 d. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
