---
frontmatter_id: bulk-update-review-workflow
slash_command: /bulk-update-review-workflow
description: Pauses mass field changes, merges, or deletes above a set size for human review before execution. The recipe creates the approval gate and routes the queued change to a reviewer.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Pauses large bulk field updates, merges, or deletes for a human reviewer who sees a diff sample and AI risk rating
    before anything is applied, with an audit trail and rollback snapshot.
  parameters:
  - name: record_threshold
    type: number
    label: Record count above which a bulk operation requires review
    default: 500
    required: false
  - name: sample_size
    type: number
    label: Number of records in the diff preview sample
    default: 20
    required: false
  - name: normal_timeout
    type: duration
    label: Decision timeout for normal-risk operations
    default: 24 h
    required: false
  - name: high_risk_timeout
    type: duration
    label: Decision timeout for high-risk operations
    default: 4 h
    required: false
  - name: rollback_window
    type: duration
    label: Window in which a mass revert is possible after execution
    default: 24 h
    required: false
  - name: review_channel_name
    type: string
    label: Slack channel for review cards
    default: '#revops-bulk-reviews'
    required: false
  requirements:
  - slot: bulk_operation_event
    kind: event
    meaning: A bulk change operation was requested (field update, record merge, segment move, or mass delete) affecting many
      records
    properties:
    - name: operation_type
      type: text
      meaning: 'Kind of bulk operation: field_update, record_merge, segment_move, or mass_delete'
      optional: false
    - name: record_count
      type: number
      meaning: Number of records the operation affects
      optional: false
    - name: diff_preview
      type: json
      meaning: Before and after values for a sample of the first affected records
      optional: true
    - name: originator
      type: text
      meaning: Who or what initiated the operation
      optional: false
  - slot: revops_slack
    kind: integration
    meaning: Slack workspace connection able to post interactive review cards to the RevOps bulk review channel
    channel: slack
  - slot: revops_lead
    kind: attribute
    meaning: The RevOps lead user who is escalated to and @mentioned for critical or timed-out operations
  steps:
  - id: s1
    builds: automation
    uses:
    - record_threshold
    instruction: Create a workflow named 'Bulk update review gate' that intercepts mass-change operations (record merge suggestions,
      segment moves, and field updates affecting more than {record_threshold} records) and holds them for human review with
      a diff preview before anything is applied.
  - id: s2
    builds: webhook
    uses:
    - s1
    - bulk_operation_event
    - record_threshold
    instruction: Configure a webhook trigger, callable by other workflows or manual operations, that accepts {bulk_operation_event.operation_type},
      {bulk_operation_event.record_count} (processed only when greater than {record_threshold}), {bulk_operation_event.diff_preview}
      and {bulk_operation_event.originator}.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - sample_size
    instruction: Loop over the first {sample_size} records in the bulk operation and, for each, show the current value next
      to the proposed value to build a representative diff preview that the reviewer can check instead of reviewing every
      record.
  - id: s4
    builds: agent
    uses:
    - s1
    - s3
    instruction: Run an AI assessment of the bulk operation's risk using scope (record count), change magnitude (small field
      tweak versus status reset), data sensitivity (personal, financial, or lifecycle stage data), reversibility, and historical
      precedent of similar bulk operations going wrong. Output a risk_score of low, medium, high, or critical and a list of
      specific concerns for the reviewer.
  - id: s5
    builds: slack
    uses:
    - s1
    - s4
    - revops_slack
    - revops_lead
    - review_channel_name
    instruction: Post a review card to {review_channel_name} via {revops_slack} containing the operation summary, record count,
      risk_score, the diff preview sample from "Build a sample of the diff", and the concerns from "Rate how risky it is".
      Include buttons Approve All, Approve Sample Only, and Reject. For critical-risk operations also @mention {revops_lead}.
  - id: s6
    builds: automation
    uses:
    - s1
    - s5
    - normal_timeout
    - high_risk_timeout
    - revops_lead
    instruction: Pause until an approval decision is received on the review card. Use a timeout of {normal_timeout} for normal
      operations and {high_risk_timeout} for high-risk or critical operations. On timeout, treat as reject and escalate to
      {revops_lead}.
  - id: s7
    builds: automation
    uses:
    - s1
    - s6
    - sample_size
    - revops_lead
    instruction: 'Branch on the decision from "Put the diff to a human": Approve All applies the change to all records; Approve
      Sample Only applies the change to the {sample_size} sample records and holds the remaining records for further review;
      Reject archives the operation and notifies the originator with the reason; Timeout is handled as reject with escalation
      to {revops_lead}.'
  - id: s8
    builds: automation
    uses:
    - s1
    - s7
    - rollback_window
    instruction: Execute the approved scope and call back the originator workflow with the approved scope (all or sample only).
      Log the execution time, approver name, scope record count, and originator workflow as a full audit trail. Store a snapshot
      of pre-change values so the change can be mass-reverted within {rollback_window}.
  - id: s9
    builds: dashboard
    uses:
    - s1
    - s8
    instruction: Validate and publish the workflow. Monitor weekly bulk-operation volume, approval-rate distribution by originator,
      average time to decision, and post-execution rollback rate.
