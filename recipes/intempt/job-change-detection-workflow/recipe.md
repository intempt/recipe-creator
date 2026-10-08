---
description: 'Given a known contact job change, routes two task plays: an AE task to protect the old account and an SDR task to pursue the new account.'
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - b2b-saas
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
