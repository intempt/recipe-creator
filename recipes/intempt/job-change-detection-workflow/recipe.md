---
frontmatter_id: job-change-detection-workflow
slash_command: /job-change-detection-workflow
description: 'Given a known contact job change, routes two task plays: an AE task to protect the old account and an SDR task to pursue the new account.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: When a known champion or economic buyer changes employer, the customer gets an urgent AE/CSM save task for the
    old account and an SDR warm-outreach task for the new one.
  parameters:
  - name: scan_day
    type: enum
    label: Weekly scan day
    default: monday
    required: false
    options:
    - monday
    - tuesday
    - wednesday
    - thursday
    - friday
  - name: sla_business_days
    type: number
    label: Days allowed to contact after a move (business days)
    default: 5
    required: false
  - name: warm_window
    type: duration
    label: Window to reach out at the new company after job change
    default: 30 d
    required: false
  requirements:
  - slot: champion_contact
    kind: attribute
    meaning: A contact is marked as champion or economic buyer on an active deal or customer account
  - slot: job_change_event
    kind: event
    meaning: A contact changed employer
    properties:
    - name: previous_company
      type: string
      meaning: Employer before the change
      optional: false
    - name: new_company
      type: string
      meaning: Employer after the change
      optional: false
    - name: change_date
      type: date
      meaning: Date the job change was detected
      optional: true
  - slot: enrichment_integration
    kind: integration
    meaning: A contact enrichment provider that refreshes employment data on tracked contacts
    channel: email
  - slot: crm_accounts
    kind: integration
    meaning: CRM connection holding accounts, deals and contacts
    channel: hubspot
  - slot: customer_account_segment
    kind: segment
    meaning: Accounts that are existing customers
  - slot: open_deal_segment
    kind: segment
    meaning: Accounts with an open deal
  - slot: ae_owner
    kind: attribute
    meaning: The AE or CSM assigned to an account
  - slot: sdr_team
    kind: attribute
    meaning: The SDR assigned to prospect outreach at a new company
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - champion_contact
    - job_change_event
    - enrichment_integration
    instruction: 'Create a workflow named ''Job-change detection and dual response'' triggered when a contact at an existing
      customer or open-deal account changes employer, detected either by a scheduled enrichment refresh or by a signal provider
      webhook. Branch into two parallel plays: protect the old account and pursue the new account.'
  - id: s2
    builds: automation
    uses:
    - s1
    - champion_contact
    instruction: Configure a scheduled trigger every {scan_day} morning that scans all contacts marked as champion or economic
      buyer on active deals and customer accounts. Use the job-change detection cadence from "Run both plays on a move" as
      the basis for the scan.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - enrichment_integration
    instruction: Configure an enrich step that refreshes employment data for tracked contacts. Flag a contact when its email-domain
      to company mapping changes. Output a list of contacts whose company changed since the last refresh.
  - id: s4
    builds: automation
    uses:
    - s1
    - s3
    - customer_account_segment
    - open_deal_segment
    instruction: 'Branch each changed contact by the kind of account it was at: customer, open deal, or prospect. Route customers
      to champion-departure rescue, open deals to urgent multi-threading, and prospects to warm follow at the new company.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s4
    instruction: On the customer and open-deal branch, run AI research on the old company's leadership page and public professional
      search to identify 2 to 3 likely replacement decision-makers in similar roles, with titles and inferred contact details.
  - id: s6
    builds: task
    uses:
    - s1
    - s5
    - ae_owner
    - sla_business_days
    instruction: 'Create an urgent task for the assigned {ae_owner} (customer or open deal). Text: ''Your champion [Name]
      just left for [New Company]. Replacement candidates identified: [list]. Suggested action: warm intro through [Departed
      champion] if relationship is good, else cold outreach to replacement.'' Require contact within {sla_business_days} business
      days.'
  - id: s7
    builds: automation
    uses:
    - s1
    - s4
    - crm_accounts
    instruction: 'On the departed-to-new-company branch, find records to check whether the new company already exists in the
      CRM. If it exists, link the contact and surface the relationship to the assigned AE. If it does not, create a new account
      and contact record flagged ''warm signal: ex-customer champion now here''.'
  - id: s8
    builds: task
    uses:
    - s1
    - s7
    - sdr_team
    - warm_window
    instruction: 'Create an SDR task for the new-company outreach with the text: ''Warm signal: [Champion name] (your ally
      at [Old company]) just joined [New company]. Suggested outreach: congratulate the move, ask if they could use the same
      approach at their new role.'' Set priority HIGH and a deadline within {warm_window} of the job change.'
  - id: s9
    builds: report
    uses:
    - s1
    - s6
    - s8
    instruction: Validate and publish the workflow. Track job-change detection volume per quarter, old-account save rate (champion-departure
      deals that did not stall), and new-account conversion rate (departed-champion pursuits that became meetings).
