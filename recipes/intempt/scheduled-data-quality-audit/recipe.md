---
frontmatter_id: scheduled-data-quality-audit
slash_command: /scheduled-data-quality-audit
description: Runs weekly filter queries across account and user records to surface stale records, missing required fields, and abandoned data for RevOps review.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Runs a weekly CRM hygiene audit that finds duplicate, stale and incomplete account, user and deal records, queues
    merge suggestions for RevOps approval, and posts a Slack report.
  parameters:
  - name: audit_day_time
    type: string
    label: Audit schedule (day and time)
    default: Sunday 21:00
  - name: skip_if_recent_days
    type: duration
    label: Skip if last audit completed within
    default: 5 d
  - name: account_stale_days
    type: duration
    label: Account inactivity threshold
    default: 365 d
  - name: bounced_email_age_days
    type: duration
    label: Bounced email age threshold
    default: 90 d
  - name: deal_stuck_days
    type: duration
    label: Deal stuck in early stage threshold
    default: 180 d
  - name: slack_channel
    type: string
    label: Slack channel for weekly report
    default: '#revops'
  requirements:
  - slot: account_record
    kind: attribute
    meaning: Account records in the CRM with domain, name, legal name, industry, size, region, customer status and last activity
      date
  - slot: user_record
    kind: attribute
    meaning: User (contact) records in the CRM with email, name, phone, role, company, and email bounce status
  - slot: deal_record
    kind: attribute
    meaning: Deal records in the CRM with pipeline stage, stage entry date, close date and amount
  - slot: bulk_update_review_workflow
    kind: integration
    meaning: A workflow that receives the cleanup queue and routes it to RevOps for human approval of bulk record updates
    channel: hubspot
  - slot: revops_slack
    kind: destination
    meaning: A Slack channel where the RevOps team receives the weekly hygiene report
    channel: slack
  steps:
  - id: s1
    builds: automation
    uses:
    - account_record
    - user_record
    - deal_record
    instruction: Create a workflow named 'Weekly data quality audit' that scans {account_record}, {user_record} and {deal_record}
      for hygiene issues and produces a structured cleanup queue.
  - id: s2
    builds: automation
    uses:
    - s1
    - audit_day_time
    - skip_if_recent_days
    instruction: Configure a scheduled trigger to run the full audit every {audit_day_time}. Skip the run if the last audit
      completed within {skip_if_recent_days}. Use the workflow from "Turn cleanup into a routine".
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - account_record
    - user_record
    instruction: Configure a find-records step that identifies likely duplicate Accounts (same domain, similar names, same
      legal name with different formatting) and likely duplicate Users (same email, or same name plus phone) in {account_record}
      and {user_record}. Output a list of duplicate-candidate pairs or groups with a similarity score. Use the results of
      "Turn cleanup into a routine" and "Run it on Sunday night".
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - account_record
    - user_record
    - deal_record
    - account_stale_days
    - bounced_email_age_days
    - deal_stuck_days
    instruction: 'Configure a second find-records step for stale data: Accounts with no activity in {account_stale_days} or
      more that are not customers; Users with bounced emails older than {bounced_email_age_days}; Deals in early stages for
      {deal_stuck_days} or more. Output the staleness list with a category label for each record. Use the results of "Turn
      cleanup into a routine" and "Run it on Sunday night".'
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - account_record
    - user_record
    - deal_record
    instruction: 'Configure a third find-records step for incomplete records: Accounts missing industry, size or region; Users
      missing role or company; Deals missing close date or amount. Output the incomplete records grouped by completeness category,
      to inform whether to trigger enrichment or queue for manual review. Use the results of "Turn cleanup into a routine"
      and "Run it on Sunday night".'
  - id: s6
    builds: automation
    uses:
    - s1
    - s3
    - s4
    - s5
    instruction: Configure an AI research step that examines the duplicate candidates from "Find the duplicates" and suggests
      merge actions. For each group, pick the survivor record (most complete, most recent activity), list the data to merge
      in from the duplicate, and flag conflicts for human resolution, such as differing industry classifications. Output structured
      merge suggestions with confidence scores. Use the results of "Turn cleanup into a routine", "Find the duplicates", "Find
      the stale records" and "Find the gaps".
  - id: s7
    builds: webhook
    uses:
    - s1
    - s6
    - bulk_update_review_workflow
    instruction: Configure a webhook that sends the merge-and-cleanup queue to {bulk_update_review_workflow} for human approval.
      Include the total findings count, a summary by category, the AI confidence distribution, and links to the underlying
      records. RevOps reviews on Monday morning, approves the high-confidence batch and handles edge cases manually. Use the
      results of "Turn cleanup into a routine" and "Propose the merges".
  - id: s8
    builds: automation
    uses:
    - s1
    - s6
    - s7
    - slack_channel
    - revops_slack
    instruction: Configure a Slack step that posts the weekly hygiene report to {slack_channel} on {revops_slack}. Include
      the duplicate count, stale count, incompleteness rate and week-over-week trends. Highlight improvements (for example,
      CRM completeness up 3%) and concerns (for example, a growing stale-record pile, which signals slow upstream follow-up).
      Frame hygiene as an ongoing program. Use the results of "Turn cleanup into a routine", "Propose the merges" and "Send
      the queue for approval".
  - id: s9
    builds: automation
    uses:
    - s1
    - s8
    instruction: Validate and publish the workflow. Monitor weekly run completion, find-volume trends (a growing pile suggests
      upstream issues such as sales not closing out leads or no enrichment at signup), and the post-cleanup CRM completeness
      metric. Use the results of "Turn cleanup into a routine" and "Report the week's hygiene".
