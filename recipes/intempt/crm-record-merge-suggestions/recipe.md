---
frontmatter_id: crm-record-merge-suggestions
slash_command: /crm-record-merge-suggestions
description: On new account or contact creation, checks existing CRM records with exact-match filters and creates a review task when a possible duplicate is found.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
visibility: draft
rejected: Its purpose is merging duplicate CRM records and queuing HubSpot review tasks; HubSpot writes are not planned on
  Blu.
prerequisites:
  integrations:
    - { value: hubspot, severity: blocking }
portable:
  summary: Checks new account and contact records against existing CRM records, merges near-certain duplicates and queues
    uncertain ones for review.
  parameters:
  - name: high_confidence_threshold
    type: number
    label: High-confidence threshold (auto-merge above this score)
    default: 90
    required: false
  - name: medium_confidence_threshold
    type: number
    label: Medium-confidence threshold (review queue at or above this score)
    default: 60
    required: false
  - name: review_sla
    type: duration
    label: Review SLA for queued duplicate tasks
    default: 5 d
    required: false
  - name: fuzzy_name_distance
    type: number
    label: Maximum Levenshtein distance for fuzzy name match
    default: 3
    required: false
  - name: low_confidence_tag
    type: string
    label: Tag applied to low-confidence candidates
    default: review-candidate
    required: false
  requirements:
  - slot: account_created_event
    kind: event
    meaning: A new account record was created in the CRM
    properties:
    - name: account_id
      type: string
      meaning: Identifier of the new account
      optional: false
    - name: domain
      type: string
      meaning: Web domain of the account
      optional: true
    - name: name
      type: string
      meaning: Name of the account
      optional: true
    - name: primary_contact
      type: string
      meaning: Primary contact of the account
      optional: true
  - slot: user_created_event
    kind: event
    meaning: A new user or contact record was created
    properties:
    - name: user_id
      type: string
      meaning: Identifier of the new user or contact
      optional: false
    - name: email
      type: string
      meaning: Email address of the user
      optional: true
    - name: name
      type: string
      meaning: Full name of the user
      optional: true
    - name: utm_source
      type: string
      meaning: Source campaign tag captured at creation
      optional: true
  - slot: crm_records
    kind: integration
    meaning: A connected CRM system holding existing account and contact records that can be searched by exact-match filters
    channel: hubspot
  - slot: revops_task_queue
    kind: destination
    meaning: A task queue where RevOps staff receive review tasks
    channel: hubspot
  steps:
  - id: s1
    builds: automation
    uses:
    - account_created_event
    - user_created_event
    instruction: Create a workflow named 'Real-time CRM dedup' triggered immediately when an account is created or a user
      is created. Its purpose is to catch duplicates at the moment of creation rather than letting them propagate and need
      cleanup later.
  - id: s2
    builds: automation
    uses:
    - s1
    - crm_records
    - fuzzy_name_distance
    dependsOn:
    - s1
    instruction: 'Configure a find-records step that searches {crm_records} for existing records similar to the newly created
      record from "Check at the moment of creation". Match criteria: same domain for accounts; same email for users; fuzzy
      name match with Levenshtein distance less than {fuzzy_name_distance}; same primary contact. Return a list of candidate
      matches with similarity scores.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    dependsOn:
    - s1
    instruction: 'Add a branch: if the search in "Look for a match" returned no candidates, the record is unique, so hand
      off to the standard onboarding flow auto enrich workflow. If one or more candidates were returned, continue to AI confidence
      scoring in "Score each pair".'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    dependsOn:
    - s1
    instruction: 'Configure an AI step that compares the new record from "Check at the moment of creation" to each candidate
      from "Look for a match" and produces a confidence score from 0 to 100 per pair. Inputs: all available fields, recent
      activity, and contextual clues such as a shared {account_created_event.utm_source} or {user_created_event.utm_source}
      suggesting the same person. Treat role-based addresses such as sales@ versus a named address such as john@ at the same
      domain as different people, not duplicates. Output a ranked list of candidates with confidence and reasoning.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s4
    - high_confidence_threshold
    - medium_confidence_threshold
    - low_confidence_tag
    dependsOn:
    - s1
    instruction: 'Add a multi-split on the top candidate''s confidence score from "Score each pair": high when the score is
      above {high_confidence_threshold} routes to "Merge into the older record"; medium when the score is at or above {medium_confidence_threshold}
      and not high routes to "Queue the uncertain pairs"; low when the score is below {medium_confidence_threshold} proceeds
      with the new record and applies the tag {low_confidence_tag} for periodic re-evaluation.'
  - id: s6
    builds: automation
    uses:
    - s1
    - s5
    dependsOn:
    - s1
    instruction: On the high-confidence branch, merge the new record into the existing record. Keep the existing record as
      the survivor to preserve history. Copy any new fields from the new record onto the survivor. Mark the new record as
      merged into the existing record's identifier. Inbound webhooks referencing the new record must still resolve and redirect
      to the survivor.
  - id: s7
    builds: automation
    uses:
    - s1
    - s5
    - revops_task_queue
    - review_sla
    dependsOn:
    - s1
    instruction: On the medium-confidence branch, do not merge. Create a task in {revops_task_queue} containing both records
      side by side, the AI reasoning for the suspected duplicate, and merge and separate decision buttons. Set the review
      due within {review_sla}, because uncertain duplicates accumulate quickly if not handled.
  - id: s8
    builds: report
    uses:
    - s1
    - s6
    - s7
    dependsOn:
    - s1
    instruction: 'Validate and publish the workflow. Monitor three measures: weekly auto-merge volume (shows the workflow
      catches real duplicates); false-positive rate from a sample audit of auto-merges (were any wrong); and review-queue
      depth (a high depth suggests too many medium-confidence cases and the need to tune the AI scoring prompt). Use these
      alongside a scheduled data-quality audit as a defense-in-depth pattern.'
