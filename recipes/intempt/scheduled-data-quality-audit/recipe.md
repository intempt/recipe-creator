---
id: scheduled-data-quality-audit
title: Weekly CRM hygiene audit
slash_command: /scheduled-data-quality-audit
group: Workflows
owner: intempt
summary: Scans every Sunday for duplicates, stale records and missing fields, then hands RevOps a reviewed
  cleanup queue on Monday morning.
description: >-
  Weekly: scan for duplicate accounts/users, stale records, missing required fields, and abandoned data
  to AI-suggests merges and cleanups to batch into approval queue for RevOps review. Replaces the manual
  'when did we last clean the CRM?' problem with a continuous hygiene program.
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
    - data-hygiene
    - scheduled-audit
    - crm-cleanup
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new workflow, from step 1 "Turn cleanup into a routine"
    - A new workflow, from step 2 "Run it on Sunday night"
    - A new workflow, from step 3 "Find the duplicates"
    - A new workflow, from step 4 "Find the stale records"
    - A new workflow, from step 5 "Find the gaps"
    - A new workflow, from step 6 "Propose the merges"
    - A new workflow, from step 7 "Send the queue for approval"
    - A new workflow, from step 8 "Report the week's hygiene"
    - A new workflow, from step 9 "Publish and watch the trend"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Turn cleanup into a routine
    summary: >-
      A weekly scan of the CRM for hygiene problems that produces a structured cleanup queue, in place
      of the someday we should clean the CRM problem.
    builds: workflow
    description: >-
      Create a workflow 'Weekly data quality audit' that scans the CRM for hygiene issues and produces
      a structured cleanup queue. Goal: replace the ad-hoc 'we should clean the CRM someday' problem with
      a continuous, low-effort hygiene program.
  - id: s2
    title: Run it on Sunday night
    summary: >-
      The full audit runs overnight so the queue is ready on Monday. It skips itself if an audit finished
      within the last five days.
    builds: workflow
    description: >-
      Configure scheduled trigger: every Sunday night, run the full audit so the cleanup queue is ready
      for RevOps Monday morning. Skip if last audit completed within 5 days (avoid duplicate work). Use
      the result of "Turn cleanup into a routine".
    dependsOn:
      - s1
  - id: s3
    title: Find the duplicates
    summary: >-
      Accounts on the same domain, with similar names, or the same legal name formatted differently, and
      users on the same email or the same name and phone. Each candidate pair or group comes with a similarity
      score.
    builds: workflow
    description: >-
      Configure find-records step that identifies likely duplicate Accounts (same domain, similar names,
      same legal name with different formatting) and likely duplicate Users (same email, same name+phone).
      Outputs: list of duplicate-candidate pairs/groups with similarity score. Use the result of "Turn
      cleanup into a routine", "Run it on Sunday night".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Find the stale records
    summary: >-
      Accounts with no activity for over a year that are not customers, users whose email bounced more
      than 90 days ago, and deals stuck in an early stage for over 180 days. Not all of these are deletions,
      some just need re-engaging, but they all bloat reporting and slow segmentation.
    builds: workflow
    description: >-
      Configure second find-records step for stale data: Accounts with no activity in 365+ days that aren't
      customers, Users with bounced emails older than 90 days, Deals stuck in early stages for 180+ days.
      These aren't always cuts (sometimes just need re-engagement) but they bloat reporting and slow segmentation.
      Outputs the staleness list with category labels. Use the result of "Turn cleanup into a routine",
      "Run it on Sunday night".
    dependsOn:
      - s1
      - s2
  - id: s5
    title: Find the gaps
    summary: >-
      Accounts missing industry, size or region, users missing a role or company, and deals missing a
      close date or an amount, grouped by what is missing so you can tell whether to enrich them or look
      by hand.
    builds: workflow
    description: >-
      Configure third find-records step for incomplete records: Accounts missing industry / size / region,
      Users missing role / company, Deals missing close-date / amount. Outputs list of incomplete records
      by completeness category: informs whether to trigger enrichment workflows or queue for manual review.
      Use the result of "Turn cleanup into a routine", "Run it on Sunday night".
    dependsOn:
      - s1
      - s2
  - id: s6
    title: Propose the merges
    summary: >-
      For each duplicate candidate: which record should survive, judged on how complete it is and how
      recently it was active, what to copy across from the other, and which conflicts a human has to settle,
      such as two different industry classifications. Every suggestion carries a confidence score.
    builds: workflow
    description: >-
      Configure AI research step that examines the duplicate candidates and suggests merge actions: which
      record is the survivor (most-complete, most-recent activity), what data to merge in from the duplicate,
      what conflicts to flag for human resolution (e.g. different industry classifications between dup
      records). Outputs structured merge-suggestions with confidence scores. Use the result of "Turn cleanup
      into a routine", "Find the duplicates", "Find the stale records", "Find the gaps".
    dependsOn:
      - s1
      - s3
      - s4
      - s5
  - id: s7
    title: Send the queue for approval
    summary: >-
      The merge and cleanup queue is handed to the bulk update review gate with the total findings, a
      summary per category, the spread of confidence and links to the records, so RevOps can approve the
      confident batch and handle the edge cases by hand.
    builds: workflow
    description: >-
      Configure webhook step that hands off the merge-and-cleanup queue to the bulk-update-review-workflow
      for human approval. Includes: total findings count, summary by category, AI-confidence distribution,
      links to the underlying records. RevOps reviews Monday morning, approves the high-confidence batch,
      manually handles the edge cases. Use the result of "Turn cleanup into a routine", "Propose the merges".
    dependsOn:
      - s1
      - s6
  - id: s8
    title: Report the week's hygiene
    summary: >-
      A post to the RevOps channel with the duplicate count, the stale count, the incompleteness rate
      and the movement week over week, saying plainly when completeness improved and when the stale pile
      is growing, which usually points at slow follow up upstream.
    builds: workflow
    description: >-
      Configure Slack step posting the weekly hygiene report to #revops: duplicate count, stale count,
      incompleteness rate, week-over-week trends. Highlights celebrations (CRM completeness up 3%) and
      concerns (stale-record pile growing: symptom of slow follow-up upstream). Surfaces hygiene as an
      ongoing program, not a fire drill. Use the result of "Turn cleanup into a routine", "Propose the
      merges", "Send the queue for approval".
    dependsOn:
      - s1
      - s6
      - s7
  - id: s9
    title: Publish and watch the trend
    summary: >-
      Validated and published, tracking that the weekly run completes, whether the pile of findings is
      growing, which points at problems further upstream, and how complete the CRM is after each cleanup.
    builds: workflow
    description: >-
      Validate and publish. Monitor: weekly run completion, find-volume trends (a growing pile suggests
      upstream issues: sales not closing out leads, no enrichment on signup), and post-cleanup CRM-completeness
      metric. The hygiene KPI nobody had before this workflow. Use the result of "Turn cleanup into a
      routine", "Report the week's hygiene".
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