---

# Follow a champion who moves

Slash command: /job-change-detection-workflow

## Step 1: Run both plays on a move

Create a workflow 'Job-change detection and dual response' triggered when a contact at an existing customer/deal account changes employer (detected via scheduled enrichment refresh OR signal provider webhook). Branches into two parallel plays: protect the old account, pursue the new account.

## Step 2: Scan champions every Monday

Configure scheduled trigger: every Monday morning, scan all contacts marked as 'champion' or 'economic buyer' on active deals + customer accounts. The job-change-detection cadence is the key infrastructure for this workflow. Use the result of "Run both plays on a move".

## Step 3: Refresh where they work

This step builds a workflow.
Configure enrich step that refreshes employment data for tracked contacts. Most providers (Clearbit, Apollo, LinkedIn-feeds) flag when an email-domain to company mapping changes: that's the signal. Output: list of contacts whose company changed since last refresh. Use the result of "Run both plays on a move", "Scan champions every Monday".

## Step 4: Split by kind of account

This step builds a workflow.
Branch: was the contact at a CUSTOMER account, OPEN-DEAL account, or PROSPECT account? Each gets different downstream treatment. Customer to champion-departure rescue. Open-deal to urgent multi-threading. Prospect to warm-follow at new company. Use the result of "Run both plays on a move", "Refresh where they work".

## Step 5: Find who replaces them

This step builds a workflow.
AI research step on the customer/deal branch: scrape the old company's leadership page + LinkedIn-via-public-search to identify likely replacement decision-makers in similar roles. Outputs 2-3 candidate names with titles and inferred contact info. Saves AE the manual hunt. Use the result of "Run both plays on a move", "Split by kind of account".

## Step 6: Tell the CSM or AE to act

This step builds a workflow.
Create urgent task for the assigned CSM (customer) or AE (open deal): 'Your champion [Name] just left for [New Company]. Replacement candidates identified: [list]. Suggested action: warm intro through [Departed champion] if relationship is good, else cold outreach to replacement.' SLA: contact within 5 business days: champion-gone deals stall fast. Use the result of "Run both plays on a move", "Find who replaces them".

## Step 7: Check if we know the new firm

This step builds a workflow.
Find-records step on the departed-to-new-company branch: is the new company already in our CRM? If yes (link the contact, surface the relationship to the assigned AE. If no) create new Account + contact record with 'warm signal: ex-customer champion now here' flag. Use the result of "Run both plays on a move", "Split by kind of account".

## Step 8: Chase them at the new place

This step builds a workflow.
Create SDR task for the new-company outreach: 'Warm signal: [Champion name] (your ally at [Old company]) just joined [New company]. Suggested outreach: congratulate the move, ask if they could use the same approach at their new role.' Priority: HIGH (warm signals decay; reach out within 30 days of job change). Use the result of "Run both plays on a move", "Check if we know the new firm".

## Step 9: Publish and track both sides

This step builds a workflow.
Validate and publish. Monitor: job-change detection volume per quarter, old-account-save rate (champion-departure deals that DIDN'T stall), new-account-conversion rate (departed-champion pursuits that became meetings). These are some of the highest-quality signals in B2B. Use the result of "Run both plays on a move", "Tell the CSM or AE to act", "Chase them at the new place".
