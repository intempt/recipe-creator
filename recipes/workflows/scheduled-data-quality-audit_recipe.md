---
name: scheduled-data-quality-audit
description: 'Use when a user mentions "scheduled data quality audit", "weekly data hygiene workflow", "CRM data quality automation", or asks for related help. Weekly: scan for duplicate accounts/users, stale records, missing required fields, and abandoned data → AI-suggests merges and cleanups → batch into approval queue for RevOps review. Replaces the manual ''when did we last clean the CRM?'' problem with a continuous hygiene program.'
arguments: []
intempt:
  id: scheduled-data-quality-audit
  version: 1.0.0
  slashCommand: /scheduled-data-quality-audit
  group: Workflows
  shortDescription: "Creates a weekly scheduled workflow that produces a RevOps approval queue of duplicate, stale, and missing-field CRM records with AI cleanup suggestions."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: workflow-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [data-hygiene, scheduled-audit, crm-cleanup]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_workflow
    - configure_workflow_wait_until_step
    - configure_find_records_step
    - configure_ai_research_step
    - configure_webhook_step
    - configure_slack_step
    - publish_workflow
  procedure:
    - step: 1
      title: Build the Audit Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Weekly data quality audit'' that scans the CRM for hygiene issues and produces a structured cleanup queue. Goal: replace the ad-hoc ''we should clean the CRM someday'' problem with a continuous, low-effort hygiene program.'
      prompt: 'Create a workflow ''Weekly data quality audit'' that scans the CRM for hygiene issues and produces a structured cleanup queue. Goal: replace the ad-hoc ''we should clean the CRM someday'' problem with a continuous, low-effort hygiene program.'
    - step: 2
      title: Weekly Scheduled Trigger
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: schedule
      dependsOn:
      - workflow
      description: 'Configure scheduled trigger: every Sunday night, run the full audit so the cleanup queue is ready for RevOps Monday morning. Skip if last audit completed within 5 days (avoid duplicate work).'
      prompt: 'Configure scheduled trigger: every Sunday night, run the full audit so the cleanup queue is ready for RevOps Monday morning. Skip if last audit completed within 5 days (avoid duplicate work).'
    - step: 3
      title: Find Potential Duplicates
      command: configure_find_records_step
      produces: step
      bindsAs: dups
      dependsOn:
      - workflow
      - schedule
      description: 'Configure find-records step that identifies likely duplicate Accounts (same domain, similar names, same legal name with different formatting) and likely duplicate Users (same email, same name+phone). Outputs: list of duplicate-candidate pairs/groups with similarity score.'
      prompt: 'Configure find-records step that identifies likely duplicate Accounts (same domain, similar names, same legal name with different formatting) and likely duplicate Users (same email, same name+phone). Outputs: list of duplicate-candidate pairs/groups with similarity score.'
    - step: 4
      title: Find Stale Records
      command: configure_find_records_step
      produces: step
      bindsAs: stale
      dependsOn:
      - workflow
      - schedule
      description: 'Configure second find-records step for stale data: Accounts with no activity in 365+ days that aren''t customers, Users with bounced emails older than 90 days, Deals stuck in early stages for 180+ days. These aren''t always cuts — sometimes just need re-engagement — but they bloat reporting and slow segmentation. Outputs the staleness list with category labels.'
      prompt: 'Configure second find-records step for stale data: Accounts with no activity in 365+ days that aren''t customers, Users with bounced emails older than 90 days, Deals stuck in early stages for 180+ days. These aren''t always cuts — sometimes just need re-engagement — but they bloat reporting and slow segmentation. Outputs the staleness list with category labels.'
    - step: 5
      title: Find Missing Required Fields
      command: configure_find_records_step
      produces: step
      bindsAs: missing
      dependsOn:
      - workflow
      - schedule
      description: 'Configure third find-records step for incomplete records: Accounts missing industry / size / region, Users missing role / company, Deals missing close-date / amount. Outputs list of incomplete records by completeness category — informs whether to trigger enrichment workflows or queue for manual review.'
      prompt: 'Configure third find-records step for incomplete records: Accounts missing industry / size / region, Users missing role / company, Deals missing close-date / amount. Outputs list of incomplete records by completeness category — informs whether to trigger enrichment workflows or queue for manual review.'
    - step: 6
      title: AI-Suggest Merges and Cleanups
      command: configure_ai_research_step
      produces: step
      bindsAs: suggest
      dependsOn:
      - workflow
      - dups
      - stale
      - missing
      description: 'Configure AI research step that examines the duplicate candidates and suggests merge actions: which record is the survivor (most-complete, most-recent activity), what data to merge in from the duplicate, what conflicts to flag for human resolution (e.g. different industry classifications between dup records). Outputs structured merge-suggestions with confidence scores.'
      prompt: 'Configure AI research step that examines the duplicate candidates and suggests merge actions: which record is the survivor (most-complete, most-recent activity), what data to merge in from the duplicate, what conflicts to flag for human resolution (e.g. different industry classifications between dup records). Outputs structured merge-suggestions with confidence scores.'
    - step: 7
      title: Send to Approval Queue
      command: configure_webhook_step
      produces: step
      bindsAs: queue
      dependsOn:
      - workflow
      - suggest
      description: 'Configure webhook step that hands off the merge-and-cleanup queue to the bulk-update-review-workflow for human approval. Includes: total findings count, summary by category, AI-confidence distribution, links to the underlying records. RevOps reviews Monday morning, approves the high-confidence batch, manually handles the edge cases.'
      prompt: 'Configure webhook step that hands off the merge-and-cleanup queue to the bulk-update-review-workflow for human approval. Includes: total findings count, summary by category, AI-confidence distribution, links to the underlying records. RevOps reviews Monday morning, approves the high-confidence batch, manually handles the edge cases.'
    - step: 8
      title: Post Weekly Hygiene Report
      command: configure_slack_step
      produces: step
      bindsAs: report
      dependsOn:
      - workflow
      - suggest
      - queue
      description: 'Configure Slack step posting the weekly hygiene report to #revops: duplicate count, stale count, incompleteness rate, week-over-week trends. Highlights celebrations (CRM completeness up 3%) and concerns (stale-record pile growing — symptom of slow follow-up upstream). Surfaces hygiene as an ongoing program, not a fire drill.'
      prompt: 'Configure Slack step posting the weekly hygiene report to #revops: duplicate count, stale count, incompleteness rate, week-over-week trends. Highlights celebrations (CRM completeness up 3%) and concerns (stale-record pile growing — symptom of slow follow-up upstream). Surfaces hygiene as an ongoing program, not a fire drill.'
    - step: 9
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - report
      description: 'Validate and publish. Monitor: weekly run completion, find-volume trends (a growing pile suggests upstream issues — sales not closing out leads, no enrichment on signup), and post-cleanup CRM-completeness metric. The hygiene KPI nobody had before this workflow.'
      prompt: 'Validate and publish. Monitor: weekly run completion, find-volume trends (a growing pile suggests upstream issues — sales not closing out leads, no enrichment on signup), and post-cleanup CRM-completeness metric. The hygiene KPI nobody had before this workflow.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Scheduled Data Quality Audit

