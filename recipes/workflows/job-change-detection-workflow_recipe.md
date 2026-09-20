---
name: job-change-detection-workflow
description: Use when a user mentions "job change detection workflow", "decision-maker movement", "champion job change", or asks for related help. Detect when a decision-maker at a customer account changes jobs (via enrichment refresh or LinkedIn signal). Branches into two plays, (a) re-establish at old account (find replacement, AE task) and (b) pursue at new account (warm intro opportunity, SDR task). The classic 'follow your champion' play.
arguments: []
intempt:
  id: job-change-detection-workflow
  title: "Follow a champion who moves"
  version: 1.0.0
  slashCommand: /job-change-detection-workflow
  group: Workflows
  shortDescription: "Spots when a champion changes employer and runs both plays: protect the account they left, and chase the one they joined."
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
      title: "Run both plays on a move"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Triggered when a contact at a customer or open deal account changes employer, picked up by a scheduled enrichment refresh or a signal provider. It splits into two parallel plays: protect the old account, pursue the new one."
      prompt: 'Create a workflow ''Job-change detection and dual response'' triggered when a contact at an existing customer/deal account changes employer (detected via scheduled enrichment refresh OR signal provider webhook). Branches into two parallel plays: protect the old account, pursue the new account.'
    - step: 2
      title: "Scan champions every Monday"
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: schedule
      dependsOn:
      - workflow
      description: "Weekly, it goes through every contact marked champion or economic buyer on an active deal or a customer account. That cadence is the engine behind the whole workflow."
      prompt: 'Configure scheduled trigger: every Monday morning, scan all contacts marked as ''champion'' or ''economic buyer'' on active deals + customer accounts. The job-change-detection cadence is the key infrastructure for this workflow.'
    - step: 3
      title: "Refresh where they work"
      command: configure_enrich_step
      produces: step
      bindsAs: refresh
      dependsOn:
      - workflow
      - schedule
      description: "Employment data is refreshed for the tracked contacts, and most providers flag it when the mapping between an email domain and a company changes. The output is the list of people whose company has changed since the last run."
      prompt: 'Configure enrich step that refreshes employment data for tracked contacts. Most providers (Clearbit, Apollo, LinkedIn-feeds) flag when an email-domain to company mapping changes: that''s the signal. Output: list of contacts whose company changed since last refresh.'
    - step: 4
      title: "Split by kind of account"
      command: configure_workflow_branch_step
      produces: step
      bindsAs: branch
      dependsOn:
      - workflow
      - refresh
      description: "A customer account goes to the departure rescue, an open deal to urgent multi threading, and a prospect to a warm follow at the new company."
      prompt: 'Branch: was the contact at a CUSTOMER account, OPEN-DEAL account, or PROSPECT account? Each gets different downstream treatment. Customer to champion-departure rescue. Open-deal to urgent multi-threading. Prospect to warm-follow at new company.'
    - step: 5
      title: "Find who replaces them"
      command: configure_ai_research_step
      produces: step
      bindsAs: find_replacement
      dependsOn:
      - workflow
      - branch
      description: "On the customer and deal branches, the old company's leadership page and public search are read for two or three likely replacements in similar roles, with titles and inferred contact details, so the rep does not have to hunt."
      prompt: 'AI research step on the customer/deal branch: scrape the old company''s leadership page + LinkedIn-via-public-search to identify likely replacement decision-makers in similar roles. Outputs 2-3 candidate names with titles and inferred contact info. Saves AE the manual hunt.'
    - step: 6
      title: "Tell the CSM or AE to act"
      command: configure_create_task_step
      produces: step
      bindsAs: old_task
      dependsOn:
      - workflow
      - find_replacement
      description: "An urgent task naming who left, where they went and the replacement candidates, suggesting a warm introduction through the departed champion if the relationship was good and cold outreach to the replacement if it was not. Contact within five working days, because deals without a champion stall fast."
      prompt: 'Create urgent task for the assigned CSM (customer) or AE (open deal): ''Your champion [Name] just left for [New Company]. Replacement candidates identified: [list]. Suggested action: warm intro through [Departed champion] if relationship is good, else cold outreach to replacement.'' SLA: contact within 5 business days: champion-gone deals stall fast.'
    - step: 7
      title: "Check if we know the new firm"
      command: configure_find_records_step
      produces: step
      bindsAs: new_match
      dependsOn:
      - workflow
      - branch
      description: "If their new employer is already an account, the contact is linked and the relationship surfaced to the AE. If not, an account and contact are created, flagged as a warm signal because a champion from an existing customer now works there."
      prompt: 'Find-records step on the departed-to-new-company branch: is the new company already in our CRM? If yes (link the contact, surface the relationship to the assigned AE. If no) create new Account + contact record with ''warm signal: ex-customer champion now here'' flag.'
    - step: 8
      title: "Chase them at the new place"
      command: configure_create_task_step
      produces: step
      bindsAs: new_task
      dependsOn:
      - workflow
      - new_match
      description: "An SDR task explaining the connection and suggesting they congratulate the move and ask whether the same approach would help in the new role. High priority, because warm signals decay within about 30 days."
      prompt: 'Create SDR task for the new-company outreach: ''Warm signal: [Champion name] (your ally at [Old company]) just joined [New company]. Suggested outreach: congratulate the move, ask if they could use the same approach at their new role.'' Priority: HIGH (warm signals decay; reach out within 30 days of job change).'
    - step: 9
      title: "Publish and track both sides"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - old_task
      - new_task
      description: "Validated and published, tracking job changes detected each quarter, how many of the affected deals avoid stalling, and how many pursuits at the new company turn into meetings."
      prompt: 'Validate and publish. Monitor: job-change detection volume per quarter, old-account-save rate (champion-departure deals that DIDN''T stall), new-account-conversion rate (departed-champion pursuits that became meetings). These are some of the highest-quality signals in B2B.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Follow a champion who moves

