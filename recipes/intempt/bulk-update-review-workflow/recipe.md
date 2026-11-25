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
visibility: draft
rejected: Its purpose is intercepting bulk record changes from other workflows (webhook trigger), holding them for an interactive
  approval and executing or rolling them back; Blu has no webhook trigger and does not run record changes.
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
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
---

# Review gate for bulk updates

Slash command: /bulk-update-review-workflow

## Step 1: Gate the mass changes

Create a workflow named 'Bulk update review gate' that intercepts mass-change operations (record merge suggestions, segment moves, and field updates affecting more than 500 records) and holds them for human review with a diff preview before anything is applied.
