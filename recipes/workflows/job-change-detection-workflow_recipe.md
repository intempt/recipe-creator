---
name: job-change-detection-workflow
description: Use when a user mentions "job change detection workflow", "decision-maker movement", "champion job change", or asks for related help. Detect when a decision-maker at a customer account changes jobs (via enrichment refresh or LinkedIn signal). Branches into two plays — (a) re-establish at old account (find replacement, AE task) and (b) pursue at new account (warm intro opportunity, SDR task). The classic 'follow your champion' play.
arguments: []
intempt:
  id: job-change-detection-workflow
  version: 1.0.0
  slashCommand: /job-change-detection-workflow
  group: Workflows
  shortDescription: "Detect when a decision-maker at a customer account changes jobs (via enrichment refresh or LinkedIn signal). Branches into two plays — (a) re-establish at old account (find replacement, AE task) and (b) pursue at new account (warm intro opportunity, SDR task). The classic 'follow your champion' play."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: workflow-builder
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [signal-triggered, job-change, champion-tracking]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: external_signal_received, severity: blocking }
  invokesCommands:
    - create_workflow
    - configure_workflow_wait_until_step
    - configure_enrich_step
    - configure_workflow_branch_step
    - configure_ai_research_step
    - configure_create_task_step
    - configure_find_records_step
    - publish_workflow
  procedure:
    - step: 1
      title: Build the Job-Change Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Job-change detection and dual response'' triggered when a contact at an existing customer/deal account changes employer (detected via scheduled enrichment refresh OR signal provider webhook). Branches into two parallel plays: protect the old account, pursue the new account.'
      prompt: 'Create a workflow ''Job-change detection and dual response'' triggered when a contact at an existing customer/deal account changes employer (detected via scheduled enrichment refresh OR signal provider webhook). Branches into two parallel plays: protect the old account, pursue the new account.'
    - step: 2
      title: Daily Enrichment Refresh for Key Contacts
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: schedule
      dependsOn:
      - workflow
      description: 'Configure scheduled trigger: every Monday morning, scan all contacts marked as ''champion'' or ''economic buyer'' on active deals + customer accounts. The job-change-detection cadence is the key infrastructure for this workflow.'
      prompt: 'Configure scheduled trigger: every Monday morning, scan all contacts marked as ''champion'' or ''economic buyer'' on active deals + customer accounts. The job-change-detection cadence is the key infrastructure for this workflow.'
    - step: 3
      title: Refresh Contact Enrichment
      command: configure_enrich_step
      produces: step
      bindsAs: refresh
      dependsOn:
      - workflow
      - schedule
      description: 'Configure enrich step that refreshes employment data for tracked contacts. Most providers (Clearbit, Apollo, LinkedIn-feeds) flag when an email-domain → company mapping changes — that''s the signal. Output: list of contacts whose company changed since last refresh.'
      prompt: 'Configure enrich step that refreshes employment data for tracked contacts. Most providers (Clearbit, Apollo, LinkedIn-feeds) flag when an email-domain → company mapping changes — that''s the signal. Output: list of contacts whose company changed since last refresh.'
    - step: 4
      title: Branch by Account Relationship
      command: configure_workflow_branch_step
      produces: step
      bindsAs: branch
      dependsOn:
      - workflow
      - refresh
      description: 'Branch: was the contact at a CUSTOMER account, OPEN-DEAL account, or PROSPECT account? Each gets different downstream treatment. Customer → champion-departure rescue. Open-deal → urgent multi-threading. Prospect → warm-follow at new company.'
      prompt: 'Branch: was the contact at a CUSTOMER account, OPEN-DEAL account, or PROSPECT account? Each gets different downstream treatment. Customer → champion-departure rescue. Open-deal → urgent multi-threading. Prospect → warm-follow at new company.'
    - step: 5
      title: 'Old-Account: Find Replacement Contact'
      command: configure_ai_research_step
      produces: step
      bindsAs: find_replacement
      dependsOn:
      - workflow
      - branch
      description: 'AI research step on the customer/deal branch: scrape the old company''s leadership page + LinkedIn-via-public-search to identify likely replacement decision-makers in similar roles. Outputs 2-3 candidate names with titles and inferred contact info. Saves AE the manual hunt.'
      prompt: 'AI research step on the customer/deal branch: scrape the old company''s leadership page + LinkedIn-via-public-search to identify likely replacement decision-makers in similar roles. Outputs 2-3 candidate names with titles and inferred contact info. Saves AE the manual hunt.'
    - step: 6
      title: 'Old-Account: Create CSM/AE Task'
      command: configure_create_task_step
      produces: step
      bindsAs: old_task
      dependsOn:
      - workflow
      - find_replacement
      description: 'Create urgent task for the assigned CSM (customer) or AE (open deal): ''Your champion [Name] just left for [New Company]. Replacement candidates identified: [list]. Suggested action: warm intro through [Departed champion] if relationship is good, else cold outreach to replacement.'' SLA: contact within 5 business days — champion-gone deals stall fast.'
      prompt: 'Create urgent task for the assigned CSM (customer) or AE (open deal): ''Your champion [Name] just left for [New Company]. Replacement candidates identified: [list]. Suggested action: warm intro through [Departed champion] if relationship is good, else cold outreach to replacement.'' SLA: contact within 5 business days — champion-gone deals stall fast.'
    - step: 7
      title: 'New-Account: Match or Create'
      command: configure_find_records_step
      produces: step
      bindsAs: new_match
      dependsOn:
      - workflow
      - branch
      description: 'Find-records step on the departed-to-new-company branch: is the new company already in our CRM? If yes — link the contact, surface the relationship to the assigned AE. If no — create new Account + contact record with ''warm signal: ex-customer champion now here'' flag.'
      prompt: 'Find-records step on the departed-to-new-company branch: is the new company already in our CRM? If yes — link the contact, surface the relationship to the assigned AE. If no — create new Account + contact record with ''warm signal: ex-customer champion now here'' flag.'
    - step: 8
      title: 'New-Account: Create SDR Task'
      command: configure_create_task_step
      produces: step
      bindsAs: new_task
      dependsOn:
      - workflow
      - new_match
      description: 'Create SDR task for the new-company outreach: ''Warm signal — [Champion name] (your ally at [Old company]) just joined [New company]. Suggested outreach: congratulate the move, ask if they could use the same approach at their new role.'' Priority: HIGH (warm signals decay; reach out within 30 days of job change).'
      prompt: 'Create SDR task for the new-company outreach: ''Warm signal — [Champion name] (your ally at [Old company]) just joined [New company]. Suggested outreach: congratulate the move, ask if they could use the same approach at their new role.'' Priority: HIGH (warm signals decay; reach out within 30 days of job change).'
    - step: 9
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - old_task
      - new_task
      description: 'Validate and publish. Monitor: job-change detection volume per quarter, old-account-save rate (champion-departure deals that DIDN''T stall), new-account-conversion rate (departed-champion pursuits that became meetings). These are some of the highest-quality signals in B2B.'
      prompt: 'Validate and publish. Monitor: job-change detection volume per quarter, old-account-save rate (champion-departure deals that DIDN''T stall), new-account-conversion rate (departed-champion pursuits that became meetings). These are some of the highest-quality signals in B2B.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Job Change Detection Workflow

