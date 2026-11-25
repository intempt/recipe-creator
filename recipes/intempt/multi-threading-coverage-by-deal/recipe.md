---
frontmatter_id: multi-threading-coverage-by-deal
slash_command: /multi-threading-coverage-by-deal
description: Emails a weekly digest of how many distinct stakeholders are engaged on each open deal, open deals by threading
  level and stage, and pipeline dollars at risk from single-threaded deals.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a weekly digest of stakeholder coverage on open deals by threading level and stage, the pipeline in single-threaded
    deals, and win rate by threading level.
  parameters:
  - name: window_closed
    type: duration
    label: Window of closed deals included
    default: 90 d
    required: false
  - name: win_rate_window
    type: duration
    label: Window for win rate by threading level
    default: 12 mo
    required: false
  - name: benchmark_min_stakeholders
    type: number
    label: Stakeholders a well-covered deal should have
    default: 5
    required: false
  - name: single_threaded_max
    type: number
    label: Most contacts on a single-threaded deal
    default: 1
    required: false
  - name: lightly_threaded_max
    type: number
    label: Most contacts on a lightly threaded deal
    default: 3
    required: false
  - name: multi_threaded_max
    type: number
    label: Most contacts on a multi-threaded deal
    default: 6
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_stage_event
    kind: event
    meaning: A deal's stage was changed
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: new_stage
      type: string
      meaning: Stage the deal moved to
      optional: false
    - name: user_ids
      type: text
      meaning: Users associated with the deal at the stage change
      optional: false
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a customer
    properties:
    - name: deal_ids
      type: text
      meaning: Deals the meeting is linked to
      optional: false
    - name: user_ids
      type: text
      meaning: Users who attended the meeting
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked won
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  - slot: deal_lost_event
    kind: event
    meaning: A deal was marked lost
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_stage_event
    - meeting_scheduled_event
    - deal_won_event
    - deal_lost_event
    - window_closed
    - win_rate_window
    - benchmark_min_stakeholders
    - single_threaded_max
    - lightly_threaded_max
    - multi_threaded_max
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes open deals (a {deal_stage_event.deal_id}
      with no {deal_won_event} or {deal_lost_event}) and counts each deal''s distinct contacts in {deal_stage_event.user_ids}
      and in {meeting_scheduled_event.user_ids} of meetings whose {meeting_scheduled_event.deal_ids} include it. It writes:
      open deals by current {deal_stage_event.new_stage} and threading level, single-threaded (up to {single_threaded_max}
      contact), lightly (up to {lightly_threaded_max}), multi (up to {multi_threaded_max}) or deeply threaded (more); the
      sum of the latest {deal_stage_event.amount} in single-threaded deals; the share of open deals with at least {benchmark_min_stakeholders}
      contacts; win rate by threading level for deals closed in the last {win_rate_window}; the same counts for deals closed
      in the last {window_closed}. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Multi threading coverage

Slash command: /multi-threading-coverage-by-deal

## Step 1: Email the weekly threading digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes open deals (a deal id with no deal won event or deal lost event) and counts each deal's distinct contacts in user ids and in user ids of meetings whose deal ids include it. It writes: open deals by current new stage and threading level, single-threaded (up to 1 contact), lightly (up to 3), multi (up to 6) or deeply threaded (more); the sum of the latest amount in single-threaded deals; the share of open deals with at least 5 contacts; win rate by threading level for deals closed in the last 12 mo; the same counts for deals closed in the last 90 d. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
