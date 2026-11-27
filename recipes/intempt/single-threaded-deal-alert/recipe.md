---
frontmatter_id: single-threaded-deal-alert
slash_command: /single-threaded-deal-alert
description: Finds accounts with a late stage deal where only one person on the buyer's side is engaged and emails the rep
  three other people at the account to bring in.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Flags late-stage deals where only one buyer-side contact is engaged, emails the rep three other people at the account
    to bring in, and sends a weekly multi-threading digest.
  parameters:
  - name: lateStageNames
    type: text
    label: Late-stage deal stages
    default: Demo, Proposal, Closing
    required: false
  - name: minDealAgeDays
    type: number
    label: Minimum deal age before flagging (days)
    default: 14
    required: false
  - name: agedRiskDays
    type: number
    label: Days single-threaded before a deal counts as high-loss-risk
    default: 30
    required: false
  - name: multiThreadTarget
    type: number
    label: Target share of mid/late-stage deals multi-threaded (%)
    default: 70
    required: false
  - name: coachingGapThreshold
    type: number
    label: Coaching gap threshold for multi-threaded share (%)
    default: 50
    required: false
  - name: suggestedContactCount
    type: number
    label: Number of suggested contacts to add
    default: 3
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the reps who get the alerts
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_engagement_event
    kind: event
    meaning: A buyer-side contact attended a meeting on a deal or replied to an email on a deal
    properties:
    - name: contact
      type: text
      meaning: Buyer-side contact who attended or replied
      optional: false
  - slot: deal_stage
    kind: attribute
    meaning: Current pipeline stage of the account's open deal (Demo, Proposal, Closing, etc.)
  - slot: deal_created_date
    kind: attribute
    meaning: The date the account's open deal was created
  - slot: exec_buyer_flag
    kind: attribute
    meaning: The deal has a single executive decision-maker buyer
    optional: true
  - slot: job_title
    kind: attribute
    meaning: A user's job title
  steps:
  - id: s1
    builds: attribute
    uses:
    - deal_engagement_event
    instruction: 'Build a computed attribute on accounts named "threading_depth", a whole number refreshed daily: the count
      of distinct {deal_engagement_event.contact} values on the account''s {deal_engagement_event} events in the last 90 days.'
  - id: s2
    builds: segment
    uses:
    - s1
    - deal_stage
    - deal_created_date
    - exec_buyer_flag
    - lateStageNames
    - minDealAgeDays
    dependsOn:
    - s1
    instruction: 'Build a new segment of accounts named "Single-Threaded Late-Stage Deals". An account is in it when all of these
      are true: its threading_depth from "Count who is actually engaged" is exactly 1; it has an open deal whose {deal_stage}
      is one of {lateStageNames}; that deal''s {deal_created_date} is more than {minDealAgeDays} days ago; its {exec_buyer_flag}
      is not true. It is an account segment: threading_depth is an account attribute, never read as a user attribute. When the
      project keeps deals as deal records, the stage and the deal age are read from the account''s deal records. A condition whose
      signal the project does not hold is left out and named as left out; the segment''s name states no window its rule lacks.'
  - id: s3
    builds: automation
    uses:
    - s2
    - deal_engagement_event
    - job_title
    - deal_stage
    - suggestedContactCount
    - alert_recipients
    dependsOn:
    - s2
    instruction: 'Build an automation triggered when an account enters the segment from "Find the risky ones". An analysis step
      names the one engaged {deal_engagement_event.contact}, then picks the {suggestedContactCount} other users of the account
      most likely to influence the purchase, by {job_title}: peers, their manager and related teams. Then it emails {alert_recipients}
      the account name, {deal_stage}, the engaged contact, and those {suggestedContactCount} people with their titles and emails,
      asking the rep to bring them in. When the project has no exec-buyer attribute, {job_title} values with VP, Chief, Head or
      Director stand in for it, named as the stand-in; with no job titles either, the alert is sent without that check and names
      it as left out. The alert is never dropped.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - deal_stage
    - lateStageNames
    - multiThreadTarget
    - coachingGapThreshold
    - agedRiskDays
    - digest_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts whose {deal_stage}
      is one of {lateStageNames} and writes these figures: the share with threading_depth from "Count who is actually engaged"
      of 2 or more, against {multiThreadTarget}%; the average threading_depth by {deal_stage}; the accounts in the segment
      from "Find the risky ones" for more than {agedRiskDays} days, each by name. When the multi-threaded share is below {coachingGapThreshold}%,
      the email''s first line says so. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Single threaded deal alert

Slash command: /single-threaded-deal-alert

## Step 1: Count who is actually engaged

Build a computed attribute on accounts named "threading_depth", a whole number refreshed daily: the count of distinct contact values on the account's deal engagement event events in the last 90 days.

## Step 2: Find the risky ones

Build a new segment of accounts named "Single-Threaded Late-Stage Deals". An account is in it when all of these are true: its threading_depth from "Count who is actually engaged" is exactly 1; it has an open deal whose deal stage is one of Demo, Proposal, Closing; that deal's deal created date is more than 14 days ago; its exec buyer flag is not true. It is an account segment: threading_depth is an account attribute, never read as a user attribute. When the project keeps deals as deal records, the stage and the deal age are read from the account's deal records. A condition whose signal the project does not hold is left out and named as left out; the segment's name states no window its rule lacks.

## Step 3: Give the rep three names

Build an automation triggered when an account enters the segment from "Find the risky ones". An analysis step names the one engaged contact, then picks the 3 other users of the account most likely to influence the purchase, by job title: peers, their manager and related teams. Then it emails the email addresses of the reps who get the alerts the account name, deal stage, the engaged contact, and those 3 people with their titles and emails, asking the rep to bring them in. When the project has no exec-buyer attribute, job title values with VP, Chief, Head or Director stand in for it, named as the stand-in; with no job titles either, the alert is sent without that check and names it as left out. The alert is never dropped.

## Step 4: Email the weekly threading digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts whose deal stage is one of Demo, Proposal, Closing and writes these figures: the share with threading_depth from "Count who is actually engaged" of 2 or more, against 70%; the average threading_depth by deal stage; the accounts in the segment from "Find the risky ones" for more than 30 days, each by name. When the multi-threaded share is below 50%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
