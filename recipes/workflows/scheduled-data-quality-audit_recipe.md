---
name: scheduled-data-quality-audit
description: 'Use when a user mentions "scheduled data quality audit", "weekly data hygiene workflow", "CRM data quality automation", or asks for related help. Weekly: scan for duplicate accounts/users, stale records, missing required fields, and abandoned data to AI-suggests merges and cleanups to batch into approval queue for RevOps review. Replaces the manual ''when did we last clean the CRM?'' problem with a continuous hygiene program.'
arguments: []
intempt:
  id: scheduled-data-quality-audit
  title: "Weekly CRM hygiene audit"
  version: 1.0.0
  slashCommand: /scheduled-data-quality-audit
  group: Workflows
  shortDescription: "Scans every Sunday for duplicates, stale records and missing fields, then hands RevOps a reviewed cleanup queue on Monday morning."
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
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
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
      title: "Turn cleanup into a routine"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "A weekly scan of the CRM for hygiene problems that produces a structured cleanup queue, in place of the someday we should clean the CRM problem."
      prompt: 'Create a workflow ''Weekly data quality audit'' that scans the CRM for hygiene issues and produces a structured cleanup queue. Goal: replace the ad-hoc ''we should clean the CRM someday'' problem with a continuous, low-effort hygiene program.'
    - step: 2
      title: "Run it on Sunday night"
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: schedule
      dependsOn:
      - workflow
      description: "The full audit runs overnight so the queue is ready on Monday. It skips itself if an audit finished within the last five days."
      prompt: 'Configure scheduled trigger: every Sunday night, run the full audit so the cleanup queue is ready for RevOps Monday morning. Skip if last audit completed within 5 days (avoid duplicate work).'
    - step: 3
      title: "Find the duplicates"
      command: configure_find_records_step
      produces: step
      bindsAs: dups
      dependsOn:
      - workflow
      - schedule
      description: "Accounts on the same domain, with similar names, or the same legal name formatted differently, and users on the same email or the same name and phone. Each candidate pair or group comes with a similarity score."
      prompt: 'Configure find-records step that identifies likely duplicate Accounts (same domain, similar names, same legal name with different formatting) and likely duplicate Users (same email, same name+phone). Outputs: list of duplicate-candidate pairs/groups with similarity score.'
    - step: 4
      title: "Find the stale records"
      command: configure_find_records_step
      produces: step
      bindsAs: stale
      dependsOn:
      - workflow
      - schedule
      description: "Accounts with no activity for over a year that are not customers, users whose email bounced more than 90 days ago, and deals stuck in an early stage for over 180 days. Not all of these are deletions, some just need re-engaging, but they all bloat reporting and slow segmentation."
      prompt: 'Configure second find-records step for stale data: Accounts with no activity in 365+ days that aren''t customers, Users with bounced emails older than 90 days, Deals stuck in early stages for 180+ days. These aren''t always cuts (sometimes just need re-engagement) but they bloat reporting and slow segmentation. Outputs the staleness list with category labels.'
    - step: 5
      title: "Find the gaps"
      command: configure_find_records_step
      produces: step
      bindsAs: missing
      dependsOn:
      - workflow
      - schedule
      description: "Accounts missing industry, size or region, users missing a role or company, and deals missing a close date or an amount, grouped by what is missing so you can tell whether to enrich them or look by hand."
      prompt: 'Configure third find-records step for incomplete records: Accounts missing industry / size / region, Users missing role / company, Deals missing close-date / amount. Outputs list of incomplete records by completeness category: informs whether to trigger enrichment workflows or queue for manual review.'
    - step: 6
      title: "Propose the merges"
      command: configure_ai_research_step
      produces: step
      bindsAs: suggest
      dependsOn:
      - workflow
      - dups
      - stale
      - missing
      description: "For each duplicate candidate: which record should survive, judged on how complete it is and how recently it was active, what to copy across from the other, and which conflicts a human has to settle, such as two different industry classifications. Every suggestion carries a confidence score."
      prompt: 'Configure AI research step that examines the duplicate candidates and suggests merge actions: which record is the survivor (most-complete, most-recent activity), what data to merge in from the duplicate, what conflicts to flag for human resolution (e.g. different industry classifications between dup records). Outputs structured merge-suggestions with confidence scores.'
    - step: 7
      title: "Send the queue for approval"
      command: configure_webhook_step
      produces: step
      bindsAs: queue
      dependsOn:
      - workflow
      - suggest
      description: "The merge and cleanup queue is handed to the bulk update review gate with the total findings, a summary per category, the spread of confidence and links to the records, so RevOps can approve the confident batch and handle the edge cases by hand."
      prompt: 'Configure webhook step that hands off the merge-and-cleanup queue to the bulk-update-review-workflow for human approval. Includes: total findings count, summary by category, AI-confidence distribution, links to the underlying records. RevOps reviews Monday morning, approves the high-confidence batch, manually handles the edge cases.'
    - step: 8
      title: "Report the week's hygiene"
      command: configure_slack_step
      produces: step
      bindsAs: report
      dependsOn:
      - workflow
      - suggest
      - queue
      description: "A post to the RevOps channel with the duplicate count, the stale count, the incompleteness rate and the movement week over week, saying plainly when completeness improved and when the stale pile is growing, which usually points at slow follow up upstream."
      prompt: 'Configure Slack step posting the weekly hygiene report to #revops: duplicate count, stale count, incompleteness rate, week-over-week trends. Highlights celebrations (CRM completeness up 3%) and concerns (stale-record pile growing: symptom of slow follow-up upstream). Surfaces hygiene as an ongoing program, not a fire drill.'
    - step: 9
      title: "Publish and watch the trend"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - report
      description: "Validated and published, tracking that the weekly run completes, whether the pile of findings is growing, which points at problems further upstream, and how complete the CRM is after each cleanup."
      prompt: 'Validate and publish. Monitor: weekly run completion, find-volume trends (a growing pile suggests upstream issues: sales not closing out leads, no enrichment on signup), and post-cleanup CRM-completeness metric. The hygiene KPI nobody had before this workflow.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Weekly CRM hygiene audit