# Weekly CRM hygiene audit

Scans every Sunday for duplicates, stale records and missing fields, then hands RevOps a reviewed cleanup queue on Monday morning.

## Steps

1. **Turn cleanup into a routine** (builds workflow)

   A weekly scan of the CRM for hygiene problems that produces a structured cleanup queue, in place of the someday we should clean the CRM problem.

2. **Run it on Sunday night** (builds workflow)

   The full audit runs overnight so the queue is ready on Monday. It skips itself if an audit finished within the last five days.

3. **Find the duplicates** (builds workflow)

   Accounts on the same domain, with similar names, or the same legal name formatted differently, and users on the same email or the same name and phone. Each candidate pair or group comes with a similarity score.

4. **Find the stale records** (builds workflow)

   Accounts with no activity for over a year that are not customers, users whose email bounced more than 90 days ago, and deals stuck in an early stage for over 180 days. Not all of these are deletions, some just need re-engaging, but they all bloat reporting and slow segmentation.

5. **Find the gaps** (builds workflow)

   Accounts missing industry, size or region, users missing a role or company, and deals missing a close date or an amount, grouped by what is missing so you can tell whether to enrich them or look by hand.

6. **Propose the merges** (builds workflow)

   For each duplicate candidate: which record should survive, judged on how complete it is and how recently it was active, what to copy across from the other, and which conflicts a human has to settle, such as two different industry classifications. Every suggestion carries a confidence score.

7. **Send the queue for approval** (builds workflow)

   The merge and cleanup queue is handed to the bulk update review gate with the total findings, a summary per category, the spread of confidence and links to the records, so RevOps can approve the confident batch and handle the edge cases by hand.

8. **Report the week's hygiene** (builds workflow)

   A post to the RevOps channel with the duplicate count, the stale count, the incompleteness rate and the movement week over week, saying plainly when completeness improved and when the stale pile is growing, which usually points at slow follow up upstream.

9. **Publish and watch the trend** (builds workflow)

   Validated and published, tracking that the weekly run completes, whether the pile of findings is growing, which points at problems further upstream, and how complete the CRM is after each cleanup.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new workflow, from step 1 "Turn cleanup into a routine"
- A new workflow, from step 2 "Run it on Sunday night"
- A new workflow, from step 3 "Find the duplicates"
- A new workflow, from step 4 "Find the stale records"
- A new workflow, from step 5 "Find the gaps"
- A new workflow, from step 6 "Propose the merges"
- A new workflow, from step 7 "Send the queue for approval"
- A new workflow, from step 8 "Report the week's hygiene"
- A new workflow, from step 9 "Publish and watch the trend"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
