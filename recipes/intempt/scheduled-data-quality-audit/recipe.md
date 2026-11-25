---
frontmatter_id: scheduled-data-quality-audit
slash_command: /scheduled-data-quality-audit
description: Builds segments of stale accounts and incomplete user records, and runs a weekly audit that emails RevOps the
  duplicate, stale and incomplete record counts with merge suggestions.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds stale-account and incomplete-record segments and emails RevOps a weekly hygiene audit with duplicates, stale
    and incomplete counts and merge suggestions.
  parameters:
  - name: account_stale_days
    type: duration
    label: Account inactivity threshold
    default: 365 d
    required: false
  - name: bounced_email_age_days
    type: duration
    label: Bounced email age threshold
    default: 90 d
    required: false
  - name: deal_stuck_days
    type: duration
    label: Deal stuck in early stage threshold
    default: 180 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: account_domain
    kind: attribute
    meaning: The account's web domain
  - slot: account_last_activity
    kind: attribute
    meaning: Date of the account's last recorded activity
  - slot: customer_status
    kind: attribute
    meaning: Whether the account is a customer, such as customer or prospect
  - slot: account_industry
    kind: attribute
    meaning: The account's industry
  - slot: account_size
    kind: attribute
    meaning: The account's employee count
  - slot: account_region
    kind: attribute
    meaning: The account's region
  - slot: user_role
    kind: attribute
    meaning: The user's job role
  - slot: user_company
    kind: attribute
    meaning: The user's company name
  - slot: phone
    kind: attribute
    meaning: The user's phone number
    optional: true
  - slot: email_bounced
    kind: event
    meaning: An email to the user hard-bounced
  - slot: deal_stage
    kind: attribute
    meaning: The stage of the account's open deal
    optional: true
  - slot: deal_stage_entered
    kind: attribute
    meaning: Date the account's deal entered its current stage
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - account_last_activity
    - customer_status
    - account_stale_days
    instruction: Build a new segment of accounts named "Stale accounts". An account is in it when its {customer_status} is
      not customer and its {account_last_activity} is more than {account_stale_days} ago or has no value.
  - id: s2
    builds: segment
    uses:
    - user_role
    - user_company
    - email_bounced
    - bounced_email_age_days
    instruction: 'Build a new segment of users named "Incomplete or bounced users". A user is in it when any one of these
      is true: {user_role} has no value; {user_company} has no value; they did {email_bounced} more than {bounced_email_age_days}
      ago.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - account_domain
    - account_industry
    - account_size
    - account_region
    - phone
    - deal_stage
    - deal_stage_entered
    - deal_stuck_days
    - digest_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation that runs every Sunday at 21:00 on a schedule. Each run it analyzes accounts and users
      and writes these figures: accounts sharing an {account_domain}, and users sharing an email or a name plus {phone}, as
      duplicate groups, each with the record to keep (most complete, latest activity) and any conflicting values; the number
      of accounts in the segment from "Find the stale accounts"; the number of users in the segment from "Find the incomplete
      user records"; accounts missing {account_industry}, {account_size} or {account_region}; accounts whose {deal_stage}
      is Discovery or Qualification with {deal_stage_entered} more than {deal_stuck_days} ago; each count against last week.
      Then it emails these figures as plain-text lines to {digest_recipients}. Nothing is changed or merged.'
---

# Weekly CRM hygiene audit

Slash command: /scheduled-data-quality-audit

## Step 1: Find the stale accounts

Build a new segment of accounts named "Stale accounts". An account is in it when its customer status is not customer and its account last activity is more than 365 d ago or has no value.

## Step 2: Find the incomplete user records

Build a new segment of users named "Incomplete or bounced users". A user is in it when any one of these is true: user role has no value; user company has no value; they did email bounced more than 90 d ago.

## Step 3: Email the weekly hygiene audit

Build an automation that runs every Sunday at 21:00 on a schedule. Each run it analyzes accounts and users and writes these figures: accounts sharing an account domain, and users sharing an email or a name plus phone, as duplicate groups, each with the record to keep (most complete, latest activity) and any conflicting values; the number of accounts in the segment from "Find the stale accounts"; the number of users in the segment from "Find the incomplete user records"; accounts missing account industry, account size or account region; accounts whose deal stage is Discovery or Qualification with deal stage entered more than 180 d ago; each count against last week. Then it emails these figures as plain-text lines to the email addresses that get the digest. Nothing is changed or merged.