---

# Catch duplicates as they arrive

Slash command: /crm-record-merge-suggestions

## Step 1: Check at the moment of creation

Create a workflow named 'Real-time CRM dedup' triggered immediately when an account is created or a user is created. Its purpose is to catch duplicates at the moment of creation rather than letting them propagate and need cleanup later.

## Step 2: Look for a match

Configure a find-records step that searches crm records for existing records similar to the newly created record from "Check at the moment of creation". Match criteria: same domain for accounts; same email for users; fuzzy name match with Levenshtein distance less than 3; same primary contact. Return a list of candidate matches with similarity scores.

## Step 3: Stop early if it is new

Add a branch: if the search in "Look for a match" returned no candidates, the record is unique, so hand off to the standard onboarding flow auto enrich workflow. If one or more candidates were returned, continue to AI confidence scoring in "Score each pair".

## Step 4: Score each pair

Configure an AI step that compares the new record from "Check at the moment of creation" to each candidate from "Look for a match" and produces a confidence score from 0 to 100 per pair. Inputs: all available fields, recent activity, and contextual clues such as a shared utm source or utm source suggesting the same person. Treat role-based addresses such as sales@ versus a named address such as john@ at the same domain as different people, not duplicates. Output a ranked list of candidates with confidence and reasoning.

## Step 5: Act on the confidence

Add a multi-split on the top candidate's confidence score from "Score each pair": high when the score is above 90 routes to "Merge into the older record"; medium when the score is at or above 60 and not high routes to "Queue the uncertain pairs"; low when the score is below 60 proceeds with the new record and applies the tag review-candidate for periodic re-evaluation.

## Step 6: Merge into the older record

On the high-confidence branch, merge the new record into the existing record. Keep the existing record as the survivor to preserve history. Copy any new fields from the new record onto the survivor. Mark the new record as merged into the existing record's identifier. Inbound webhooks referencing the new record must still resolve and redirect to the survivor.

## Step 7: Queue the uncertain pairs

On the medium-confidence branch, do not merge. Create a task in revops task queue containing both records side by side, the AI reasoning for the suspected duplicate, and merge and separate decision buttons. Set the review due within 5 d, because uncertain duplicates accumulate quickly if not handled.

## Step 8: Publish and audit the merges

Validate and publish the workflow. Monitor three measures: weekly auto-merge volume (shows the workflow catches real duplicates); false-positive rate from a sample audit of auto-merges (were any wrong); and review-queue depth (a high depth suggests too many medium-confidence cases and the need to tune the AI scoring prompt). Use these alongside a scheduled data-quality audit as a defense-in-depth pattern.
