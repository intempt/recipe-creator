---
name: bulk-update-review-workflow
description: Use when a user mentions "bulk update review workflow", "mass change approval", "batch update gate", or asks for related help. Mass field updates, record merges, or segment moves over a threshold pause for human review before execution. Shows the diff preview, allows partial approval (apply to subset), prevents the 'mass update went wrong' nightmare every RevOps team has seen.
arguments: []
intempt:
  id: bulk-update-review-workflow
  version: 1.0.0
  slashCommand: /bulk-update-review-workflow
  group: Workflows
  shortDescription: "Produces a workflow with steps that gate bulk field updates, merges, or segment moves over a threshold through human diff-preview and partial approval."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: workflow-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [bulk-operations, approval-gate, data-safety]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_workflow
    - configure_webhook_step
    - configure_loop_step
    - configure_ai_research_step
    - configure_slack_step
    - configure_workflow_wait_until_step
    - configure_workflow_multi_split_step
    - publish_workflow
  procedure:
    - step: 1
      title: Build the Bulk-Update Review Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Bulk update review gate'' that intercepts mass-change operations (record-merge suggestions, segment moves, field updates affecting >threshold records) and requires human review with diff preview before applying. Goal: prevent the ''mass update broke everything'' moment that haunts every RevOps team.'
      prompt: 'Create a workflow ''Bulk update review gate'' that intercepts mass-change operations (record-merge suggestions, segment moves, field updates affecting >threshold records) and requires human review with diff preview before applying. Goal: prevent the ''mass update broke everything'' moment that haunts every RevOps team.'
    - step: 2
      title: Webhook Receives Pending Bulk Operation
      command: configure_webhook_step
      produces: step
      bindsAs: webhook
      dependsOn:
      - workflow
      description: 'Configure webhook trigger called by other workflows or manual operations. Payload: operation_type (field_update / record_merge / segment_move / mass_delete), record_count (must be > configurable threshold to trigger review), diff_preview (sample of before/after for first 10 records), originator (who or what initiated).'
      prompt: 'Configure webhook trigger called by other workflows or manual operations. Payload: operation_type (field_update / record_merge / segment_move / mass_delete), record_count (must be > configurable threshold to trigger review), diff_preview (sample of before/after for first 10 records), originator (who or what initiated).'
    - step: 3
      title: Loop Through Sample for Diff
      command: configure_loop_step
      produces: step
      bindsAs: sample_loop
      dependsOn:
      - workflow
      - webhook
      description: 'Configure loop step that iterates over the first 20 records in the bulk operation to build a representative diff preview. For each: show current value → proposed value. This lets the reviewer eyeball a sample rather than reviewing all 500-5000 records.'
      prompt: 'Configure loop step that iterates over the first 20 records in the bulk operation to build a representative diff preview. For each: show current value → proposed value. This lets the reviewer eyeball a sample rather than reviewing all 500-5000 records.'
    - step: 4
      title: AI Risk Assessment
      command: configure_ai_research_step
      produces: step
      bindsAs: risk
      dependsOn:
      - workflow
      - sample_loop
      description: 'Configure AI step that assesses the bulk operation risk based on: scope (record count), change magnitude (small field tweak vs. status reset), data sensitivity (PII / financial / lifecycle stage), reversibility (can this be undone?), and historical precedent (have similar bulk ops gone wrong?). Output: risk_score (low/medium/high/critical) + specific concerns to highlight to reviewer.'
      prompt: 'Configure AI step that assesses the bulk operation risk based on: scope (record count), change magnitude (small field tweak vs. status reset), data sensitivity (PII / financial / lifecycle stage), reversibility (can this be undone?), and historical precedent (have similar bulk ops gone wrong?). Output: risk_score (low/medium/high/critical) + specific concerns to highlight to reviewer.'
    - step: 5
      title: Build Slack Review Card
      command: configure_slack_step
      produces: step
      bindsAs: slack_card
      dependsOn:
      - workflow
      - risk
      - sample_loop
      description: 'Configure Slack step that posts a rich review card to #revops-bulk-reviews: operation summary, record count, risk score, diff preview (sample), specific concerns flagged by AI. Interactive buttons: Approve All / Approve Sample Only / Reject. For critical-risk operations, additionally require manual @mention of RevOps lead.'
      prompt: 'Configure Slack step that posts a rich review card to #revops-bulk-reviews: operation summary, record count, risk score, diff preview (sample), specific concerns flagged by AI. Interactive buttons: Approve All / Approve Sample Only / Reject. For critical-risk operations, additionally require manual @mention of RevOps lead.'
    - step: 6
      title: Wait for Decision with Timeout
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: wait
      dependsOn:
      - workflow
      - slack_card
      description: 'Configure wait-until step: pause until approval decision received. Timeout: 24 hours for normal ops, 4 hours for high-risk (high-risk should not sit overnight). On timeout: default-reject + escalate to RevOps lead.'
      prompt: 'Configure wait-until step: pause until approval decision received. Timeout: 24 hours for normal ops, 4 hours for high-risk (high-risk should not sit overnight). On timeout: default-reject + escalate to RevOps lead.'
    - step: 7
      title: Branch on Decision
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: branch
      dependsOn:
      - workflow
      - wait
      description: 'Multi-split: APPROVE-ALL → execute on all records; APPROVE-SAMPLE → execute only on the 20 sample records, hold the rest for further review (most cautious option); REJECT → archive operation + notify originator with reason; TIMEOUT → treated as reject + escalation. Each branch routes accordingly.'
      prompt: 'Multi-split: APPROVE-ALL → execute on all records; APPROVE-SAMPLE → execute only on the 20 sample records, hold the rest for further review (most cautious option); REJECT → archive operation + notify originator with reason; TIMEOUT → treated as reject + escalation. Each branch routes accordingly.'
    - step: 8
      title: Execute Approved Operation
      command: configure_webhook_step
      produces: step
      bindsAs: execute
      dependsOn:
      - workflow
      - branch
      description: 'Configure execution step that calls back to the originator workflow with the approval scope (all / sample-only). Logs: operation executed at [time], approver [name], scope [count], originator [workflow]. Full audit trail. Includes rollback metadata (snapshot of pre-change values) so a mass-revert is possible if needed within 24 hours.'
      prompt: 'Configure execution step that calls back to the originator workflow with the approval scope (all / sample-only). Logs: operation executed at [time], approver [name], scope [count], originator [workflow]. Full audit trail. Includes rollback metadata (snapshot of pre-change values) so a mass-revert is possible if needed within 24 hours.'
    - step: 9
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - execute
      description: 'Validate and publish. Monitor: bulk-op volume per week, approval-rate distribution (high rejection rate = upstream sources making bad suggestions), avg time-to-decision, post-execution rollback rate (the chart that proves the review gate''s value — typically <2% with review, 10%+ without).'
      prompt: 'Validate and publish. Monitor: bulk-op volume per week, approval-rate distribution (high rejection rate = upstream sources making bad suggestions), avg time-to-decision, post-execution rollback rate (the chart that proves the review gate''s value — typically <2% with review, 10%+ without).'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Bulk Update Review Workflow