Spots when a champion changes employer and runs both plays: protect the account they left, and chase the one they joined.

## Before you run it

- Send the `external_signal_received` event

## What it does

1. **Run both plays on a move** (`create_workflow`)

   Triggered when a contact at a customer or open deal account changes employer, picked up by a scheduled enrichment refresh or a signal provider. It splits into two parallel plays: protect the old account, pursue the new one.

2. **Scan champions every Monday** (`configure_workflow_wait_until_step`)

   Weekly, it goes through every contact marked champion or economic buyer on an active deal or a customer account. That cadence is the engine behind the whole workflow.

3. **Refresh where they work** (`configure_enrich_step`)

   Employment data is refreshed for the tracked contacts, and most providers flag it when the mapping between an email domain and a company changes. The output is the list of people whose company has changed since the last run.

4. **Split by kind of account** (`configure_workflow_branch_step`)

   A customer account goes to the departure rescue, an open deal to urgent multi threading, and a prospect to a warm follow at the new company.

5. **Find who replaces them** (`configure_ai_research_step`)

   On the customer and deal branches, the old company's leadership page and public search are read for two or three likely replacements in similar roles, with titles and inferred contact details, so the rep does not have to hunt.

6. **Tell the CSM or AE to act** (`configure_create_task_step`)

   An urgent task naming who left, where they went and the replacement candidates, suggesting a warm introduction through the departed champion if the relationship was good and cold outreach to the replacement if it was not. Contact within five working days, because deals without a champion stall fast.

7. **Check if we know the new firm** (`configure_find_records_step`)

   If their new employer is already an account, the contact is linked and the relationship surfaced to the AE. If not, an account and contact are created, flagged as a warm signal because a champion from an existing customer now works there.

8. **Chase them at the new place** (`configure_create_task_step`)

   An SDR task explaining the connection and suggesting they congratulate the move and ask whether the same approach would help in the new role. High priority, because warm signals decay within about 30 days.

9. **Publish and track both sides** (`publish_workflow`)

   Validated and published, tracking job changes detected each quarter, how many of the affected deals avoid stalling, and how many pursuits at the new company turn into meetings.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