---

# Review gate for bulk updates

Slash command: /bulk-update-review-workflow

## Step 1: Gate the mass changes

Create a workflow 'Bulk update review gate' that intercepts mass-change operations (record-merge suggestions, segment moves, field updates affecting >threshold records) and requires human review with diff preview before applying. Goal: prevent the 'mass update broke everything' moment that haunts every RevOps team.

## Step 2: Accept the operation

Configure webhook trigger called by other workflows or manual operations. Payload: operation_type (field_update / record_merge / segment_move / mass_delete), record_count (must be > configurable threshold to trigger review), diff_preview (sample of before/after for first 10 records), originator (who or what initiated). Use the result of "Gate the mass changes".

## Step 3: Build a sample of the diff

This step builds a workflow.
Configure loop step that iterates over the first 20 records in the bulk operation to build a representative diff preview. For each: show current value to proposed value. This lets the reviewer eyeball a sample rather than reviewing all 500-5000 records. Use the result of "Gate the mass changes", "Accept the operation".

## Step 4: Rate how risky it is

This step builds a workflow.
Configure AI step that assesses the bulk operation risk based on: scope (record count), change magnitude (small field tweak vs. status reset), data sensitivity (PII / financial / lifecycle stage), reversibility (can this be undone?), and historical precedent (have similar bulk ops gone wrong?). Output: risk_score (low/medium/high/critical) + specific concerns to highlight to reviewer. Use the result of "Gate the mass changes", "Build a sample of the diff".

## Step 5: Put the diff to a human

This step builds a workflow.
Configure Slack step that posts a rich review card to #revops-bulk-reviews: operation summary, record count, risk score, diff preview (sample), specific concerns flagged by AI. Interactive buttons: Approve All / Approve Sample Only / Reject. For critical-risk operations, additionally require manual @mention of RevOps lead. Use the result of "Gate the mass changes", "Rate how risky it is", "Build a sample of the diff".

## Step 6: Wait for the decision

This step builds a workflow.
Configure wait-until step: pause until approval decision received. Timeout: 24 hours for normal ops, 4 hours for high-risk (high-risk should not sit overnight). On timeout: default-reject + escalate to RevOps lead. Use the result of "Gate the mass changes", "Put the diff to a human".

## Step 7: Apply all, some or nothing

This step builds a workflow.
Multi-split: APPROVE-ALL to execute on all records; APPROVE-SAMPLE to execute only on the 20 sample records, hold the rest for further review (most cautious option); REJECT to archive operation + notify originator with reason; TIMEOUT to treated as reject + escalation. Each branch routes accordingly. Use the result of "Gate the mass changes", "Wait for the decision".

## Step 8: Run it and keep the receipts

Configure execution step that calls back to the originator workflow with the approval scope (all / sample-only). Logs: operation executed at [time], approver [name], scope [count], originator [workflow]. Full audit trail. Includes rollback metadata (snapshot of pre-change values) so a mass-revert is possible if needed within 24 hours. Use the result of "Gate the mass changes", "Apply all, some or nothing".

## Step 9: Publish and watch rollbacks

This step builds a workflow.
Validate and publish. Monitor: bulk-op volume per week, approval-rate distribution (high rejection rate = upstream sources making bad suggestions), avg time-to-decision, post-execution rollback rate (the chart that proves the review gate's value: typically <2% with review, 10%+ without). Use the result of "Gate the mass changes", "Run it and keep the receipts".
