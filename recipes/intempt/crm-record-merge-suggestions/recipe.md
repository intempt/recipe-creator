---
id: crm-record-merge-suggestions
title: Catch duplicates as they arrive
slash_command: /crm-record-merge-suggestions
group: Workflows
owner: intempt
summary: Checks every new account or contact against what you already have, merges the obvious duplicates,
  and queues the doubtful ones for a person to judge.
description: >-
  Real-time on record creation: find similar existing records, AI computes match confidence, high-confidence
  pairs auto-merge, medium-confidence flag for review, low-confidence ignore. Prevents duplicates entering
  the CRM rather than cleaning them up later.
version: 2.0.0
classification:
  product:
    - sales
  agent: workflow-builder
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - dedup
    - real-time
    - record-quality
prerequisites:
  events:
    - value: account_created
      severity: blocking
steps:
  - id: s1
    title: Check at the moment of creation
    summary: >-
      Runs the instant an account or user is created, so duplicates are caught before they spread rather
      than cleaned up months later.
    builds: workflow
    description: >-
      Create a workflow 'Real-time CRM dedup' triggered immediately on account_created OR user_created
      events. Goal: catch duplicates at creation moment rather than letting them propagate, then needing
      cleanup later.
  - id: s2
    title: Look for a match
    summary: >-
      Searches for records that look the same: the same domain for accounts, the same email for people,
      a close name match, or the same primary contact, returning candidates with a similarity score.
    builds: workflow
    description: >-
      Configure find-records step that searches for existing records similar to the newly-created one.
      Match criteria: same domain (for accounts), same email (for users), fuzzy name match (Levenshtein
      distance < 3), same primary contact. Returns: list of candidate matches with similarity scores.
      Use the result of "Check at the moment of creation".
    dependsOn:
      - s1
  - id: s3
    title: Stop early if it is new
    summary: >-
      No candidates means the record is genuinely new and it goes on to normal onboarding and enrichment.
      Candidates mean it carries on to scoring.
    builds: workflow
    description: >-
      Branch step: did the search find any candidate matches? If NO matches (record is unique, proceed
      to standard onboarding flow (handoff to auto-enrich-new-accounts). If YES matches found) continue
      to AI confidence scoring. Use the result of "Check at the moment of creation", "Look for a match".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Score each pair
    summary: >-
      Every candidate is scored 0 to 100 against the new record on all its fields, recent activity and
      context such as arriving from the same campaign. It knows two addresses at one company are usually
      two people rather than one duplicate, and it explains every score.
    builds: workflow
    description: >-
      Configure AI step that compares the new record to each candidate match and produces a confidence
      score (0-100) per pair. Inputs: all available fields, recent activity, contextual clues (e.g. same
      source UTM suggests same person). Considers nuances (e.g. 'sales@acme.com' and 'john@acme.com' are
      different people at same company, not duplicates). Output: ranked match candidates with confidence
      + reasoning. Use the result of "Check at the moment of creation", "Stop early if it is new".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Act on the confidence
    summary: >-
      Above 90 merges automatically. Between 60 and 90 goes to the review queue and is never merged on
      its own. Below 60 carries on as a new record, tagged for a later look.
    builds: workflow
    description: >-
      Multi-split based on top candidate's confidence score: HIGH (>90) (auto-merge into existing record;
      MEDIUM (60-90)) flag for review in dedup queue, do NOT auto-merge; LOW (<60): likely not a duplicate,
      proceed with new record but tag as 'review-candidate' for periodic re-evaluation. Use the result
      of "Check at the moment of creation", "Score each pair".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Merge into the older record
    summary: >-
      The existing record survives so its history is kept, any new fields are copied across, and the new
      record is marked as merged into it. References to the new one still work and point at the survivor.
    builds: workflow
    description: >-
      On high-confidence branch: merge the new record into the existing one. Keep the existing record
      as survivor (preserves history), copy any new fields from the new record, mark the new record as
      'merged into [existing_id]'. The new record reference still works for inbound webhooks but redirects
      to the survivor. Use the result of "Check at the moment of creation", "Act on the confidence".
    dependsOn:
      - s1
      - s5
  - id: s7
    title: Queue the uncertain pairs
    summary: >-
      A RevOps task showing both records side by side with the reasoning for the suspicion and a merge
      or separate decision, to be cleared within five working days before the queue builds up.
    builds: workflow
    description: >-
      On medium-confidence branch: create a RevOps task with both records side-by-side, AI's reasoning
      for the suspicion, and merge/separate decision buttons. SLA: review within 5 business days: uncertain
      duplicates accumulate fast if not handled. Use the result of "Check at the moment of creation",
      "Act on the confidence".
    dependsOn:
      - s1
      - s5
  - id: s8
    title: Publish and audit the merges
    summary: >-
      Validated and published, watching auto merges per week, the false positive rate from a sample audit
      of them, and the depth of the review queue, which grows when too much lands in the middle band.
    builds: workflow
    description: >-
      Validate and publish. Monitor: auto-merge volume per week (proves the workflow is catching real
      duplicates), false-positive rate (sample audit of auto-merges: were any wrong?), review-queue depth
      (high = too many medium-confidence cases, suggests AI prompt tuning). Together with the scheduled-data-quality-audit,
      this is the dedup defense-in-depth pattern. Use the result of "Check at the moment of creation",
      "Merge into the older record", "Queue the uncertain pairs".
    dependsOn:
      - s1
      - s6
      - s7
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s7
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Catch duplicates as they arrive

Checks every new account or contact against what you already have, merges the obvious duplicates, and queues the doubtful ones for a person to judge.

## Steps

1. **Check at the moment of creation** (builds workflow)

   Runs the instant an account or user is created, so duplicates are caught before they spread rather than cleaned up months later.

2. **Look for a match** (builds workflow)

   Searches for records that look the same: the same domain for accounts, the same email for people, a close name match, or the same primary contact, returning candidates with a similarity score.

3. **Stop early if it is new** (builds workflow)

   No candidates means the record is genuinely new and it goes on to normal onboarding and enrichment. Candidates mean it carries on to scoring.

4. **Score each pair** (builds workflow)

   Every candidate is scored 0 to 100 against the new record on all its fields, recent activity and context such as arriving from the same campaign. It knows two addresses at one company are usually two people rather than one duplicate, and it explains every score.

5. **Act on the confidence** (builds workflow)

   Above 90 merges automatically. Between 60 and 90 goes to the review queue and is never merged on its own. Below 60 carries on as a new record, tagged for a later look.

6. **Merge into the older record** (builds workflow)

   The existing record survives so its history is kept, any new fields are copied across, and the new record is marked as merged into it. References to the new one still work and point at the survivor.

7. **Queue the uncertain pairs** (builds workflow)

   A RevOps task showing both records side by side with the reasoning for the suspicion and a merge or separate decision, to be cleared within five working days before the queue builds up.

8. **Publish and audit the merges** (builds workflow)

   Validated and published, watching auto merges per week, the false positive rate from a sample audit of them, and the depth of the review queue, which grows when too much lands in the middle band.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## Availability

Coming soon: waiting on the engine to build workflow.