## Procedure

1. **Build the Job-Change Workflow** [`create_workflow`] — Create a workflow 'Job-change detection and dual response' triggered when a contact at an existing customer/deal account changes employer (detected via scheduled enrichment refresh OR signal provider webhook). Branches into two parallel plays: protect the old account, pursue the new account. → produces: workflow
2. **Daily Enrichment Refresh for Key Contacts** [`configure_workflow_wait_until_step`] — Configure scheduled trigger: every Monday morning, scan all contacts marked as 'champion' or 'economic buyer' on active deals + customer accounts. The job-change-detection cadence is the key infrastructure for this workflow. → produces: step
3. **Refresh Contact Enrichment** [`configure_enrich_step`] — Configure enrich step that refreshes employment data for tracked contacts. Most providers (Clearbit, Apollo, LinkedIn-feeds) flag when an email-domain → company mapping changes — that's the signal. Output: list of contacts whose company changed since last refresh. → produces: step
4. **Branch by Account Relationship** [`configure_workflow_branch_step`] — Branch: was the contact at a CUSTOMER account, OPEN-DEAL account, or PROSPECT account? Each gets different downstream treatment. Customer → champion-departure rescue. Open-deal → urgent multi-threading. Prospect → warm-follow at new company. → produces: step
5. **Old-Account: Find Replacement Contact** [`configure_ai_research_step`] — AI research step on the customer/deal branch: scrape the old company's leadership page + LinkedIn-via-public-search to identify likely replacement decision-makers in similar roles. Outputs 2-3 candidate names with titles and inferred contact info. Saves AE the manual hunt. → produces: step
6. **Old-Account: Create CSM/AE Task** [`configure_create_task_step`] — Create urgent task for the assigned CSM (customer) or AE (open deal): 'Your champion [Name] just left for [New Company]. Replacement candidates identified: [list]. Suggested action: warm intro through [Departed champion] if relationship is good, else cold outreach to replacement.' SLA: contact within 5 business days — champion-gone deals stall fast. → produces: step
7. **New-Account: Match or Create** [`configure_find_records_step`] — Find-records step on the departed-to-new-company branch: is the new company already in our CRM? If yes — link the contact, surface the relationship to the assigned AE. If no — create new Account + contact record with 'warm signal: ex-customer champion now here' flag. → produces: step
8. **New-Account: Create SDR Task** [`configure_create_task_step`] — Create SDR task for the new-company outreach: 'Warm signal — [Champion name] (your ally at [Old company]) just joined [New company]. Suggested outreach: congratulate the move, ask if they could use the same approach at their new role.' Priority: HIGH (warm signals decay; reach out within 30 days of job change). → produces: step
9. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: job-change detection volume per quarter, old-account-save rate (champion-departure deals that DIDN'T stall), new-account-conversion rate (departed-champion pursuits that became meetings). These are some of the highest-quality signals in B2B. → produces: workflow
