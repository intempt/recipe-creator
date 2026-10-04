---
id: bulk-update-review-workflow
title: Review gate for bulk updates
slash_command: /bulk-update-review-workflow
group: Workflows
owner: intempt
curator: trishik
summary: Stops a mass field change, merge or delete above the size you set, shows a sample of before and
  after, and lets a reviewer approve all, some or none.
description: >-
  Mass field updates, record merges, or segment moves over a threshold pause for human review before execution.
  Shows the diff preview, allows partial approval (apply to subset), prevents the 'mass update went wrong'
  nightmare every RevOps team has seen.
version: 2.0.0
classification:
  product:
    - sales
  agent: workflow-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - bulk-operations
    - approval-gate
    - data-safety
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new workflow, from step 1 "Gate the mass changes"
    - A new workflow, from step 2 "Accept the operation"
    - A new workflow, from step 3 "Build a sample of the diff"
    - A new workflow, from step 4 "Rate how risky it is"
    - A new workflow, from step 5 "Put the diff to a human"
    - A new workflow, from step 6 "Wait for the decision"
    - A new workflow, from step 7 "Apply all, some or nothing"
    - A new workflow, from step 8 "Run it and keep the receipts"
    - A new workflow, from step 9 "Publish and watch rollbacks"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Gate the mass changes
    summary: >-
      Sits in front of mass operations: field updates, record merges, segment moves and deletes touching
      more records than the number you set. Nothing runs until someone has seen the diff.
    builds: workflow
    description: >-
      Create a workflow 'Bulk update review gate' that intercepts mass-change operations (record-merge
      suggestions, segment moves, field updates affecting >threshold records) and requires human review
      with diff preview before applying. Goal: prevent the 'mass update broke everything' moment that
      haunts every RevOps team.
  - id: s2
    title: Accept the operation
    summary: >-
      A webhook that other workflows or manual operations call, carrying the kind of operation, how many
      records it touches, a before and after sample of the first ten, and who started it.
    builds: workflow
    description: >-
      Configure webhook trigger called by other workflows or manual operations. Payload: operation_type
      (field_update / record_merge / segment_move / mass_delete), record_count (must be > configurable
      threshold to trigger review), diff_preview (sample of before/after for first 10 records), originator
      (who or what initiated). Use the result of "Gate the mass changes".
    dependsOn:
      - s1
  - id: s3
    title: Build a sample of the diff
    summary: >-
      Walks the first 20 records and shows the current value against the proposed one, so a reviewer can
      eyeball a sample instead of reading thousands of rows.
    builds: workflow
    description: >-
      Configure loop step that iterates over the first 20 records in the bulk operation to build a representative
      diff preview. For each: show current value to proposed value. This lets the reviewer eyeball a sample
      rather than reviewing all 500-5000 records. Use the result of "Gate the mass changes", "Accept the
      operation".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Rate how risky it is
    summary: >-
      Scored low, medium, high or critical on how many records are involved, how big the change is, whether
      the data is personal or financial, whether it can be undone, and whether operations like it have
      gone wrong before, with the specific concerns spelled out.
    builds: workflow
    description: >-
      Configure AI step that assesses the bulk operation risk based on: scope (record count), change magnitude
      (small field tweak vs. status reset), data sensitivity (PII / financial / lifecycle stage), reversibility
      (can this be undone?), and historical precedent (have similar bulk ops gone wrong?). Output: risk_score
      (low/medium/high/critical) + specific concerns to highlight to reviewer. Use the result of "Gate
      the mass changes", "Build a sample of the diff".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Put the diff to a human
    summary: >-
      A review card in the RevOps channel with the summary, the record count, the risk score, the sample
      diff and the flagged concerns, plus approve all, approve the sample only, or reject. Critical operations
      also need the RevOps lead named.
    builds: workflow
    description: >-
      Configure Slack step that posts a rich review card to #revops-bulk-reviews: operation summary, record
      count, risk score, diff preview (sample), specific concerns flagged by AI. Interactive buttons:
      Approve All / Approve Sample Only / Reject. For critical-risk operations, additionally require manual
      @mention of RevOps lead. Use the result of "Gate the mass changes", "Rate how risky it is", "Build
      a sample of the diff".
    dependsOn:
      - s1
      - s4
      - s3
  - id: s6
    title: Wait for the decision
    summary: >-
      Paused until someone answers: 24 hours for a normal operation, 4 for a high risk one, which should
      never sit overnight. A timeout rejects it and escalates to the RevOps lead.
    builds: workflow
    description: >-
      Configure wait-until step: pause until approval decision received. Timeout: 24 hours for normal
      ops, 4 hours for high-risk (high-risk should not sit overnight). On timeout: default-reject + escalate
      to RevOps lead. Use the result of "Gate the mass changes", "Put the diff to a human".
    dependsOn:
      - s1
      - s5
  - id: s7
    title: Apply all, some or nothing
    summary: >-
      Approve all runs on every record. Approve the sample runs on the 20 shown and holds the rest back.
      Reject archives the operation and tells whoever asked why. A timeout counts as a rejection plus
      an escalation.
    builds: workflow
    description: >-
      Multi-split: APPROVE-ALL to execute on all records; APPROVE-SAMPLE to execute only on the 20 sample
      records, hold the rest for further review (most cautious option); REJECT to archive operation +
      notify originator with reason; TIMEOUT to treated as reject + escalation. Each branch routes accordingly.
      Use the result of "Gate the mass changes", "Wait for the decision".
    dependsOn:
      - s1
      - s6
  - id: s8
    title: Run it and keep the receipts
    summary: >-
      Calls back to the originating workflow with the approved scope and logs the time, the approver,
      the record count and the origin, along with a snapshot of the previous values so the whole thing
      can be reversed within 24 hours.
    builds: workflow
    description: >-
      Configure execution step that calls back to the originator workflow with the approval scope (all
      / sample-only). Logs: operation executed at [time], approver [name], scope [count], originator [workflow].
      Full audit trail. Includes rollback metadata (snapshot of pre-change values) so a mass-revert is
      possible if needed within 24 hours. Use the result of "Gate the mass changes", "Apply all, some
      or nothing".
    dependsOn:
      - s1
      - s7
  - id: s9
    title: Publish and watch rollbacks
    summary: >-
      Validated and published, with bulk operations per week, the approval rate, which flags a source
      making bad suggestions, the average time to a decision, and the rollback rate after execution, typically
      under 2% with the gate and over 10% without.
    builds: workflow
    description: >-
      Validate and publish. Monitor: bulk-op volume per week, approval-rate distribution (high rejection
      rate = upstream sources making bad suggestions), avg time-to-decision, post-execution rollback rate
      (the chart that proves the review gate's value: typically <2% with review, 10%+ without). Use the
      result of "Gate the mass changes", "Run it and keep the receipts".
    dependsOn:
      - s1
      - s8
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s8
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Review gate for bulk updates

Stops a mass field change, merge or delete above the size you set, shows a sample of before and after, and lets a reviewer approve all, some or none.

## Steps

1. **Gate the mass changes** (builds workflow)

   Sits in front of mass operations: field updates, record merges, segment moves and deletes touching more records than the number you set. Nothing runs until someone has seen the diff.

2. **Accept the operation** (builds workflow)

   A webhook that other workflows or manual operations call, carrying the kind of operation, how many records it touches, a before and after sample of the first ten, and who started it.

3. **Build a sample of the diff** (builds workflow)

   Walks the first 20 records and shows the current value against the proposed one, so a reviewer can eyeball a sample instead of reading thousands of rows.

4. **Rate how risky it is** (builds workflow)

   Scored low, medium, high or critical on how many records are involved, how big the change is, whether the data is personal or financial, whether it can be undone, and whether operations like it have gone wrong before, with the specific concerns spelled out.

5. **Put the diff to a human** (builds workflow)

   A review card in the RevOps channel with the summary, the record count, the risk score, the sample diff and the flagged concerns, plus approve all, approve the sample only, or reject. Critical operations also need the RevOps lead named.

6. **Wait for the decision** (builds workflow)

   Paused until someone answers: 24 hours for a normal operation, 4 for a high risk one, which should never sit overnight. A timeout rejects it and escalates to the RevOps lead.

7. **Apply all, some or nothing** (builds workflow)

   Approve all runs on every record. Approve the sample runs on the 20 shown and holds the rest back. Reject archives the operation and tells whoever asked why. A timeout counts as a rejection plus an escalation.

8. **Run it and keep the receipts** (builds workflow)

   Calls back to the originating workflow with the approved scope and logs the time, the approver, the record count and the origin, along with a snapshot of the previous values so the whole thing can be reversed within 24 hours.

9. **Publish and watch rollbacks** (builds workflow)

   Validated and published, with bulk operations per week, the approval rate, which flags a source making bad suggestions, the average time to a decision, and the rollback rate after execution, typically under 2% with the gate and over 10% without.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new workflow, from step 1 "Gate the mass changes"
- A new workflow, from step 2 "Accept the operation"
- A new workflow, from step 3 "Build a sample of the diff"
- A new workflow, from step 4 "Rate how risky it is"
- A new workflow, from step 5 "Put the diff to a human"
- A new workflow, from step 6 "Wait for the decision"
- A new workflow, from step 7 "Apply all, some or nothing"
- A new workflow, from step 8 "Run it and keep the receipts"
- A new workflow, from step 9 "Publish and watch rollbacks"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
