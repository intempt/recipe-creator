---
frontmatter_id: champion-change-detection
slash_command: /champion-change-detection
description: Flags when a deal contact goes quiet using engagement recency, and triggers a rep re-engagement workflow before the deal stalls.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: placeholder
  parameters:
  - name: active_window
    type: duration
    label: Window for active champion response
    default: 21 d
    required: false
  - name: quiet_window
    type: duration
    label: Window after which champion is quiet
    default: 45 d
    required: false
  - name: recent_gone_window
    type: duration
    label: Lookback for newly GONE champions
    default: 7 d
    required: false
  - name: warm_contact_window
    type: duration
    label: Window for other active contact engagement
    default: 30 d
    required: false
  - name: escalation_window
    type: duration
    label: GONE duration before escalation
    default: 14 d
    required: false
  requirements:
  - slot: deal_object
    kind: event
    meaning: A deal record in the CRM with its stage, owner, and ARR
  - slot: champion_contact
    kind: attribute
    meaning: The identified champion contact linked to a deal
  - slot: email_engagement
    kind: event
    meaning: A customer emailed or responded to outreach or an email bounced
    properties:
    - name: event_type
      type: string
      meaning: 'Kind of email event: bounce, open, reply'
      optional: false
    - name: contact_id
      type: string
      meaning: Contact the email was sent to
      optional: false
  - slot: contact_enrichment
    kind: integration
    meaning: A data enrichment source that refreshes contact job title and company
    channel: email
  - slot: champion_gone_segment
    kind: segment
    meaning: Open deals whose champion has left or gone quiet
    creatable: true
    definition: open deals where champion_status transitioned to GONE in the last {recent_gone_window}, plus open deals where
      champion_status is QUIET for more than {quiet_window}, excluding closed-lost deals
  - slot: ae_owner
    kind: attribute
    meaning: The account executive who owns the deal
    optional: true
  - slot: slack_workspace
    kind: integration
    meaning: A Slack workspace to post critical alerts to the AE and their manager
    channel: slack
  - slot: crm_deal_tags
    kind: destination
    meaning: CRM destination where deal risk tags can be written
    optional: true
    channel: hubspot
  steps:
  - id: s1
    builds: attribute
    uses:
    - deal_object
    - champion_contact
    - email_engagement
    - contact_enrichment
    - active_window
    - quiet_window
    instruction: Create a daily-refreshed AI-derived attribute 'champion_status' on {deal_object}. Set it to ACTIVE if the
      champion responded to outreach in the last {active_window}; QUIET if there was no response for {active_window} to {quiet_window};
      GONE if any hard email bounce, an explicit departure signal, an enrichment refresh showing a new company or new title
      at the same company for {champion_contact}, or an opened-but-no-reply pattern combined with an account-domain consistency
      failure is detected; otherwise UNCLEAR when the deal has no identified champion. Use {email_engagement} and {contact_enrichment}
      as inputs.
  - id: s2
    builds: segment
    uses:
    - s1
    - recent_gone_window
    - quiet_window
    instruction: Build segment 'Champion-change deals' of open deals where champion_status transitioned to GONE in the last
      {recent_gone_window}, plus open deals where champion_status has been QUIET for more than {quiet_window}. Exclude deals
      in closed-lost. Use the result of "Track the champion daily".
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - contact_enrichment
    - slack_workspace
    - crm_deal_tags
    - warm_contact_window
    - ae_owner
    instruction: 'Create a workflow that fires when champion_status transitions to GONE. (1) Identify replacement-champion
      candidates at the account with a similar role, a peer, or a manager-up contact, using {contact_enrichment}. (2) Create
      an urgent task for the AE titled ''Champion gone: re-engage stakeholders'' including the candidate list and prior deal
      context. (3) Post a critical-tier alert to {slack_workspace} addressed to the AE and their manager. (4) Set the champion-risk
      tag on the deal in {crm_deal_tags} so forecast calls reflect the risk. (5) If the account has any other active contact
      with engagement in the last {warm_contact_window}, prioritize that contact as a warm handoff. Do not send any email
      automatically; the rep must reach out personally. Use the result of "Track the champion daily" and "Find deals that
      lost theirs".'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - escalation_window
    instruction: 'Compose a champion risk dashboard showing: count of open deals by champion_status; total ARR of deals with
      GONE champions as the at-risk forecast; champion-departure rate trend; re-engagement success rate (deals that recovered
      after a champion change versus deals that were lost); and time from champion-gone alert to rep action. Add an escalation
      list of deals where the champion has been GONE for more than {escalation_window} with no rep action. Use the result
      of "Track the champion daily", "Find deals that lost theirs", and "Get the rep moving".'
---

# Champion change detection

Slash command: /champion-change-detection

## Step 1: Track the champion daily

Create an AI-derived attribute 'champion_status' on the Deal object. Compute the deal's current champion status: ACTIVE (responding to outreach in last 21 days), QUIET (no response 21-45 days), GONE (bounced email OR explicit departure signal OR LinkedIn enrichment shows new company OR new title at same company), or UNCLEAR (deal has no identified champion: separate flag). Refreshed daily. The GONE detection combines: hard email bounces, opened-but-no-reply patterns, enrichment data refresh, and account-domain consistency checks.

## Step 2: Find deals that lost theirs

Build a segment 'Champion-change deals' capturing open deals where champion_status transitioned to GONE in the last 7 days. Also includes deals where status is QUIET for 45+ days (effectively gone). Excludes deals already in closed-lost (handled separately). Use the result of "Track the champion daily".

## Step 3: Get the rep moving

Create a workflow firing when champion_status transitions to GONE. Step sequence: (1) identify replacement-champion candidates from the account (similar role, peer, manager up: pulled from enrichment); (2) create an urgent task for the AE: 'Champion gone: re-engage stakeholders' with the candidate list and prior deal context; (3) post critical-tier Slack alert to the AE and their manager (this is a deal-saving moment); (4) flag the deal in CRM with champion-risk tag so forecast calls reflect reality; (5) IF account has any other active contact (engagement signal in last 30 days), prioritize that contact as warm-handoff. Don't auto-send email: rep must reach out personally. Use the result of "Track the champion daily", "Find deals that lost theirs".

## Step 4: See the ARR behind the risk

Compose a champion risk dashboard: count of open deals by champion_status, total ARR with GONE champions (the at-risk forecast), champion-departure rate trend, re-engagement success rate (deals that recovered after champion-change vs. died), and time-to-rep-action on champion-gone alerts. Surface deals where champion has been GONE 14+ days with no rep action (escalation pile). Use the result of "Track the champion daily", "Find deals that lost theirs", "Get the rep moving".
