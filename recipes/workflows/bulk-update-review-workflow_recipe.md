---
name: bulk-update-review-workflow
description: Use when a user mentions "bulk update review workflow", "mass change approval", "batch update gate", or asks for related help. Mass field updates, record merges, or segment moves over a threshold pause for human review before execution. Shows the diff preview, allows partial approval (apply to subset), prevents the 'mass update went wrong' nightmare every RevOps team has seen.
arguments: []
intempt:
  id: bulk-update-review-workflow
  title: "Review gate for bulk updates"
  version: 1.0.0
  slashCommand: /bulk-update-review-workflow
  group: Workflows
  shortDescription: "Stops a mass field change, merge or delete above the size you set, shows a sample of before and after, and lets a reviewer approve all, some or none."
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
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
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
      title: "Gate the mass changes"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Sits in front of mass operations: field updates, record merges, segment moves and deletes touching more records than the number you set. Nothing runs until someone has seen the diff."
      prompt: 'Create a workflow ''Bulk update review gate'' that intercepts mass-change operations (record-merge suggestions, segment moves, field updates affecting >threshold records) and requires human review with diff preview before applying. Goal: prevent the ''mass update broke everything'' moment that haunts every RevOps team.'
    - step: 2
      title: "Accept the operation"
      command: configure_webhook_step
      produces: step
      bindsAs: webhook
      dependsOn:
      - workflow
      description: "A webhook that other workflows or manual operations call, carrying the kind of operation, how many records it touches, a before and after sample of the first ten, and who started it."
      prompt: 'Configure webhook trigger called by other workflows or manual operations. Payload: operation_type (field_update / record_merge / segment_move / mass_delete), record_count (must be > configurable threshold to trigger review), diff_preview (sample of before/after for first 10 records), originator (who or what initiated).'
    - step: 3
      title: "Build a sample of the diff"
      command: configure_loop_step
      produces: step
      bindsAs: sample_loop
      dependsOn:
      - workflow
      - webhook
      description: "Walks the first 20 records and shows the current value against the proposed one, so a reviewer can eyeball a sample instead of reading thousands of rows."
      prompt: 'Configure loop step that iterates over the first 20 records in the bulk operation to build a representative diff preview. For each: show current value to proposed value. This lets the reviewer eyeball a sample rather than reviewing all 500-5000 records.'
    - step: 4
      title: "Rate how risky it is"
      command: configure_ai_research_step
      produces: step
      bindsAs: risk
      dependsOn:
      - workflow
      - sample_loop
      description: "Scored low, medium, high or critical on how many records are involved, how big the change is, whether the data is personal or financial, whether it can be undone, and whether operations like it have gone wrong before, with the specific concerns spelled out."
      prompt: 'Configure AI step that assesses the bulk operation risk based on: scope (record count), change magnitude (small field tweak vs. status reset), data sensitivity (PII / financial / lifecycle stage), reversibility (can this be undone?), and historical precedent (have similar bulk ops gone wrong?). Output: risk_score (low/medium/high/critical) + specific concerns to highlight to reviewer.'
    - step: 5
      title: "Put the diff to a human"
      command: configure_slack_step
      produces: step
      bindsAs: slack_card
      dependsOn:
      - workflow
      - risk
      - sample_loop
      description: "A review card in the RevOps channel with the summary, the record count, the risk score, the sample diff and the flagged concerns, plus approve all, approve the sample only, or reject. Critical operations also need the RevOps lead named."
      prompt: 'Configure Slack step that posts a rich review card to #revops-bulk-reviews: operation summary, record count, risk score, diff preview (sample), specific concerns flagged by AI. Interactive buttons: Approve All / Approve Sample Only / Reject. For critical-risk operations, additionally require manual @mention of RevOps lead.'
    - step: 6
      title: "Wait for the decision"
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: wait
      dependsOn:
      - workflow
      - slack_card
      description: "Paused until someone answers: 24 hours for a normal operation, 4 for a high risk one, which should never sit overnight. A timeout rejects it and escalates to the RevOps lead."
      prompt: 'Configure wait-until step: pause until approval decision received. Timeout: 24 hours for normal ops, 4 hours for high-risk (high-risk should not sit overnight). On timeout: default-reject + escalate to RevOps lead.'
    - step: 7
      title: "Apply all, some or nothing"
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: branch
      dependsOn:
      - workflow
      - wait
      description: "Approve all runs on every record. Approve the sample runs on the 20 shown and holds the rest back. Reject archives the operation and tells whoever asked why. A timeout counts as a rejection plus an escalation."
      prompt: 'Multi-split: APPROVE-ALL to execute on all records; APPROVE-SAMPLE to execute only on the 20 sample records, hold the rest for further review (most cautious option); REJECT to archive operation + notify originator with reason; TIMEOUT to treated as reject + escalation. Each branch routes accordingly.'
    - step: 8
      title: "Run it and keep the receipts"
      command: configure_webhook_step
      produces: step
      bindsAs: execute
      dependsOn:
      - workflow
      - branch
      description: "Calls back to the originating workflow with the approved scope and logs the time, the approver, the record count and the origin, along with a snapshot of the previous values so the whole thing can be reversed within 24 hours."
      prompt: 'Configure execution step that calls back to the originator workflow with the approval scope (all / sample-only). Logs: operation executed at [time], approver [name], scope [count], originator [workflow]. Full audit trail. Includes rollback metadata (snapshot of pre-change values) so a mass-revert is possible if needed within 24 hours.'
    - step: 9
      title: "Publish and watch rollbacks"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - execute
      description: "Validated and published, with bulk operations per week, the approval rate, which flags a source making bad suggestions, the average time to a decision, and the rollback rate after execution, typically under 2% with the gate and over 10% without."
      prompt: 'Validate and publish. Monitor: bulk-op volume per week, approval-rate distribution (high rejection rate = upstream sources making bad suggestions), avg time-to-decision, post-execution rollback rate (the chart that proves the review gate''s value: typically <2% with review, 10%+ without).'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Review gate for bulk updates

