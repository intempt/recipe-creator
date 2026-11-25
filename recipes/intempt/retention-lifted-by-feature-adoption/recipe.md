---
frontmatter_id: retention-lifted-by-feature-adoption
slash_command: /retention-lifted-by-feature-adoption
description: Builds a segment of users who adopt a given feature in their first week and emails a weekly digest comparing
  how long they stay against users who never touch it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a segment of first-week adopters of a chosen feature and emails a weekly digest of their retention against
    non-adopters, with W4 and W12 gaps flagged.
  parameters:
  - name: target_id
    type: string
    label: Feature identifier (click event target_id) to analyse
    required: true
  - name: adoption_window
    type: duration
    label: Window after User created that counts as early adoption
    default: 7 d
    required: false
  - name: strong_lever_gap_pp
    type: number
    label: W4 retention gap (percentage points) above which the feature is flagged as a strong retention lever
    default: 15
    required: false
  - name: weak_gap_pp
    type: number
    label: W12 retention gap (percentage points) below which the feature is flagged as not retention-driving
    default: 5
    required: false
  - name: low_exposure_share
    type: number
    label: Early adopter share of the base (%) below which first-week exposure is flagged as too low
    default: 30
    required: false
  - name: time_range
    type: duration
    label: Signup period analysed
    default: 12 w
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: feature_click_event
    kind: event
    meaning: A customer clicked a feature element in the product
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked feature element
      optional: false
  - slot: user_created_event
    kind: event
    meaning: A new user account was created
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  steps:
  - id: s1
    builds: segment
    uses:
    - feature_click_event
    - user_created_event
    - target_id
    - adoption_window
    - time_range
    instruction: Build a new segment of users named "Early Feature Adopters". A user is in it when they did {user_created_event}
      in the last {time_range} and did {feature_click_event} with {feature_click_event.target_id} equal to {target_id} within
      {adoption_window} after their {user_created_event}.
  - id: s2
    builds: automation
    uses:
    - s1
    - user_created_event
    - session_start_event
    - strong_lever_gap_pp
    - weak_gap_pp
    - low_exposure_share
    - time_range
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {user_created_event}
      in the last {time_range}, in weekly signup cohorts, in two groups: users in the segment from "Find first week feature
      adopters" (adopters) and the others (non-adopters). It writes, for weeks 1, 2, 4, 8 and 12 after signup: the % of each
      group that did {session_start_event} that week, the gap in percentage points, and each group''s size; the week with
      the largest gap; adopters as a % of all signups. Then it emails these figures as plain-text lines, each with its window,
      to {digest_recipients}. The email says the feature is a strong retention lever when the week-4 gap is above {strong_lever_gap_pp}
      points, not retention-driving when the week-12 gap is under {weak_gap_pp} points, and flags first-week exposure when
      adopters are under {low_exposure_share}% of signups. Nothing else is sent.'
---

# Retention lift from a feature

Slash command: /retention-lifted-by-feature-adoption

## Step 1: Find first week feature adopters

Build a new segment of users named "Early Feature Adopters". A user is in it when they did user created event in the last 12 w and did feature click event with target id equal to the feature identifier (click event target_id) to analyse within 7 d after their user created event.

## Step 2: Email the weekly feature retention digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did user created event in the last 12 w, in weekly signup cohorts, in two groups: users in the segment from "Find first week feature adopters" (adopters) and the others (non-adopters). It writes, for weeks 1, 2, 4, 8 and 12 after signup: the % of each group that did session start event that week, the gap in percentage points, and each group's size; the week with the largest gap; adopters as a % of all signups. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email says the feature is a strong retention lever when the week-4 gap is above 15 points, not retention-driving when the week-12 gap is under 5 points, and flags first-week exposure when adopters are under 30% of signups. Nothing else is sent.
