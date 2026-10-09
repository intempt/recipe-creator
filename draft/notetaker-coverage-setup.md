---
description: Configures the Blu notetaker auto-join setting using one of five coarse modes. It sets broad meeting coverage, not opt-out or deal value rules.
author:
  first_name: Sid
  last_name: Chaudhary
  job_title: Founder & CEO
  avatar: https://cdn.intempt.com/assets/author-profile-pics/sid.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Decide which calls get recorded

Slash command: /notetaker-coverage-setup

## Step 1: Review your meeting types

List all configured meeting types in the project. For each, surface: name, default duration, current notetaker auto-join setting, and meetings-per-month count over the last 90 days. This is the baseline for designing coverage rules: types with high volume and high revenue impact (demo, discovery, close, renewal) should have autojoin on; types with low strategic value (internal sync, recurring 1:1) likely shouldn't.

## Step 2: Set the auto-join rules

Configure notetaker autojoin rules based on the meeting-type audit. Default policy: ON for Discovery, Demo, Proposal, Close, Renewal, and Customer Success calls; OFF for Internal Sync, 1:1, Recurring Standup, Interview. Layer on overrides: ON for any meeting linked to a deal with value > $50K regardless of type; OFF if any attendee has notetaker-opt-out flag. Hosts can manually override per-meeting via add_blu_to_live_meeting or the meeting record toggle. Use the result of "Review your meeting types".

## Step 3: Track coverage and failures

Compose a notetaker coverage dashboard: % of meetings with notetaker present (target: 80%+ for revenue-impacting types), coverage broken down by meeting type and rep, failed-join count (notetaker invited but didn't join (usually a calendar permission issue), and manual-add count (hosts having to invite Blu manually) signal of misconfigured rules). Flag any type with <60% coverage as a configuration gap. Use the result of "Review your meeting types", "Set the auto-join rules".