Stops a mass field change, merge or delete above the size you set, shows a sample of before and after, and lets a reviewer approve all, some or none.

## Before you run it

- Connect slack

## What it does

1. **Gate the mass changes** (`create_workflow`)

   Sits in front of mass operations: field updates, record merges, segment moves and deletes touching more records than the number you set. Nothing runs until someone has seen the diff.

2. **Accept the operation** (`configure_webhook_step`)

   A webhook that other workflows or manual operations call, carrying the kind of operation, how many records it touches, a before and after sample of the first ten, and who started it.

3. **Build a sample of the diff** (`configure_loop_step`)

   Walks the first 20 records and shows the current value against the proposed one, so a reviewer can eyeball a sample instead of reading thousands of rows.

4. **Rate how risky it is** (`configure_ai_research_step`)

   Scored low, medium, high or critical on how many records are involved, how big the change is, whether the data is personal or financial, whether it can be undone, and whether operations like it have gone wrong before, with the specific concerns spelled out.

5. **Put the diff to a human** (`configure_slack_step`)

   A review card in the RevOps channel with the summary, the record count, the risk score, the sample diff and the flagged concerns, plus approve all, approve the sample only, or reject. Critical operations also need the RevOps lead named.

6. **Wait for the decision** (`configure_workflow_wait_until_step`)

   Paused until someone answers: 24 hours for a normal operation, 4 for a high risk one, which should never sit overnight. A timeout rejects it and escalates to the RevOps lead.

7. **Apply all, some or nothing** (`configure_workflow_multi_split_step`)

   Approve all runs on every record. Approve the sample runs on the 20 shown and holds the rest back. Reject archives the operation and tells whoever asked why. A timeout counts as a rejection plus an escalation.

8. **Run it and keep the receipts** (`configure_webhook_step`)

   Calls back to the originating workflow with the approved scope and logs the time, the approver, the record count and the origin, along with a snapshot of the previous values so the whole thing can be reversed within 24 hours.

9. **Publish and watch rollbacks** (`publish_workflow`)

   Validated and published, with bulk operations per week, the approval rate, which flags a source making bad suggestions, the average time to a decision, and the rollback rate after execution, typically under 2% with the gate and over 10% without.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
