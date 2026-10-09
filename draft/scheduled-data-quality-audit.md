---
description: Runs weekly filter queries across account and user records to surface stale records, missing required fields, and abandoned data for RevOps review.
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