Scans every Sunday for duplicates, stale records and missing fields, then hands RevOps a reviewed cleanup queue on Monday morning.

## Before you run it

- Connect slack

## What it does

1. **Turn cleanup into a routine** (`create_workflow`)

   A weekly scan of the CRM for hygiene problems that produces a structured cleanup queue, in place of the someday we should clean the CRM problem.

2. **Run it on Sunday night** (`configure_workflow_wait_until_step`)

   The full audit runs overnight so the queue is ready on Monday. It skips itself if an audit finished within the last five days.

3. **Find the duplicates** (`configure_find_records_step`)

   Accounts on the same domain, with similar names, or the same legal name formatted differently, and users on the same email or the same name and phone. Each candidate pair or group comes with a similarity score.

4. **Find the stale records** (`configure_find_records_step`)

   Accounts with no activity for over a year that are not customers, users whose email bounced more than 90 days ago, and deals stuck in an early stage for over 180 days. Not all of these are deletions, some just need re-engaging, but they all bloat reporting and slow segmentation.

5. **Find the gaps** (`configure_find_records_step`)

   Accounts missing industry, size or region, users missing a role or company, and deals missing a close date or an amount, grouped by what is missing so you can tell whether to enrich them or look by hand.

6. **Propose the merges** (`configure_ai_research_step`)

   For each duplicate candidate: which record should survive, judged on how complete it is and how recently it was active, what to copy across from the other, and which conflicts a human has to settle, such as two different industry classifications. Every suggestion carries a confidence score.

7. **Send the queue for approval** (`configure_webhook_step`)

   The merge and cleanup queue is handed to the bulk update review gate with the total findings, a summary per category, the spread of confidence and links to the records, so RevOps can approve the confident batch and handle the edge cases by hand.

8. **Report the week's hygiene** (`configure_slack_step`)

   A post to the RevOps channel with the duplicate count, the stale count, the incompleteness rate and the movement week over week, saying plainly when completeness improved and when the stale pile is growing, which usually points at slow follow up upstream.

9. **Publish and watch the trend** (`publish_workflow`)

   Validated and published, tracking that the weekly run completes, whether the pile of findings is growing, which points at problems further upstream, and how complete the CRM is after each cleanup.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
