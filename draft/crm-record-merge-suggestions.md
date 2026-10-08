---
description: On new account or contact creation, checks existing CRM records with exact-match filters and creates a review task when a possible duplicate is found.
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
---

# Catch duplicates as they arrive

Slash command: /crm-record-merge-suggestions

## Step 1: Check at the moment of creation

Create a workflow 'Real-time CRM dedup' triggered immediately on account_created OR user_created events. Goal: catch duplicates at creation moment rather than letting them propagate, then needing cleanup later.

## Step 2: Look for a match

This step builds a workflow.
Configure find-records step that searches for existing records similar to the newly-created one. Match criteria: same domain (for accounts), same email (for users), fuzzy name match (Levenshtein distance < 3), same primary contact. Returns: list of candidate matches with similarity scores. Use the result of "Check at the moment of creation".

## Step 3: Stop early if it is new

This step builds a workflow.
Branch step: did the search find any candidate matches? If NO matches (record is unique, proceed to standard onboarding flow (handoff to auto-enrich-new-accounts). If YES matches found) continue to AI confidence scoring. Use the result of "Check at the moment of creation", "Look for a match".

## Step 4: Score each pair

This step builds a workflow.
Configure AI step that compares the new record to each candidate match and produces a confidence score (0-100) per pair. Inputs: all available fields, recent activity, contextual clues (e.g. same source UTM suggests same person). Considers nuances (e.g. 'sales@example.com' and 'john@example.com' are different people at same company, not duplicates). Output: ranked match candidates with confidence + reasoning. Use the result of "Check at the moment of creation", "Stop early if it is new".

## Step 5: Act on the confidence

This step builds a workflow.
Multi-split based on top candidate's confidence score: HIGH (>90) (auto-merge into existing record; MEDIUM (60-90)) flag for review in dedup queue, do NOT auto-merge; LOW (<60): likely not a duplicate, proceed with new record but tag as 'review-candidate' for periodic re-evaluation. Use the result of "Check at the moment of creation", "Score each pair".

## Step 6: Merge into the older record

This step builds a workflow.
On high-confidence branch: merge the new record into the existing one. Keep the existing record as survivor (preserves history), copy any new fields from the new record, mark the new record as 'merged into [existing_id]'. The new record reference still works for inbound webhooks but redirects to the survivor. Use the result of "Check at the moment of creation", "Act on the confidence".

## Step 7: Queue the uncertain pairs

This step builds a workflow.
On medium-confidence branch: create a RevOps task with both records side-by-side, AI's reasoning for the suspicion, and merge/separate decision buttons. SLA: review within 5 business days: uncertain duplicates accumulate fast if not handled. Use the result of "Check at the moment of creation", "Act on the confidence".

## Step 8: Publish and audit the merges

Validate and publish. Monitor: auto-merge volume per week (proves the workflow is catching real duplicates), false-positive rate (sample audit of auto-merges: were any wrong?), review-queue depth (high = too many medium-confidence cases, suggests AI prompt tuning). Together with the scheduled-data-quality-audit, this is the dedup defense-in-depth pattern. Use the result of "Check at the moment of creation", "Merge into the older record", "Queue the uncertain pairs".
