---
frontmatter_id: champion-change-detection
slash_command: /champion-change-detection
description: Flags when the champion on an open deal goes quiet or leaves, using email replies and bounces, and emails the
  rep team an alert plus a weekly digest before the deal stalls.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tracks each deal champion's email replies and bounces, flags accounts whose champion went quiet or left, and emails
    the team an alert and a weekly digest.
  parameters:
  - name: active_window
    type: duration
    label: A champion who replied within this window is active
    default: 21 d
    required: false
  - name: quiet_window
    type: duration
    label: No reply for this long makes the champion gone
    default: 45 d
    required: false
  - name: warm_contact_window
    type: duration
    label: Window for other contacts at the account who replied
    default: 30 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses that get the champion alerts
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: champion_contact
    kind: attribute
    meaning: 'A user attribute marking the deal champion: true, or a role / contact-role value equal to champion'
  - slot: deal_stage
    kind: attribute
    meaning: The stage of the account's open deal, such as Discovery, Proposal, Closed Won or Closed Lost
  - slot: deal_amount
    kind: attribute
    meaning: The annual value of the account's open deal
    optional: true
  - slot: email_engagement
    kind: event
    meaning: An email to a contact was replied to, opened or bounced
    properties:
    - name: event_type
      type: string
      meaning: 'Kind of email event: reply, open or bounce'
      optional: false
  steps:
  - id: s1
    builds: attribute
    uses:
    - champion_contact
    - email_engagement
    - active_window
    - quiet_window
    instruction: Build a computed attribute on users named "champion_status", for users whom {champion_contact} marks as the
      champion (true, or a role value equal to champion). Set it to GONE when the user did {email_engagement} with {email_engagement.event_type}
      equal to bounce in the last {quiet_window}, or did not do {email_engagement} with {email_engagement.event_type} equal
      to reply in the last {quiet_window}; QUIET when their last {email_engagement} with {email_engagement.event_type} equal
      to reply was between {active_window} and {quiet_window} ago; ACTIVE when they did {email_engagement} with {email_engagement.event_type}
      equal to reply in the last {active_window}. Users it does not mark as the champion get no value.
  - id: s2
    builds: segment
    uses:
    - s1
    - deal_stage
    dependsOn:
    - s1
    instruction: Build a new segment of accounts named "Champion-change deals". An account is in it when its {deal_stage}
      is not Closed Won and not Closed Lost, and at least one of its users has the attribute from "Track the champion daily"
      equal to GONE or QUIET. When an account segment can't hold its users' attribute, say why and build it with the {deal_stage}
      condition alone, named "Open deals"; the steps that use it then check the champion in their analysis.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - email_engagement
    - deal_stage
    - warm_contact_window
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation triggered when an account enters the segment from "Find deals that lost theirs". It
      analyzes the account and writes: the account name, its {deal_stage}, the champion and their status from "Track the champion
      daily", and the other users at the account who did {email_engagement} with {email_engagement.event_type} equal to reply
      in the last {warm_contact_window}, as warm contacts to reach next. Then it emails these lines as an alert to {alert_recipients}.
      When the segment from "Find deals that lost theirs" has no champion condition in its rule, the email goes out only through
      a condition after the analysis: send only when the account''s champion is GONE or QUIET, else nothing is sent; the card
      says this gate. It never emails the account''s contacts.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - deal_amount
    - digest_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the accounts in
      the segment from "Find deals that lost theirs" and writes these figures: the number of accounts in it now and 7 days
      ago; how many have a champion GONE and how many QUIET by the attribute from "Track the champion daily"; the sum of {deal_amount}
      across the accounts in it, as the deal value at risk; the accounts that left the segment in the last 7 days with a deal
      still open, as recovered. When that segment has no champion condition in its rule, each figure counts only its accounts
      with a champion GONE or QUIET. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Champion change detection

Slash command: /champion-change-detection

## Step 1: Track the champion daily

Build a computed attribute on users named "champion_status", for users whom champion contact marks as the champion (true, or a role value equal to champion). Set it to GONE when the user did email engagement with event type equal to bounce in the last 45 d, or did not do email engagement with event type equal to reply in the last 45 d; QUIET when their last email engagement with event type equal to reply was between 21 d and 45 d ago; ACTIVE when they did email engagement with event type equal to reply in the last 21 d. Users it does not mark as the champion get no value.

## Step 2: Find deals that lost theirs

Build a new segment of accounts named "Champion-change deals". An account is in it when its deal stage is not Closed Won and not Closed Lost, and at least one of its users has the attribute from "Track the champion daily" equal to GONE or QUIET. When an account segment can't hold its users' attribute, say why and build it with the deal stage condition alone, named "Open deals"; the steps that use it then check the champion in their analysis.

## Step 3: Alert the rep team

Build an automation triggered when an account enters the segment from "Find deals that lost theirs". It analyzes the account and writes: the account name, its deal stage, the champion and their status from "Track the champion daily", and the other users at the account who did email engagement with event type equal to reply in the last 30 d, as warm contacts to reach next. Then it emails these lines as an alert to the email addresses that get the champion alerts. When the segment from "Find deals that lost theirs" has no champion condition in its rule, the email goes out only through a condition after the analysis: send only when the account's champion is GONE or QUIET, else nothing is sent; the card says this gate. It never emails the account's contacts.

## Step 4: Email the weekly champion-risk digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the accounts in the segment from "Find deals that lost theirs" and writes these figures: the number of accounts in it now and 7 days ago; how many have a champion GONE and how many QUIET by the attribute from "Track the champion daily"; the sum of deal amount across the accounts in it, as the deal value at risk; the accounts that left the segment in the last 7 days with a deal still open, as recovered. When that segment has no champion condition in its rule, each figure counts only its accounts with a champion GONE or QUIET. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