## Procedure

1. **Build the Audit Workflow** [`create_workflow`] — Create a workflow 'Weekly data quality audit' that scans the CRM for hygiene issues and produces a structured cleanup queue. Goal: replace the ad-hoc 'we should clean the CRM someday' problem with a continuous, low-effort hygiene program. → produces: workflow
2. **Weekly Scheduled Trigger** [`configure_workflow_wait_until_step`] — Configure scheduled trigger: every Sunday night, run the full audit so the cleanup queue is ready for RevOps Monday morning. Skip if last audit completed within 5 days (avoid duplicate work). → produces: step
3. **Find Potential Duplicates** [`configure_find_records_step`] — Configure find-records step that identifies likely duplicate Accounts (same domain, similar names, same legal name with different formatting) and likely duplicate Users (same email, same name+phone). Outputs: list of duplicate-candidate pairs/groups with similarity score. → produces: step
4. **Find Stale Records** [`configure_find_records_step`] — Configure second find-records step for stale data: Accounts with no activity in 365+ days that aren't customers, Users with bounced emails older than 90 days, Deals stuck in early stages for 180+ days. These aren't always cuts — sometimes just need re-engagement — but they bloat reporting and slow segmentation. Outputs the staleness list with category labels. → produces: step
5. **Find Missing Required Fields** [`configure_find_records_step`] — Configure third find-records step for incomplete records: Accounts missing industry / size / region, Users missing role / company, Deals missing close-date / amount. Outputs list of incomplete records by completeness category — informs whether to trigger enrichment workflows or queue for manual review. → produces: step
6. **AI-Suggest Merges and Cleanups** [`configure_ai_research_step`] — Configure AI research step that examines the duplicate candidates and suggests merge actions: which record is the survivor (most-complete, most-recent activity), what data to merge in from the duplicate, what conflicts to flag for human resolution (e.g. different industry classifications between dup records). Outputs structured merge-suggestions with confidence scores. → produces: step
7. **Send to Approval Queue** [`configure_webhook_step`] — Configure webhook step that hands off the merge-and-cleanup queue to the bulk-update-review-workflow for human approval. Includes: total findings count, summary by category, AI-confidence distribution, links to the underlying records. RevOps reviews Monday morning, approves the high-confidence batch, manually handles the edge cases. → produces: step
8. **Post Weekly Hygiene Report** [`configure_slack_step`] — Configure Slack step posting the weekly hygiene report to #revops: duplicate count, stale count, incompleteness rate, week-over-week trends. Highlights celebrations (CRM completeness up 3%) and concerns (stale-record pile growing — symptom of slow follow-up upstream). Surfaces hygiene as an ongoing program, not a fire drill. → produces: step
9. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: weekly run completion, find-volume trends (a growing pile suggests upstream issues — sales not closing out leads, no enrichment on signup), and post-cleanup CRM-completeness metric. The hygiene KPI nobody had before this workflow. → produces: workflow