## Procedure

1. **Build the Bulk-Update Review Workflow** [`create_workflow`] — Create a workflow 'Bulk update review gate' that intercepts mass-change operations (record-merge suggestions, segment moves, field updates affecting >threshold records) and requires human review with diff preview before applying. Goal: prevent the 'mass update broke everything' moment that haunts every RevOps team. → produces: workflow
2. **Webhook Receives Pending Bulk Operation** [`configure_webhook_step`] — Configure webhook trigger called by other workflows or manual operations. Payload: operation_type (field_update / record_merge / segment_move / mass_delete), record_count (must be > configurable threshold to trigger review), diff_preview (sample of before/after for first 10 records), originator (who or what initiated). → produces: step
3. **Loop Through Sample for Diff** [`configure_loop_step`] — Configure loop step that iterates over the first 20 records in the bulk operation to build a representative diff preview. For each: show current value → proposed value. This lets the reviewer eyeball a sample rather than reviewing all 500-5000 records. → produces: step
4. **AI Risk Assessment** [`configure_ai_research_step`] — Configure AI step that assesses the bulk operation risk based on: scope (record count), change magnitude (small field tweak vs. status reset), data sensitivity (PII / financial / lifecycle stage), reversibility (can this be undone?), and historical precedent (have similar bulk ops gone wrong?). Output: risk_score (low/medium/high/critical) + specific concerns to highlight to reviewer. → produces: step
5. **Build Slack Review Card** [`configure_slack_step`] — Configure Slack step that posts a rich review card to #revops-bulk-reviews: operation summary, record count, risk score, diff preview (sample), specific concerns flagged by AI. Interactive buttons: Approve All / Approve Sample Only / Reject. For critical-risk operations, additionally require manual @mention of RevOps lead. → produces: step
6. **Wait for Decision with Timeout** [`configure_workflow_wait_until_step`] — Configure wait-until step: pause until approval decision received. Timeout: 24 hours for normal ops, 4 hours for high-risk (high-risk should not sit overnight). On timeout: default-reject + escalate to RevOps lead. → produces: step
7. **Branch on Decision** [`configure_workflow_multi_split_step`] — Multi-split: APPROVE-ALL → execute on all records; APPROVE-SAMPLE → execute only on the 20 sample records, hold the rest for further review (most cautious option); REJECT → archive operation + notify originator with reason; TIMEOUT → treated as reject + escalation. Each branch routes accordingly. → produces: step
8. **Execute Approved Operation** [`configure_webhook_step`] — Configure execution step that calls back to the originator workflow with the approval scope (all / sample-only). Logs: operation executed at [time], approver [name], scope [count], originator [workflow]. Full audit trail. Includes rollback metadata (snapshot of pre-change values) so a mass-revert is possible if needed within 24 hours. → produces: step
9. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: bulk-op volume per week, approval-rate distribution (high rejection rate = upstream sources making bad suggestions), avg time-to-decision, post-execution rollback rate (the chart that proves the review gate's value — typically <2% with review, 10%+ without). → produces: workflow
