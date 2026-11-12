---
frontmatter_id: dormant-high-ltv-concierge
slash_command: /dormant-high-ltv-concierge
description: When one of your most valuable accounts stops showing up for a month, it briefs the CSM and asks them to call. Nothing is sent automatically.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: When a top-value account goes quiet for a month, the CSM gets an urgent briefing task and manager alert to call,
    with a retention dashboard tracking results. Nothing is sent automatically.
  parameters:
  - name: dormancy_threshold
    type: duration
    label: Days without session activity before an account counts as dormant
    default: 30 d
    required: false
  - name: ltv_top_percent
    type: number
    label: Top percentile by LTV that counts as high-LTV
    default: 10
    required: false
  - name: csm_contact_window
    type: duration
    label: Window in which a recent CSM contact rules out dormancy
    default: 30 d
    required: false
  - name: response_target
    type: duration
    label: Target CSM response time on dormancy alerts
    default: 48 h
    required: false
  - name: re_engagement_window
    type: duration
    label: Window after CSM outreach to count re-engagement
    default: 14 d
    required: false
  - name: churn_window
    type: duration
    label: Window for measuring churn after dormancy
    default: 90 d
    required: false
  requirements:
  - slot: account_session_event
    kind: event
    meaning: A user started a session on a customer account
    properties:
    - name: account_id
      type: string
      meaning: Account the session belongs to
      optional: false
  - slot: account_revenue_attributes
    kind: attribute
    meaning: 'Account revenue fields: cumulative paid revenue and current monthly recurring revenue'
  - slot: csm_contact_record
    kind: event
    meaning: A CSM logged a contact or meeting with a customer account
    properties:
    - name: contact_date
      type: date
      meaning: Date of the CSM contact
      optional: false
  - slot: pause_status_attribute
    kind: attribute
    meaning: Account flag marking a known temporary pause such as legal review or annual leave
    optional: true
  - slot: high_ltv_dormant_accounts
    kind: segment
    meaning: Accounts in the top LTV tier with no session activity for the dormancy threshold and no recent CSM contact
    creatable: true
    definition: accounts where account_ltv is in the top {ltv_top_percent} percent AND days_dormant is at least {dormancy_threshold}
      AND no CSM contact in the last {csm_contact_window}, excluding accounts flagged with a temporary pause status
  - slot: crm_account_record
    kind: integration
    meaning: CRM system where account risk tags can be written
    channel: hubspot
  - slot: slack_workspace
    kind: integration
    meaning: Slack workspace used to message CSMs and their managers
    channel: slack
  - slot: csm_task_queue
    kind: destination
    meaning: Task queue where urgent CSM follow-up tasks are created
    channel: hubspot
  - slot: support_ticket_data
    kind: knowledge
    meaning: Recent support tickets and last meeting summaries for customer accounts
    optional: true
  steps:
  - id: s1
    builds: attribute
    instruction: Create AI-derived attributes on the account object. 'days_dormant' is the number of days since the last session
      start by any user on the account. 'account_ltv' is cumulative revenue paid plus projected forward LTV, calculated as
      current MRR from {account_revenue_attributes} multiplied by the historical retention curve for similar accounts. Mark
      accounts in the top {ltv_top_percent} percent of customers by account_ltv as high-LTV. Refresh both attributes daily.
      Session starts come from {account_session_event.account_id}.
  - id: s2
    builds: segment
    uses:
    - s1
    - high_ltv_dormant_accounts
    - pause_status_attribute
    - csm_contact_record
    instruction: Build the segment {high_ltv_dormant_accounts} using the attributes from "Track dormancy and value". Include
      accounts where account_ltv is in the top {ltv_top_percent} percent AND days_dormant is at least {dormancy_threshold}
      AND there is no CSM contact in the last {csm_contact_window}. Exclude accounts with a known temporary pause status from
      {pause_status_attribute}, such as paused for legal review or team on annual leave, which CSMs flag separately.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - high_ltv_dormant_accounts
    - support_ticket_data
    - csm_task_queue
    - slack_workspace
    - crm_account_record
    instruction: 'Create a workflow that runs daily for newly dormant accounts in {high_ltv_dormant_accounts} from "Find the
      valuable ones gone quiet". Step 1: refresh account context, including usage trajectory (was usage declining before the
      account went dormant?), recent tickets from {support_ticket_data}, and the last meeting summary. Step 2: compose a context
      note for the CSM with days dormant, last activity date, any decline pattern, recent support topics, and a suggested
      outreach angle (check-in, re-onboarding offer, or executive sponsor introduction). Step 3: create an urgent CSM task
      in {csm_task_queue} with the full context attached. Step 4: send a Slack direct message to the assigned CSM and their
      manager in {slack_workspace}, since high-LTV dormancy is escalation-worthy. Step 5: tag the account in {crm_account_record}
      as ''churn-risk: dormant''. Do not send any customer email automatically; outreach must be personal.'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - response_target
    - re_engagement_window
    - churn_window
    instruction: 'Build a VIP retention dashboard using the data from "Track dormancy and value", "Find the valuable ones
      gone quiet", and "Brief the CSM and escalate". Show: the count of accounts in the high-LTV dormant segment; ARR at risk
      in that segment; CSM response time on dormancy alerts against a target of {response_target}; re-engagement success rate,
      meaning accounts that return to active within {re_engagement_window} of CSM outreach; and {churn_window} churn rate
      split into accounts with CSM contact within {response_target} of dormancy versus accounts with no CSM contact.'
---

# Concierge for dormant big accounts

Slash command: /dormant-high-ltv-concierge

## Step 1: Track dormancy and value

Create AI-derived attributes on the Account object: 'days_dormant' (days since last Session start by ANY user on the account) and 'account_ltv' (cumulative revenue paid, plus projected forward LTV based on current MRR × historical retention curve for similar accounts). LTV tier: top 10% of customers by LTV = high-LTV. Refreshed daily.

## Step 2: Find the valuable ones gone quiet

Build a segment 'Dormant high-LTV accounts' capturing accounts where account_ltv is in the top 10% AND days_dormant >= 30 AND the account has not had CSM contact in last 30 days. Excludes accounts with a known temporary-pause status (e.g. 'paused for legal review', 'team on annual leave', these are flagged by CSM separately). Use the result of "Track dormancy and value".

## Step 3: Brief the CSM and escalate

Create a workflow firing daily for newly-dormant high-LTV accounts. Step sequence: (1) refresh account context: usage trajectory (was it declining before going dormant?), recent support tickets, last meeting summary; (2) compose a context blob for CSM with: dormancy days, last activity date, decline pattern if any, recent support topics, suggested outreach angle (check-in / re-onboarding offer / executive sponsor intro); (3) create urgent CSM task with full context attached; (4) post Slack DM to the named CSM + their manager (high-LTV dormancy is escalation-worthy); (5) tag account in CRM as 'churn-risk: dormant' for forecast visibility. Don't auto-send any email: concierge outreach must be personal. Use the result of "Track dormancy and value", "Find the valuable ones gone quiet".

## Step 4: Prove the call is worth making

Compose a VIP retention dashboard: count of high-LTV dormant accounts (the at-risk pile), ARR at risk in this segment, CSM response time on dormancy alerts (target: <48hr), re-engagement success rate (dormant-account-to-active-again within 14 days of CSM outreach), and 90-day churn rate split by 'CSM contacted within 48hr of dormancy' vs. 'no CSM contact': typically the gap is dramatic and proves the workflow's value. Use the result of "Track dormancy and value", "Find the valuable ones gone quiet", "Brief the CSM and escalate".
