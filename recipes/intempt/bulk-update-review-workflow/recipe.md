---
description: Pauses mass field changes, merges, or deletes above a set size for human review before execution. The recipe creates the approval gate and routes the queued change to a reviewer.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - social
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
