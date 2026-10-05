---
name: crm-record-merge-suggestions
description: 'Use when a user mentions "CRM record merge suggestions", "real-time dedup workflow", "duplicate detection on create", or asks for related help. Real-time on record creation: find similar existing records, AI computes match confidence, high-confidence pairs auto-merge, medium-confidence flag for review, low-confidence ignore. Prevents duplicates entering the CRM rather than cleaning them up later.'
arguments: []
intempt:
  id: crm-record-merge-suggestions
  version: 1.0.0
  slashCommand: /crm-record-merge-suggestions
  group: Workflows
  shortDescription: "Produces a real-time CRM dedup workflow that finds similar records and flags or merges high-confidence duplicates."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: workflow-builder
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [dedup, real-time, record-quality]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: account_created, severity: blocking }
  invokesCommands:
    - create_workflow
    - configure_find_records_step
    - configure_workflow_branch_step
    - configure_ai_research_step
    - configure_workflow_multi_split_step
    - configure_update_attribute_step
    - configure_create_task_step
    - publish_workflow
  procedure:
    - step: 1
      title: Build the Real-Time Dedup Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Real-time CRM dedup'' triggered immediately on account_created OR user_created events. Goal: catch duplicates at creation moment rather than letting them propagate, then needing cleanup later.'
      prompt: 'Create a workflow ''Real-time CRM dedup'' triggered immediately on account_created OR user_created events. Goal: catch duplicates at creation moment rather than letting them propagate, then needing cleanup later.'
    - step: 2
      title: Find Similar Existing Records
      command: configure_find_records_step
      produces: step
      bindsAs: search
      dependsOn:
      - workflow
      description: 'Configure find-records step that searches for existing records similar to the newly-created one. Match criteria: same domain (for accounts), same email (for users), fuzzy name match (Levenshtein distance < 3), same primary contact. Returns: list of candidate matches with similarity scores.'
      prompt: 'Configure find-records step that searches for existing records similar to the newly-created one. Match criteria: same domain (for accounts), same email (for users), fuzzy name match (Levenshtein distance < 3), same primary contact. Returns: list of candidate matches with similarity scores.'
    - step: 3
      title: Branch on Match Found
      command: configure_workflow_branch_step
      produces: step
      bindsAs: found_branch
      dependsOn:
      - workflow
      - search
      description: 'Branch step: did the search find any candidate matches? If NO matches — record is unique, proceed to standard onboarding flow (handoff to auto-enrich-new-accounts). If YES matches found — continue to AI confidence scoring.'
      prompt: 'Branch step: did the search find any candidate matches? If NO matches — record is unique, proceed to standard onboarding flow (handoff to auto-enrich-new-accounts). If YES matches found — continue to AI confidence scoring.'
    - step: 4
      title: AI Compute Match Confidence
      command: configure_ai_research_step
      produces: step
      bindsAs: ai_confidence
      dependsOn:
      - workflow
      - found_branch
      description: 'Configure AI step that compares the new record to each candidate match and produces a confidence score (0-100) per pair. Inputs: all available fields, recent activity, contextual clues (e.g. same source UTM suggests same person). Considers nuances (e.g. ''sales@acme.com'' and ''john@acme.com'' are different people at same company, not duplicates). Output: ranked match candidates with confidence + reasoning.'
      prompt: 'Configure AI step that compares the new record to each candidate match and produces a confidence score (0-100) per pair. Inputs: all available fields, recent activity, contextual clues (e.g. same source UTM suggests same person). Considers nuances (e.g. ''sales@acme.com'' and ''john@acme.com'' are different people at same company, not duplicates). Output: ranked match candidates with confidence + reasoning.'
    - step: 5
      title: Multi-Split by Confidence
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: conf_split
      dependsOn:
      - workflow
      - ai_confidence
      description: 'Multi-split based on top candidate''s confidence score: HIGH (>90) — auto-merge into existing record; MEDIUM (60-90) — flag for review in dedup queue, do NOT auto-merge; LOW (<60) — likely not a duplicate, proceed with new record but tag as ''review-candidate'' for periodic re-evaluation.'
      prompt: 'Multi-split based on top candidate''s confidence score: HIGH (>90) — auto-merge into existing record; MEDIUM (60-90) — flag for review in dedup queue, do NOT auto-merge; LOW (<60) — likely not a duplicate, proceed with new record but tag as ''review-candidate'' for periodic re-evaluation.'
    - step: 6
      title: 'High-Confidence: Auto-Merge'
      command: configure_update_attribute_step
      produces: step
      bindsAs: merge
      dependsOn:
      - workflow
      - conf_split
      description: 'On high-confidence branch: merge the new record into the existing one. Keep the existing record as survivor (preserves history), copy any new fields from the new record, mark the new record as ''merged into [existing_id]''. The new record reference still works for inbound webhooks but redirects to the survivor.'
      prompt: 'On high-confidence branch: merge the new record into the existing one. Keep the existing record as survivor (preserves history), copy any new fields from the new record, mark the new record as ''merged into [existing_id]''. The new record reference still works for inbound webhooks but redirects to the survivor.'
    - step: 7
      title: 'Medium-Confidence: Flag for Review'
      command: configure_create_task_step
      produces: step
      bindsAs: review_task
      dependsOn:
      - workflow
      - conf_split
      description: 'On medium-confidence branch: create a RevOps task with both records side-by-side, AI''s reasoning for the suspicion, and merge/separate decision buttons. SLA: review within 5 business days — uncertain duplicates accumulate fast if not handled.'
      prompt: 'On medium-confidence branch: create a RevOps task with both records side-by-side, AI''s reasoning for the suspicion, and merge/separate decision buttons. SLA: review within 5 business days — uncertain duplicates accumulate fast if not handled.'
    - step: 8
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - merge
      - review_task
      description: 'Validate and publish. Monitor: auto-merge volume per week (proves the workflow is catching real duplicates), false-positive rate (sample audit of auto-merges — were any wrong?), review-queue depth (high = too many medium-confidence cases, suggests AI prompt tuning). Together with the scheduled-data-quality-audit, this is the dedup defense-in-depth pattern.'
      prompt: 'Validate and publish. Monitor: auto-merge volume per week (proves the workflow is catching real duplicates), false-positive rate (sample audit of auto-merges — were any wrong?), review-queue depth (high = too many medium-confidence cases, suggests AI prompt tuning). Together with the scheduled-data-quality-audit, this is the dedup defense-in-depth pattern.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Crm Record Merge Suggestions