---

# Weekly CRM hygiene audit

Slash command: /scheduled-data-quality-audit

## Step 1: Turn cleanup into a routine

Create a workflow 'Weekly data quality audit' that scans the CRM for hygiene issues and produces a structured cleanup queue. Goal: replace the ad-hoc 'we should clean the CRM someday' problem with a continuous, low-effort hygiene program.

## Step 2: Run it on Sunday night

This step builds a workflow.
Configure scheduled trigger: every Sunday night, run the full audit so the cleanup queue is ready for RevOps Monday morning. Skip if last audit completed within 5 days (avoid duplicate work). Use the result of "Turn cleanup into a routine".

## Step 3: Find the duplicates

This step builds a workflow.
Configure find-records step that identifies likely duplicate Accounts (same domain, similar names, same legal name with different formatting) and likely duplicate Users (same email, same name+phone). Outputs: list of duplicate-candidate pairs/groups with similarity score. Use the result of "Turn cleanup into a routine", "Run it on Sunday night".

## Step 4: Find the stale records

This step builds a workflow.
Configure second find-records step for stale data: Accounts with no activity in 365+ days that aren't customers, Users with bounced emails older than 90 days, Deals stuck in early stages for 180+ days. These aren't always cuts (sometimes just need re-engagement) but they bloat reporting and slow segmentation. Outputs the staleness list with category labels. Use the result of "Turn cleanup into a routine", "Run it on Sunday night".

## Step 5: Find the gaps

Configure third find-records step for incomplete records: Accounts missing industry / size / region, Users missing role / company, Deals missing close-date / amount. Outputs list of incomplete records by completeness category: informs whether to trigger enrichment workflows or queue for manual review. Use the result of "Turn cleanup into a routine", "Run it on Sunday night".

## Step 6: Propose the merges

This step builds a workflow.
Configure AI research step that examines the duplicate candidates and suggests merge actions: which record is the survivor (most-complete, most-recent activity), what data to merge in from the duplicate, what conflicts to flag for human resolution (e.g. different industry classifications between dup records). Outputs structured merge-suggestions with confidence scores. Use the result of "Turn cleanup into a routine", "Find the duplicates", "Find the stale records", "Find the gaps".

## Step 7: Send the queue for approval

Configure webhook step that hands off the merge-and-cleanup queue to the bulk-update-review-workflow for human approval. Includes: total findings count, summary by category, AI-confidence distribution, links to the underlying records. RevOps reviews Monday morning, approves the high-confidence batch, manually handles the edge cases. Use the result of "Turn cleanup into a routine", "Propose the merges".

## Step 8: Report the week's hygiene

This step builds a workflow.
Configure Slack step posting the weekly hygiene report to #revops: duplicate count, stale count, incompleteness rate, week-over-week trends. Highlights celebrations (CRM completeness up 3%) and concerns (stale-record pile growing: symptom of slow follow-up upstream). Surfaces hygiene as an ongoing program, not a fire drill. Use the result of "Turn cleanup into a routine", "Propose the merges", "Send the queue for approval".

## Step 9: Publish and watch the trend

Validate and publish. Monitor: weekly run completion, find-volume trends (a growing pile suggests upstream issues: sales not closing out leads, no enrichment on signup), and post-cleanup CRM-completeness metric. The hygiene KPI nobody had before this workflow. Use the result of "Turn cleanup into a routine", "Report the week's hygiene".
