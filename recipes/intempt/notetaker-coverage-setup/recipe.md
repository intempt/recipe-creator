---
frontmatter_id: notetaker-coverage-setup
slash_command: /notetaker-coverage-setup
description: Configures the Blu notetaker auto-join setting using one of five coarse modes. It sets broad meeting coverage, not opt-out or deal value rules.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Automatically sends the Blu notetaker to revenue-relevant meetings, audits meeting types first, and tracks notetaker
    coverage and join failures on a dashboard.
  parameters:
  - name: coverage_target_pct
    type: number
    label: Target notetaker coverage (%) for revenue-impacting meeting types
    default: 80
    required: false
  - name: config_gap_threshold_pct
    type: number
    label: Coverage below which a meeting type is flagged as a configuration gap (%)
    default: 60
    required: false
  - name: high_value_deal_threshold
    type: number
    label: Deal value above which meetings get the notetaker regardless of type (USD)
    default: 50000
    required: false
  - name: audit_window
    type: duration
    label: Lookback window for meeting volume audit
    default: 90 d
    required: false
  requirements:
  - slot: meeting_type_list
    kind: attribute
    meaning: The project's configured meeting types with their default duration and notetaker auto-join setting
  - slot: meeting_held
    kind: event
    meaning: A customer or internal meeting took place
    properties:
    - name: meeting_type
      type: string
      meaning: The configured meeting type of the meeting
      optional: false
    - name: notetaker_present
      type: boolean
      meaning: Whether the notetaker joined the meeting
      optional: false
    - name: notetaker_join_failed
      type: boolean
      meaning: Whether the notetaker was invited but did not join
      optional: true
    - name: notetaker_manually_added
      type: boolean
      meaning: Whether a host manually invited the notetaker
      optional: true
    - name: rep
      type: string
      meaning: The sales rep who hosted the meeting
      optional: false
    - name: linked_deal_value
      type: number
      meaning: Value of the deal linked to the meeting
      optional: true
  - slot: notetaker_opt_out_flag
    kind: attribute
    meaning: A meeting attendee has the notetaker opt-out flag set
  - slot: blu_notetaker
    kind: integration
    meaning: The Blu notetaker service connected to the project's calendar and meeting records
    channel: hubspot
  steps:
  - id: s1
    builds: report
    uses:
    - meeting_type_list
    - meeting_held
    - audit_window
    instruction: 'List all configured meeting types in the project. For each, surface: name, default duration, current notetaker
      auto-join setting, and meetings-per-month count over the last {audit_window}. This is the baseline for designing coverage
      rules: types with high volume and high revenue impact (demo, discovery, close, renewal) should have autojoin on; types
      with low strategic value (internal sync, recurring 1:1) likely shouldn''t.'
  - id: s2
    builds: automation
    uses:
    - s1
    - blu_notetaker
    - notetaker_opt_out_flag
    - high_value_deal_threshold
    instruction: Configure notetaker auto-join rules based on the meeting-type audit in "Review your meeting types". Turn
      auto-join ON for Discovery, Demo, Proposal, Close, Renewal, and Customer Success meetings; turn it OFF for Internal
      Sync, 1:1, Recurring Standup, and Interview meetings. Add an override that turns auto-join ON for any meeting linked
      to a deal with value above {high_value_deal_threshold} USD, regardless of meeting type. Add an override that turns auto-join
      OFF if any attendee has the {notetaker_opt_out_flag} set. Hosts can still override per meeting by adding the notetaker
      to a live meeting or using the meeting record toggle.
  - id: s3
    builds: dashboard
    uses:
    - s1
    - s2
    - meeting_held
    - coverage_target_pct
    - config_gap_threshold_pct
    instruction: Build a notetaker coverage dashboard showing the percentage of meetings with the notetaker present, with
      a target of {coverage_target_pct}% or higher for revenue-impacting meeting types. Break coverage down by meeting type
      and by {meeting_held.rep}. Show failed-join count (notetaker invited but did not join, usually a calendar permission
      issue) and manual-add count (hosts inviting the notetaker by hand), both signals of misconfigured rules. Flag any meeting
      type with coverage below {config_gap_threshold_pct}% as a configuration gap. Base this on the results of "Review your
      meeting types" and "Set the auto-join rules".
---

# Decide which calls get recorded

Slash command: /notetaker-coverage-setup

## Step 1: Review your meeting types

List all configured meeting types in the project. For each, surface: name, default duration, current notetaker auto-join setting, and meetings-per-month count over the last 90 days. This is the baseline for designing coverage rules: types with high volume and high revenue impact (demo, discovery, close, renewal) should have autojoin on; types with low strategic value (internal sync, recurring 1:1) likely shouldn't.

## Step 2: Set the auto-join rules

Configure notetaker autojoin rules based on the meeting-type audit. Default policy: ON for Discovery, Demo, Proposal, Close, Renewal, and Customer Success calls; OFF for Internal Sync, 1:1, Recurring Standup, Interview. Layer on overrides: ON for any meeting linked to a deal with value > $50K regardless of type; OFF if any attendee has notetaker-opt-out flag. Hosts can manually override per-meeting via add_blu_to_live_meeting or the meeting record toggle. Use the result of "Review your meeting types".

## Step 3: Track coverage and failures

Compose a notetaker coverage dashboard: % of meetings with notetaker present (target: 80%+ for revenue-impacting types), coverage broken down by meeting type and rep, failed-join count (notetaker invited but didn't join (usually a calendar permission issue), and manual-add count (hosts having to invite Blu manually) signal of misconfigured rules). Flag any type with <60% coverage as a configuration gap. Use the result of "Review your meeting types", "Set the auto-join rules".
