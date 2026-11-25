---
frontmatter_id: pql-signal-to-sdr-task
slash_command: /pql-signal-to-sdr-task
description: When a free user's behaviour says they are ready for a conversation, it emails an SDR everything needed for the
  first touch, and a weekly digest of first-touch speed.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Scores free users on product behaviour, emails SDRs a first-touch brief for each user who crosses the bar, and
    sends a weekly digest of PQL volume and first-touch speed.
  parameters:
  - name: pqlThreshold
    type: number
    label: PQL score threshold (0-100)
    default: 70
    required: false
  - name: outreachCooldown
    type: duration
    label: Window with no recent outreach
    default: 30 d
    required: false
  - name: sessionWindow
    type: duration
    label: Usage depth session window
    default: 14 d
    required: false
  - name: firstTouchSla
    type: duration
    label: First touch SLA
    default: 24 h
    required: false
  - name: untouchedAlertWindow
    type: duration
    label: Untouched lead alert window
    default: 48 h
    required: false
  - name: untouchedAlertShare
    type: number
    label: Share of PQLs untouched that triggers a flag (%)
    default: 20
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the SDRs who get the briefs
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: free_user_activity
    kind: event
    meaning: A user used a product feature
    properties:
    - name: feature_name
      type: text
      meaning: Name of the feature used
      optional: false
    - name: plan_tier
      type: string
      meaning: Account plan tier of the user
      optional: true
  - slot: outreach_event
    kind: event
    meaning: A sales or marketing outreach was sent to a user
  - slot: opt_out_list
    kind: segment
    meaning: Users who opted out of sales outreach
  - slot: plan_attribute
    kind: attribute
    meaning: The user's plan, such as free, trial or a paid plan name
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  - slot: company_size
    kind: attribute
    meaning: The number of employees at the user's company
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - free_user_activity
    - session_start
    - sessionWindow
    instruction: 'Build a computed attribute on users named "pql_score", a number from 0 to 100, refreshed daily: 40 points
      scaled by the number of distinct {free_user_activity.feature_name} values the user used in the last {sessionWindow};
      30 points scaled by their {session_start} count in that window; 30 points scaled by the number of other users with the
      same email domain who did {session_start} in that window.'
  - id: s2
    builds: segment
    uses:
    - s1
    - plan_attribute
    - outreach_event
    - opt_out_list
    - pqlThreshold
    - outreachCooldown
    dependsOn:
    - s1
    instruction: 'Build a new segment of users named "Product Qualified Leads". A user is in it when all of these are true:
      their {plan_attribute} is free; their pql_score from "Score free users on behaviour" is {pqlThreshold} or more; they
      had no {outreach_event} in the last {outreachCooldown}; they are not in {opt_out_list}.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - free_user_activity
    - session_start
    - company_size
    - sessionWindow
    - firstTouchSla
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation triggered when a user enters the segment from "Find product qualified leads". An analysis
      step writes: their pql_score from "Score free users on behaviour"; their top 3 {free_user_activity.feature_name} values;
      their {session_start} count in the last {sessionWindow}; their {company_size}; other users from their email domain.
      Then it emails {alert_recipients} the user''s name, email and this brief, asking for a first touch within {firstTouchSla}.'
  - id: s4
    builds: automation
    uses:
    - s2
    - outreach_event
    - firstTouchSla
    - untouchedAlertWindow
    - untouchedAlertShare
    - digest_recipients
    dependsOn:
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users who entered
      the segment from "Find product qualified leads" in the last 7 days and the 4 weeks before, and writes these figures:
      the count for each week; the share who got an {outreach_event} within {firstTouchSla} of entering; the share with no
      {outreach_event} after {untouchedAlertWindow}. When that untouched share is above {untouchedAlertShare}%, the email''s
      first line says so. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Product qualified lead to SDR task

Slash command: /pql-signal-to-sdr-task

## Step 1: Score free users on behaviour

Build a computed attribute on users named "pql_score", a number from 0 to 100, refreshed daily: 40 points scaled by the number of distinct feature name values the user used in the last 14 d; 30 points scaled by their session start count in that window; 30 points scaled by the number of other users with the same email domain who did session start in that window.

## Step 2: Find product qualified leads

Build a new segment of users named "Product Qualified Leads". A user is in it when all of these are true: their plan attribute is free; their pql_score from "Score free users on behaviour" is 70 or more; they had no outreach event in the last 30 d; they are not in opt out list.

## Step 3: Give the SDR the context

Build an automation triggered when a user enters the segment from "Find product qualified leads". An analysis step writes: their pql_score from "Score free users on behaviour"; their top 3 feature name values; their session start count in the last 14 d; their company size; other users from their email domain. Then it emails the email addresses of the SDRs who get the briefs the user's name, email and this brief, asking for a first touch within 24 h.

## Step 4: Email the weekly PQL digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users who entered the segment from "Find product qualified leads" in the last 7 days and the 4 weeks before, and writes these figures: the count for each week; the share who got an outreach event within 24 h of entering; the share with no outreach event after 48 h. When that untouched share is above 20%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