## Procedure

1. **Build the Real-Time Dedup Workflow** [`create_workflow`] — Create a workflow 'Real-time CRM dedup' triggered immediately on account_created OR user_created events. Goal: catch duplicates at creation moment rather than letting them propagate, then needing cleanup later. → produces: workflow
2. **Find Similar Existing Records** [`configure_find_records_step`] — Configure find-records step that searches for existing records similar to the newly-created one. Match criteria: same domain (for accounts), same email (for users), fuzzy name match (Levenshtein distance < 3), same primary contact. Returns: list of candidate matches with similarity scores. → produces: step
3. **Branch on Match Found** [`configure_workflow_branch_step`] — Branch step: did the search find any candidate matches? If NO matches — record is unique, proceed to standard onboarding flow (handoff to auto-enrich-new-accounts). If YES matches found — continue to AI confidence scoring. → produces: step
4. **AI Compute Match Confidence** [`configure_ai_research_step`] — Configure AI step that compares the new record to each candidate match and produces a confidence score (0-100) per pair. Inputs: all available fields, recent activity, contextual clues (e.g. same source UTM suggests same person). Considers nuances (e.g. 'sales@acme.com' and 'john@acme.com' are different people at same company, not duplicates). Output: ranked match candidates with confidence + reasoning. → produces: step
5. **Multi-Split by Confidence** [`configure_workflow_multi_split_step`] — Multi-split based on top candidate's confidence score: HIGH (>90) — auto-merge into existing record; MEDIUM (60-90) — flag for review in dedup queue, do NOT auto-merge; LOW (<60) — likely not a duplicate, proceed with new record but tag as 'review-candidate' for periodic re-evaluation. → produces: step
6. **High-Confidence: Auto-Merge** [`configure_update_attribute_step`] — On high-confidence branch: merge the new record into the existing one. Keep the existing record as survivor (preserves history), copy any new fields from the new record, mark the new record as 'merged into [existing_id]'. The new record reference still works for inbound webhooks but redirects to the survivor. → produces: step
7. **Medium-Confidence: Flag for Review** [`configure_create_task_step`] — On medium-confidence branch: create a RevOps task with both records side-by-side, AI's reasoning for the suspicion, and merge/separate decision buttons. SLA: review within 5 business days — uncertain duplicates accumulate fast if not handled. → produces: step
8. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: auto-merge volume per week (proves the workflow is catching real duplicates), false-positive rate (sample audit of auto-merges — were any wrong?), review-queue depth (high = too many medium-confidence cases, suggests AI prompt tuning). Together with the scheduled-data-quality-audit, this is the dedup defense-in-depth pattern. → produces: workflow
